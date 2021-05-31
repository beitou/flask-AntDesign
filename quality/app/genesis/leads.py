
import random

import requests


class Leads():

    def __init__(self):
        self.url = "https://api-qa.xiaobangtouzi.com"

    def form_commit(self, token, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = self.url + "/crm/form/commit"
        method = "POST"
        headers = {
            'content-type': "application/json",
            'x-request-token': token,
        }
        response = requests.request(method=method, url=url, json=kwargs, headers=headers)
        result = response.json()
        print(response.status_code)
        print(result)
        return result

    def step_1(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        name = record.get('name', None)
        name = random.choice(["大坏猫", "二猫", "小猫"]) if not name or name == "random" else name
        sex = record.get('sex', None)
        sex = random.randint(0, 2) if sex == "random" else sex
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": None,
            "formTemplateCode": "ins_questionnaire_form_step1",
            "body": [
                {
                    "name": "姓",
                    "code": "realname",
                    "value": name
                },
                {
                    "name": "性别",
                    "code": "gender",
                    "value": sex
                }
            ]
        }
        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_2(self, parentFormSn, record, token):
        """
        # 由于这一步只有这一个参数，不能为空，因为若不写此参数等同于随机。
        :param parentFormSn:
        :param record:
        :return:
        """
        beneficiary = record.get('beneficiary', None)
        if not beneficiary or beneficiary == "random":
            beneficiary = ",".join(list(set([str(random.randint(1, 5)) for _ in range(random.randint(1, 3))])))
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step2",
            "body": [
                {
                    "name": "为谁投保",
                    "code": "insured",
                    "value": beneficiary
                }
            ]
        }
        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_3(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        son = record.get('son', None)
        try:
            son = int(son)
        except TypeError:
            son = "random"
        son = random.randint(1, 4) if son == "random" else son
        son = 0 if son <= 0 else son
        son = 3 if son >= 3 else son

        daughter = 0

        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step3",
            "body": [
                {
                    "name": "投保的⼉⼦个数",
                    "code": "sonAmount",
                    "value": son
                },
                {
                    "name": "投保的女儿个数",
                    "code": "daughterAmount",
                    "value": daughter
                }
            ]
        }
        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_4(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step4",
            "body": [
            ]
        }
        # 这里暂时使用固定日期代替随机，即随机命中时间100%是1988/12/31
        birthday = record.get('birthday', None)
        birthday = "1988/12/31" if not birthday or birthday == "random" else birthday
        data['body'].append({
            "name": "本人生年月",
            "code": "birthday",
            "value": birthday
        })

        # 如果配偶生日不存在则不需要处理和提交信息。
        spouse_birthday = record.get('spouse_birthday', None)
        if spouse_birthday:
            spouse_birthday = "1988/12/31" if spouse_birthday == "random" else spouse_birthday
            data['body'].append({
                "name": "配偶出生年月",
                "code": "birthdaySpouse",
                "value": spouse_birthday
            })

        # 如果父亲生日不存在则不需要处理和提交信息。
        father_birthday = record.get('father_birthday', None)
        if father_birthday:
            father_birthday = "1988/12/31" if father_birthday == "random" else father_birthday
            data['body'].append({
                "name": "父亲出生年月",
                "code": "birthdayFather",
                "value": father_birthday
            })

        # 如果母亲生日不存在则不需要处理和提交信息。
        mother_birthday = record.get('mother_birthday', None)
        if mother_birthday:
            mother_birthday = "1988/12/31" if mother_birthday == "random" else mother_birthday
            data['body'].append({
                "name": "母亲出生年月",
                "code": "birthdayMother",
                "value": mother_birthday
            })

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_5(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step5",
            "body": [
            ]
        }

        security = record.get('security', None)
        security = random.randint(1, 3) if not security or security == "random" else security
        data['body'].append({
            "name": "本人社保情况",
            "code": "socialInsuranceType",
            "value": security
        })

        # 如果没有社保则不需要提交
        spouse_security = record.get('spouse_security', None)
        if spouse_security:
            spouse_security = random.randint(1, 3) if spouse_security == "random" else spouse_security
            data['body'].append({
                "name": "配偶社保情况",
                "code": "socialInsuranceTypeSpouse",
                "value": spouse_security
            })

        # 如果没有社保则不需要提交
        father_security = record.get('father_security', None)
        if spouse_security:
            father_security = random.randint(1, 3) if father_security == "random" else father_security
            data['body'].append({
                "name": "父亲社保情况",
                "code": "socialInsuranceTypeFather",
                "value": father_security
            })

        # 如果没有社保则不需要提交
        mother_security = record.get('mother_security', None)
        if mother_security:
            mother_security = random.randint(1, 3) if mother_security == "random" else mother_security
            data['body'].append({
                "name": "母亲社保情况",
                "code": "socialInsuranceTypeMother",
                "value": mother_security
            })

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_6(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step6",
            "body": [
            ]
        }

        income = record.get('income', None)
        income = random.randint(0, 1000) if not income or income == "random" else income
        data['body'].append({
            "name": "本人年收入",
            "code": "annualIncome",
            "value": income
        })

        # 如果没有社保则不需要提交
        spouse_income = record.get('spouse_income', None)
        if spouse_income:
            spouse_income = random.randint(0, 1000) if spouse_income == "random" else spouse_income
            data['body'].append({
                "name": "配偶本人年收入",
                "code": "annualIncomeSpouse",
                "value": spouse_income
            })

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_7(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        housing_loan = record.get('housing_loan', None)
        housing_loan = random.random(0, 99999) if not housing_loan or housing_loan == "random" else housing_loan
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step7",
            "body": [
                {
                    "name": "每月房贷",
                    "code": "monthlyMortgage",
                    "value": housing_loan
                }
            ]
        }

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_8(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        loan_duration = record.get('loan_duration', None)
        loan_duration = random.random(0, 35) if not loan_duration or loan_duration == "random" else loan_duration
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step8",
            "body": [
                {
                    "name": "房贷剩余年限",
                    "code": "mortgageRemainingYears",
                    "value": loan_duration
                }
            ]
        }

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_9(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        location = record.get('location', None)
        location = "320100-320100" if not location or location == "random" else location
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step9",
            "body": [
                {
                    "name": "地区码表",
                    "code": "location",
                    "value": location
                }
            ]
        }

        fromSn = self.form_commit(token, **data)
        return fromSn

    def step_10(self, parentFormSn, record, token):
        """
        :param parentFormSn:
        :param record:
        :return:
        """
        data = {
            "sceneCode": "sceneBuyInsuranceCounsellingService",
            "formSn": None,
            "parentFormSn": parentFormSn,
            "formTemplateCode": "ins_questionnaire_form_step10",
            "body": [
            ]
        }

        demand = record.get('demand', None)
        demand = random.randint(1, 4) if not demand or demand == "random" else demand
        data['body'].append({
            "name": "主要需求",
            "code": "primaryDemand",
            "value": demand
        })

        content = record.get('demand', None)
        content = "我想吃鱼" if not content or content == "random" else content
        data['body'].append({
            "name": "主要需求内容",
            "code": "primaryDemandContent",
            "value": content
        })

        fromSn = self.form_commit(token, **data)
        return fromSn

