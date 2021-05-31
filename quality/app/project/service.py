
from datetime import datetime
from datetime import timedelta

from app.utils.mysql import Mysql

QA = [
    "陈帅", "刘丽雨", "齐桓杰", "万莞羚", "田孝庆",
    "赵志强", "耿金龙", "姜成龙", "刘苹苹", "闫茜",
    "张力达",
]


class Service():

    def __init__(self):
        self.db = Mysql()

    @staticmethod
    def classify_by_level(issues):
        """
        :param issues:
        :return:
        """
        serious = {
            '危险': 0,
            '严重': 0,
            '一般': 0,
            '轻微': 0,
            '微小': 0
        }
        for issue in issues:
            if issue['priority'] == 'Highest':
                serious['危险'] += 1
            if issue['priority'] == 'High':
                serious['严重'] += 1
            if issue['priority'] == 'Medium':
                serious['一般'] += 1
            if issue['priority'] == 'Low':
                serious['轻微'] += 1
            if issue['priority'] == 'Lowest':
                serious['微小'] += 1
        return serious

    @staticmethod
    def classify_by_department(issues):
        """
        :param issues:
        :return:
        """
        department = {
            '基础服务': 0,
            '保险服务': 0,
            '财商基金': 0,
            '保险供应链': 0
        }
        for issue in issues:
            if issue['business'] == 'FNDN':
                department['基础服务'] += 1
            if issue['business'] == 'INSU':
                department['保险服务'] += 1
            if issue['business'] == 'FQ':
                department['财商基金'] += 1
            if issue['business'] == 'INSC':
                department['保险供应链'] += 1

        return department

    @staticmethod
    def classify_by_tester(issues):
        """
        :param issues:
        :return:
        """
        tester = {}
        for issue in issues:
            # 暂时过滤掉非QA人员提的问题
            if issue['reporter_display_name'] not in QA:
                continue
            if issue['reporter_display_name'] not in tester:
                tester.setdefault(issue['reporter_display_name'], 1)
            else:
                tester[issue['reporter_display_name']] += 1
        return tester

    @staticmethod
    def classify_by_developer(issues):
        """
        :param issues:
        :return:
        """
        developer = {}
        for issue in issues:
            # 暂时过滤掉QA人员提的问题
            if issue['assignee_display_name'] in QA:
                continue
            if issue['assignee_display_name'] not in developer:
                developer.setdefault(issue['assignee_display_name'], 1)
            else:
                developer[issue['assignee_display_name']] += 1
        return developer

    @staticmethod
    def classify_by_status(issues):
        """
        :param issues:
        :return:
        """
        status = {}
        for issue in issues:
            if issue['status'] not in status:
                status.setdefault(issue['status'], 1)
            else:
                status[issue['status']] += 1
        return status

    def search(self, data):
        """
        :param data:
        :return:
        """
        current = datetime.now()
        last_month = current - timedelta(days=30)
        filter = {
            'database': "quality",
            'table': "defect",
            'where': {
                'logic': 'and',
                'terms': {
                    'great': {
                        'created': last_month.strftime("%Y-%m-%d")
                    },
                    'less': {
                        'created': current.strftime("%Y-%m-%d")
                    }
                }
            },
            'size': 1000
        }
        issues = self.db.search(**filter)
        return {
            'serious': self.classify_by_level(issues),
            'status': self.classify_by_status(issues),
            'tester': self.classify_by_tester(issues),
            'developer': self.classify_by_developer(issues),
            'department': self.classify_by_department(issues),
            # 'smoke': {
            #     'pass': 82,
            #     'fail': 18
            # }
        }


if __name__ == '__main__':
    service = Service()
    service.search({})
