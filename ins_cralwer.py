# -*- coding:utf-8 -*-
#@Time  :    2020/3/26 12:50
#@Author:    Shaw
#@mail  :    shaw@bupt.edu.cn
#@File  :    test.py
#@Description：

from util import util_ins
import configparser

class ins_cralwer(object):

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read("config.ini")

    # 观察网页,获取初始的variables
    def get_init_variables(self, ins_name):
        id = self.cf.get(ins_name, 'id')
        first = self.cf.get('ins_name', 'first')
        after = self.cf.get('ins_name', 'after')
        init_variables = {
        "id": id,
        "first": int(first),
        "after": after
        }
        return init_variables

    # 构造variables
    def joint_variables(self, ins_name, after):
        id = self.cf.get(ins_name, 'id')
        first = self.cf.get('ins_name', 'first')
        init_variables = {
            "id": id,
            "first": int(first),
            "after": after
        }
        return init_variables

    # 构造url
    def joint_url(self, ins_name, variables):
        url = self.cf.get(ins_name, "url")
        query_hash = self.cf.get(ins_name, "query_hash")
        url = f"{url}?query_hash={query_hash}&variables={variables}"
        print(url)

    # 获取下一个afet值
    def get_next_after(self, dict_result):
        page_info = dict_result['data']['user']['edge_owner_to_timeline_media']['page_info']
        # next_page
        if page_info['has_next_page'] == 'true':
            end_cursor = page_info['end_cursor']
            return end_cursor
        else:
            return ""

    def download(self, dict_result, ins_name, count):
        # 读取已经爬取过的url
        f = open(f'log/{ins_name}.txt', 'r+')
        list_line = [line.strip() for line in f]
        f.close()

        edges = dict_result['data']['user']['edge_owner_to_timeline_media']['edges']
        for edge in edges:
            url = edge['node']['display_url']
            if url in list_line:
                print('url is exist!!!')
            else:
                util_ins.save_picture(url, str(count))
            count += 1

        return count+1

    def process(self, ins_name):
        # 1、获取初始的url
        init_variables = self.get_init_variables(ins_name)
        url = self.joint_url(ins_name, init_variables)

        # 后期可自行设置
        init_count = 0

        # 循环构造下一次链接请求
        # 获取结果
        result = util_ins.get_website_result(url)
        dict_result = eval(result)
        count = self.download(dict_result=dict_result, ins_name=ins_name, count=init_count)
        next_after = self.get_next_after(dict_result)

        while next_after:
            # 获取新的get请求参数
            variables = self.joint_variables(ins_name, next_after)
            new_url = self.joint_url(ins_name, variables)

            result = util_ins.get_website_result(new_url)
            dict_result = eval(result)
            count = self.download(dict_result=dict_result, ins_name=ins_name, count=count)
            next_after = self.get_next_after(dict_result)

        print("全部下载完毕！")


if __name__ == '__main__':
    ins_cralwer = ins_cralwer()
    ins_name = "bbc_travel"
