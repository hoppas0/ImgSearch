import base64
import requests as req
from io import BytesIO


def urltobase64(url):
    # 图片保存在内存
    response = req.get(url)
    # 得到图片的base64编码
    ls_f = base64.b64encode(BytesIO(response.content).read())
    # 将base64编码进行解码
    # imgdata = base64.b64decode(ls_f)
    return ls_f



if __name__ == "__main__":
    url = 'https://img3.saucenao.com/dA2/86767/867670574.jpg?auth=xa7vODyYEuJzP5ONSYLuxg&exp=1672776000'
    print(type(urltobase64(url)))
    print(urltobase64(url))
