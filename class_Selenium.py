# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

import os.path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

from alive_progress import alive_bar

import class_YAML
import class_OS
import class_Network

# ================================
# 阶段【类定义】
# ================================

class class_selenium:

    def __init__(self):

        self.obj_os = class_OS.class_os()
        self.obj_network = class_Network.class_request()

        file_yaml = "Wechat_MP.yaml"
        obj_yaml = class_YAML.class_yaml()

        self.path_converge_to_base = obj_yaml.yaml_param_get_value(
            yaml_file=file_yaml,
            key_path="converge/path/converge_to",
            split_with="/"
        )

        self.path_page_resource_suffix = obj_yaml.yaml_param_get_value(
            yaml_file=file_yaml,
            key_path="converge/path/page_resource_suffix",
            split_with="/"
        )

        self.file_total_tag_already_save_as = obj_yaml.yaml_param_get_value(
            yaml_file=file_yaml,
            key_path="converge/file/total_tag_already_save_as",
            split_with="/"
        )

        self.file_total_article_already_save_as = obj_yaml.yaml_param_get_value(
            yaml_file=file_yaml,
            key_path="converge/file/total_article_already_save_as",
            split_with="/"
        )

        self.obj_os.execute_os_command_local('mkdir -p %s' % self.path_converge_to_base)

        print("路径 - 存放总路径【%s】" % self.path_converge_to_base)

    # 分析HTML中的元素，并反馈列表
    def HTML_parse_TAG_return_list(self, selenium_driver, TAG_name, attr_name):

        data_return = []

        element_link_list = selenium_driver.find_elements(By.TAG_NAME, TAG_name)

        for_element_link_list_item_cursor = 1
        for element_link_list_item in element_link_list:

            element_link_list_item_target = element_link_list_item.get_attribute(attr_name)

            # print(")))))))))))))))))))) %d" % for_element_link_list_item_cursor)
            # print(element_link_list_item_target)

            if element_link_list_item_target != "" and element_link_list_item_target is not None and not element_link_list_item_target.endswith('/'):
                data_return.append(element_link_list_item_target)

            for_element_link_list_item_cursor += 1

        # print(data_return)
        return data_return

    # 将页面上<link>标签关联的资源下载到当前页面路径下的【./asset】目录中
    # 后期改成了通用方法
    def HTML_save_TAG_resource(self, list_data, path_base, path_sub, file_name, is_image=False, image_name_slot_no=""):

        data_return = []

        # 创建目录
        HTML_save_TAG_link_path = os.path.join(path_base, file_name.split(".html")[0] + path_sub)

        if '"' in HTML_save_TAG_link_path:
            HTML_save_TAG_link_path = HTML_save_TAG_link_path.replace('"','\"')

        self.obj_os.execute_os_command_local("mkdir -p '%s'" % HTML_save_TAG_link_path)

        # 循环列表
        for_list_data_item_cursor = 1
        for list_data_item in list_data:

            if is_image:
                list_data_item_file_name = list_data_item.split("/")[image_name_slot_no] + ".jpg"
            else:
                list_data_item_file_name = list_data_item.split("/")[-1]

            list_data_item_file_path = os.path.join(HTML_save_TAG_link_path, list_data_item_file_name)

            # print("------ %d " % for_list_data_item_cursor)
            # print("源头文件【%s】" % list_data_item)
            # print("目标文件【%s】" % list_data_item_file_name)
            # print()

            # 存储到本地
            self.obj_network.download_url(
                url=list_data_item,
                to_file_name=list_data_item_file_path
            )

            if is_image:
                if list_data_item_file_name.split('.')[-2] not in data_return:
                    data_return.append(list_data_item_file_name.split('.')[-2])
            else:
                if list_data_item_file_name not in data_return:
                    data_return.append(list_data_item_file_name)

            for_list_data_item_cursor += 1

        return data_return

    def get_HTML_code_TAG_attr(self, HTML_code, attr_name):

        data_return = ""

        if attr_name + "=\"" in HTML_code:
            data_return = HTML_code.split(attr_name + "=\"")[1].split("\"")[0]

        # print(data_return)

        return data_return

    def get_HTML_code_search_string(self, HTML_code, Tag_name, attr_name):

        data_return = []

        for_HTML_code_split_item_cursor = 1
        for HTML_code_split_item in HTML_code.split('<' + Tag_name):

            HTML_code_split_item_target_1 = HTML_code_split_item.split('>')[0]

            if attr_name + "=" in HTML_code_split_item_target_1:

                print("========= %s" % for_HTML_code_split_item_cursor)
                # print(HTML_code_split_item_target_1)

                HTML_code_split_item_target_2 = HTML_code_split_item_target_1.split(attr_name + "=\"")[1].split("\"")[0]

                print(HTML_code_split_item_target_2)

                if HTML_code_split_item_target_2 not in data_return:
                    data_return.append(HTML_code_split_item_target_2)

                for_HTML_code_split_item_cursor += 1

        # print(data_return)

        return data_return

    # 将URL保存为【HTML】
    def URL_save_as_HTML(self, html_url, save_as_directory, save_as_file_name):

        # 返回是否保存成功
        # True 成功
        # False 不成功
        data_return = False

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--save-page-as-mhtml')
        self.driver_getHtml = webdriver.Chrome(options=chrome_options)

        self.driver_getHtml.get(html_url)

        WebDriverWait(self.driver_getHtml, 60).until(visibility_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(5)

        # 下载页面包含的资源
        # -------------- <link>
        getHtml_Tag_link_list = self.HTML_parse_TAG_return_list(
            selenium_driver=self.driver_getHtml,
            TAG_name='link',
            attr_name='href'
        )
        getHtml_Tag_link_list_already_local = self.HTML_save_TAG_resource(list_data=getHtml_Tag_link_list, path_base=save_as_directory, path_sub=self.path_page_resource_suffix,
                                    file_name=save_as_file_name)

        # print("@@@@@@@@@@@@@@ Already in Local / <link>【%s】" % getHtml_Tag_link_list_already_local)
        # print(" ------------- %s" % str(len(getHtml_Tag_link_list_already_local)))
        # print()

        # -------------- <scirpt>
        getHtml_Tag_script_list = self.HTML_parse_TAG_return_list(
            selenium_driver=self.driver_getHtml,
            TAG_name='script',
            attr_name='src'
        )

        # print("标签【script】: %s" % getHtml_Tag_script_list)
        getHtml_Tag_script_list_already_local = self.HTML_save_TAG_resource(list_data=getHtml_Tag_script_list,
                                                                          path_base=save_as_directory,
                                                                          path_sub=self.path_page_resource_suffix,
                                                                          file_name=save_as_file_name)

        # print("@@@@@@@@@@@@@@ Already in Local / <script>【%s】" % getHtml_Tag_script_list_already_local)
        # print(" ------------- %s" % str(len(getHtml_Tag_script_list_already_local)))
        # print()

        # -------------- Image
        getHtml_Tag_img_list = self.HTML_parse_TAG_return_list(
            selenium_driver=self.driver_getHtml,
            TAG_name='img',
            attr_name='data-src'
        )
        getHtml_Tag_img_list_already_local = self.HTML_save_TAG_resource(list_data=getHtml_Tag_img_list, path_base=save_as_directory, path_sub=self.path_page_resource_suffix,
                                    file_name=save_as_file_name, is_image=True, image_name_slot_no=-2)

        # print("============== 图片列表")
        # for_getHtml_Tag_img_list_item_cursor = 1
        # for getHtml_Tag_img_list_item in getHtml_Tag_img_list:
        #     print("--------- %s" % getHtml_Tag_img_list_item)
        #     for_getHtml_Tag_img_list_item_cursor += 1
        # print("@@@@@@@@@@@@@@ Already in Local / image【%s】" % getHtml_Tag_img_list_already_local)
        # print(" ------------- %s" % str(len(getHtml_Tag_img_list_already_local)))
        # print()

        # 所有完整的列表：合一
        getHtml_Tag_list_already_local = []

        for getHtml_Tag_link_list_already_local_item in getHtml_Tag_link_list_already_local:
            if getHtml_Tag_link_list_already_local_item not in getHtml_Tag_list_already_local:
                getHtml_Tag_list_already_local.append(getHtml_Tag_link_list_already_local_item)

        for getHtml_Tag_script_list_already_local_item in getHtml_Tag_script_list_already_local:
            if getHtml_Tag_script_list_already_local_item not in getHtml_Tag_list_already_local:
                getHtml_Tag_list_already_local.append(getHtml_Tag_script_list_already_local_item)

        for getHtml_Tag_img_list_already_local_item in getHtml_Tag_img_list_already_local:
            if getHtml_Tag_img_list_already_local_item not in getHtml_Tag_list_already_local:
                getHtml_Tag_list_already_local.append(getHtml_Tag_img_list_already_local_item)

        # 还要把网页中对应的远程的资源的位置改到本地

        # 获取源页面代码
        getHtml_page_source = self.driver_getHtml.page_source

        # 最终代码
        getHtml_page_source_finally = ""

        # 每次循环的当行代码
        getHtml_page_source_finally_current = ""

        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print("源码 / 页面【%s】" % html_url)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(getHtml_page_source)
        # print("-----------------------------")
        # print()

        # 开始处理页面代码
        for getHtml_page_source_line in getHtml_page_source.splitlines():

            # print("Current【%s】" % getHtml_page_source_line)

            string_replace = ""
            string_replace_to = ""
            target_file_name = ""
            is_image = False

            if getHtml_page_source_line.strip().startswith("<link"):
                # print("))))))))))) 识别到【link】")
                # print(getHtml_page_source_line)
                # print("-----------")

                is_image = False

                string_replace = self.get_HTML_code_TAG_attr(
                    HTML_code=getHtml_page_source_line,
                    attr_name="href"
                )

            if getHtml_page_source_line.strip().startswith("<script"):
                # print("))))))))))) 识别到【script】")
                # print(getHtml_page_source_line)
                # print()

                is_image = False

                string_replace = self.get_HTML_code_TAG_attr(
                    HTML_code=getHtml_page_source_line,
                    attr_name="src"
                )

            if getHtml_page_source_line.strip().startswith("<img"):
                # print("))))))))))) 识别到【img】")
                # print(getHtml_page_source_line)
                # print()

                is_image = True

                string_replace = self.get_HTML_code_TAG_attr(
                    HTML_code=getHtml_page_source_line,
                    attr_name="data-src"
                )

            if getHtml_page_source_line.strip().startswith("<span"):
                # print("))))))))))) 识别到【span】")
                # print(getHtml_page_source_line)
                # print()

                is_image = True

                string_replace = self.get_HTML_code_TAG_attr(
                    HTML_code=getHtml_page_source_line,
                    attr_name="data-src"
                )

            # 这一段会匹配到一大段代码
            # 这一段的代码替换就在这里操作
            # 原始代码：getHtml_page_source_line - 需要替换的代码
            if "data-src" in getHtml_page_source_line and "span class" in getHtml_page_source_line and "rich_media_content" in getHtml_page_source_line:

                # print("))))))))))) 识别到【span / data-src / image】")

                # 找到一个替换一个
                for_getHtml_page_source_line_item_cursor = 1
                for getHtml_page_source_line_item in getHtml_page_source_line.split("=\""):

                    getHtml_page_source_line_item_target = getHtml_page_source_line_item.split("\"")[0]

                    if getHtml_page_source_line_item_target != "":

                        if getHtml_page_source_line_item_target.startswith('http'):

                            # print("---- Line %s" % for_getHtml_page_source_line_item_cursor)
                            # print(getHtml_page_source_line_item_target)

                            getHtml_page_source_line_item_target_part_diff = ""

                            if "/" in getHtml_page_source_line_item_target:
                                getHtml_page_source_line_item_target_part_diff = getHtml_page_source_line_item_target.split('/')[-2]

                            if getHtml_page_source_line_item_target_part_diff in getHtml_Tag_img_list_already_local:

                                target_file_path_base = save_as_file_name.split(".html")[0] + self.path_page_resource_suffix

                                # Old
                                # 替换图片引用
                                # getHtml_page_source_line_item_target_replace_to_1 = "./" + target_file_path_base + "/" + getHtml_page_source_line_item_target_part_diff + ".jpg"
                                getHtml_page_source_line_item_target_replace_to_1 = target_file_path_base + "/" + getHtml_page_source_line_item_target_part_diff + ".jpg"

                                getHtml_page_source_line_item_target_replace_to_2 = getHtml_page_source_line_item_target_replace_to_1 + '" src="' + getHtml_page_source_line_item_target_replace_to_1 + '"'

                                # New
                                # getHtml_page_source_line_item_target_replace_to_1 = target_file_path_base + "/" + getHtml_page_source_line_item_target_part_diff + ".jpg"
                                # getHtml_page_source_line_item_target_replace_to_2 = getHtml_page_source_line_item_target_replace_to_1 + '"'

                                # print("替换为：【%s】" % getHtml_page_source_line_item_target_replace_to_2)
                                # print()

                                getHtml_page_source_line = getHtml_page_source_line.replace(getHtml_page_source_line_item_target + "\"", getHtml_page_source_line_item_target_replace_to_2)

                            for_getHtml_page_source_line_item_cursor += 1

                # 将图片标签的span替换为img

                for_getHtml_page_source_line_span_item_cursor_twice = 1
                for getHtml_page_source_line_span_item in getHtml_page_source_line.split("<span"):
                    getHtml_page_source_line_item_content = getHtml_page_source_line_span_item.split('>')[0]

                    if "src" in getHtml_page_source_line_item_content:
                        # print("[span] --------- %s" % for_getHtml_page_source_line_span_item_cursor_twice)
                        # print(getHtml_page_source_line_item_content)
                        # print()

                        # 后面真正执行替换的时候，在替换目标字符串上需要做响应的修改
                        replace_string = "<span" + getHtml_page_source_line_item_content + ">"
                        replace_to_string = "<img" + getHtml_page_source_line_item_content + "><span>"

                        if replace_string in getHtml_page_source_line:
                            # print("匹配到【%s】" % replace_string)

                            getHtml_page_source_line = getHtml_page_source_line.replace(
                                replace_string,
                                replace_to_string
                            )

                        for_getHtml_page_source_line_span_item_cursor_twice += 1

                for_getHtml_page_source_line_img_item_cursor_twice = 1
                for getHtml_page_source_line_img_item in getHtml_page_source_line.split("<img"):
                    getHtml_page_source_line_item_content = getHtml_page_source_line_img_item.split('>')[0]

                    # if "rich_pages wxw-img" in getHtml_page_source_line_item_content and "src" in getHtml_page_source_line_item_content:
                    if "src" in getHtml_page_source_line_item_content:
                        print("[img] --------- %s" % for_getHtml_page_source_line_img_item_cursor_twice)
                        print("之前：【%s】" % getHtml_page_source_line_item_content)
                        print("******************")

                        if "class" not in getHtml_page_source_line_item_content and "alt=\"图片\"" in getHtml_page_source_line_item_content:

                            replace_string = "<img" + getHtml_page_source_line_item_content + ">"

                            # replace_to_string = "<img class='wx_widget_placeholder'" + getHtml_page_source_line_item_content + ">"
                            replace_to_string = "<img class='rich_pages wxw-img'" + getHtml_page_source_line_item_content + ">"

                            getHtml_page_source_line = getHtml_page_source_line.replace(
                                replace_string,
                                replace_to_string
                            )

                        # 解决部分微信公众号爬取的文章的图片不显示的问题
                        if " class=\"" not in getHtml_page_source_line_item_content and " class " in getHtml_page_source_line_item_content:
                            getHtml_page_source_line = getHtml_page_source_line.replace(
                                "class",
                                "class=\"wx_widget_placeholder\""
                            )

                        # if " class=\"wx_widget_placeholder" in getHtml_page_source_line_item_content:
                        #     getHtml_page_source_line = getHtml_page_source_line.replace(
                        #         "class=\"",
                        #         "class=\"wx_widget_placeholder "
                        #     )

                        for_getHtml_page_source_line_img_item_cursor_twice += 1

                    print("之后【%s】" % getHtml_page_source_line_item_content)
                    print("******************")
                    print()

                # 最终整合

                # print("@@@@@@@@@@@@@@")
                # print(getHtml_page_source_line)
                # print("@@@@@@@@@@@@@@")

                getHtml_page_source_finally_current = getHtml_page_source_line
                getHtml_page_source_finally += getHtml_page_source_finally_current

                # print("@@@@@@@@")
                # print(getHtml_page_source_finally_current)

                continue

            if string_replace != "":

                # print("要替换的文本【%s】" % string_replace)

                if is_image:
                    target_file_name = string_replace.split('/')[-2]
                else:
                    target_file_name = string_replace.split('/')[-1]

                # 替换为
                target_file_path_base = save_as_file_name.split(".html")[0] + self.path_page_resource_suffix
                string_replace_to = "./" + target_file_path_base + "/" + target_file_name

                if target_file_name in getHtml_Tag_list_already_local:
                    # print("要替换的文本【%s】" % string_replace)
                    # print("替换为的文本【%s】" % string_replace_to)
                    # print()

                    getHtml_page_source_finally_current = getHtml_page_source_line.replace(
                        string_replace,
                        string_replace_to
                    )

                    if is_image:
                        getHtml_page_source_finally_current = getHtml_page_source_finally_current.split('>')[0] + ' src="' + string_replace_to + '">'

                    getHtml_page_source_finally += getHtml_page_source_finally_current

            getHtml_page_source_finally_current = getHtml_page_source_line
            getHtml_page_source_finally += getHtml_page_source_finally_current

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # 最终输出到本地的HTML中
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        # print(getHtml_page_source_finally)

        getHtml_page_source_finally_file = os.path.join(save_as_directory,save_as_file_name)

        with open(getHtml_page_source_finally_file, 'w') as f:
            f.write(getHtml_page_source_finally)

            data_return = True

        return data_return

    # 解析单个TAG页
    def analyze_wechat_mp_tag_page(self, url):

        data_return = False

        self.browser = webdriver.Chrome()
        self.browser.get(url=url)

        wechat_MP_author_avatar = self.browser.find_element(By.CLASS_NAME, "album__author-avatar").get_attribute('src')
        wechat_MP_author_name = self.browser.find_element(By.CLASS_NAME, "album__author-name").text

        wechat_MP_Tag_name = self.browser.find_element(By.ID, "js_tag_name").text
        wechat_MP_Tag_num = self.browser.find_element(By.CLASS_NAME, "album__num").text.split('个')[0]

        wechat_MP_Tag_Item_ul = self.browser.find_element(By.CLASS_NAME, "album__list")

        wechat_MP_Tag_Item_ul_item_list = wechat_MP_Tag_Item_ul.find_elements(By.XPATH, 'li')

        wechat_MP_Tag_Item_ul_item_title_pos_num = 0

        print("###################################")
        print("作者：%s - 头像【%s】" % (wechat_MP_author_name, wechat_MP_author_avatar))
        print("---------------")
        print("标签名称【%s】文章数量【%s】" % (wechat_MP_Tag_name, wechat_MP_Tag_num))
        print("###################################")
        print()

        # 创建相关目录
        path_converge_to_current_tag = self.path_converge_to_base + "/" \
                                       + wechat_MP_author_name + "/"\
                                       + wechat_MP_Tag_name

        print("路径 - 当前标签【%s】" % path_converge_to_current_tag)
        print('---------------')
        print()

        self.obj_os.execute_os_command_local('mkdir -p %s' % path_converge_to_current_tag)

        # 全局列表 - 已经存储过的文章
        # total_tag_already_save_as_file_name = "total_tag_already_save_as.conf"

        total_article_already_save_as = []
        current_article_already_save_as = []

        with open(self.file_total_article_already_save_as, "r") as f:
            for line in f:
                if line is not None and line != "":
                    total_article_already_save_as.append(line.strip('\n'))

        # 当前标签已经存储过的文章数量
        # current_tag_alraedy_save_num = 0

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(total_article_already_save_as)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        while_wechat_MP_Tag_Item_ul_item_title_pos_num_cursor = 1

        # 有的TAG的文章是有序号的
        # while wechat_MP_Tag_Item_ul_item_title_pos_num != "1.":

        # 进度
        progress_percent = 0

        # 有的TAG的文章是没有序号的
        while_enable_wechat_MP_Tag = True
        while while_enable_wechat_MP_Tag:

            for_wechat_MP_Tag_Item_ul_item_cursor = 1
            for wechat_MP_Tag_Item_ul_item in wechat_MP_Tag_Item_ul_item_list:
                wechat_MP_Tag_Item_ul_item_img = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME, 'album__item-img').get_attribute('style')

                wechat_MP_Tag_Item_ul_item_title = wechat_MP_Tag_Item_ul_item.get_attribute('data-title')
                wechat_MP_Tag_Item_ul_item_article_link = wechat_MP_Tag_Item_ul_item.get_attribute('data-link')

                wechat_MP_Tag_Item_ul_item_id = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME, 'mask_ellipsis').find_element(
                    By.CLASS_NAME, 'mask_ellipsis_text').get_attribute('id')

                wechat_MP_Tag_Item_ul_item_title_pos_num = wechat_MP_Tag_Item_ul_item \
                    .find_element(By.XPATH, '//*[@id="' + wechat_MP_Tag_Item_ul_item_id + '"]/span[1]').text

                wechat_MP_Tag_Item_ul_item_create_time = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME, 'js_article_create_time').text

                # #############################
                # 进度
                # #############################
                progress_percent = int(len(current_article_already_save_as)) / int(wechat_MP_Tag_num)
                print("################## 进度：%s" % progress_percent)
                print("当前TAG的所有文章【%s】" % wechat_MP_Tag_num)
                print("当前已存储的文章【%s】" % int(len(current_article_already_save_as)))
                print("----------------------")
                print()

                if int(wechat_MP_Tag_num) == int(len(current_article_already_save_as)) or wechat_MP_Tag_Item_ul_item_title_pos_num == "1.":
                    while_enable_wechat_MP_Tag = False

                    # 设置返回值，标明当前TAG标签合集页面爬取完毕
                    data_return = True

                print("============================= %03d / %s: %s | [%s]%s" % (
                    for_wechat_MP_Tag_Item_ul_item_cursor, wechat_MP_Tag_num, wechat_MP_Tag_Item_ul_item_create_time,
                    wechat_MP_Tag_Item_ul_item_title_pos_num, wechat_MP_Tag_Item_ul_item_title))

                print("文章地址：【%s】" % wechat_MP_Tag_Item_ul_item_article_link)
                print("封面地址：【%s】" % wechat_MP_Tag_Item_ul_item_img)

                # 转储本地

                # 文件名
                wechat_MP_Tag_Item_ul_item_file_name = wechat_MP_Tag_Item_ul_item_title_pos_num + wechat_MP_Tag_Item_ul_item_title + ".html"
                # 完整路径
                path_output_wechat_MP_Tag_Item_ul_item_file_name = os.path.join(path_converge_to_current_tag, wechat_MP_Tag_Item_ul_item_file_name)

                print("路径 - 当前文章 / 转储【%s】" % path_output_wechat_MP_Tag_Item_ul_item_file_name)

                # 如果已经存储过
                if wechat_MP_Tag_Item_ul_item_file_name in total_article_already_save_as:
                    if wechat_MP_Tag_Item_ul_item_file_name not in current_article_already_save_as:
                        current_article_already_save_as.append(wechat_MP_Tag_Item_ul_item_file_name)

                    continue

                URL_save_as_HTML_result = False

                if wechat_MP_Tag_Item_ul_item_file_name not in total_article_already_save_as:
                    URL_save_as_HTML_result = self.URL_save_as_HTML(
                        html_url=wechat_MP_Tag_Item_ul_item_article_link,
                        save_as_directory=path_converge_to_current_tag,
                        save_as_file_name=wechat_MP_Tag_Item_ul_item_file_name
                    )

                if URL_save_as_HTML_result:
                    total_article_already_save_as.append(wechat_MP_Tag_Item_ul_item_file_name)

                    current_article_already_save_as.append(wechat_MP_Tag_Item_ul_item_file_name)

                    with open(self.file_total_article_already_save_as, "a+") as f:
                        # print(wechat_MP_Tag_Item_ul_item_file_name)

                        f.write(wechat_MP_Tag_Item_ul_item_file_name+"\n")

                print()

                # 自增
                for_wechat_MP_Tag_Item_ul_item_cursor += 1

            scrollTo_Parameter_2 = while_wechat_MP_Tag_Item_ul_item_title_pos_num_cursor * 1000
            self.browser.execute_script(
                "window.scrollTo(0," + str(scrollTo_Parameter_2) + ")"
                # 'document.documentElement.scrollTop=2000'
            )

            while_wechat_MP_Tag_Item_ul_item_title_pos_num_cursor += 1
            wechat_MP_Tag_Item_ul_item_list = wechat_MP_Tag_Item_ul.find_elements(By.XPATH, 'li')

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
