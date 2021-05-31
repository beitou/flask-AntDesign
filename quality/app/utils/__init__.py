
import os
import hashlib
import datetime
import subprocess

import qrcode

from app.utils.mysql import Mysql


def get_dependence_info():
    with open('requirements.txt') as file:
        dependence = file.readlines()
    return dict([d.strip().split('=') for d in dependence])


def shell(cmd, save=False, path="shell.log"):
    """
    :param cmd:
    :return:
    """
    status, output = subprocess.getstatusoutput(cmd)
    if save:
        with open(path, "w") as file:
            file.write(output)
    else:
        print(output)
    return status, output


def get_current_datetime(format="%Y-%m-%d %H:%M:%S"):
    current = datetime.datetime.now()
    return current.strftime(format)


def time_format(time, format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format)


def make_qrcode(url="https://www.xiaobangguihua.com/"):
    """
    :param url:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(url.encode("utf-8"))
    name = md5.hexdigest()

    img = qrcode.make(data=url)
    path = os.path.join(os.getcwd(), "dist", "static", "img", "qrcode")
    if not os.path.exists(path):
        os.makedirs(path)
    file = os.path.join(path, name + ".png")
    if not os.path.exists(file):
        img.save(file)

    return name + ".png"


def visited_record(request):
    """
    :param data:
    :return:
    """
    record = {}
    record.setdefault('database', "quality")
    record.setdefault('table', "board")
    record.setdefault('data', {
        'platform': 'quality',
        'host': request.host,
        'path': request.path,
        'method': request.method,
        'visited': datetime.datetime.now()
    })
    mysql = Mysql()
    mysql.create(**record)


def query_to_dict(results):
    """
    # 将BaseQuery对象转换为可以json序列化的普通python对象。
    # 通常采用Model.query方法返回的数据需要使用次方法转换。
    # 注意，如果只返回一条数据直接调用to_dict方法即可。
    :param results:
    :return:
    """
    results = list(map(lambda x: x.to_dict(), results))
    # results = list(x for x in results if x['enable'] == 0)
    for result in results:
        if 'created' in result and not isinstance(result['created'], str):
            result['created'] = result['created'].strftime('%Y-%m-%d %H:%M:%S')
    return results


if __name__ == '__main__':
    print(make_qrcode())
