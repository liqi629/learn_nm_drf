

from apps.testcases.models import Testcases
from apps.configures.models import Configures

def get_count_by_project(datas):


    datas_list = []
    for item in datas:


        interface_id = item['id']


        testcases_count = Testcases.objects.filter(interface_id=interface_id,
                                                   is_delete=False).count()
        configures_count = Configures.objects.filter(interface_id=interface_id,
                                                     is_delete=False).count()


        item['testcases'] = testcases_count
        item['configures'] = configures_count


        datas_list.append(item)
    return datas_list