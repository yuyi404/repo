import time
import requests
import os
import re

# RED = "\033[31m"
# RESET = "\033[0m"
# GREEN = "\033[32m"

print('Tips: 如果出现错误,请检查你的cookie是否正确!')

print("=============================================================")

with open('cookie.txt', 'rb') as file:
    cookie = file.read()

headers = {
    'cookie': cookie,
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


text =eval(input('输入你要爬取的快手主页地址:'))
pattern = r'https?://[^\s]+'

# 查找链接
link = re.findall(pattern, text)
print(link)
for links in link:

    links_url = requests.get(links, allow_redirects=True,headers=headers)
    final_url = links_url.url
    print()
    print('--------------------------------------------------')
    id_list =re.findall("profile/(.*?)\?fid",final_url)
    print(id_list)
    print(('匹配到主页地址数:',len(link)))
    print('--------------------------------------------------')

    total_count = 0  # 总视频数量
    filtered_count = 0  # 过滤掉的视频数量

    for principalId in id_list:
        url = f'https://live.kuaishou.com/live_api/profile/public?count=5000&pcursor=&principalId={principalId}&hasMore=true'

        for _ in range(3):  # 尝试3次
            req = requests.get(url, headers=headers).json()
            time.sleep(5)
            try:

                lists = req['data']['list']
                ids = lists[0]['author']['id']
                name = lists[0]['author']['name']

                current_path = os.getcwd()
                path = f"{name}.txt"
                # print(path)
                if os.path.exists(path):

                    print(('用户ID:', ids))
                    print(('用户昵称:', name))
                    print('--------------------------------------------------')
                video_count = 0  # 用户视频数量
                filtered_count = 0  # 用户被过滤掉的视频数量

                for i, item in enumerate(lists):
                    playUrl = item['playUrl']
                    if playUrl.endswith("mp4"):
                        filtered_count += 1
                        playUrl = " "  # 将以mp4结尾的playUrl替换为空格
                    if playUrl.strip():
                        print(playUrl)
                        with open(path, mode='a', encoding='utf-8') as f:
                            f.write(playUrl + '\n')  # 写入playUrl并换行
                        video_count += 1
                print('----------------------------------------------------------------')
                print(f"{name}的视频数量:{video_count}")
                print(f"{name}被过滤掉的视频数量:{filtered_count}")
                print('----------------------------------------------------------------')

                total_count += video_count
                filtered_count += filtered_count

                break  # 如果成功则跳出重试循环
            except Exception as e:
                print(f"获取用户信息失败:{e}")
                continue  # 如果出现异常则重试

# print(f"共过滤掉的视频数量:{filtered_count}")  # 输出过滤掉的视频数量
# print(f"总共获取到视频数量:{total_count}")  # 输出总视频数量
print(f"爬取的数据保存至:{current_path}")
print()
eval(input('按任意键结束运行......'))
