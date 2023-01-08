#基本来自示例代码
import asyncio
from loguru import logger
from PicImageSearch import Network, SauceNAO
from PicImageSearch.model import SauceNAOResponse

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
filename = "E:/my/tu/robot/20.png"
api_key = "f53999896aafed5928d4ae136c5d0d600039b467"
bypass = True  # 是否绕过DNS污染


@logger.catch()
async def ImgSearch(filename:str, api_key:str) -> SauceNAOResponse:
    async with Network(proxies=proxies, bypass=bypass) as client:
        saucenao = SauceNAO(client=client, api_key=api_key, hide=3)
        # resp = await saucenao.search(url=url)
        resp = await saucenao.search(file=filename)
        # show_result(resp)
        return resp

def show_result(resp: SauceNAOResponse) -> None:
    logger.info(resp.status_code)  # HTTP 状态码
    logger.info(resp.origin)  # 原始数据
    logger.info(resp.url)
    logger.info(resp.raw[0].origin)
    logger.info(resp.long_remaining)
    logger.info(resp.short_remaining)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].similarity)
    logger.info(resp.raw[0].hidden)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].author)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].ext_urls)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ImgSearch(filename,api_key))
