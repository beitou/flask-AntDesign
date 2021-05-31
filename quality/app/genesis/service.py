
import json

import pymysql
import requests


from flask import current_app
from kafka import KafkaProducer

from app.utils.mysql import Mysql
from app.genesis.leads import Leads


class Service():

    def __init__(self):
        self.db = Mysql()
        self.host = "https://api-qa.xiaobangtouzi.com"

    def _get_admin_token(self):
        """
        # 这里暂时用的焦老板手机号，不是所有人手机号可以生成用户token。
        :return:
        """
        url = self.host + "/admin-user/api/get-token"
        params = {
            "mobile": str("18811051343")
        }
        response = requests.get(url, params)
        result =response.json()
        print(result)
        return result['data']['token']

    def leads(self, data):
        """
        :param data:
        :return:
        """
        results = self.db.search(**data)
        return results

    def create_leads(self, data):
        """
        # 先查出ID对应的数据，在使用构建方法创建。
        :param data:
        :return:
        """
        id = data.pop('id')
        token = data.pop('token')

        data.setdefault("database", "quality")
        data.setdefault("table", "genesis")
        data.setdefault("where", {
            "terms": {
                "id": id,
            }
        })
        results = self.db.search(**data)
        # 查不到记录就直接返回吧。
        if not results:
            return
        else:
            results = results[0]

        leads_sn = []
        formSn, leads = None, Leads()
        for step in range(1, 11):
            result = getattr(leads, 'step_' + str(step))(formSn, results, token)
            if result['status'] != 200:
                return result
            leads_sn.append(result["data"]["formSn"])

        return leads_sn

    def search(self, data):
        """
        :param data:
        :return:
        """
        # 这里有一个特殊逻辑，搜索请求会携带finish id。
        if 'id' in data and data['id']:
            id = data.pop('id')
            by = data.pop('by')
            data['where'] = {
                'terms': {
                    by: id
                }
            }
            # 这里是使用id精确查找，需要放开翻页限制
            data['page'] = 0
            data['size'] = 99999999

        data['order'] = 'finish_id'
        data['reverse'] = 'desc'
        results = self.db.search(**data)
        return results

    def delete_leads_by_user_id(self, user_id, type):
        """
        # 目前是从ins_user表通过user_id查询uuid，再通过uuid查询custom_sn
        # 通过uuid与custom_sn来将测试环境的leads数据删除。
        # 1、delete from customer_dictionary_info where customer_sn = 'C384812470788685824';
        # 2、delete from customer_account where customer_sn = 'C384812470788685824';
        # 3、delete from customer where customer_sn = 'C384812470788685824';
        # 4、delete from leads where uuid = '3448c1f5adee467c84e120c8390e4ce7';
        # 5、delete from form where uuid = '3448c1f5adee467c84e120c8390e4ce7';
        # 6、delete from form_group where uuid = '3448c1f5adee467c84e120c8390e4ce7';
        :param user_id:
        :param type:
        :return:
        """
        result = {}

        filter = {
            'database': "insurance",
            'table': "ins_user",
            'where': {
                'terms': {
                    'id': user_id
                }
            }
        }
        uuid = self.db.search(**filter)
        if uuid and 'uuid' in uuid[0]:
            uuid = uuid[0]['uuid']

        filter = {
            'database': "crm",
            'table': "customer_account",
            'where': {
                'terms': {
                    'uuid': uuid
                }
            }
        }
        customer_sn = self.db.search(**filter)
        if customer_sn and 'customer_sn' in customer_sn[0]:
            customer_sn = customer_sn[0]['customer_sn']

        print(uuid, customer_sn)

        if uuid:
            filter = {
                'database': "crm",
                'table': "leads",
                'where': {
                    'terms': {
                        'uuid': uuid,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.leads', count)

            filter = {
                'database': "crm",
                'table': "form",
                'where': {
                    'terms': {
                        'uuid': uuid,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.form', count)

            filter = {
                'database': "crm",
                'table': "form_group",
                'where': {
                    'terms': {
                        'uuid': uuid,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.form_group', count)

        if customer_sn:
            filter = {
                'database': "crm",
                'table': "customer_dictionary_info",
                'where': {
                    'terms': {
                        'customer_sn': customer_sn,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.customer_dictionary_info', count)

            filter = {
                'database': "crm",
                'table': "customer_account",
                'where': {
                    'terms': {
                        'customer_sn': customer_sn,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.customer_account', count)

            filter = {
                'database': "crm",
                'table': "customer_dictionary_info",
                'where': {
                    'terms': {
                        'customer_sn': customer_sn,
                    }
                }
            }
            count = self.db.delete(**filter)
            result.setdefault('crm.customer_dictionary_info', count)

        if type == 'user':
            # 清理用户
            print("清理用户")
            url = "https://api-qa.xiaobangtouzi.com/user-center/account-test/remove?uuid=" + str(uuid)
            response = requests.get(url)
            print(response.json())
        print("清理线索")

        return result

    def delete_by_finish_id(self, data):
        """
        :param data:
        :return:
        """
        result = {}

        for record in data:
            type = record.get('type', 'leads')
            user_id = record.get('user_id')
            leads_sn = record.get('leads_sn')
            finish_id = record.get('finish_id')

            if user_id:

                # 这里是删除问卷线索子流程
                leads = self.delete_leads_by_user_id(user_id, type)
                result.update(leads)
                # 子流程流程结束

                filter = {
                    'database': "insurance",
                    'table': "ins_user",
                    'where': {
                        'terms': {
                            'id': user_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_user', count)

                filter = {
                    'database': "insurance",
                    'table': "ins_questionnaire",
                    'where': {
                        'terms': {
                            'user_id': user_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_questionnaire', count)

                filter = {
                    'database': "insurance",
                    'table': "ins_questionnaire_role",
                    'where': {
                        'terms': {
                            'user_id': user_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_questionnaire_role', count)

                filter = {
                    'database': "insurance",
                    'table': "ins_follow_detail",
                    'where': {
                        'terms': {
                            'user_id': user_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_follow_detail', count)

                filter = {
                    'database': "insurance",
                    'table': "ins_reminder",
                    'where': {
                        'terms': {
                            'user_id': user_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_reminder', count)

            if leads_sn:
                filter = {
                    'database': "insurance",
                    'table': "ins_leads_service",
                    'where': {
                        'terms': {
                            'leads_sn': leads_sn,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_leads_service', count)

                filter = {
                    'database': "crm",
                    'table': "leads",
                    'where': {
                        'terms': {
                            'leads_sn': leads_sn,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('crm.leads', count)

                filter = {
                    'database': "crm",
                    'table': "leads_record",
                    'where': {
                        'terms': {
                            'leads_sn': leads_sn,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('crm.leads_record', count)

                filter = {
                    'database': "crm",
                    'table': "insurance_questionnaire_distribution_event",
                    'where': {
                        'terms': {
                            'leads_sn': leads_sn,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('crm.insurance_questionnaire_distribution_event', count)

            if finish_id:
                filter = {
                    'database': "insurance",
                    'table': "ins_questionnaire",
                    'where': {
                        'terms': {
                            'finish_id': finish_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_questionnaire', count)

                filter = {
                    'database': "insurance",
                    'table': "ins_leads_service",
                    'where': {
                        'terms': {
                            'finish_id': finish_id,
                        }
                    }
                }
                count = self.db.delete(**filter)
                result.setdefault('insurance.ins_leads_service', count)

        return result

    def count(self, data):
        """
        :param data:
        :return:
        """
        return self.db.count(**data)

    def captcha_code(self, data):
        """
        :param data:
        :return:
        """
        phone = data.get('phone')
        config = current_app.config.get('CATPCHA')

        connect = pymysql.connect(**config)

        cursor = connect.cursor()
        sql_count = 'select count(code) from user_center.account_sms where phone = %s'
        sql_code = 'select code from user_center.account_sms where phone = %s order by id desc limit 1'
        cursor.execute(sql_count, phone)
        count = cursor.fetchall()
        cursor.execute(sql_code, phone)
        code = cursor.fetchall()
        cursor.close()
        connect.close()
        """
        # 每次验证码生成都会存到数据库，查不到则认为是新用户。
        # 当查询到验证码时，返回验证码个数与值((1,),) (('703110',),)
        # 当不存在验证码时，返回验证码个数与空元祖((0,),) ()
        """
        if code:
            return int(count[0][0]), code[0][0]
        else:
            return int(count[0][0]), None


    def create_event(self, data):
        """
        :param data:
        :return:
        """
        producer = KafkaProducer(
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            bootstrap_servers='ckafka.xiaobangtouzi.com:9092'
        )
        producer.send('event-bus-qa', data)
        producer.close()


if __name__ == '__main__':
    pass
    # data = [
    #     {
    #         'user_id': 60015,
    #         'leads_sn': "L359111069563617280",
    #         'finish_id': 10069198
    #     }
    # ]
    # service = Service()
    # print(service.delete_by_finish_id(data))
    # service.delete_leads_by_user_id(205890)
