
# from utils import shell
# from utils import get_current_datetime
from app.utils import get_current_datetime, shell


class Monkey():

    def __init__(self):
        self._exist_adb()

    def _exist_adb(self):
        """
        :return:
        """
        ADB_NOT_EXIST = "'adb' 不是内部或外部命令，也不是可运行的程序\n或批处理文件。"
        status, output = shell("adb version")
        if status == 1 or output == ADB_NOT_EXIST:
            print("The 'adb' instruction cannot be found. \n" +
                  "Please set it through the path variable and restart!")
            exit(status)

    def get_devices(self):
        """
        # 获取连接到机器的所有终端设备
        :return:
        """
        _, devices = shell("adb devices")
        return dict([device.split('\t') for device in devices.split('\n')[1:] if device])

    def install_apk(self, path):
        for device in self.get_devices():
            cmd = "adb -s {0} install {1}".format(device, path)
        status, output = shell(cmd)
        if status != 0:
            print("Failed to install package, monkey quit!")
            exit(1)
        print("Apk installed successfully, ready to start monkey！")

    def parse_log(self, log, blacklist=None, whitelist=None):
        """
        :param log:
        :return:
        """
        with open(log) as file:
            lines = file.readlines()
        for line in lines:
            if line.lower().find("exception") != -1:
                print(line)
            if line.lower().find("anr") != -1:
                print(line)

    def run(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        cmd = "adb shell monkey -p {package} -v -v -v {count}".format(**kwargs)
        if 'ignore' in kwargs and kwargs['ignore'] == True:
            cmd += " --ignore-crashes"
        cmd += " --pkg-blacklist-file com.android.mediacenter"
        log = get_current_datetime("monkey_%Y%m%d_%H%M%S.log")
        status, _ = shell(cmd, True, log)
        if status != 0:
            pass
        self.parse_log(log)


if __name__ == '__main__':
    params = {
        "app": None,
        "package": "com.xiaobang.insurance",
        "count" :10000,
        "ignore": False,
    }
    blacklist = [
        "flipjava.io.IOException",
    ]
    whitelist = [
        "java.lang.NullPointerException",
    ]
    print("Start to run monkey at ", get_current_datetime())
    monkey = Monkey()
    monkey.install_apk("C:/Users/lichenglong/software/app-huawei-release.apk")
    monkey.run(**params)
    print("Stop to run monkey at ", get_current_datetime())
