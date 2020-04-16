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
    def save_picture(url, ins_name, file_path):
        status_code = requests.get(url=url,headers=headers).status_code
        if status_code == 200:
            result = requests.get(url)
            file_name = f"data/{ins_name}/{file_path}.jpg"
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
