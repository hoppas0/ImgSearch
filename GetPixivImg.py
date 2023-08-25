import os
import time
import requests
import asyncio
import aiohttp


async def getPixivImg(url: str, name: str = ""):
    """
    通过pixiv网址下载图片
    当name不为空时，就用name来为下载的图片命名，否则用Pixiv的名字
    :param name: str
    :param url: str
    :return: Int
    """
    # 得到返回的网页
    html = requests.get(url=url)
    print("html:", html)
    # 从网页代码里找到目标图片的url
    url_list = html.text.split('"')
    print("url_list", url_list)
    for url in url_list:
        if 'https://i.pximg.net/img-original/' in url:
            img_url = url
            break
    else:
        return 0
    print("img_url", img_url)
    headers_download = {
        "referer": "https://www.pixiv.net/"
        # 这里携带referer因为p站的图片链接都是防盗链
        # 只要加上这个链接就会认为你是从p站访问过来的就会让你正常访问了
    }
    response = requests.get(url=img_url, headers=headers_download)
    # name = url.split("/")[-1]
    if not os.path.exists("PixivImage"):
        os.mkdir("PixivImage")
    if name == "":      # 当name为空时，使用Pixiv原名
        imageName = url.split("/")[-1]
    else:
        imageName = name
    with open("./PixivImage/" + imageName, "wb") as f:
        f.write(response.content)  # 将图片二进制数据存入，图片也就得到了
    print(imageName + "下载成功")
    time.sleep(1)
    return 1


if __name__ == "__main__":
    name = "test.jpg"
    # url = "https://www.pixiv.net/artworks/97099960"
    url = "https://www.pixiv.net/artworks/74718584"
    getPixivImg(name, url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getPixivImg(url,'123.jpg'))
