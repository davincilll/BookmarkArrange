# 用于整理pdf的书签内容

## 目前已有的功能

1. 根据正则表达式对缩进进行整理
2. 使用交互式命令的方式手动快速填写书签对应的页数

## 使用方法
1. 将未处理的书签放在files/input.txt下
2. 代码说明
   ```python
    # 实例化书签对象
    catalogue = Catalogue()
    # 读取目录信息
    catalogue.inputRawContentFromFile("./files/input.txt")
    # 分割得到每一行
    catalogue.getRowLinesByRowContent()
    # 判断是否需要调用交互式的方式填写page状态
    needPageInfo = not catalogue.getPageStatus()
    if needPageInfo:
        BookmarkUtil.supplementPageOfBookmarkByInteractive(catalogue.BookmarkLines)
    # 生成format的目录
    catalogue.generateFormatContent()
    # 输出到output.txt中
    catalogue.outputFormatContent2File("./files/output.txt")
   ```

## 说明
基本骨架已经搭建好了，后面就是丰富功能了。欢迎大家pr和指正。

## 后面可能会陆续加上的功能
1. 使用yaml解耦配置（目前是将正则表达式放在BookmarkUtil类下作为属性）
2. 进一步拓展命令行功能（目前是只在交互式填写page时使用了命令行，这里采用的是设计模式里的命令模式，前置的引导还需要在main中手动实现）
3. 使用图像分割与图像识别取代交互式填写page的方式
4. 根据标题去豆瓣、淘宝、孔夫子旧书网抓取筛选获得raw目录信息
5. 批量整理
