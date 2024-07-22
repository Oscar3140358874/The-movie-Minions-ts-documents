import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiofiles

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


async def download_ts(url1, name, session):
    async with session.get(url1) as resp:
        async with aiofiles.open(f'ts文件2/{name}', mode='wb') as fppt:
            await fppt.write(await resp.content.read())
    print(f'{name}', '下载完毕')


async def aio_download(up_url):  # up_url是'https://v7.dious.cc'
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open("小黄人大眼萌.m3u8", mode='r', encoding='utf-8') as fpc:
            async for line in fpc:
                if str(line).startswith('#'):
                    continue
                line = str(line).strip()
                # 拼接ts的url
                ts_url = up_url + line
                task = asyncio.create_task(download_ts(ts_url, line, session))  # 创建任务
                tasks.append(task)
            await asyncio.wait(tasks)  # 等待任务结束


asyncio.run(aio_download('https://v7.dious.cc'))
