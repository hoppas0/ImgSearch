# ImgSearch

基于 PicImageSearch 的搜图小程序，可以利用 SauceNAO 搜出图片的来源（pixiv、twitter等都可以）。还可以把要搜的图放在一个文件夹里，自动下载图片的原图（如果能搜到并且原图来自pixiv的话）

![avatar](https://files.catbox.moe/y0th5c.png)
![avatar](https://files.catbox.moe/zfs9ek.png)

## 如何使用

首先去 [SauceNAO](https://saucenao.com/) 获得 api key，具体方法如下：

1.打开 [SauceNAO](https://saucenao.com/)，点击右下角的 Account

2.在 Register 中注册你的账号

3.注册登录成功后，点击个人页面左上角的 api

4.然后出现的一大串英文和数字就是 api key 

然后在 ImgSearch.exe(main.exe) 的同级目录下创建 apikey.txt，将 api key 填入其中，这样就不用每次都手动填写 api key 了

接下来你要点击浏览按钮，打开你已经存放了图片的文件夹，例如示例图片中我打开了 tu 文件夹

如果你只是想搜图，你可以直接点击左侧列表里的图片，例如示例图片中我点击了 80130917_p0.png ，中间用来显示 80130917_p0.png 图片，右面是搜图的结果

如果点击了“自动搜图并下载”，它会在同级目录下创建一个名叫 PixivImages 的文件夹，并且把搜到的原图下载到这个文件夹里。而且，下载的图片的名字和原图片名是相同的，方便比较查出哪些图片没有下载。
例如，下面是我用来测试的10张图片

![avatar](https://files.catbox.moe/h1qhw4.png)

选择图片的命名方式为”原文件名“，点击“自动搜图并下载”按钮后，得到的结果如下图（如果原图不来自pixiv或者出现了网络问题，那么就会跳过这张图去下载下一个,并且被跳过的图片会放在FailedImages文件夹里）

![avatar](https://files.catbox.moe/mpfj79.png)

因为图片的名字是相同的，所以排序方式也是相同的，这样就方便找出哪些图没有下载

如果你选择图片的命名方式为”原Pixiv名“，那么下载后得到的结果如下图

![avatar](https://files.catbox.moe/smxglu.png)

## 注意

由于网络问题和我的代码问题，所以它运行的可能有些慢，并且有时候会无响应。搜图的话大概5秒就能看到结果，请耐心等待，不要频繁操作。如果是批量下载的话，那将会根据图片数量等待一段时间，建议点完“自动搜图并下载”之后就挂在后台不管，全部下载好之后就可以正常操作了
