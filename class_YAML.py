# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

from ruamel import yaml

# ================================
# 阶段【类定义】
# ================================

class class_yaml:

    def __init__(self):
        pass

    def yaml_param_get_value(self, key_path, split_with, yaml_file="", yaml_data=""):

        # 初始对象
        obj_yaml = False

        # 从文件中获取还是从临时的数据中获取
        if yaml_file != "":
            obj_yaml = yaml.safe_load(open(
                file=yaml_file,
                encoding="utf-8"
            ))

            if type(obj_yaml) is list:
                obj_yaml = obj_yaml[0]

        if yaml_data != "":
            obj_yaml = yaml.load(yaml_data, Loader=yaml.SafeLoader)

            if type(obj_yaml) is list:
                obj_yaml = obj_yaml[0]

        # 显示
        # print(obj_yaml)

        # 键名路径值
        key_path_result_set = obj_yaml

        # 拆分键名路径
        key_path_split_list = key_path.split(split_with)
        key_path_split_list_len = len(key_path_split_list)

        # 返回值
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

    # 这一版本的思路是：
    # YAML转成字典
    # 通过字典的数据结构完成修改
    # 字典转成YAML
    # 写入目标文件
    # -------------
    # 因此，set_value的方法只会吐出修改完成后的字典格式数据
    def yaml_param_set_value(self, key_path, key_value, split_sign="", yaml_data="", yaml_file=""):

        # 返回值
        data_return = False

        # 初始对象
        obj_yaml = False

        # 从文件中获取还是从临时的数据中获取
        if yaml_file != "":
            # v0.1
            obj_yaml = yaml.safe_load(open(
                file=yaml_file,
                encoding="utf-8"
            ))
            if type(obj_yaml) is list:
                obj_yaml = obj_yaml[0]

            # v0.2
            # obj_yaml = open(yaml_file, encoding='utf-8')

        if yaml_data != "":
            # v0.1
            # obj_yaml = yaml.load(yaml_data, Loader=yaml.SafeLoader)
            # v0.2
            obj_yaml = yaml.load(yaml_data, Loader=yaml.RoundTripLoader)

            if type(obj_yaml) is list:
                obj_yaml = obj_yaml[0]

        # 显示
        print("")
        print("==================================")
        print("解析到的YAML数据：" + str(obj_yaml))
        print("解析到的YAML数据 / 类型：" + str(type(obj_yaml)))
        print("键名路径：" + key_path)
        print("键名路径 / 切分字符：" + split_sign)
        # print("键值 / 要修改成的：" + key_value)

        # 获取键名切分后的列表
        key_path_split_list = key_path.split(split_sign)
        key_path_split_list_len = len(key_path_split_list)

        # print(key_path_split_list)

        # 循环键名切分后获取访问到目标键的动态参数名
        # --- 动态循环变量需要与下面的YAML文件内容的变量联动 / 所以需要保持一致
        key_path_object_variable_name = "yaml_content_old"
        key_path_split_list_item_cursor = 1

        # 修改前后YAML文件的内容
        yaml_content_old = obj_yaml
        yaml_content_new = False

        for key_path_split_list_item in key_path_split_list:

            # 迭代 / 最终获得目标参数名
            if key_path_split_list_item.isdigit():
                key_path_object_variable_name += "[" + str(key_path_split_list_item) + "]"
            else:
                key_path_object_variable_name += "[\'" + str(key_path_split_list_item) + "\']"

            # 到达了 键名路径的 最后一项
            if key_path_split_list_item_cursor == key_path_split_list_len:
                print("最终得到的动态参数名：" + key_path_object_variable_name)

                # print()
                # print("------------------")
                # print("修改之前：")
                # print(yaml_content_old)

                # 修改
                # v0.1
                # exec(key_path_object_variable_name + ' = \"{}\"'.format(str(key_value)))
                # v0.2
                # print(type(key_value))
                # print(key_value)

                if key_value.isdigit():
                    exec(key_path_object_variable_name + ' = int(key_value)')
                else:
                    exec(key_path_object_variable_name + ' = key_value')

                yaml_content_new = yaml_content_old

                # print("------------------")
                # print("修改之后：")
                # print(yaml_content_new)

                # print()

            # 自增
            key_path_split_list_item_cursor += 1

        # 返回值
        data_return_dict = yaml_content_new

        # v0.1
        # data_return_yaml = yaml.dump(data_return_dict)
        # v0.2
        data_return_yaml = yaml.dump(data_return_dict, Dumper=yaml.RoundTripDumper)

        # 其中 如果要设置的是Bool类型的，会添加【'false'】，所以，需要替换掉
        data_return_yaml = data_return_yaml\
                                .replace('\'false\'','false')\
                                .replace('\'true\'','true')

        # 显示
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(data_return_yaml)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        # 返回阶段
        return data_return_yaml, data_return_dict

    # 将字典类型的YAML文件写入YAML文件
    def yaml_write_to_file(self, file_name, yaml_data_dict):

        with open(file=file_name, mode='w', encoding="utf-8") as write_f:
            yaml.dump(yaml_data_dict, write_f, Dumper=yaml.RoundTripDumper)

# ================================
# 阶段【变量定义】
# ================================

# obj_yaml = class_yaml()
#
# file_yaml = "Testing.yaml"

# ================================
# 阶段【测试】
# ================================

# yaml_value = obj_yaml.yaml_param_get_value(
#     yaml_file=file_yaml,
#     key_path="people/0/name",
#     split_with="/"
# )
#
# print(yaml_value)

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
