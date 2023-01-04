# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import requests
from bs4 import BeautifulSoup

# ================================
# 阶段【类定义】
# ================================

class class_request:

    def __init__(self):
        pass

    def get_html_BS4(self, url):

        data_return = ""

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
        }

        # requests==latest
        # obj_res = requests.get(url=url, headers=header, verify=False).encoding('utf-8')

        # requests==2.24.0
        obj_response = requests.get(url=url, headers=header, verify=False)

        soup = BeautifulSoup(obj_response.text, 'html.parser')

        # print("000000000000000000000000000000")
        # print(soup)
        # print("000000000000000000000000000000")

        data_return = soup

        # return data_return.head.find('script').text
        return data_return

    def analyze_html_text_handle_script(self, html_BS4, witch=""):

        data_return = ""

        html_head = html_BS4.head.prettify()
        html_body = html_BS4.body.prettify()

        # JavaScript 代码
        html_script_full = []
        html_script_current = ""

        html_script_current_enable = False

        for_script_id = 0
        for line in str(html_body).splitlines():

            if "<script" in line:
                for_script_id += 1
                html_script_current_enable = True

                # print('====================')
                # print("JavaScript - 编号【%d】：开始" % for_script_id)

                continue

            if "</script" in line:

                # print('--------------------')
                # print("JavaScript - 编号【%d】：结束" % for_script_id)

                # print('--------------------')
                # print(html_script_current)

                # print()

                html_script_full.append(html_script_current)

                html_script_current = ""
                html_script_current_enable = False

            if html_script_current_enable:
                html_script_current += line + "\n"

        # print(len(html_script_full))
        # print(html_script_full[10])

        html_script_full_witch = witch - 1
        # print("在数组中的需要【%d】" % html_script_full_witch)

        data_return = html_script_full[html_script_full_witch]

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
