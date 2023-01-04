# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import json

# ================================
# 阶段【类定义】
# ================================

class class_json:

    def __init__(self):
        pass

    # 以下这段JS的解析逻辑是以腾讯微信公众号的合集页面为样本分析得出的
    # 在其他的环境中未必适合
    def get_json_from_javascript_variable(self, javascript_data, variable_search_string):

        data_return = ""

        JS_Variable_value_enable = False
        JS_Variable_value = "{"

        JS_Variable_value_current = ""

        for html_script_data_line in javascript_data.splitlines():

            html_script_data_line = html_script_data_line

            if variable_search_string in html_script_data_line:
                JS_Variable_value_enable = True

                # print("==========================")
                # print(html_script_data_line)

                continue

            if "};" in html_script_data_line:
                JS_Variable_value_enable = False

            if JS_Variable_value_enable:

                # print("==========================")
                # print(html_script_data_line)

                JS_Variable_value_current = ""
                html_script_data_line_part_1 = ""
                html_script_data_line_part_2 = ""

                if ":" not in html_script_data_line:

                    JS_Variable_value_current = html_script_data_line

                    if "}" in html_script_data_line:

                        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        # print(JS_Variable_value[:-1])
                        # print("-----------------------------------")
                        # print()

                        if JS_Variable_value.endswith(','):
                            JS_Variable_value = JS_Variable_value[:-1]

                else:

                    html_script_data_line_part_1 = html_script_data_line.strip().split(': ')[0]
                    html_script_data_line_part_2 = html_script_data_line.strip().split(': ')[1]

                    # print("000000000000000000")
                    # print("---------- Part 1: 【%s】" % html_script_data_line_part_1)
                    # print("---------- Part 2: 【%s】" % html_script_data_line_part_2)

                    if not html_script_data_line_part_1.startswith('"') or \
                            not html_script_data_line_part_1.startswith("'") or \
                            not html_script_data_line_part_1.endwith('"') or \
                            not html_script_data_line_part_1.endwith("'"):
                        html_script_data_line_part_1 = "\"" + html_script_data_line_part_1 + "\""

                    # 进一步处理第二段
                    if ',' in html_script_data_line_part_2:
                        html_script_data_line_part_2 = html_script_data_line_part_2[::-1].split(',')[1][::-1]
                        html_script_data_line_part_2 = "\"" + html_script_data_line_part_2 + "\","

                # 整合处理
                if not html_script_data_line_part_2.endswith(',') and html_script_data_line_part_2 not in ['[',']','{','}']:
                    html_script_data_line_part_2 = "\"" + html_script_data_line_part_2 + "\","


                if html_script_data_line_part_1 != "" and html_script_data_line_part_2 != "":
                    JS_Variable_value_current = html_script_data_line_part_1 + ":" + html_script_data_line_part_2

                    # print("000000000000000000")
                    # print("---------- Part 1: 【%s】" % html_script_data_line_part_1)
                    # print("---------- Part 2: 【%s】" % html_script_data_line_part_2)

                # print("@@@@@@@@@@@@@@@@@@@@@@@@ Current 【%s】" % JS_Variable_value_current)

                JS_Variable_value += JS_Variable_value_current

                # 重置循环段项
                # JS_Variable_value_current = ""
                # html_script_data_line_part_1 = ""
                # html_script_data_line_part_2 = ""

        if JS_Variable_value.endswith(','):
            JS_Variable_value = JS_Variable_value[:-1]

        JS_Variable_value += "}"

        data_return = JS_Variable_value.strip()
        return data_return

    def json_param_get_value(self, key_path, split_with, json_file="", json_data=""):

        # print("====================")
        # print(json_data)
        # print("--------------------")

        json_data_dict = json.loads(json_data)

        # print(json_data_dict['albumId'])

        obj_json = False

        if json_file != "":
            obj_json = json.load(json_file)

        if json_data != "":
            obj_json = json.loads(json_data)

        key_path_result_set = obj_json

        key_path_split_list = key_path.split(split_with)
        key_path_split_list_len = len(key_path_split_list)

        data_return = False

        key_path_split_list_item_cursor = 1
        for key_path_split_list_item in key_path_split_list:

            # 判断当前键名是否是数字
            if key_path_split_list_item.isdigit():
                key_path_split_list_item = int(key_path_split_list_item)

            # 迭加 / 直到获得到键名
            key_path_result_set = key_path_result_set[key_path_split_list_item]

            # 如果到达了键名路径的最后一个，则可以收尾了
            if key_path_split_list_item_cursor == key_path_split_list_len:
                data_return = key_path_result_set

            # 自增
            key_path_split_list_item_cursor += 1

        # 返回阶段 / 显示
        # print(data_return)

        # 返回阶段
        return data_return

# ================================
# 阶段【变量定义】
# ================================

# ================================
# 阶段【测试】
# ================================

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
