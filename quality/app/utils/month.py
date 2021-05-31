
from app.utils.code import Code
from app.utils.mysql import Mysql
from app.utils.wechat import WeChat

QA = [
    "陈帅（技术）", "刘丽雨", "齐桓杰", "万莞羚", "田孝庆",
    "赵志强", "耿金龙", "姜成龙", "刘苹苹", "闫茜",
    "张力达", "宿宇", "李丽莉",
]


class Month():

    def __init__(self):
        self.db = Mysql()
        self.wechat = WeChat()
        self.data = []
        self.code = []

    def get_defects(self, start, end, status):
        """
        :param start:
        :param end:
        :return:
        """
        filter = {
            "database": "quality",
            "table": "defect",
            "where": {
                "terms": {
                    "great": {
                        status: start
                    },
                    "less": {
                        status: end
                    }
                },
                "logic": "and"
            },
            "size": 2000
        }
        self.data = self.db.search(**filter)

    def get_codes(self, start, end):
        filter = {
            "database": "quality",
            "table": "gitlab",
            "where": {
                "terms": {
                    "great": {
                        'created_at': start
                    },
                    "less": {
                        'created_at': end
                    }
                },
                "logic": "and"
            },
            "size": 2000
        }
        self.code = self.db.search(**filter)

    def item_101(self):
        result = {}
        for record in self.data:
            # 只统计QA人员提的缺陷，非QA人员不统计
            if record['reporter_display_name'] not in QA:
                continue
            if record['reporter_display_name'] not in result:
                result.setdefault(record['reporter_display_name'], 1)
            else:
                result[record['reporter_display_name']] += 1
        return result

    def item_102(self):
        department = {
            '基础服务': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '财商基金': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '保险服务': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '保险供应链': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
        }

        for record in self.data:
            # 只统计基础，财商基金，保险和供应链
            if record['business'] not in ['基础服务', '财商基金', '保险服务', '保险供应链']:
                continue
            if record['priority'] in ['Highest', 'High']:
                department[record['business']]['serious'] += 1
            department[record['business']]['total'] += 1

        # 计算严重问题占比
        for _, values in department.items():
            values['percent'] = "{0:.2f}%".format(100 * values['serious'] / values['total'])

        return department

    def item_103(self):
        result, average = {}, len(self.data) / len(QA)
        for record in self.data:
            # 只统计QA人员提的缺陷，非QA人员不统计
            if record['reporter_display_name'] not in QA:
                continue
            if record['reporter_display_name'] not in result:
                result.setdefault(record['reporter_display_name'], {
                    'serious': 0,
                    'total': 0,
                    'percent': 0,
                })

            if record['priority'] in ['Highest', 'High']:
                result[record['reporter_display_name']]['serious'] += 1
            result[record['reporter_display_name']]['total'] += 1

        # 计算严重问题占比
        for _, value in result.items():
            percent = 100 * value['serious'] / value['total']
            value['percent'] = "{0:.2f}%".format(percent)

        # 筛选满足条件的QA红榜
        cups = {}
        for tester in result:
            if result[tester]['total'] < average or result[tester]['serious'] / result[tester]['total'] < 0.3:
                continue
            cups.setdefault(tester, result[tester])

        return cups

    def item_104(self):
        """
        :return:
        """
        result = {}

        for record in self.data:
            # 不统计QA人员提的缺陷，目前产品没有排除在外。
            if record['assignee_display_name'] in QA:
                continue

            if record['assignee_display_name'] not in result:
                result.setdefault(record['assignee_display_name'], {
                    'serious': 0,
                    'total': 0,
                    'percent': 0,
                })

            if record['priority'] in ['Highest', 'High']:
                result[record['assignee_display_name']]['serious'] += 1
            result[record['assignee_display_name']]['total'] += 1

        # 计算严重问题占比
        for _, value in result.items():
            percent = 100 * value['serious'] / value['total']
            value['percent'] = "{0:.2f}%".format(percent)

        # 筛选满足条件的RD红榜
        cups = {}
        for developer in result:
            if result[developer]['total'] < 20 or result[developer]['serious'] / result[developer]['total'] > 0.2:
                continue
            cups.setdefault(developer, result[developer])

        return cups

    def item_105(self):
        result, average = {}, len(self.data) / len(QA)
        for record in self.data:
            # 只统计QA人员提的缺陷，非QA人员不统计
            if record['reporter_display_name'] not in QA:
                continue
            if record['reporter_display_name'] not in result:
                result.setdefault(record['reporter_display_name'], {
                    'serious': 0,
                    'total': 0,
                    'percent': 0,
                })

            if record['priority'] in ['Highest', 'High']:
                result[record['reporter_display_name']]['serious'] += 1
            result[record['reporter_display_name']]['total'] += 1

        # 计算严重问题占比
        for _, value in result.items():
            percent = 100 * value['serious'] / value['total']
            value['percent'] = "{0:.2f}%".format(percent)

        # 筛选满足条件的QA红榜
        cups = {}
        for tester in result:
            if result[tester]['total'] > 0.6 * average:
                continue
            cups.setdefault(tester, result[tester])

        return cups

    def item_106(self):
        """
        :return:
        """
        result = {}

        for record in self.data:
            # 不统计QA人员提的缺陷，目前产品没有排除在外。
            if record['assignee_display_name'] in QA:
                continue

            if record['assignee_display_name'] not in result:
                result.setdefault(record['assignee_display_name'], {
                    'serious': 0,
                    'total': 0,
                    'percent': 0,
                })

            if record['priority'] in ['Highest', 'High']:
                result[record['assignee_display_name']]['serious'] += 1
            result[record['assignee_display_name']]['total'] += 1

        # 计算严重问题占比
        for _, value in result.items():
            percent = 100 * value['serious'] / value['total']
            value['percent'] = "{0:.2f}%".format(percent)

        average = len(self.data) / len(result)

        # 筛选满足条件的RD红榜
        cups = {}
        for developer in result:
            if result[developer]['total'] < 1.5 * average or result[developer]['serious'] / result[developer]['total'] < 0.3:
                continue
            cups.setdefault(developer, result[developer])

        return cups

    def item_108(self):
        users = self.wechat.get_user_and_department()
        department = {u['email'].split('@')[0]: u['department'] for u in users}
        result = {}
        for code in self.code:
            # 提交10万行代码以上，肯定是外部库或新服务！
            if code['total'] > 100000:
                continue
            try:
                name = code['committer_email'].split('@')[0]
                name = Code.user_adapter(name)
                if name == 'cibot':
                    continue
                dep = department[name]
            except KeyError:
                pass
                # print("error:", code)
            if dep not in result:
                result.setdefault(dep, {
                    'code': code['total'],
                    'bugs': 0
                })
            else:
                result[dep]['code'] += code['total']

        for record in self.data:
            result[record['business']]['bugs'] += 1

        for dep in result.keys():
            bpk = result[dep]['bugs'] / (result[dep]['code'] / 1000)
            result[dep]['bpk'] = round(bpk, 3)
        return result

    def item_109(self):
        """
        :return:
        """
        result = {}

        for record in self.data:
            # 不统计QA人员提的缺陷，目前产品没有排除在外。
            if record['reporter_display_name'] not in QA:
                continue

            if record['reporter_display_name'] not in result:
                result.setdefault(record['reporter_display_name'], {
                    'invalid': 0,
                    'total': 0,
                    'percent': 0,
                })

            if record['status'] == '已拒绝':
                result[record['reporter_display_name']]['invalid'] += 1
            result[record['reporter_display_name']]['total'] += 1

        # 计算严重问题占比
        for _, value in result.items():
            percent = 100 - 100 * value['invalid'] / value['total']
            value['percent'] = "{0:.2f}%".format(percent)

        return result

    def item_111(self):
        """
        :return:
        """
        result = {}

        for record in self.data:
            # 这里需要已关闭的issue，未关闭无法统计修复时间。
            if record['status'] != '已关闭':
                continue

            created = record['created']
            updated = record['updated']
            diff = updated - created
            minutes = diff.total_seconds() / 60 / 60

            if record['business'] not in result:
                result.setdefault(record['business'], {
                    'hours': minutes,
                    'count': 1,
                    'average': 0,
                })
            else:
                result[record['business']]['hours'] += minutes
                result[record['business']]['count'] += 1

        for team in result:
            result[team]['average'] = result[team]['hours'] / result[team]['count']
            result[team]['hours'] = "{:.2f}".format(result[team]['hours'])
            result[team]['average'] = "{:.2f}".format(result[team]['average'])

        return result

    def item_201_202(self):
        department = {
            '基础服务': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '财商基金': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '保险服务': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
            '保险供应链': {
                'serious': 0,
                'total': 0,
                'percent': 0,
            },
        }

        for record in self.data:
            # 只统计基础，财商基金，保险和供应链
            if record['business'] not in ['基础服务', '财商基金', '保险服务', '保险供应链']:
                continue
            if record['classify'] != 'online':
                continue
            if record['priority'] in ['Highest', 'High']:
                department[record['business']]['serious'] += 1
            department[record['business']]['total'] += 1

        # 计算严重问题占比
        for _, values in department.items():
            values['percent'] = "{0:.2f}%".format(100 * values['serious'] / values['total'])

        return department


if __name__ == '__main__':
    start = "2019-12-01"
    end = "2019-12-31"
    month = Month()
    month.get_defects(start, end, "created")
    month.get_codes(start, end)
    print("测试缺陷数", month.item_101())
    print("严重缺陷占比", month.item_102())
    print("测试红榜", month.item_103())
    print("开发红榜", month.item_104())
    print("测试预警线", month.item_105())
    print("开发预警线", month.item_106())
    print("千行代码缺陷率", month.item_108())
    print("缺陷有效率", month.item_109())
    print("缺陷生存周期", month.item_111())
    print("线上问题", month.item_201_202())
