# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import class_Network
import class_YAML
import class_JSON
import class_Selenium

from tqdm.notebook import trange

# ================================
# 阶段【类定义】
# ================================

# ================================
# 阶段【变量定义】
# ================================

obj_network = class_Network.class_request()
obj_json = class_JSON.class_json()
obj_selenium = class_Selenium.class_selenium()

file_yaml = "Wechat_MP.yaml"
obj_yaml = class_YAML.class_yaml()

file_total_tag_already_save_as = obj_yaml.yaml_param_get_value(
    yaml_file=file_yaml,
    key_path="converge/file/total_tag_already_save_as",
    split_with="/"
)

total_tag_already_save_as = []
current_tag_already_save_as = []

with open(file_total_tag_already_save_as, "r") as f:
    for line in f:
        if line is not None and line != "":
            total_tag_already_save_as.append(line.strip('\n'))

wechat_mp_collections_item_list = obj_yaml.yaml_param_get_value(
    yaml_file=file_yaml,
    key_path="wechat_mp/collections",
    split_with="/"
)

for wechat_mp_collections_item_list_item in wechat_mp_collections_item_list:

    wechat_mp_collections_item_list_item_name = wechat_mp_collections_item_list_item['name']
    wechat_mp_collections_item_list_item_url = wechat_mp_collections_item_list_item['url']

    if wechat_mp_collections_item_list_item_name in total_tag_already_save_as:

        continue

    else:

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("标签名称：【%s】" % wechat_mp_collections_item_list_item_name)
        print("--------------------------------")
        print("URL【%s】" % wechat_mp_collections_item_list_item_url)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print()

        analyze_wechat_mp_tag_page_result = obj_selenium.analyze_wechat_mp_tag_page(wechat_mp_collections_item_list_item_url)

        if analyze_wechat_mp_tag_page_result:
            total_tag_already_save_as.append(wechat_mp_collections_item_list_item_name)

            # 追加写入文件
            with open(file_total_tag_already_save_as, "a+") as f:

                # print(wechat_MP_Tag_Item_ul_item_file_name)

                f.write(wechat_mp_collections_item_list_item_name + "\n")


# ================================
# 阶段【测试】
# ================================

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
