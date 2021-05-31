#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from flask import json
from jira import JIRA
import json
from datetime import datetime
from datetime import timedelta

from app import app
from app.utils.mysql import Mysql
from app.utils.wechat import WeChat


class JiraOperation:
    def __init__(self):
        try:
            self.jira = JIRA(app.config['JIRA_SERVER'], basic_auth=('lichenglong', 'tyl.0808'))
            # self.message = RobotMessage(key='5e189e48-efd5-4507-ac09-dc280cdc98a0')

        except Exception as e:
            print('获取JIRA数据异常', e)

    def sprint_original_info(self, board_id):           # 根据board_id获取全部全部sprint原始信息
        return self.jira.sprints(board_id)

    @staticmethod
    def handle_datetime(time):
        time = time.split('T')
        time = time[0]+' '+time[1].split('.')[0]
        return time

    def bug_original_info(self, board_id, sprint_id):   # 根据sprint_id获取原始的BUG信息
        bug_length = []
        sprint_count = 0
        for every_sprint in self.sprint_original_info(board_id):
            if every_sprint.id == sprint_id:
                jql = 'sprint=%d' % every_sprint.id
                iteration_bug_total = self.jira.search_issues(jql, maxResults=200, json_result=True)
                # self.json_analysis(iteration_bug_total)
                for bug_data in iteration_bug_total['issues']:
                    if bug_data['fields']['issuetype']['name'] == '缺陷':
                        bug_length.append(bug_data)
            else:
                sprint_count += 1
        if sprint_count == len(self.sprint_original_info(board_id)):
            print('未找到对应的sprint_id')
        # self.json_analysis(bug_length)
        return bug_length

    def sprint_search(self, board_id):      # 根据board_id获取封装好的全部的sprint内容
        sprint_data = []
        for sprint in self.jira.sprints(board_id):
            sprint_data.append({'id': sprint.id, 'name': sprint.name, 'state': sprint.state})
        return sprint_data

    def sprint_search_demands(self, sprint_id):      # 根据board_id获取封装好的全部的sprint内容
        result = self.jira.search_issues(
            "sprint="+sprint_id,
            fields="summary,issuetype",
            maxResults=500,
            json_result=True)
        issues = list(filter(
            lambda r: r['fields']['issuetype']['name'] != '缺陷',
            result['issues'])
        )
        return issues

    def bug_search(self, board_id, sprint_id):      # 根据原始BUG信息返回封装好的BUG信息
        bug_length = []
        sprint_name = ''
        for sprint in self.sprint_search(board_id):  # 根据sprint_id找到sprint_name
            if sprint['id'] == sprint_id:
                sprint_name = sprint['name']
        if self.bug_original_info(board_id, sprint_id):
            for bug_data in self.bug_original_info(board_id, sprint_id):
                if bug_data['fields']['components']:
                    bug_info = {
                        'business': '保险',
                        'endpoint': bug_data['fields']['components'][0]['name'],
                        'sprint': sprint_name,
                        'summary': bug_data['fields']['summary'],
                        'url': 'http://jira.xioabangtouzi.com/browse/%s' % bug_data['key'],
                        'key': bug_data['key'],
                        'priority': bug_data['fields']['priority']['name'],
                        'status': bug_data['fields']['status']['name'],
                        'reporter': bug_data['fields']['creator']['displayName'],
                        'assignee': bug_data['fields']['assignee']['displayName'],
                        'created': self.handle_datetime(bug_data['fields']['created']),
                        'updated': self.handle_datetime(bug_data['fields']['updated']),
                    }
                    bug_length.append(bug_info)
                else:
                    bug_info = {
                        'business': '保险',
                        'endpoint': '无',
                        'sprint': sprint_name,
                        'summary': bug_data['fields']['summary'],
                        'url': 'http://jira.xioabangtouzi.com/browse/%s' % bug_data['key'],
                        'key': bug_data['key'],
                        'priority': bug_data['fields']['priority']['name'],
                        'status': bug_data['fields']['status']['name'],
                        'reporter': bug_data['fields']['creator']['displayName'],
                        'assignee': bug_data['fields']['assignee']['displayName'],
                        'created': self.handle_datetime(bug_data['fields']['created']),
                        'updated': self.handle_datetime(bug_data['fields']['updated']),
                    }
                    bug_length.append(bug_info)
            # self.json_analysis(bug_length)
        return bug_length

    def everyone_bug_search(self, tester_name):         # 按照报告人姓名统计BUG
        tester_list = {}
        tester_list_info = tester_list.fromkeys(tester_name)
        for name in tester_list_info.keys():
            tester_list[name] = []
        all_bug_list = self.bug_original_info(4, 31)
        for bug_data in all_bug_list:
            for name in tester_list_info.keys():
                if bug_data['fields']['creator']['displayName'] == name:
                    tester_list_info[name].append(bug_data)
                    break
        return tester_list

    @staticmethod
    def json_analysis(bug_txt):         # BUG信息转成json格式
        bug_issue = json.dumps(bug_txt, ensure_ascii=False)
        with open('/Users/qihuanjie/Desktop/bug_data.txt', 'w') as txt_file:
            txt_file.write(bug_issue)

    @staticmethod
    def bug_statistics(bug_collection):          # 统计BUG优先级
        bug_level_statistics = {
            'highest': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        if bug_collection:
            for bug_level in bug_collection:
                if bug_level['priority'] == 'Highest':
                    bug_level_statistics['highest'] += 1
                elif bug_level['priority'] == 'High':
                    bug_level_statistics['high'] += 1
                elif bug_level['priority'] == 'Medium':
                    bug_level_statistics['medium'] += 1
                elif bug_level['priority'] == 'Low':
                    bug_level_statistics['low'] += 1
            # highest_percent = str(round(bug_level_statistics['highest'] / len(bug_collection) * 100)) + '%'
        return bug_level_statistics

    @staticmethod
    def time_delay():
        time = datetime.now()+timedelta(seconds=-31)
        return time

    def bug_search_schedulers(self):  # 判断每隔1min是否有新增的BUG
        new_bug_list = []
        local_time = datetime.now()
        print(local_time)
        bug_list = self.bug_info_statistics()
        print(datetime.now())
        for updated_time in bug_list:
            if (local_time - datetime.strptime(updated_time['updated'], '%Y-%m-%d %H:%M:%S')).total_seconds() < 95:
                print('发现新增BUG')
                new_bug_list.append(updated_time)
        for send_message in new_bug_list:
            self.message.send_message(send_message)

    def mouth_statistics(self, start_date, end_date):    # 统计每个项目的BUG级别数量
        """
        :param start_date:
        :param end_date:
        :return:
        """
        basic_service_sprint, insurance_service_sprint, financial_quotient_sprint, supply_chain_sprint = [], [], [], []
        bug_level_count = {'基础服务': {}, '保险服务': {}, '财商基金': {}, '保险供应链': {}}
        # 获取基础服务项目所有迭代的BUG
        for sprint in self.sprint_original_info(3):
            basic_service_sprint.append(sprint.id)
        basic_service_bug = self.every_project_bug(3, basic_service_sprint)
        # 按照开始和结束时间筛选出基础服务项目所有的BUG
        bug_basic = self.appointed_bug(basic_service_bug, start_date, end_date)
        # 统计保险服务项目BUG级别
        bug_level_count['基础服务'] = self.bug_statistics(bug_basic)

        # 获取保险服务项目所有迭代的BUG
        for sprint in self.sprint_original_info(4):
            insurance_service_sprint.append(sprint.id)
        insurance_service_bug = self.every_project_bug(4, insurance_service_sprint)
        # 按照开始和结束时间筛选出保险服务项目所有的BUG
        bug_insurance = self.appointed_bug(insurance_service_bug, start_date, end_date)
        # 统计保险服务项目BUG级别
        bug_level_count['保险服务'] = self.bug_statistics(bug_insurance)

        # 获取财商基金项目所有迭代的BUG
        for sprint in self.sprint_original_info(5):
            financial_quotient_sprint.append(sprint.id)
        financial_quotient_bug = self.every_project_bug(5, financial_quotient_sprint)
        # 按照开始和结束时间筛选出财商基金项目所有的BUG
        bug_financial = self.appointed_bug(financial_quotient_bug, start_date, end_date)
        # 统计财商基金项目BUG级别
        bug_level_count['财商基金'] = self.bug_statistics(bug_financial)

        # 获取保险供应链项目所有迭代的BUG
        for sprint in self.sprint_original_info(6):
            supply_chain_sprint.append(sprint.id)
        supply_chain_bug = self.every_project_bug(6, supply_chain_sprint)
        # 按照开始和结束时间筛选出保险供应链项目所有的BUG
        bug_supply = self.appointed_bug(supply_chain_bug, start_date, end_date)
        # 统计保险供应链项目BUG级别
        bug_level_count['保险供应链'] = self.bug_statistics(bug_supply)
        print(bug_level_count)

    def every_project_bug(self, board_id, project_sprint):      # 根据项目维度查找BUG数量
        project_bug_list = []
        for iteration_sprint in project_sprint:
            every_sprint_bug = self.bug_search(board_id, iteration_sprint)
            if every_sprint_bug:
                project_bug_list.extend(every_sprint_bug)
        # for bug in every_sprint_bug:
        # project_bug_list.append(bug)
        return project_bug_list

    @staticmethod
    def appointed_bug(bug_list, start_date, end_date):       # 根据指定时间筛选出BUG
        created_time = ''
        excepted_bug_list = []
        for bug_info in bug_list:
            created_time = datetime.strptime(bug_info['created'], '%Y-%m-%d %H:%M:%S')
            if (created_time >= datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')) and \
                    (created_time <= datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')):
                excepted_bug_list.append(bug_info)
        return excepted_bug_list

    def save_jira_bugs(self, start=None, end=None):
        """
        :param start: 开始时间，不设置则为前一天时间
        :param end: 结束时间，不设置则为当前时间
        :return:
        """
        mysql = Mysql()
        wechat = WeChat()
        project = {'FNDN': 3, 'INSU': 4, 'FQ': 5, 'INSC': 6, 'GFE': 44}
        users = wechat.get_user_and_department()
        department = {u['email'].split('@')[0]: u['department'] for u in users}

        if start is None:
            start = datetime.strftime("%Y-%m-%d %H:%M", datetime.now() - timedelta(days=1))

        if end is None:
            end = datetime.strftime("%Y-%m-%d %H:%M", datetime.now())

        data = {
            'bug': 0,
            'online': 0,
            'others': 0
        }

        for name, board_id in project.items():
            jql = "project = {0} and (created > '{1}' and created < '{2}')".format(name, start, end)
            print(jql)
            result = self.jira.search_issues(jql, maxResults=500, json_result=True)
            for issue in result['issues']:
                if issue['fields']['issuetype']['name'] == '缺陷':
                    data['online'] += 1
                    classify = 'online'
                elif issue['fields']['issuetype']['name'] == 'Defect':
                    data['bug'] += 1
                    classify = 'bug'
                else:
                    data['others'] += 1
                    classify = issue['fields']['issuetype']['name']
                    continue
                # print(issue)
                reporter = issue['fields']['creator']['name']
                card = {
                    'id': issue['key'],
                    'business': department[reporter],
                    'endpoint': issue['fields']['components'][0]['name'] if issue['fields']['components'] else None,
                    'sprint': "",
                    'classify': classify,
                    'summary': issue['fields']['summary'].replace('\'', '"'),
                    'priority': issue['fields']['priority']['name'],
                    'status': issue['fields']['status']['name'],
                    'reporter_name': issue['fields']['creator']['name'],
                    'reporter_display_name': issue['fields']['creator']['displayName'],
                    'assignee_name': issue['fields']['assignee']['name'] if issue['fields']['assignee'] else '未分配',
                    'assignee_display_name': issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else '未分配',
                    'created': self.handle_datetime(issue['fields']['created']),
                    'updated': self.handle_datetime(issue['fields']['updated']),
                    'url': 'http://jira.xiaobangtouzi.com/browse/%s' % issue['key'],
                }
                # print(card)
                filter = {
                    'database': "quality",
                    'table': "defect",
                    'data': card,
                }
                count = mysql.create(**filter)
                print("成功插入jira信息{0}条，id是{1}".format(count, card['id']))
        print(data)


if __name__ == '__main__':
    jira = JiraOperation()
    # sprint_search = jira.sprint_search(4)
    # print(sprint_search)
    # bug_count = jira.everyone_bug_search(['齐桓杰'])
    # result = jira.bug_search(4, 39)
    # print(result)
    # jira.bug_search_schedulers(4, 31)
    # jira.mouth_statistics('2018-10-20 19:00:20', '2019-10-27 17:00:00')
    jira.save_jira_bugs('2019-12-01 00:00', '2019-12-31 23:59')
