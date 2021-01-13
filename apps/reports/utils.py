import re

from datetime import datetime
from django.db.models import Count



def format_output(datas):
    datas_list = []
    for item in datas:


        if item['result']:

            result = 'Pass'
        else:

            result = 'Fail'
          # result = 'Pass' if item['result'] else 'Fail'

        mtch = re.search(r'(.*)T(.*)\..*?', item['create_time'])
        item['create_time'] = mtch.group(1)+' '+mtch.group(2)
        item['result'] = result
        datas_list.append(item)

    return datas_list

def get_file_contents(filename, chunk_size=512):
    with open(filename, encoding='utf-8') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break