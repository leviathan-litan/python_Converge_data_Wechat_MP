# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================
import time

import class_Network
import class_YAML
import class_JSON
import class_Selenium

import progress
from alive_progress import alive_bar
from tqdm import tqdm

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

# obj_bar = progress.bar.Bar('Tag in Tags', max=len(wechat_mp_collections_item_list))

# with tqdm(total=len(wechat_mp_collections_item_list), desc='标签列表', leave=True, unit='B', unit_scale=True, iterable=None) as bar_tag:
    # bar_tag.set_description("所有标签")

# with alive_bar(len(wechat_mp_collections_item_list), title="标签列表") as bar_tag:

for_wechat_mp_collections_item_list_item_cursor = 1
for wechat_mp_collections_item_list_item in wechat_mp_collections_item_list:

    # time.sleep(3)

    wechat_mp_collections_item_list_item_name = wechat_mp_collections_item_list_item['name']
    wechat_mp_collections_item_list_item_url = wechat_mp_collections_item_list_item['url']

    # Display
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ %s / %s" % (for_wechat_mp_collections_item_list_item_cursor, len(wechat_mp_collections_item_list)))
    print("标签名称：【%s】" % wechat_mp_collections_item_list_item_name)
    print("--------------------------------")
    print("URL【%s】" % wechat_mp_collections_item_list_item_url)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()

    if len(wechat_mp_collections_item_list) == len(current_tag_already_save_as):

        continue

    if wechat_mp_collections_item_list_item_name in total_tag_already_save_as:

        if wechat_mp_collections_item_list_item_name not in current_tag_already_save_as:

            # print(wechat_mp_collections_item_list_item_name)

            current_tag_already_save_as.append(wechat_mp_collections_item_list_item_name)

            # bar_tag()
            # bar_tag.update(1)

    else:

        analyze_wechat_mp_tag_page_result = obj_selenium.analyze_wechat_mp_tag_page(wechat_mp_collections_item_list_item_url)

        if analyze_wechat_mp_tag_page_result:

            if wechat_mp_collections_item_list_item_name not in total_tag_already_save_as:
                total_tag_already_save_as.append(wechat_mp_collections_item_list_item_name)

            if wechat_mp_collections_item_list_item_name not in current_tag_already_save_as:
                current_tag_already_save_as.append(wechat_mp_collections_item_list_item_name)

                # bar_tag()
                # bar_tag.update(1)

            # 追加写入文件
            with open(file_total_tag_already_save_as, "a+") as f:

                # print(wechat_MP_Tag_Item_ul_item_file_name)

                f.write(wechat_mp_collections_item_list_item_name + "\n")

    # For循环结束阶段
    for_wechat_mp_collections_item_list_item_cursor += 1

    # bar_tag.close()

# ================================
# 阶段【测试】
# ================================

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
