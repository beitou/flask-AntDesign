import datetime
import time

from dateutil.parser import parse
from flask import request
from flask import jsonify
from flask_mail import Message
from app import db, mail
from app.submit.models import SubmitData,TestReportData,CostTimeData
from app.submit.service import Service
from app.submit import submit


@submit.route('/submit/api/v1/search/sprint', strict_slashes=False)
def api_v1_search_sprint():

    data = request.values.to_dict()

    if 'team' not in data or not data['team']:
        return jsonify({
            'status': 400,
            'message': '接口错误，缺少team参数！',
            'data': data
        })

    service = Service()
    sprints = service.search_sprint(data.get('team'))

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': sprints
    })


@submit.route('/submit/api/v1/search/demand', strict_slashes=False)
def api_v1_search_demand():

    data = request.values.to_dict()

    if 'sprint' not in data or not data['sprint']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [sprint]',
            'data': data
        })

    service = Service()
    demands = service.search_demand(data.get('sprint'))

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': demands
    })


@submit.route('/submit/api/v1/search/repository', strict_slashes=False)
def api_v1_search_repository():

    data = request.values.to_dict()
    if 'group' not in data or not data['group']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [group]',
            'data': data
        })

    service = Service()
    groups = service.search_git_repository(data.get('group'))

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': groups
    })


@submit.route('/submit/api/v1/search/branch', strict_slashes=False)
def api_v1_search_branch():

    data = request.values.to_dict()

    if 'repository' not in data or not data['repository']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter [repository]',
            'data': data
        })

    service = Service()
    groups = service.search_git_branch(data.get('repository'))

    return jsonify({
        'status': 0,
        'message': 'ok',
        'data': groups
    })


@submit.route('/submit/api/v1/submit/data/search',methods=['GET'],strict_slashes=False)
def api_v1_search_submit_data():
    data = []
    total = 0
    keyword = request.args.get("keyword", "")
    submit_status = request.args.get("submit_status")
    if keyword == "" and submit_status == "":
        try:
            submit_datas = SubmitData.query.all()
            for item in submit_datas:
                total = total+1
                # item['create_at'] = time_format(item['create_at'])
                data_serialize = SubmitData.submitdata_schema(item)
                data.append(data_serialize)
            return jsonify({
                'status': 0,
                'total':total,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            db.session.rollback()
            return jsonify({
                'status': 500,
                'message': u'获取数据失败，请重试',
                'data': {
                    'error': str(error)
                }
            })

    else:
        try:
            if submit_status == "all":
                submit_datas = SubmitData.query.filter(SubmitData.name.like("%" + keyword + "%")).all()
            else:
                submit_datas = SubmitData.query.filter(SubmitData.submit_status==submit_status,SubmitData.name.like("%"+keyword +"%") ).all()
            for item in submit_datas:
                total = total+1
                data_serialize = SubmitData.submitdata_schema(item)
                data.append(data_serialize)
            return jsonify({
                'status': 0,
                'total':total,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            db.session.rollback()
            return jsonify({
                'status': 500,
                'message': u'获取数据失败，请重试',
                'data': {
                    'error': str(error)
                }
            })


@submit.route('/submit/api/v1/send/submit/mail',methods=['POST'],strict_slashes=False)
def api_v1_send_submit_mail():
    try:
        if request.method == 'POST':
            data = request.get_json()
            # 提交代码时使用如下
            # msg = Message(subject=data['project']['name'],sender='qa@xiaobangtouzi.com',recipients=data['project']['pm']+data['project']['qa']+['developer@xiaobangtouzi.com','pdc@xiaobangtouzi.com'])
            # 自己调试，使用如下
            msg = Message(subject=data['project']['name'], sender='jiangchenglong@xiaobangtouzi.com',recipients=[','.join(dict(data['project']['pm']).values())+","+','.join(dict(data['project']['qa']).values())])
            msg.body = u'新项目提测' +':'+ data['project']['name'] + "," + u'辛苦qa同学到提测平台查看，接入测试,有问题随时沟通'
            mail.send(msg)
            return jsonify({
                'status': 0,
                'message': u'提测邮件发送成功',
                'data': ''
            })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message':u'提测邮件发送失败，请重试',
            'data': {
                    'error': str(error)
            }
        })


@submit.route('/submit/api/v1/save/submit/data',methods=['POST'],strict_slashes=False)
def api_v1_save_submit_data():
    try:
        if request.method == "POST":
            data = request.get_json(force=True)
            submiter_name = ','.join(dict(data['submiter']).keys())
            submiter_mail = ','.join(dict(data['submiter']).values())
            name = data['project']['name']
            version = data['project']['version']
            pm_name = ','.join(dict(data['project']['pm']).keys())
            pm_mail = ','.join(dict(data['project']['pm']).values())
            fe_name = ','.join(dict(data['project']['fe']).keys())
            fe_mail = ','.join(dict(data['project']['fe']).values())
            rd_name = ','.join(dict(data['project']['rd']).keys())
            rd_mail = ','.join(dict(data['project']['rd']).values())
            qa_name = ','.join(dict(data['project']['qa']).keys())
            qa_mail = ','.join(dict(data['project']['qa']).values())
            prd = data['project']['prd']
            tech = data['project']['tech']
            team = data['environment']['jira']['team']
            sprint = data['environment']['jira']['sprint']
            card = data['environment']['jira']['card']
            group = data['environment']['git']['group']
            repository = data['environment']['git']['repository']
            branch = data['environment']['git']['branch']
            host = data['environment']['host']
            selftest = data['admittance']['selftest']
            testcase = data['admittance']['testcase']
            smoke = data['admittance']['smoke']
            influence = data['admittance']['influence']
            fe_start = data['cost']['fe']['start']
            fe_end = data['cost']['fe']['end']
            rd_start = data['cost']['rd']['start']
            rd_end = data['cost']['rd']['end']
            cc_recs = data['cc_recs']
            sub_mail_recs = pm_mail+","+qa_mail
            submit_status = 'wait'

            submit_data = SubmitData(submiter_name=submiter_name,submiter_mail=submiter_mail,name=name,version=version,pm_name=pm_name,pm_mail=pm_mail,
                                     fe_name=fe_name,fe_mail=fe_mail,rd_name=rd_name,rd_mail=rd_mail,qa_name=qa_name,qa_mail=qa_mail,prd=prd,tech=tech,
                                     team=team,sprint=sprint,card=card,group=group,repository=repository,branch=branch,host=host,selftest=selftest,
                                     testcase=testcase,smoke=smoke,influence=influence,fe_start=fe_start,fe_end=fe_end,rd_start=rd_start,rd_end=rd_end,
                                     cc_recs=cc_recs,sub_mail_recs=sub_mail_recs,submit_status=submit_status)


            db.session.add(submit_data)
            db.session.commit()

            return jsonify({
                'status': 0,
                'message': u'提测成功',
                'data': ''
            })

    except Exception as error:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '提测失败，请检查输入内容是否正确:',
            'data': {
                    'error': str(error)
            }
        })


# 点击保存按钮，发送测试邮件，暂时逻辑是首次保存，发送邮件，也可以每次保存都发送；或者点击保存可以有个是否发送邮件的弹窗
@submit.route('/submit/api/v1/send/testreport/mail',methods=['POST'],strict_slashes=False)
def api_v1_send_testreport_mail():
    try:
        if request.method == 'POST':
            data = request.get_json()
            tr_datas = TestReportData.query.filter(TestReportData.submit_data_id == data['submit_data_id']).first()
            if tr_datas:
                return u'该测试报告已经发送过邮件，本次保存将不发送邮件'
            else:
                submit_data = SubmitData.query.filter(SubmitData.id == data['submit_data_id']).first()
                # 提交代码时使用如下
                # msg = Message(subject=submit_data.name,sender='qa@xiaobangtouzi.com',recipients=[submit_data.submiter_mail,submit_data.pm_mail,submit_data.rd_mail,submit_data.fe_mail,submit_data.qa_mail,'developer@xiaobangtouzi.com','pdc@xiaobangtouzi.com'])
                # 自己调试，使用如下
                msg = Message(subject=submit_data.name, sender='jiangchenglong@xiaobangtouzi.com',recipients=[submit_data.submiter_mail,submit_data.pm_mail,submit_data.rd_mail,submit_data.fe_mail,submit_data.qa_mail])
                msg.body = data['t_summary']+"\n"+data['t_link']+"\n"+u'辛苦项目相关人员查看测试报告'
                mail.send(msg)
                return jsonify({
                    'status': 0,
                    'message': u'测试报告邮件发送成功',
                    'data': ''
                })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'测试报告发送失败，请查看后重试',
            'data': {
                    'error': str(error)
            }
        })


# 点击测试报告页面的 保存按钮，如果是首次保存，则是新建数据到数据库,如果是二次保存，则是更新原有的数据；
@submit.route('/submit/api/v1/save/testreport/data',methods=['POST'],strict_slashes=False)
def api_v1_save_testreport_data():
    try:
        if request.method == "POST":
            data = request.get_json(force=True)
            tr_datas = TestReportData.query.filter(TestReportData.submit_data_id == data['submit_data_id']).first()
            if tr_datas:
                tr_datas.t_os_name = data['t_os_name']
                tr_datas.t_browsers = data['t_browsers']
                tr_datas.t_phones = data['t_phones']
                tr_datas.t_link = data['t_link']
                tr_datas.t_methods = data['t_methods']
                tr_datas.t_summary = data['t_summary']
                tr_datas.t_memo = data['t_memo']
                tr_datas.bug_fatal = data['bug_fatal']
                tr_datas.bug_serious = data['bug_serious']
                tr_datas.bug_general = data['bug_general']
                tr_datas.bug_low = data['bug_low']
                tr_datas.bug_suggest = data['bug_suggest']
                tr_datas.bug_new = data['bug_new']
                tr_datas.bug_processing = data['bug_processing']
                tr_datas.bug_resolve = data['bug_resolve']
                tr_datas.bug_refuse = data['bug_refuse']
                tr_datas.bug_closed = data['bug_closed']
                tr_datas.bug_function = data['bug_function']
                tr_datas.bug_data = data['bug_data']
                tr_datas.bug_ui = data['bug_ui']
                tr_datas.bug_compatibility = data['bug_compatibility']
                tr_datas.bug_performance = data['bug_performance']
                tr_datas.bug_security = data['bug_security']
                tr_datas.submit_data_id = data['submit_data_id']
                db.session.commit()
            else:
                t_os_name = data['t_os_name']
                t_browsers = data['t_browsers']
                t_phones = data['t_phones']
                t_link = data['t_link']
                t_methods = data['t_methods']
                t_summary = data['t_summary']
                t_memo = data['t_memo']
                bug_fatal = data['bug_fatal']
                bug_serious = data['bug_serious']
                bug_general = data['bug_general']
                bug_low = data['bug_low']
                bug_suggest = data['bug_suggest']
                bug_new = data['bug_new']
                bug_processing = data['bug_processing']
                bug_resolve = data['bug_resolve']
                bug_refuse = data['bug_refuse']
                bug_closed = data['bug_closed']
                bug_function = data['bug_function']
                bug_data = data['bug_data']
                bug_ui = data['bug_ui']
                bug_compatibility = data['bug_compatibility']
                bug_performance = data['bug_performance']
                bug_security = data['bug_security']
                submit_data_id = data['submit_data_id']

                test_report_data = TestReportData(t_os_name=t_os_name,t_browsers=t_browsers,t_phones=t_phones,t_link=t_link,
                                                  t_methods=t_methods,t_summary=t_summary,t_memo=t_memo,bug_fatal=bug_fatal,bug_serious=bug_serious,
                                                  bug_general=bug_general,bug_low=bug_low,bug_suggest=bug_suggest,bug_new=bug_new,
                                                  bug_processing=bug_processing,bug_resolve=bug_resolve, bug_refuse=bug_refuse,
                                                  bug_closed=bug_closed,bug_function=bug_function,bug_data=bug_data,bug_ui=bug_ui,
                                                  bug_compatibility=bug_compatibility,bug_performance=bug_performance,bug_security=bug_security,
                                                  submit_data_id=submit_data_id)

                db.session.add(test_report_data)
                db.session.commit()
            return jsonify({
                'status': 0,
                'message': u'测试数据保存成功',
                'data': ''
            })

    except Exception as error:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': u'每一项都是必填项，请全部填写后再次保存',
            'data': {
                    'error': str(error)
            }
        })


# 点击查看按钮调用的接口，获取测试报告的全部数据:测试报告表里的数据，以及会返回开发时间，测试环境时间，预发环境时间，
# 该接口只需要需要传一个submit_data_id参数
@submit.route('/submit/api/v1/testreport/data/search',methods=['GET'],strict_slashes=False)
def api_v1_get_time_data():
    data = []
    timedata = {}
    try:
        if request.method=='GET':
            submit_data_id = request.args.get("submit_data_id")
            submit_data_id = int(submit_data_id)
            tr_datas = TestReportData.query.filter(TestReportData.submit_data_id == submit_data_id).all()
            if tr_datas:
                for item in tr_datas:
                    data_serialize = TestReportData.test_report_data_schema(item)
                    data.append(data_serialize)
            # else:
            #     return jsonify({
            #       'status': 400,
            #       'message': u'submit_data_id参数错误，找不到对应的提测记录',
            #       'data': ''
            #     })

            cost_time_data = CostTimeData.query.filter(CostTimeData.submit_data_id==submit_data_id).first()
            if cost_time_data:
                c_data = CostTimeData.cost_time_data_schema(cost_time_data)
                qa_time = (int(c_data['c_staging_start'])-int(c_data['c_qa_start']))/60/60/24
                staging_time = (int(c_data['c_online_start']) - int(c_data['c_staging_start']))/60/60/24

                dev_time = int(c_data['c_dev_time'])
                timedata['c_dev_time']=dev_time
                qa_total_time = int(c_data['c_qa_count'])*int(qa_time)
                timedata['c_qa_total_time']=qa_total_time
                staging_total_time = int(c_data['c_qa_count'])*int(staging_time)
                timedata['c_staging_total_time']=staging_total_time
            else:
                pass

            data.append(timedata)

            return jsonify({
              'status': 0,
              'message': u'获取数据成功',
              'data': data
            })
        else:
            return jsonify({
              'status': 400,
              'message': u'获取数据失败，请求方式应该为get,请检查请求方法',
              'data': ''
            })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'发生异常，请检查代码',
            'data': {
                    'error': str(error)
            }
        })


# 改造更新状态接口，后续替换原有的update接口，存储点击操作的时间以备用,注意事项：更新接口传name改传submit_id
@submit.route('/submit/api/v1/submit/data/update',methods=['GET','POST'],strict_slashes=False)
def api_v1_update_submit_data():
    try:
        if request.method=='GET':
            submit_data_id = request.args.get("submit_data_id")
            operate_status = request.args.get("operate_status")
            submit_data = SubmitData.query.filter(SubmitData.id==submit_data_id).first()
            if submit_data:
                submit_data.submit_status = operate_status
                db.session.commit()
                # 计算开发时间
                fe_time = (parse(submit_data.fe_end)-parse(submit_data.fe_start)).days+1
                rd_time = (parse(submit_data.rd_end)-parse(submit_data.rd_start)).days+1
                # fe_count = len(list(','.split(submit_data.fe_name)))
                fe_count = len(submit_data.fe_name.split(","))
                rd_count = len(submit_data.rd_name.split(","))
                # 统计开发时间，单位为天
                dev_time = fe_count*fe_time + rd_count*rd_time
                # 统计测试人数
                qa_count = len(submit_data.qa_name.split(","))

                # 将更新状态的时间记录，并进行保存,一般是按照顺序进行点击和展示
                if operate_status == 'qa':
                  qa_start = int(time.time())
                  cost_time_data = CostTimeData(c_qa_start=qa_start,submit_data_id=submit_data_id,c_dev_time=dev_time,c_qa_count=qa_count)
                  db.session.add(cost_time_data)
                  db.session.commit()

                elif operate_status == 'staging':
                  staging_start = int(time.time())
                  cost_time_data = CostTimeData.query.filter(CostTimeData.submit_data_id == submit_data_id).first()
                  cost_time_data.c_staging_start = staging_start
                  db.session.commit()

                elif operate_status == 'online':
                  online_start = int(time.time())
                  cost_time_data = CostTimeData.query.filter(CostTimeData.submit_data_id == submit_data_id).first()
                  cost_time_data.c_online_start = online_start
                  db.session.commit()

                return jsonify({
                  'status': 0,
                  'message': u'状态更新成功',
                  'data': ''
                })
            else:
                db.session.rollback()
                return jsonify({
                  'status': 400,
                  'message': u'submit_data_id找不到对应的提测记录，请检查submit_data_id是否正确',
                  'data': ''
                })
        else:
          return u"方法的请求方式不对，应该为get方式"
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'系统错误,请重试',
            'data': {
                    'error': str(error)
            }
        })


# # 准备废弃，更新提测记录的接口
# @submit.route('/submit/api/v1/submit/data/update',methods=['GET','POST'],strict_slashes=False)
# def api_v1_update_submit_data():
#     try:
#         if request.method=='GET':
#             name = request.args.get("name")
#             operate_status = request.args.get("operate_status")
#             submit_data = SubmitData.query.filter(SubmitData.name==name).first()
#             if submit_data:
#                 submit_data.submit_status = operate_status
#                 db.session.commit()
#                 return jsonify({
#                     'status': 0,
#                     'message': u'更新成功',
#                     'data': ''
#                 })
#             else:
#                 db.session.rollback()
#                 return jsonify({
#                   'status': 500,
#                   'message': u'更新失败，请重试',
#                   'data': ''
#                 })
#
#     except Exception as error:
#         return jsonify({
#             'status': 500,
#             'message': u'更新失败,请重试',
#             'data': {
#                     'error': str(error)
#             }
#         })
