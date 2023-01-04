# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import os

import class_Time

# ================================
# 阶段【类定义】
# ================================

class class_os:

    # 构造函数
    def __init__(self):
        pass

    # 执行操作系统命令 / 本机
    # 输出：
    # 按行排列的结果
    # 一共有多少行
    def execute_os_command_local(self, os_command):

        # 变量
        data_return = []
        data_return_len = 0

        # 显示
        print("将执行的命令：%s" % (os_command))

        # 处理
        os_command_result = os.popen(os_command).read().splitlines()
        # os_command_result_size = len(os_command_result)

        for line in os_command_result:
            # 过滤：空行
            if line.strip() != "":
                data_return.append(line)

        # 最后，获取一下结果集的大小
        data_return_len = len(data_return)

        # 输出
        return data_return, data_return_len

    # 执行操作系统命令 / 远程
    def execute_os_command_remote(self, os_command):
        pass

    # 查找文件 / 在指定目录中，根据时间点查找文件
    # 以指定时间点分隔更早的若干个文件 或 以指定时间点分隔更新的若干个文件 或 指定时间段内的若干文件
    # 在时间点选择的时候，才需要启用参数：older_newer / 时间段的时候，不需要
    # counts：
    # 时间段：默认：全部
    # 时间点：默认：1
    # 这里的时间段的选择和通常的选择有所差别，是为了适应MySQL Binlog的场景而做的改动
    # range:
    # old   / 更旧
    # new   / 更新
    # inner / 时间段内
    # out / 时间段外
    def find_file_in_directory_by_time(self, directory_path, datetime_begin, datetime_end="", time_range="", counts="*"):

        # 变量
        # 最终结果
        search_result_list_file = []

        # 返回值
        return_data = []

        # 操作系统命令
        os_command = "ls -ltr --time-style='+%Y-%m-%d %H:%M:%S' " + directory_path + " | awk '{print $6\" \"$7\" \"$8}'"

        # 显示
        # print("目录：%s" % (directory_path))
        # print("开始时间：%s" % (datetime_begin))
        # print("结束时间：%s" % (datetime_end))
        # print("更旧 / 更新：%s" % (older_newer))
        # print("数量：%s" % (counts))
        # print("-----------------------")
        # print("命令：%s" % (os_command))

        # 执行命令
        os_command_result, os_command_result_len = self.execute_os_command_local(
            os_command=os_command
        )

        # 显示
        # print("=================================")
        # print("结果集长度：%s" % (os_command_result_len))
        # print("############# 结果集 #############")
        # print(os_command_result)
        # print("#################################")

        # 重置：结果集大小
        if counts == "*":
            counts = os_command_result_len
        else:
            counts = int(counts)

        # 条件处理
        if datetime_end == "":
            # 时间点 / 以datetime_begin为基准
            # old / new

            if time_range == "old":

                # print("Section:【Old】")

                for_loop_old = 1
                for result_item in os_command_result[::-1]:
                    # 显示
                    # print("============================ Loop: old / %s" % for_loop_old)

                    # 变量
                    result_item_name = result_item.split()[2]
                    result_item_time = result_item.split()[0] + " " + result_item.split()[1]

                    is_matched = class_Time.class_time.is_target_time_newer(
                        time_target=result_item_time,
                        time_compare=datetime_begin,
                        old_or_new=time_range
                    )

                    if is_matched:

                        if for_loop_old <= counts:
                            # 显示
                            # print("名称：%s" % result_item_name)
                            # print("时间：%s" % result_item_time)
                            # print("是否匹配：%s" % is_matched)

                            # 追加最终返回列表
                            # search_result_list_file.append(directory_path + '/' + result_item_name)
                            search_result_list_file.append(result_item_name)

                        # 自增
                        for_loop_old += 1

            elif time_range == "new":

                # print("Section:【New】")

                for_loop_new = 1
                for result_item in os_command_result:

                    # 显示
                    # print("============================ Loop: new / %s" % for_loop_new)

                    # 变量
                    result_item_name = result_item.split()[2]
                    result_item_time = result_item.split()[0] + " " + result_item.split()[1]

                    is_matched = class_Time.class_time.is_target_time_newer(
                        time_target=result_item_time,
                        time_compare=datetime_begin,
                        old_or_new=time_range
                    )

                    if is_matched:

                        if for_loop_new <= counts:
                            # 显示
                            # print("名称：%s" % result_item_name)
                            # print("时间：%s" % result_item_time)
                            # print("是否匹配：%s" % is_matched)

                            # 追加最终返回列表
                            # search_result_list_file.append(directory_path + '/' + result_item_name)
                            search_result_list_file.append(result_item_name)

                        # 自增
                        for_loop_new += 1

        else:
            # 时间段
            list_begin = self.find_file_in_directory_by_time(
                directory_path=directory_path,
                counts="*",
                datetime_begin=datetime_begin,
                time_range="new"
            )[0]

            list_end = self.find_file_in_directory_by_time(
                directory_path=directory_path,
                counts="*",
                datetime_begin=datetime_end,
                time_range="old"
            )[0]

            # print("list_begin: %s" % str(list_begin))
            # print("list_end: %s" % str(list_end))

            # inner / outer
            if time_range == "inner":

                # 交集
                search_result_list_file = [ val for val in list_begin if val in list_end ]

            elif time_range == "outer":
                pass

        # 筛选数量
        search_result_loop_cursor = 1
        for search_result_item in search_result_list_file:

            if search_result_loop_cursor <= counts:
                if "index" not in search_result_item:
                    return_data.append(search_result_item)

            # 自增
            search_result_loop_cursor += 1

        # 返回阶段

        # -- 长度
        return_data_len = len(return_data)

        # -- 返回
        return return_data, return_data_len

# ================================
# 阶段【变量定义】
# ================================

# obj_linux = class_os()

# ================================
# 阶段【测试】
# ================================

# print(obj_linux.execute_os_command_local('ipconfig'))

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
