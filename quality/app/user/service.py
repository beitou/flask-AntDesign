
import ldap

from app.user.models import User
from app.utils.wechat import WeChat


class LoginService(object):

    def ldap_login(self, user, password):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        client = ldap.initialize("ldaps://ad01.xiaobang.xyz")
        client.set_option(ldap.OPT_REFERRALS, 0)
        client.protocol_version = 3
        client.set_option(ldap.OPT_TIMEOUT, 1)
        client.simple_bind_s(user, password)
        return client

    def check_password(self, password, user):
        username = "{}@xiaobang.xyz".format(user.email.split("@")[0])
        try:
          self.ldap_login(username, password)
          return True
        except ldap.INVALID_CREDENTIALS:
          return False

    def get_user_from_ldap(self, username):
        """
        # 使用管理员账号与密码登陆ldap服务，查询用户
        # 是否存在，存在则用用户信息创建User实例。
        :param username:
        :return:
        """
        client = self.ldap_login(
            "wechat_sync@xiaobang.xyz",
            "JWPRj7pa^J#3NLZ3"
        )
        try:
            result = client.search_s(
                "OU=小帮规划,DC=xiaobang,DC=xyz", ldap.SCOPE_SUBTREE,
                "(cn={})".format(username)
            )[0][1]
        except IndexError:
            return None
        except ldap.NO_SUCH_OBJECT:
            return None

        user = User()
        user.id = result.get("employeeID")[0].decode()
        user.name = result.get("name")[0].decode()
        user.display_name = result.get("displayName")[0].decode()
        user.email = result.get("mail")[0].decode()
        user.department = result.get("department")[0].decode()
        user.role = result.get("title")[0].decode()
        user.title = result.get("title")[0].decode()

        return user


class UserService():

    def __init__(self):
        self.api = WeChat("wwf1143b4d1547c208", "IyrzR40w1pK2nVWEYIxWCQ9LkOWw7Wrcf45PTEubbV4")

    def search_user(self, key=None, value=None, department=3):
        users = self.api.get_all_users(department)
        if key is None or value is None:
            return users
        users = list(filter(lambda u: u[key]==value, users))
        return users

    def search_role(self, role):
        """
        :param role:
        :return:
        """
        users = self.api.get_all_users()
        qa = list(filter(lambda u: u['position'].find("测试") != -1, users))
        fe = list(filter(lambda u: u['position'].find("前端") != -1 or u['position'].find("客户端") != -1, users))
        rd = list(filter(lambda u: u['position'].find("后端") != -1, users))
        users = self.api.get_all_users(11)
        pm = list(filter(lambda u: u['position'].find("产品经理") != -1, users))
        return {'qa': qa, 'fe': fe, 'rd': rd, 'pm': pm}


if __name__ == '__main__':
    user = UserService()
    print(user.search_user('email', "jiangchenglong@xiaobangtouzi.com"))
    print(user.search_user('userid', 'LiChengLong'))
    print(user.search_user('name', '闫茜'))
    print(user.search_user('mobile', '13651150253'))
    print(user.search_user())
