
import requests


class Sonar():

    def __init__(self):
        self.host = "https://sonar.xiaobangtouzi.com/"

    def get_component_list(self, p=1, ps=50):
        """
        :param p: 第几页数据，默认值1.
        :param ps: 每页显示几条数据，默认值50.
        :return:
        """
        url = self.host + "api/components/search_projects"
        params = {
            "p": p,
            "ps": ps,
            "f": "analysisDate"
        }
        try:
            response = requests.get(url, params)
            result = response.json()

            return result["components"]
        except Exception:
            return []

    def search_by_component(self, component, metricKeys):
        """
        :param component: like -> com.xiaobangtouzi:insurance
        :param metricKeys:
        :return:
        """
        if isinstance(metricKeys, list):
            metricKeys = ",".join(metricKeys)

        if not isinstance(metricKeys, str):
            raise Exception("metricKeys should be str or list type.")

        url = self.host + "api/measures/component"
        params = {
            "component": component,
            "metricKeys": metricKeys
        }

        data = {}
        try:
            response = requests.get(url, params)
            result = response.json()

            for measure in result["component"]["measures"]:
                data.setdefault(measure["metric"], measure["value"])
        except Exception:
            pass

        return data


if __name__ == '__main__':
    sonar = Sonar()
    components = sonar.get_component_list()
    for component in components:
        metricKeys = ['alert_status', 'bugs', 'code_smells', 'coverage', 'projects', 'vulnerabilities']
        data = sonar.search_by_component(component["key"], metricKeys)
        print(data)

