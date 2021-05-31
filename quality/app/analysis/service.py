"""
# wiki    : http://docs.xiaobangtouzi.com/pages/viewpage.action?pageId=14255745
# author  : lichenglong
# date    : 2020-01-08
# version : 1.0
"""

from datetime import datetime
from datetime import timedelta

from jira import JIRA
from jira import JIRAError
from gitlab import Gitlab
from sqlalchemy import func
from mysql.connector.errors import IntegrityError

from app import app, db
from app.utils.wechat import WeChat
from app.analysis.models import Code
from app.analysis.models import Analysis

PUBLIC_GIT_GROUPS = ['backend', 'infra', 'common', 'data', 'frontend', 'fq', 'insurance', 'apps', 'android', 'flutter']
QA = ["陈帅（技术）", "刘丽雨", "齐桓杰", "万莞羚", "田孝庆", "赵志强", "耿金龙", "姜成龙", "刘苹苹", "闫茜", "张力达", "宿宇", "李丽莉", "李成龙"]


class Service(object):

    def __init__(self):
        # 初始化jira的链接
        try:
            self.jira = JIRA(
                app.config['JIRA_SERVER'],
                basic_auth=('lichenglong', 'tyl.0808')
            )
        except JIRAError as error:
            print('获取JIRA数据异常', error)
        # 初始化gitlab的链接
        self.client = Gitlab(
            app.config['GIT_SERVER'],
            private_token='HRFQy8H8YPRpxveyDE6m',  # gitlib token, qa
            timeout=5,
            api_version='4'
        )
        self.client.auth()
        # 初始化企业微信并获取部门信息
        wechat = WeChat()
        users = wechat.get_user_and_department()
        self.department = {u['email'].split('@')[0]: u['department'] for u in users}

    @staticmethod
    def format_datetime(time):
        return time[0:10] + ' ' + time[11:19]

    @staticmethod
    def get_year_and_month(issue):
        time = issue['fields']['created']
        return time[0:4], time[5:7]

    def _wrapper_jira_card(self, issue):
        year, month = self.get_year_and_month(issue)
        card = {
            'id': issue['key'],
            'department': self.department[issue['fields']['creator']['name']],
            'summary': issue['fields']['summary'],
            'priority': issue['fields']['priority']['name'],
            'classify': issue['fields']['issuetype']['name'],
            'status': issue['fields']['status']['name'],
            'reason': 'what?',
            'created': self.format_datetime(issue['fields']['created']),
            'updated': self.format_datetime(issue['fields']['updated']),
            'reporter_name': issue['fields']['creator']['name'],
            'reporter_display_name': issue['fields']['creator']['displayName'],
            'assignee_name': issue['fields']['assignee']['name'] if issue['fields']['assignee'] else '未分配',
            'assignee_display_name': issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else '未分配',
            'url': 'http://jira.xiaobangtouzi.com/browse/%s' % issue['key'],
            'year': year,
            'month': month
        }
        return card

    def save_jira_bugs(self, data):
        """
        :param data:
        :return:
        """
        project = {'FNDN': 3, 'INSU': 4, 'FQ': 5, 'INSC': 6, 'DATA': 7, 'GFE': 44}

        start = data.get('start', None)
        if start is None:
            start = datetime.strftime("%Y-%m-%d %H:%M", datetime.now() - timedelta(days=1))

        end = data.get('end', None)
        if end is None:
            end = datetime.strftime("%Y-%m-%d %H:%M", datetime.now())

        data = {
            'bug': 0,
            'online': 0,
            'others': 0
        }

        count = 0
        for name, board_id in project.items():
            jql = "project = {0} and (created > '{1}' and created < '{2}')".format(name, start, end)
            print(jql)
            result = self.jira.search_issues(jql, maxResults=1000, json_result=True)
            for issue in result['issues']:
                if issue['fields']['issuetype']['name'] == '缺陷':
                    data['online'] += 1
                elif issue['fields']['issuetype']['name'] == 'Defect':
                    data['bug'] += 1
                else:
                    data['others'] += 1
                    continue

                issue = self._wrapper_jira_card(issue)
                exist = db.session.query(
                    Analysis
                ).filter(
                    Analysis.id == issue['id']
                ).first()
                if not exist:
                    model = Analysis(**issue)
                    db.session.add(model)
                    db.session.commit()
                    count += 1
        return count

    def _wrapper_code_lines(self, project, branch, commit):
        """
        :param project:
        :param branch:
        :param commit:
        :return:
        """
        code = {
            'project': project.name,
            'namespace': project.namespace['name'],
            'branch': branch,
            'commit_id': commit.id,
            'created': commit.created_at.replace('T', ' ')[:-5],
            'committer': commit.committer_name,
            'committer_email': commit.committer_email,
            'committed_date': commit.committed_date.replace('T', ' ')[:-5],
            'additions': commit.stats['additions'],
            'deletions': commit.stats['deletions'],
            'total': commit.stats['total'],
            'status': commit.status or 'unknown',
            'year': commit.created_at[0:4],
            'month': commit.created_at[5:7],
        }
        return code

    def save_code_lines(self, data):
        """
        :param data:
        :return:
        """
        branch = data.get('branch', 'master')

        since = data.get('start', None)
        if since is None:
            since = datetime.strftime("%Y-%m-%dT00:00:00Z", datetime.now() - timedelta(days=1))
        else:
            since = since[0:10] + 'T00:00:00Z'

        until = data.get('end', None)
        if until is None:
            until = datetime.strftime("%Y-%m-%dT00:00:00Z", datetime.now())
        else:
            until = until[0:10] + 'T23:59:59Z'

        count, namespace = 0, []
        projects = self.client.projects.list(all=True)
        for project in projects:
            # 这里排除个人git库，只统计公共群组
            if project.namespace['name'].lower() not in PUBLIC_GIT_GROUPS:
                namespace.append(project.namespace['name'])
                continue

            commits = project.commits.list(all=True, since=since, until=until, ref_name=branch)

            for commit in commits:
                commit = project.commits.get(commit.id)
                # 这里排除merge代码，不然会统计重复。
                if ("Merge" in commit.message) and ("into '{0}'".format(branch) in commit.message):
                    continue

                lines = self._wrapper_code_lines(project, branch, commit)
                model = Code(**lines)
                db.session.add(model)
                db.session.commit()
                count += 1
        return count

    @staticmethod
    def _user_adapter(name):
        """
        # 很多用户的git邮箱和名字不是公司邮箱，这里做个映射。
        :param name:
        :return:
        """
        return {
            '88431844': '',
            'www.lianshuaibing': 'lianshuaibing',
            'master': 'wusong',
            'kingshaohui': 'wangshaohui',
            'jianghaichao.': 'jianghaichao',
            'wdtxzy': 'wangdi',
        }.get(name, name)

    def task_product_quality(self, data):
        """
        # 2.产品质量
        # （1）缺陷密度：各业务线千行代码缺陷率
        # （2）缺陷数量：
        # （3）缺陷占比: 各业务线提交的缺陷数量/缺陷总数量*100%（保留2位小数）
        # （4）缺陷类型分布：所选月份，各业务线中不同缺陷类型的数量
        :param data:
        :return:
        """
        result = {
            '基础服务': {
                'code': 0,
                'bugs': 0,
                'percent': 0.0,
            },
            '财商基金': {
                'code': 0,
                'bugs': 0,
                'percent': 0.0,
            },
            '保险服务': {
                'code': 0,
                'bugs': 0,
                'percent': 0.0,
            },
            '保险供应链': {
                'code': 0,
                'bugs': 0,
                'percent': 0.0,
            },
        }

        # 通过数据库存储的jira数据查询bug数量，没有区分线上或线下。
        total = 0
        for dep in result.keys():
            count = Analysis.query.filter_by(department=dep).count()
            result[dep]['bugs'] = count
            total += count

        # 计算每个团队占bug的占比
        for dep in result.keys():
            percent = round(100 * result[dep]['bugs'] / total, 2)
            result[dep]['percent'] = percent

        # 通过数据库查询commit修改的代码行数
        commits = Code.query.all()
        for commit in commits:
            try:
                name = commit.committer_email.split('@')[0]
                name = self._user_adapter(name)
                if name == 'cibot':
                    continue
                dep = self.department[name]
            except KeyError:
                pass

            if name == 'cibot':
                continue

            # 提交10万行代码以上，肯定是外部库或新服务！
            if commit.total > 100000:
                continue

            if dep not in result:
                continue

            result[dep]['code'] += commit.total

        # 通过代码行数与bug数量计算团队的千行代码缺陷率。
        for dep in result.keys():
            bpk = result[dep]['bugs'] / (result[dep]['code'] / 1000)
            result[dep]['bpk'] = round(bpk, 3)

        return result

    def task_product_priority(self, data):
        """
        :param data:
        :return:
        """
        result = {
            '基础服务': {
                'highest': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'lowest': 0,
                'total': 0,
                'percent': 0.0,
            },
            '财商基金': {
                'highest': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'lowest': 0,
                'total': 0,
                'percent': 0.0,
            },
            '保险服务': {
                'highest': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'lowest': 0,
                'total': 0,
                'percent': 0.0,
            },
            '保险供应链': {
                'highest': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'lowest': 0,
                'total': 0,
                'percent': 0.0,
            },
        }

        # 按照部门筛选不同优先级的问题。
        total = 0
        for dep in result.keys():
            bugs = db.session.query(
                Analysis.priority,
                func.count(Analysis.priority)
            ).filter_by(
                department=dep
            ).group_by(
                Analysis.priority
            ).all()

            # 整理数据格式，并计算每个部门的全部缺陷数量，累计公司整体缺陷数量。
            for priority, number in bugs:
                result[dep][priority.lower()] = number
            result[dep]['total'] = sum(result[dep].values())
            total += result[dep]['total']

        # 计算每个部门的缺陷所占百分比
        for dep in result.keys():
            percent = round(100 * result[dep]['total'] / total, 2)
            result[dep]['percent'] = percent

        return result

    def task_product_period(self, data):
        """
        :return:
        """
        result = {
            '基础服务': {
                'list': [],
                'average': 0,
                'maximum': 0,
                'minimum': 0,
            },
            '财商基金': {
                'list': [],
                'average': 0,
                'maximum': 0,
                'minimum': 0,
            },
            '保险服务': {
                'list': [],
                'average': 0,
                'maximum': 0,
                'minimum': 0,
            },
            '保险供应链': {
                'list': [],
                'average': 0,
                'maximum': 0,
                'minimum': 0,
            },
        }

        total, bugs = 0, db.session.query(
            Analysis
        ).filter(Analysis.status == '已关闭').all()
        for bug in bugs:
            cost = bug.updated - bug.created
            hours = cost.total_seconds() / 60 / 60

            if bug.department not in result:
                continue

            result[bug.department]['list'].append(hours)

        for team in result:
            result[team]['average'] = round(sum(result[team]['list']) / len(result[team]['list']), 2)
            result[team]['maximum'] = round(max(result[team]['list']), 2)
            result[team]['minimum'] = round(min(result[team]['list']), 2)

        return result

    def task_good_coder(self, data):
        """
        :param data:
        :return:
        """
        result = {}

        bugs = Analysis.query.all()
        for bug in bugs:
            # 不统计QA人员提的缺陷，目前产品没有排除在外。
            if bug.assignee_display_name in QA:
                continue

            if bug.assignee_display_name not in result:
                result.setdefault(bug.assignee_display_name, {
                    'serious': 0,
                    'common': 0,
                    'total': 0,
                    'percent': 0,
                })

            if bug.priority in ['Highest', 'High']:
                result[bug.assignee_display_name]['serious'] += 1
            else:
                result[bug.assignee_display_name]['common'] += 1
            result[bug.assignee_display_name]['total'] += 1

        # 计算严重问题占比
        for user, value in result.items():
            percent = round(100 * value['serious'] / value['total'], 2)
            result[user]['percent'] = percent

        # 筛选满足条件的RD红榜
        cups = {}
        for developer in result:
            if result[developer]['total'] < 20 or result[developer]['percent'] > 20.0:
                continue
            cups.setdefault(developer, result[developer])

        return cups

    def task_bad_coder(self, data):
        """
        :param data:
        :return:
        """
        result = {}

        bugs = Analysis.query.all()
        for bug in bugs:
            # 不统计QA人员提的缺陷，目前产品没有排除在外。
            if bug.assignee_display_name in ['李成龙']:
                continue

            if bug.assignee_display_name not in result:
                result.setdefault(bug.assignee_display_name, {
                    'serious': 0,
                    'common': 0,
                    'total': 0,
                    'percent': 0,
                })

            if bug.priority in ['Highest', 'High']:
                result[bug.assignee_display_name]['serious'] += 1
            else:
                result[bug.assignee_display_name]['common'] += 1
            result[bug.assignee_display_name]['total'] += 1

        # 计算严重问题占比
        for user, value in result.items():
            percent = round(100 * value['serious'] / value['total'], 2)
            result[user]['percent'] = percent

        average = len(bugs) / len(result)

        # 筛选满足条件的RD红榜
        cups = {}
        for developer in result:
            if result[developer]['total'] < 1.5 * average or result[developer]['serious'] / result[developer]['total'] < 0.3:
                continue
            cups.setdefault(developer, result[developer])

        return cups

    def qa_ranking_list(self, data):
        """
        :param data:
        :return:
        """
        result = {}
        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.reporter_display_name.in_(tuple(QA))
        ).all()
        for bug in bugs:
            qa = bug.reporter_display_name
            if qa not in result:
                result.setdefault(qa, {
                    'total': 1,
                    'valid': 0,
                })
            else:
                result[qa]['total'] += 1
            if bug.status != '已拒绝':
                result[qa]['valid'] += 1

        for user, number in result.items():
            percent = round(100 * number['valid'] / number['total'], 2)
            result[user]['percent'] = percent

        return result

    def task_good_tester(self, data):
        """
        :param data:
        :return:
        """
        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.reporter_display_name.in_(tuple(QA))
        ).all()

        result, average = {}, len(bugs) / len(QA)

        for bug in bugs:
            # 只统计QA人员提的缺陷，非QA人员不统计
            qa = bug.reporter_display_name
            if qa not in QA:
                continue
            if qa not in result:
                result.setdefault(qa, {
                    'serious': 0,
                    'common': 0,
                    'total': 0,
                    'percent': 0,
                })

            if bug.priority in ['Highest', 'High']:
                result[qa]['serious'] += 1
            else:
                result[qa]['common'] += 1
            result[qa]['total'] += 1

        # 计算严重问题占比
        for _, val in result.items():
            val['percent'] = round(100 * val['serious'] / val['total'], 2)

        # 筛选满足条件的QA红榜
        cups = {}
        for tester in result:
            if result[tester]['total'] < average or result[tester]['percent'] < 30.0:
                continue
            cups.setdefault(tester, result[tester])

        return cups

    def task_bad_tester(self, data):
        """
        :param data:
        :return:
        """
        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.reporter_display_name.in_(tuple(QA))
        ).all()

        result, average = {}, len(bugs) / len(QA)

        for bug in bugs:
            # 只统计QA人员提的缺陷，非QA人员不统计
            qa = bug.reporter_display_name
            if qa not in QA:
                continue
            if qa not in result:
                result.setdefault(qa, {
                    'serious': 0,
                    'total': 0,
                    'common': 0,
                    'percent': 0,
                })

            if bug.priority in ['Highest', 'High']:
                result[qa]['serious'] += 1
            else:
                result[qa]['common'] += 1
            result[qa]['total'] += 1

        # 计算严重问题占比
        for _, val in result.items():
            val['percent'] = round(100 * val['serious'] / val['total'], 2)

        # 筛选满足条件的QA预警
        cups = {}
        for tester in result:
            if result[tester]['total'] > 0.6 * average:
                continue
            cups.setdefault(tester, result[tester])

        return cups

    def department_bug_analysis(self, data):
        """
        :param data:
        :return:
        """
        result = {
            'priority': {
                'highest': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'lowest': 0,
            },
            'status': {
                '新开': 0,
                '已解决': 0,
                '已关闭': 0,
                '已拒绝': 0,
                '重开': 0,
            },
            'total': 0,
        }
        department = data.get('department')

        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.department==department
        ).all()

        for bug in bugs:
            priority = bug.priority.lower()
            if priority not in result['priority']:
                result['priority'][priority] = 1
            else:
                result['priority'][priority] += 1
            if bug.status not in result['status']:
                result['status'][bug.status] = 1
            else:
                result['status'][bug.status] += 1

        result['total'] = len(bugs)

        return result

    def department_coder_analysis(self, data):
        """
        :param data:
        :return:
        """
        result, serious, department = {}, 0, data.get('department')

        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.department == department
        ).all()

        for bug in bugs:
            user = bug.assignee_display_name
            if user in QA:
                continue

            if user not in result:
                result.setdefault(user, {
                    'total': 1,
                    'serious': 0,
                    'cost': 0,
                    'closed': 0
                })
            else:
                result[user]['total'] += 1

            if bug.priority in ['Highest', 'High']:
                serious += 1
                result[user]['serious'] += 1

            if bug.status == '已关闭':
                diff = (bug.updated - bug.created).total_seconds()
                result[user]['cost'] += diff
                result[user]['closed'] += 1

        for user, val in result.items():
            total_percent = round(100 * result[user]['total'] / len(bugs), 2)
            result[user]['total_percent'] = total_percent
            serious_percent = round(100 * result[user]['serious'] / serious, 2)
            result[user]['serious_percent'] = serious_percent
            # 累加的秒数换算成小时，再除以统计的问题个数。
            cost, number = 0, result[user]['closed']
            if number != 0:
                cost = result[user]['cost'] / 60 / 60 / number
            result[user]['cost'] = round(cost, 2)

        return result

    def department_tester_analysis(self, data):
        """
        :param data:
        :return:
        """
        result, department = {}, data.get('department')

        bugs = db.session.query(
            Analysis
        ).filter(
            Analysis.department == department
        ).all()

        for bug in bugs:
            qa = bug.reporter_display_name
            if qa not in QA:
                continue

            if qa not in result:
                result.setdefault(qa, {
                    'total': 1,
                    'valid': 0,
                })
            else:
                result[qa]['total'] += 1

            if bug.status != '已拒绝':
                result[qa]['valid'] += 1

        return result

    def search(self, data):
        """
        :param data:
        :return:
        """
        if 'department' not in data or not data['department'] or \
           data['department'] == 'all':
            if 'good_coder' in data:
                data.pop('good_coder')
                return self.task_good_coder(data)
            if 'bad_coder' in data:
                data.pop('bad_coder')
                return self.task_bad_coder(data)
            if 'good_tester' in data:
                data.pop('good_tester')
                return self.task_good_tester(data)
            if 'bad_tester' in data:
                data.pop('bad_tester')
                print('bad_tester', data)
                return self.task_bad_tester(data)
            density = self.task_product_quality(data)
            priority = self.task_product_priority(data)
            period = self.task_product_period(data)
            good_coder = self.task_good_coder(data)
            bad_coder = self.task_bad_coder(data)
            qa_rank = self.qa_ranking_list(data)
            good_tester = self.task_good_tester(data)
            bad_tester = self.task_bad_tester(data)
            return {
                'product': {
                    'density': density,
                    'priority': priority,
                    'period': period,
                    'good_coder': good_coder,
                    'bad_coder': bad_coder,
                    'qa_rank': qa_rank,
                    'good_tester': good_tester,
                    'bad_tester': bad_tester,
                }
            }
        else:
            bug_analysis = self.department_bug_analysis(data)
            coder_analysis = self.department_coder_analysis(data)
            tester_analysis = self.department_tester_analysis(data)
            return {
                'product': {
                    'bug_analysis': bug_analysis,
                    'coder_analysis': coder_analysis,
                    'tester_analysis': tester_analysis,
                }
            }


if __name__ == '__main__':
    service = Service()
    service.save_jira_bugs({'start': '2020-01-01 00:00', 'end': '2020-01-31 23:59'})
    # service.task_product_quality()
