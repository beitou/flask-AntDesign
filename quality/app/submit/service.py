from app.utils.code import Code
from app.utils.mysql import Mysql
from app.utils.operation_jira import JiraOperation


class Service():

    def __init__(self):
        self.db = Mysql()

    def submit(self,data):
        # print(data)
        # self.data = json.loads(data)
        return data

    def search_sprint(self, board):
        """
        :param board:
        :return:
        """
        jira = JiraOperation()
        sprints = jira.sprint_search(board)
        sprints = list(filter(lambda s: s['state'] != 'CLOSED', sprints))
        return sprints

    def search_demand(self, sprint):
        """
        :param sprint:
        :return:
        """
        jira = JiraOperation()
        return jira.sprint_search_demands(sprint)

    def search_git_repository(self, group):
        """
        :param group:
        :return:
        """
        code = Code()
        return code.get_repositories(group)

    def search_git_branch(self, repository):
        """
        :param group:
        :param repository:
        :return:
        """
        code = Code()
        return code.get_branch(repository)
