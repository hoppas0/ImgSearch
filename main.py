import base64
import asyncio
import time

from PIL import Image
import PySimpleGUI as sg
import os.path
from io import BytesIO
from ImgSearch import ImgSearch
from UrlToBase64 import urltobase64
from GetPixivImg import GetPixivImg
import pyperclip

apikey = ''


async def run():
    file_list_column = [
        [sg.Text("将你的 api key 填到下方")],
        [sg.Input(key="-apikey-", size=(40, 1))],
        [sg.Text("在下面选择一个有图片的文件夹")],
        [
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse('浏览'),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
        [sg.Button(key="-download-", button_text="自动搜图并下载"),
         sg.Text("这里的下载仅限于pixiv上的图片")],
        [sg.Text(size=(40, 1), key="-remaining-")],
    ]
    image_viewer_column = [
        [sg.Text("从左边图片列表中选择一张图片:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-", size=(512, 512))],
    ]
    image_viewer2_column = [
        [sg.Image(key="-IMAGE2-", size=(256, 256))],
        [sg.Text("相似度:", key="-similarity-")],
        [sg.Text("作者:", key="-author-")],
        [sg.Input(key='-URL-', size=(20, 1)),
         sg.Button(key="-copyUrl-", button_text="复制链接")],
        [sg.Text("注意：")],
        [sg.Text("搜图前请确认是否填写好apikey")],
        [sg.Text("下载前请确认是否打开了代理")],
    ]
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
            sg.VSeperator(),
            sg.Column(image_viewer2_column),
        ]
    ]
    window = sg.Window("ImgSearch", layout)

    while True:
        event, values = window.read()
        try:
            with open('apikey.txt', 'r', encoding='utf-8') as f:
                apikey = f.readline()
                window["-apikey-"].update(apikey)
        except:
            window["-remaining-"].update("apikey.txt出错了")

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-copyUrl-":
            pyperclip.copy(values["-URL-"])



        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                   and f.lower().endswith((".png", ".gif", ".jpg"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":
            apikey = values["-apikey-"]
            try:
                # filename = os.path.join(
                #     values["-FOLDER-"], values["-FILE LIST-"][0]
                # )
                filename = values["-FOLDER-"] + '/' + values["-FILE LIST-"][0]
                window["-TOUT-"].update(filename)
                image = Image.open(filename)
                # 下面用来缩小图片方便显示，使图片最大为512*512
                w, h = image.size
                max_size = max(w, h)
                if max_size > 512:
                    image = image.resize((int(512.0 * w / max_size),
                                          int(512.0 * h / max_size)), Image.ANTIALIAS)
                if filename[-3:] == 'jpg':  # 如果是jpg文件，则用PIL转成PNG的四个通道
                    image.convert("RGBA")
                img_buffer = BytesIO()
                image.save(img_buffer, format='PNG')
                byte_data = img_buffer.getvalue()
                base64_data = base64.b64encode(byte_data)
                # window["-IMAGE-"].update(filename=filename)
                window["-IMAGE-"].update(data=base64_data)

                # 搜图并显示结果
                resp = await ImgSearch(filename, apikey)
                url = resp.raw[0].thumbnail  # 缩略图地址
                remaining = [resp.short_remaining, resp.long_remaining]
                rb64 = urltobase64(url)
                rb = base64.b64decode(rb64)
                rimg_data = BytesIO(rb)
                rimg = Image.open(rimg_data)
                if rb64[:3] == b'/9j':
                    rimg.convert("RGBA")
                rimg_buffer = BytesIO()
                rimg.save(rimg_buffer, format='PNG')
                rbyte_data = rimg_buffer.getvalue()
                rb64f = base64.b64encode(rbyte_data)
                window["-similarity-"].update(f"相似度:{resp.raw[0].similarity}")
                window["-author-"].update(f"作者:{resp.raw[0].author}")
                window["-remaining-"].update(f"剩余访问额度: 每天:{remaining[1]} 每30秒:{remaining[0]}")
                window["-URL-"].update(resp.raw[0].url)
                window["-IMAGE2-"].update(data=rb64f)
            except BaseException as e:
                print("出错了")
                print(e.args)
                window["-remaining-"].update("出错了")

        if event == "-download-":       # 这只下载，就不显示了
            # 打开文件夹
            path = values["-FOLDER-"]
            dirs = os.listdir(path)
            window["-remaining-"].update("正在下载")
            # 搜索并保存图片
            for file in dirs:
                if file[-3:] in ["jpg", "png"]:
                    filename = path+'/'+file
                    resp = await ImgSearch(filename, apikey)
                    if "pixiv.net" in resp.raw[0].url:
                        GetPixivImg(file, resp.raw[0].url)
                        if resp.short_remaining == 0:
                            time.sleep(30)
                            if resp.long_remaining == 0:
                                window["-remaining-"].update("每日访问额度用完了")
                                break
            else:
                window["-remaining-"].update("下载结束")

    window.close()


if __name__ == "__main__":
    asyncio.run(run())
