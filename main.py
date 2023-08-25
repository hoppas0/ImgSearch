import base64
import asyncio
import time

from PIL import Image
import PySimpleGUI as sg
import os.path
from io import BytesIO
from ImgSearch import ImgSearch
from UrlToBase64 import urltobase64
from GetPixivImg import getPixivImg
import pyperclip

apikey = ''
selectedLanguage = "Chinese"
expectedName = 'fileName'
languages = {
    'Chinese': {
        'SELECTLANGUAGE': '选择语言',
        'TIPS1': '将你的 api key 填到下方：',
        'TIPS2': '在下面选择一个有图片的文件夹',
        'FolderBrowse': '浏览',
        'download': '自动搜图并下载',
        'TIPS3': '这里的下载仅限于pixiv上的图片',
        'TIPS4': '从左边图片列表中选择一张图片:',
        'similarity': '相似度:',
        'author': '作者:',
        'copyUrl': '复制链接',
        'TIPS5': '注意：',
        'TIPS6': '搜图前请确认是否填写好apikey',
        'TIPS7': '下载前请确认是否打开了代理',
        'rename': '下载的图片命名为:',
        'filename': '原文件名',
        'pixivname': '原Pixiv名'
    },
    'English': {
        'SELECTLANGUAGE': 'Select language',
        'TIPS1': 'Fill in your API key below:',
        'TIPS2': 'Select a folder with pictures below',
        'FolderBrowse': 'Browse',
        'download': 'Search and download images automatically',
        'TIPS3': 'The download here is limited to images on Pixiv',
        'TIPS4': 'Select an image from the list of images on the left:',
        'similarity': 'Similarity:',
        'author': 'Author:',
        'copyUrl': 'Copy the link',
        'TIPS5': 'Warning:',
        'TIPS6': 'Before searching for images,',
        'TIPS7': 'please make sure that you fill in the apikey',
        'rename': 'The downloaded picture is named:',
        'filename': 'Original file name',
        'pixivname': 'Original Pixiv name'
    }
}


async def run():
    global apikey, languages, selectedLanguage, expectedName
    file_list_column = [
        [sg.Text("选择语言", size=(20, 1), key='-SELECTLANGUAGE-'),
         sg.Combo(["Chinese", "English"], size=(10, 1), default_value="Chinese", enable_events=True, key='-LANGUAGE-')],
        [sg.Text("将你的 api key 填到下方", key='-TIPS1-')],
        [sg.Input(key="-apikey-", size=(40, 1))],
        [sg.Text("在下面选择一个有图片的文件夹", key='-TIPS2-')],
        [
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse('浏览', key='-FolderBrowse-'),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
        [sg.Text("下载的图片命名为:", key='-rename-')],
        # [sg.Radio('原文件名', "RADIO1", default=True, key='-filename-'), sg.Radio('原Pixiv名', "RADIO1",key='-pixivname-')],
        [sg.Button('原文件名', key='-fileName-', button_color=('white', "#082567")),
         sg.Button('    ', key='-pixivName-', button_color=('#082567', "#082567"))],
        [sg.Button(key="-download-", button_text="自动搜图并下载")],
        [sg.Text("这里的下载仅限于pixiv上的图片", key='-TIPS3-')],
        [sg.Text(size=(40, 1), key="-remaining-")],
    ]
    image_viewer_column = [
        [sg.Text("从左边图片列表中选择一张图片:", key='-TIPS4-')],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-", size=(512, 512))],
    ]
    image_viewer2_column = [
        [sg.Image(key="-IMAGE2-", size=(256, 256))],
        [sg.Text("相似度:", key="-similarity-")],
        [sg.Text("作者:", key="-author-")],
        [sg.Input(key='-URL-', size=(20, 1)),
         sg.Button(key="-copyUrl-", button_text="复制链接")],
        [sg.Text("注意：", key='-TIPS5-')],
        [sg.Text("搜图前请确认是否填写好apikey", key='-TIPS6-')],
        [sg.Text("下载前请确认是否打开了代理", key='-TIPS7-')],
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
            window["-remaining-"].update(
                "apikey.txt出错了" if selectedLanguage == 'Chinese' else "APIkey .txt Something went wrong")

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-LANGUAGE-":
            selectedLanguage = values['-LANGUAGE-']
            window['-SELECTLANGUAGE-'].update(languages[selectedLanguage]['SELECTLANGUAGE'])
            window['-TIPS1-'].update(languages[selectedLanguage]['TIPS1'])
            window['-TIPS2-'].update(languages[selectedLanguage]['TIPS2'])
            window['-FolderBrowse-'].update(languages[selectedLanguage]['FolderBrowse'])
            window['-download-'].update(languages[selectedLanguage]['download'])
            window['-TIPS3-'].update(languages[selectedLanguage]['TIPS3'])
            window['-TIPS4-'].update(languages[selectedLanguage]['TIPS4'])
            window['-similarity-'].update(languages[selectedLanguage]['similarity'])
            window['-author-'].update(languages[selectedLanguage]['author'])
            window['-copyUrl-'].update(languages[selectedLanguage]['copyUrl'])
            window['-TIPS5-'].update(languages[selectedLanguage]['TIPS5'])
            window['-TIPS6-'].update(languages[selectedLanguage]['TIPS6'])
            window['-TIPS7-'].update(languages[selectedLanguage]['TIPS7'])
            window['-rename-'].update(languages[selectedLanguage]['rename'])
            if expectedName == 'fileName':
                window['-fileName-'].update(languages[selectedLanguage]['filename'])
            else:
                window['-pixivName-'].update(languages[selectedLanguage]['pixivname'])

        if event == "-fileName-":
            expectedName = 'fileName'
            window['-fileName-'].update(languages[selectedLanguage]['filename'], button_color=('white', "#082567"))
            window['-pixivName-'].update("    ", button_color=('#082567', "#082567"))

        if event == "-pixivName-":
            expectedName = 'pixivName'
            window['-fileName-'].update("    ", button_color=('#082567', "#082567"))
            window['-pixivName-'].update(languages[selectedLanguage]['pixivname'], button_color=('white', "#082567"))

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
                similarity_message = f"相似度:{resp.raw[0].similarity}%" if selectedLanguage == 'Chinese' else f"Similarity:{resp.raw[0].similarity}%"
                window["-similarity-"].update(similarity_message)
                author_message = f"作者:{resp.raw[0].author}" if selectedLanguage == 'Chinese' else f"Author:{resp.raw[0].author}"
                window["-author-"].update(author_message)
                remaining_message = f"剩余访问额度: 每天:{remaining[1]}  每30秒:{remaining[0]}" if selectedLanguage == 'Chinese' else f"Remaining access credit: One day:{remaining[1]}  30s:{remaining[0]}"
                window["-remaining-"].update(remaining_message)
                window["-URL-"].update(resp.raw[0].url)
                window["-IMAGE2-"].update(data=rb64f)
            except BaseException as e:
                print("出错了")
                print(e.args)
                window["-remaining-"].update("出错了" if selectedLanguage == 'Chinese' else 'Something went wrong')

        if event == "-download-":  # 下载时不显示正在下载的图片
            # 打开文件夹
            path = values["-FOLDER-"]
            dirs = os.listdir(path)
            window["-remaining-"].update("正在下载，请稍候" if selectedLanguage == 'Chinese' else 'Please wait')
            # 搜索并保存图片
            for file in dirs:
                if file[-3:] not in ["jpg", "png"]:
                    continue
                filename = path + '/' + file
                resp = await ImgSearch(filename, apikey)
                if resp.short_remaining == 0:
                    time.sleep(30)
                if resp.long_remaining == 0:
                    window["-remaining-"].update(
                        "每日访问额度用完了" if selectedLanguage == 'Chinese' else 'The daily access credit is running out')  # 之前是8层缩进,现在缩减到了5层
                    break
                if "pixiv.net" not in resp.raw[0].url:
                    continue
                if expectedName == 'fileName':
                    await getPixivImg(resp.raw[0].url, file)  # 异步调用GetPixivImg
                else:
                    await getPixivImg(resp.raw[0].url)          # 图片命名为原Pixiv名
            else:  # for循环正常结束
                window["-remaining-"].update("下载结束" if selectedLanguage == 'Chinese' else 'The download ends')

    window.close()


if __name__ == "__main__":
    asyncio.run(run())
