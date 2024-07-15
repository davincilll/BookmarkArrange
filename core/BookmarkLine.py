from loguru import logger


class BookmarkLine:
    # 缩进数量
    intentationCount = -1
    # 索引
    index = ""
    content = ""
    page = -1

    def __init__(self, intentationCount, index, content, page=-1):
        self.intentationCount = intentationCount
        self.index = index
        self.content = content
        self.page = page

    def __str__(self):
        logger.info(self.intentationCount * "\t" + self.index + " " + self.content + "\t" + str(self.page))
        return self.intentationCount * "\t" + self.index + " " + self.content + "\t" + str(self.page)
