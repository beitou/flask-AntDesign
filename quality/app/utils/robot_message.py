#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


class RobotMessage:
    def __init__(self, key):
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+key
        self.supply_chain_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?' \
                                'key=bc0ac7ab-3ab1-4cf7-9cd3-f3db8471c9e7'

    def send_message(self, bug_info):
        print(bug_info)
        if len(bug_info['summary']) < 30:
            bug_info['summary'] = bug_info['summary']
        else:
            bug_info['summary'] = bug_info['summary'][:30] + '...'
        header = {
            'Content-Type': 'application/json'
        }
        message_data = {
            'msgtype': 'markdown',
            'markdown': {
                'content': '新建缺陷提醒<font color=\"warning\">' + bug_info['id'] + '</font>,请相关同事注意。\n' +
                           ">BUG标题:[" + bug_info['summary'] + "](" + bug_info['url'] + ")\n" +
                           '>创建时间:<font color=\"comment\">' + bug_info['created'] + '</font>\n' +
                           '>更新时间:<font color=\"comment\">' + bug_info['updated'] + '</font>\n' +
                           '>BUG级别:<font color=\"comment\">' + bug_info['priority'] + '</font>\n' +
                           '>BUG状态:<font color=\"comment\">' + bug_info['status'] + '</font>\n' +
                           '>模块:<font color=\"comment\">' + bug_info['endpoint'] + '</font>\n' +
                           '>开发:<font color=\"comment\">' + bug_info['assignee_display_name'] + '</font>\n' +
                           '>测试:<font color=\"comment\">' + bug_info['reporter_display_name'] + '</font>\n'
            }
        }
        if 'INSC' in bug_info['id'] and bug_info['status'] == '新开':
            response = requests.post(url=self.supply_chain_url, json=message_data, headers=header)
            print(response.status_code, response.text)
        else:
            response = requests.post(url=self.supply_chain_url, json=message_data, headers=header)
            print(response.status_code, response.text)



