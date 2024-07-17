# # 这是一个示例 Python 脚本。
# import re
#
# from loguru import logger
#
#
import nb_log

from core.BookmarkUtil import BookmarkUtil
from core.Catalogue import Catalogue


def test():
    logger = nb_log.get_logger("demo")


def main():
    # 生成书签对象
    catalogue = Catalogue()
    catalogue.inputRawContentFromFile("./files/input.txt")
    catalogue.getRowLinesByRowContent()
    needPageInfo = not catalogue.getPageStatus()
    if needPageInfo:
        # 这里去完成输入事前的功能

        BookmarkUtil.supplementPageOfBookmarkByInteractive(catalogue.BookmarkLines)
    catalogue.generateFormatContent()
    catalogue.outputFormatContent2File("./files/output.txt")



if __name__ == '__main__':
    main()
    # test()
