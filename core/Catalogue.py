# 用于封装书签信息
import re

from core.BookmarkLine import BookmarkLine
from core.BookmarkUtil import BookmarkUtil
from settings.logs import nb_logger, debug_logger


class Catalogue:
    # 需要封装各类文本信息
    rowContent = ""
    formatContent = ""
    BookmarkLines: list[BookmarkLine] = []

    # 封装原始目录信息
    def __init__(self):
        pass

    # 向文件中输出内容
    def outputFormatContent2File(self, filePath):
        with open(filePath, "w", encoding="utf-8") as file:
            file.write(self.formatContent)

    # 从文件中读取内容
    def inputRawContentFromFile(self, filePath):
        with open(filePath, "r", encoding="utf-8") as file:
            text = file.read()
            self.rowContent = text

    def generateFormatContent(self):
        self.formatContent = "\n".join([str(bookmarkLine) for bookmarkLine in self.BookmarkLines])

    def getRowLinesByRowContent(self):
        temp = self.rowContent.split("\n")
        # 去除空行
        count = 0
        for line in temp:
            isEmptyLine = re.match(r"^\n", line) or line == '' or line == ' '
            if isEmptyLine:
                continue
            # 统一取消最开头的所有缩进
            line = re.sub(r"^\s+", "", line)
            count += 1
            # 按照正则表达式，进行分割字符串，分为三部分，并确定使用缩进的数量
            bookmarkLine = BookmarkUtil.acquireBookmarkLine(line, count)
            debug_logger.debug(f"整理后的bookmarkLine为{bookmarkLine}")
            self.BookmarkLines.append(bookmarkLine)

    # 获取page状态
    def getPageStatus(self):
        """
        这里查看目录的页数状态
        :return: true 表示目录页数已经确定
                false 表示目录页数还没有确定
        """
        for bookmarkLine in self.BookmarkLines:
            # 如果书签行的页面还没有确定，则返回false
            # 这里会返回false
            #     if not bookmarkLine.getPageStatus():
            #         nb_logger.warning("目录页数还没有确定")
            #         return False
            # return True
            # 这里切换成只要有一个页数存在，就会返回True
            # 因为存在部分书页的一级标题是没有书页的，但是后面是有书页的
            # todo： 以配置的形式进行切换
            if bookmarkLine.getPageStatus():
                return True
        return False
