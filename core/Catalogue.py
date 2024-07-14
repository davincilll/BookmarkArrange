# 用于封装书签信息
import re

from core.BookmarkUtil import BookmarkUtil


class Catalogue:
    # 需要封装各类文本信息
    rowContent = ""
    formatContent = ""
    BookmarkLines = []

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
            self.BookmarkLines.append(bookmarkLine)

    # 获取page状态
    def getPageStatus(self):
        pass
