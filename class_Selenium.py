# -*- coding: UTF-8 -*-

# ================================
# 阶段【导入】
# ================================

from selenium import webdriver
from selenium.webdriver.common.by import By

# ================================
# 阶段【类定义】
# ================================

class class_selenium:

    def __init__(self):
        pass

    def analyze_wechat_mp_tag_page(self, url):

        self.browser = webdriver.Chrome()
        self.browser.get(url=url)

        wechat_MP_author_avatar = self.browser.find_element(By.CLASS_NAME,
                                                                    "album__author-avatar").get_attribute('src')
        wechat_MP_author_name = self.browser.find_element(By.CLASS_NAME, "album__author-name").text

        wechat_MP_Tag_name = self.browser.find_element(By.ID, "js_tag_name").text
        wechat_MP_Tag_num = self.browser.find_element(By.CLASS_NAME, "album__num").text

        wechat_MP_Tag_Item_ul = self.browser.find_element(By.CLASS_NAME, "album__list")

        wechat_MP_Tag_Item_ul_item_list = wechat_MP_Tag_Item_ul.find_elements(By.XPATH, 'li')

        wechat_MP_Tag_Item_ul_item_title_pos_num = 0

        while_wechat_MP_Tag_Item_ul_item_title_pos_num_cursor = 1
        while wechat_MP_Tag_Item_ul_item_title_pos_num != "1.":

            for_wechat_MP_Tag_Item_ul_item_cursor = 1
            for wechat_MP_Tag_Item_ul_item in wechat_MP_Tag_Item_ul_item_list:
                wechat_MP_Tag_Item_ul_item_img = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME,
                                                                                         'album__item-img').get_attribute(
                    'style')

                wechat_MP_Tag_Item_ul_item_title = wechat_MP_Tag_Item_ul_item.get_attribute('data-title')
                wechat_MP_Tag_Item_ul_item_article_link = wechat_MP_Tag_Item_ul_item.get_attribute('data-link')

                wechat_MP_Tag_Item_ul_item_id = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME,
                                                                                        'mask_ellipsis').find_element(
                    By.CLASS_NAME, 'mask_ellipsis_text').get_attribute('id')

                wechat_MP_Tag_Item_ul_item_title_pos_num = wechat_MP_Tag_Item_ul_item \
                    .find_element(By.XPATH, '//*[@id="' + wechat_MP_Tag_Item_ul_item_id + '"]/span[1]').text

                wechat_MP_Tag_Item_ul_item_create_time = wechat_MP_Tag_Item_ul_item.find_element(By.CLASS_NAME,
                                                                                                 'js_article_create_time').text

                print("============================= %03d: %s | [%s]%s" % (
                    for_wechat_MP_Tag_Item_ul_item_cursor, wechat_MP_Tag_Item_ul_item_create_time,
                    wechat_MP_Tag_Item_ul_item_title_pos_num, wechat_MP_Tag_Item_ul_item_title))
                print("文章地址：【%s】" % wechat_MP_Tag_Item_ul_item_article_link)
                print("封面地址：【%s】" % wechat_MP_Tag_Item_ul_item_img)
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
