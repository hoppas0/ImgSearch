import os
import time
import requests


async def GetPixivImg(name:str, url:str):
    """
    通过pixiv网址下载图片
    由于这是个搜索原图并下载的程序，为了方便看出原图片是否下载到原图，所以这里下载图片的名字就是原图片的名字
    :param name: str
    :param url: str
    :return: Int
    """
    # 得到返回的网页
    html = requests.get(url=url)
    # 从网页代码里找到目标图片的url
    url_list = html.text.split('"')
    for url in url_list:
        if 'https://i.pximg.net/img-original/' in url:
            img_url = url
            break
    else:
        return 0
    headers_download = {
        "referer": "https://www.pixiv.net/"
        # 这里携带referer因为p站的图片链接都是防盗链
        # 只要加上这个链接就会认为你是从p站访问过来的就会让你正常访问了
    }
    response = requests.get(url=img_url, headers=headers_download)
    # name = url.split("/")[-1]
    if not os.path.exists("PixivImage"):
        os.mkdir("PixivImage")
    with open("./PixivImage/" + name, "wb") as f:
        f.write(response.content)  # 将图片二进制数据存入，图片也就得到了
    print(name + "下载成功")
    time.sleep(1)
    return 1


if __name__ == "__main__":
    name="test.jpg"
    url="https://www.pixiv.net/artworks/97099960"
    GetPixivImg(name, url)