#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@xiaobangtouzi.com
# Pw @ 2019-09-25 10:50
# history:
#     copy -> lichenglong -> 2019/12/05

import requests


class WeChat(object):

    def __init__(self,
                 corp_id="wwf1143b4d1547c208",
                 corp_secret="IyrzR40w1pK2nVWEYIxWCQ9LkOWw7Wrcf45PTEubbV4"
                 ):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin"
        self.token = self.get_token(corp_id, corp_secret)

    @staticmethod
    def get(url, params):
        result = None
        msg = "HTTP GET {},".format(url)
        try:
            result = requests.get(url, params=params)
        except Exception as e:
            err_msg = "{} ERROR: {}".format(msg, e)
        else:
            status_code = result.status_code
            if status_code < 400:
                # LOG
                return result.json()
            print(result.text)
            err_msg = "{} status_code: {}, ERROR: {}".format(
                msg, status_code, result.json().get("errmsg")
            )
        finally:
            if result:
                result.close()
        raise Exception(err_msg)

    def get_token(self, corp_id, corp_secret):
        url = "{}/gettoken".format(self.url)
        params = {
            "corpid": corp_id,
            "corpsecret": corp_secret
        }
        token = self.get(url, params).get("access_token")
        return token

    def get_departments(self, id=None):
        url = "{}/department/list".format(self.url)
        params = {
            "access_token": self.token
        }
        if id is not None:
            params.setdefault(id, id)

        result = self.get(url, params).get('department')

        return result

    def get_department_users(self):
        url = "{}/user/list".format(self.url)
        departments = [37, 3]
        result = []
        for department in departments:
            params = {
                "access_token": self.token,
                "department_id": department
            }

            result.extend(self.get(url, params).get("userlist"))

        return result

    def _filter(self, user):
        keys = ['userid', 'name', 'email', 'mobile', 'position', 'department']
        return {key: user[key] for key in keys}

    def get_user_and_department(self, department=37):
        department_list = self.get_departments(department)
        department_list = {d['id']: d['name'] for d in department_list}
        user_list = self._all_users(department)
        for user in user_list:
            department = department_list[user['department'][0]]
            user['department'] = department
        users = list(map(self._filter, user_list))
        return users

    def _all_users(self, department=3):
        url = "{}/user/list".format(self.url)
        params = {
          "access_token": self.token,
          "department_id": department,
          "fetch_child": 1
        }
        users = self.get(url, params).get("userlist")
        return users

    def get_all_users(self, department=37):
        users = self._all_users(department)
        users = list(map(self._filter, users))
        return users

    def get_user(self, user_id):
        url = "{}/user/get".format(self.url)
        params = {
          "access_token": self.token,
          "userid": user_id
        }

        result = self.get(url, params)
        return result


if __name__ == "__main__":
    _ = WeChat("wwf1143b4d1547c208", "IyrzR40w1pK2nVWEYIxWCQ9LkOWw7Wrcf45PTEubbV4")
    # users = _.get_department_users()
    # print(users)
    # users = _.get_users()
    # print(len(users))
    # print(users)
    user = _.get_user_and_department()
    print(user)
