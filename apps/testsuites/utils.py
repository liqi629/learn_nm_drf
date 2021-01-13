

import re



from datetime import datetime

from apps.testcases.models import Testcases



def modify_output(results):
    datas_list = []
    for item in results:
        mtch = re.search(r'(.*)T(.*)\..*?',item['create_time'])
        item['create_time'] = mtch.group(1) +' '+mtch.group(2)
        mtch = re.search(r'(.*)T(.*)\..*?', item['update_time'])
        item['update_time'] = mtch.group(1) + ' ' + mtch.group(2)
        datas_list.append(item)

    return datas_list

def get_testcases_by_interface_ids(ids_list):
    """
    通过接口ID获取用例
    :param ids_list:
    :return:
    """
    one_list =[]
    for interface_id in ids_list:
        testcases_qs = Testcases.objects.values_list('id',flat=True).\
            filter(interface_id=interface_id,is_delete=False)
        one_list.extend(list(testcases_qs))
    return one_list