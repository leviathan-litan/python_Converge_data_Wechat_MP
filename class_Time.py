# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import datetime
import arrow

# ================================
# 阶段【类定义】
# ================================

class class_time:

    def __init__(self):
        pass

    def now(self):

        obj_arrow_now = arrow.now().format("YYYY-MM-DD HH:mm:ss")

        return obj_arrow_now

    # 时间比较
    # -- 目标时间 / 最后反馈的时间，是目标时间的新旧
    # -- 比较时间 / 参与比较运算的时间
    def is_target_time_newer(self, time_target, time_compare, old_or_new, fmt="%Y-%m-%d %H:%M:%S"):

        # 变量
        datetime_target = datetime.datetime.strptime(str(time_target), fmt)
        datetime_compare = datetime.datetime.strptime(str(time_compare), fmt)

        # 返回值
        data_return = False

        # 处理
        if old_or_new == "new":
            # 如果目标时间大于比较时间，则说明目标时间更新
            data_return = datetime_target >= datetime_compare
        elif old_or_new == "old":
            # 如果目标时间小于比较时间，则说明目标时间更旧
            data_return = datetime_target <= datetime_compare

        # 返回阶段
        return data_return

# ================================
# 阶段【变量定义】
# ================================

# obj_time = class_time()

# ================================
# 阶段【测试】
# ================================

# print(obj_time.now())

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
