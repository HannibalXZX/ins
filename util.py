# -*- coding:utf-8 -*-
#@Time  :    2020/4/2 20:25
#@Author:    Shaw
#@mail  :    shaw@bupt.edu.cn
#@File  :    util.py
#@Description：

import requests
import time
cookie='''ig_did=23BBD2E7-D425-4733-8B93-52FEC0F37904; mid=XnySTgAEAAH92405mPXuQ3N3Pu3P; csrftoken=wmLW0RWM3inETWJ8GAujgiG1aGS0NUnh; shbid=11724; shbts=1585222313.429058; ds_user_id=7273260779; sessionid=7273260779%3ArbTcLPssaXtIQT%3A9; rur=FTW; urlgen="{\"185.245.42.179\": 55933}:1jHRVY:DidgQnnDFC9volHIJmbg1Ayaw1E"'''

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "cookie": cookie,
}

class util_ins(object):

    @staticmethod
    def get_website_result(url):
        req = requests.get(url=url, headers=headers)
        result = req.text
        result = result.replace('true', '\'true\'')
        result = result.replace('false', '\'false\'')
        result = result.replace('null', '\'null\'')
        return result

    @staticmethod
    def save_text(text, like_count, ins_name, file_path):
        print("save_text")
        print(text)
        try:
            fr = open(f"data/{ins_name}/text/{file_path}.txt", "w", encoding="utf-8")
            # print(type(text))
            text = text.encode('UTF-8','ignore').decode('UTF-8')
            fr.write(text + "\n")
            fr.write(str(like_count))
        except UnicodeEncodeError as err:
            print(err)
            fr.flush()
            fr.close()
        

    @staticmethod
    def save(url, ins_name, file_path, category="picture"):
        '''
        :param url: 链接
        :param ins_name: ins的用户名
        :param file_path: 文件路径
        :param category: 种类
        picture: 图片
        video：视频
        :return:
        '''
        status_code = requests.get(url=url, headers=headers).status_code
        if status_code == 200:
            result = requests.get(url)
            if "/" in file_path:
                _list = file_path.split("/")
                dir = "/".join(_list[:-1])
                base_dir = f"data/{ins_name}/media/"+dir
            else:
                base_dir = f"data/{ins_name}/media"

            import os
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

            if category == "picture":
                file_name = f"data/{ins_name}/media/{file_path}.jpg"
            elif category == "video":
                file_name = f"data/{ins_name}/media/{file_path}.mp4"
            else:
                print("输入错误！")
                return

            with open(file_name, 'wb') as f:
                f.write(result.content)
            f.close()

            print("内容获取成功,暂停0.1s....")
            time.sleep(0.1)
            fr = open(f"log/{ins_name}.txt", "a")
            fr.write(url + "\n")
            fr.flush()
            fr.close()
        else:
            print(f"没获取到资源")
            time.sleep(1)


if __name__ == '__main__':
    print(headers)
