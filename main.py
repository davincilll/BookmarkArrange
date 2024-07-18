# # 这是一个示例 Python 脚本。
# import re
#
# from loguru import logger
#
#
import nb_log

from core.BookmarkUtil import BookmarkUtil
from core.Catalogue import Catalogue


def main():
    # 生成书签对象
    catalogue = Catalogue()
    catalogue.inputRawContentFromFile("./files/input.txt")
    catalogue.getRowLinesByRowContent()
    needPageInfo = not catalogue.getPageStatus()
    if needPageInfo:
        BookmarkUtil.supplementPageOfBookmarkByInteractive(catalogue.BookmarkLines)
    catalogue.generateFormatContent()
    catalogue.outputFormatContent2File("./files/output.txt")


if __name__ == '__main__':
    main()
