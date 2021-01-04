import re

from django.db.models import Count

from apps.interfaces.models import Interfaces
from apps.testsuites.models import Testsuites

def get_count_by_project(datas):
    pass

    # datas_list = []
    # for item in datas:
    #     mtch = re.search(r'(.*)T(.*)\..*?',item['create_time'])
    #     item['create_time'] = mtch.group(1) +' '+mtch.group(2)
    #
    #     project_id = item['id']
    #     interfaces_testcases_objs = Interfaces.objects.values('id').annotate(testcases = Count('testcases')).\
    #         filter(project_id=project_id,is_delete=False)
    #     interfaces_conut = interfaces_testcases_objs.count()
    #     testcases_count = 0
    #     for one_dict in interfaces_testcases_objs:
    #         testcases_count +=one_dict['testcases']
    #
    #     interfaces_configures_objs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
    #         filter(project_id=project_id, is_delete=False)
    #     configures_count = 0
    #     for one_dict in interfaces_configures_objs:
    #         configures_count += one_dict['configures']
    #
    #     testsuites_count = Testsuites.objects.filter(project_id=project_id,is_delete=False).count()
    #
    #     item['interfaces'] = interfaces_conut
    #     item['testcases'] = testcases_count
    #     item['configures'] = configures_count
    #     item['testsuites'] = testsuites_count
    #
    #
    #     datas_list.append(item)
    # return datas_list