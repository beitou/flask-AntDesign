
import requests


class Robot():

    def __init__(self, key="2e130fe0-ee58-42c6-9dfe-8ad219a694a0"):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + key

    def send(self, msg):
        """
        :param msg: jira缺陷对象
        :return:
        """
        header = {
            "Content-Type": "application/json"
        }
        title = msg['summary'] if len(msg['summary']) < 30 else msg['summary'][:30] + "..."
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "新建缺陷提醒<font color=\"warning\">" + msg['key'] + "</font>，请相关同事注意。\n" +
                ">标题:<font color=\"comment\">" + title + "</font> \n" +
                ">创建:<font color=\"comment\">" + msg['created'] + "</font> \n" +
                ">更新:<font color=\"comment\">" + msg['updated'] + "</font> \n" +
                ">级别:<font color=\"comment\">" + msg['priority'] + "</font> \n" +
                ">状态:<font color=\"comment\">" + msg['status'] + "</font> \n" +
                ">解决:<font color=\"comment\">" + msg['resolve'] + "</font> \n" +
                ">模块:<font color=\"comment\">" + msg['endpoint'] + "</font> \n" +
                ">开发:<font color=\"comment\">" + msg['assignee'] + "</font> \n" +
                ">测试:<font color=\"comment\">" + msg['reporter'] + "</font> \n" +
                ">地址:[" + title + "](" + msg['url'] + ")"
            }
        }
        response = requests.post(url=self.url, json=data, headers=header)
        print(response.status_code, response.text)


if __name__ == '__main__':
    msg = {
        'business': '保险',
        'endpoint': "保险公众号, 保险方案",
        'sprint': "",
        'summary': "【保险方案改版1.1】从产品投保页面返回方案详情页，页面有时一直重新加载",
        'url': 'http://jira.xiaobangtouzi.com/browse/INSU-192',
        'key': "INSU-192",
        'priority': "High",
        'status': "已关闭",
        'resolve': "未解决",
        'reporter': "齐桓杰",
        'assignee': "聂笠",
        'created': "2019-09-09 11:27:29",
        'updated': "2019-09-12 17:07:48",
    }
    robot = Robot()
    robot.send(msg)