import json
import yaml
import logging
import os
from datetime import datetime


from django.conf import settings
from httprunner.task import HttpRunner
from rest_framework import status
from rest_framework.response import Response

from apps.testcases.models import Testcases
from apps.envs.models import Envs
from apps.reports.models import Reports
from apps.debugtalks.models import DeubgTalks
from apps.configures.models import Configures
from utils.myencoder import MyEncoder

logger = logging.getLogger('mytest')

def timestamp_to_datetime(summary,type=True):
    if not type:
        timestamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime.fromtimestamp(timestamp).\
            strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            timestamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
        for record in detail['records']:
            try:
                timestamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass

    return summary

def generate_testcase_files(instance,env,testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name':instance.name,
            'request':{
                'base_url':env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)
    # 获取当前用例的前置用例
    include = json.loads(instance.include,encoding='utf-8')
    # 获取当前用例请求信息
    request = json.loads(instance.request,encoding='utf-8')

    interface_name = instance.interface.name # 接口名称
    project_name = instance.interface.project.name # 项目名称

    testcase_dir_path = os.path.join(testcase_dir_path,project_name)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)
        debugtalk_obj = DeubgTalks.objects.filter(is_delete=False,project__name=project_name).first() # 这里用的__  两个下划线
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""
        #创建debugtalk.py文件

        with open(os.path.join(testcase_dir_path,'debugtalk.py'),
                  mode='w',encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path,interface_name)

    #在项目目录下创建 接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(is_delete=False,id=config_id).first()
        if config_obj:
            config_request = json.loads(config_obj.request,encoding='utf-8')
            config_request.get('config').get('request').setdefault('base_url',env.base_url)
            config_request['config']['name'] = instance.name
            testcases_list[0] = config_request

        if 'testcases' in include:
            for t_id in include.get('testcases'):
                testcase_obj = Testcases.objects.filter(is_delete=False,id=t_id).first()
                if testcase_obj:
                    try:
                        testcase_request = json.loads(testcase_obj.request,encoding='utf-8')
                    except Exception as e:
                        pass
                    else:
                        testcases_list.append(testcase_request)

    # 讲当前用例的request添加到testcases_list
    testcases_list.append(request)

    with open(os.path.join(testcase_dir_path,instance.name+'.yml'),
              mode='w',encoding='utf-8') as one_file:
        yaml.dump(testcases_list,one_file,allow_unicode=True)



def create_report(runner,report_name=None):

    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小鼠
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'],3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'].decode('utf-8'))

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body,bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary,cls=MyEncoder,indent=4,ensure_ascii=False)
    report_name = report_name +'_'+ datetime.strftime(datetime.now(),'%Y%m%d %H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path,encoding='utf-8') as stream:
        reports = stream.read()
    test_report = {
        "name":report_name,
        "result":runner.summary.get('success'),
        "success":runner.summary.get('stat').get('successes'),
        'count':runner.summary.get('stat').get('testsRun'),
        'html':reports,
        'summary':summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance,testcase_dir_path):
    runner = HttpRunner()
    runner.run(testcase_dir_path)

    runner.summary = timestamp_to_datetime(runner.summary,type=False)
    try:
        report_name = instance.name
    except Exception as e:
        report_name = '遗弃的报告'+'-'+ datetime.strftime(datetime.now())
    report_id = create_report(runner,report_name=report_name)
    data_dict = {
        "id":report_id
    }

    return Response(data_dict,status=status.HTTP_201_CREATED)