
import gitlab

from app import app
from app.utils.mysql import Mysql


class Code():

    PUBLIC_GIT_GROUPS = ['backend', 'infra', 'common', 'data', 'frontend', 'fq', 'insurance', 'apps', 'android', 'flutter']

    def __init__(self):
        print(app.config['GIT_SERVER'])
        self.client = gitlab.Gitlab(
            app.config['GIT_SERVER'],
            private_token='HRFQy8H8YPRpxveyDE6m',  # gitlib token, qa
            timeout=5,
            api_version='4'
        )
        self.client.auth()
        self.mysql = Mysql()

    @staticmethod
    def user_adapter(name):
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

    def count_code_lines(self, since, until, branch='master'):
        namespace = []
        projects = self.client.projects.list(all=True)
        for project in projects:
            # 这里排除个人git库，只统计公共群组
            if project.namespace['name'].lower() not in Code.PUBLIC_GIT_GROUPS:
                namespace.append(project.namespace['name'])
                continue

            # 这里只考虑master分支的代码
            commits = project.commits.list(all=True, since=since, until=until, ref_name=branch)

            for commit in commits:
                commit = project.commits.get(commit.id)
                # 这里排除merge代码，不然会统计重复。
                if ("Merge" in commit.message) and ("into '{0}'".format(branch) in commit.message):
                    continue

                result = {
                    'project': project.name,
                    'namespace': project.namespace['name'],
                    'branch': branch,
                    'commit_id': commit.id,
                    'created_at': commit.created_at.replace('T', ' ')[:-5],
                    'committer': commit.committer_name,
                    'committer_email': commit.committer_email,
                    'committed_date': commit.committed_date.replace('T', ' ')[:-5],
                    'additions': commit.stats['additions'],
                    'deletions': commit.stats['deletions'],
                    'total': commit.stats['total'],
                    'status': commit.status,
                }

                kwargs = {
                    'database': "quality",
                    'table': "gitlab",
                    'data': result
                }
                self.mysql.create(**kwargs)
        print(list(set(namespace)))

    def get_repositories(self, group):
        """
        :param group:
        :return:
        """
        result = []
        group = self.client.groups.get(group)
        projects = group.projects.list(all=True)
        for project in projects:
            result.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
            })
        return result

    def get_branch(self, repository):
        """
        :param group:
        :return:
        """
        # "/projects/%(project_id)s/repository/branches"
        result = []
        project = self.client.projects.get(repository)
        for branch in project.branches.list():
            result.append(branch.name)
        return result


if __name__ == "__main__":
    code = Code()
    for branch in ['master']:   #'qa', 'production',
        code.count_code_lines(
            since='2019-12-1T00:00:00Z',
            until='2019-12-31T23:59:59Z',
            branch=branch
        )
    # print(code.get_repositories('insurance'))
    # print(code.get_branch('fq'))
