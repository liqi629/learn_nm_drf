







def handle_param_type(value):
    """
    处理参数类型
    :param value:
    :return:
    """
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value, float):
        param_type = "float"
    elif isinstance(value, bool):
        param_type = "boolean"
    else:
        param_type = "string"
    return param_type


def handle_data1(datas):
    """
    [{'check':'status_code','expected':200,'comparator':'equals'}]
    转化为[{key:'status_code',value:200,comparator:'equals',param_type:'string'}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for one_validate_dict in datas:
            key = one_validate_dict.get("check")
            value = one_validate_dict.get("expected")
            comparator = one_validate_dict.get("comparator")
            result_list.append({
                "key":key,
                "value":value,
                "comparator":comparator,
                "param_type":handle_param_type(value)
            })
    return result_list


def handle_data2(datas):
    """
    [{'age':18}] 转化为[{key:'age',value:18,param_type:'int'}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for one_var_dict in datas:
            key = list(one_var_dict)[0]
            value = one_var_dict.get(key)

            result_list.append({
                "key": key,
                "value": value,
                "param_type":handle_param_type(value)
            })
    return result_list



def handle_data3(datas):
    """
    [{'token':'content.token'}] 转化为[{key:'token',value:'content.token'}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for one_dict in datas.item():
            key = list(one_dict)[0]
            value = one_dict.get(key)
            result_list.append({
                "key":key,
                "value":value
            })
    return result_list


def handle_data4(datas):
    """
    {'a':'b'}转换为[{key:'a',value:'b'},{...}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for key,value in datas.items():
            result_list.append({
                "key":key,
                "value":value
            })
    return result_list

def handle_data5(datas):
    """
    ['${setup_hook_prepare_kwargs($request)}','']转化为
    [{key:'${setup_hook_prepare_kwargs($request)}'}，{}]
    :param datas:
    :return:
    """
    result_list =[]
    if datas is not None:
        for item in datas:
            result_list.append({
                "key":item
            })
    return result_list


def handle_data6(datas):
    """
    {'username':'jack','age':12,'gender':True} 转化为
    [{key:'username',value:'jack',param_type"'string},{}]
    :param datas:
    :return:
    """
    result_list = []
    if datas is not None:
        for key,value  in datas.item():
            result_list.append({
                "key": key,
                "value": value,
                "param_type":handle_param_type(value)
            })
    return result_list