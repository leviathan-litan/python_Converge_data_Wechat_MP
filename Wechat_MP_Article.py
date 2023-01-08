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

wechat_mp_collections_item_list = obj_yaml.yaml_param_get_value(
    yaml_file=file_yaml,
    key_path="wechat_mp/collections",
    split_with="/"
)

for wechat_mp_collections_item_list_item in trange(wechat_mp_collections_item_list, desc="总体进度（所有TAG合集）"):

    wechat_mp_collections_item_list_item_url = wechat_mp_collections_item_list_item['url']

    obj_selenium.analyze_wechat_mp_tag_page(wechat_mp_collections_item_list_item_url)

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(wechat_mp_collections_item_list_item_url)
    print()

# ================================
# 阶段【测试】
# ================================

# ================================
# 阶段【执行】
# ================================

# ================================
# 阶段【结束】
# ================================
