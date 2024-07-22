import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import os

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://91mjw.tv/',
    'Cookie': 'uid_id2=7064710c-dc27-4bc5-98e0-e7307ce6b0df:3:1; pdhtkv=true; uncs=1; u_pl=18390142; pdhtkv29=true; uncs29=1'
}

url = 'https://91mjw.tv/vplay/MjI0NDA1NS0yLWhk.html'

re = requests.get(url, headers=headers)

soup = BeautifulSoup(re.text, 'html.parser')

section = soup.find_all('section', class_="container")
iframe = section[0].find('iframe')
src = iframe['src']
m3u8 = src.split('=')

re.close()

resp2 = requests.get(m3u8[-1], headers=headers)

with open('first_m3u8', mode='wb') as fout:
    fout.write(resp2.content)

with open('first_m3u8', 'r') as pd:
    real_m3u8 = pd.readlines()
    result = 'https://v7.dious.cc' + real_m3u8[-1].strip()

req3 = requests.get(result, headers=headers)  # 问题在这里，上一步没有strip()

with open('小黄人大眼萌.m3u8', 'wb') as f:
    f.write(req3.content)


n = 1
with open('小黄人大眼萌.m3u8', mode='r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line.startswith('#'):
            continue
        urls = 'https://v7.dious.cc' + line
        rep4 = requests.get(urls)
        f = open(f'ts文件/{n}.ts', mode='wb')
        f.write(rep4.content)
        rep4.close()
        f.close()
        n += 1
        print(f'完成了{n}个')
# 由于已经下载完毕所有的ts文件，但是不在此根目录内，于是注释掉，以下code均有用


key_url = 'https://v7.dious.cc/20220802/mfLq8Vnf/1500kb/hls/' + 'key.key'
req4 = requests.get(key_url)
key = req4.text

for i in range(1, 1569):
    aes = AES.new(key=b"3ea5de2ffbafccde", iv=b"0000000000000000", mode=AES.MODE_CBC)
    with open(f'/Users/linpeng/Downloads/ts文件/{i}.ts', mode='rb') as f1, open(f'/Users/linpeng/Downloads/ts文件/temp_{i}.ts', 'wb') as f2:
        bs = f1.read()
        f2.write(aes.decrypt(bs))

def merge_ts():

    lst = []
    with open('小黄人大眼萌.m3u8', 'r') as fy:
        for n in range(1, 1569):
            if line.startswith('#'):
                continue
            line = line.strip()
            lst.append(f'/Users/linpeng/Downloads/ts文件/temp_{n}.ts')
            n += 1
    s = " ".join(lst)
    os.system(f"cat {s} > movie.mp4")

merge_ts()
