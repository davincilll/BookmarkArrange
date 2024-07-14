import logging
import re

from core.BookmarkLine import BookmarkLine
from core.exception.LineSplitException import LineSplitException
from core.exception.IndexMatchException import IndexMatchException

WITHOUT_PAGEINFO_LENGTH = 2
WITH_PAGEINFO_LENGTH = 3


class BookmarkUtil:
    # 一级标题匹配
    NONE_INDENTATION_PATTERNS = [r"^第[0-9]+章"]
    # 二级标题匹配
    ONE_INDENTATION_PATTERNS = [r'^[0-9]+\.[0-9]+(?!\.[0-9]+)']
    # 三级标题匹配
    TWO_INDENTATION_PATTERNS = [r"^[0-9]+\.[0-9]+\.[0-9]+(?!\.[0-9]+)"]

    # 交互式补充书页信息
    # 跳转指定行数书签行的命令输入
    JUMP_INDEX_COMMAND = "jp"
    # 展示书签行信息的命令输入
    SHOW_COMMAND = "ls"
    # 保持不变的命令输入
    KEEP_COMMAND = "kp"

    def __init__(self):
        pass

    @classmethod
    def acquireBookmarkLine(cls, line, lineIndex):
        """按照匹配模式分割书签行，lineIndex为书签行在文件中的行号"""
        # 1. 使用标题匹配分割得到三部分
        parts = re.split(r'[\s\t]+', line)
        index = parts[0]
        page = -1
        if len(parts) == WITH_PAGEINFO_LENGTH:
            page = parts[2]
        elif len(parts) == WITHOUT_PAGEINFO_LENGTH:
            pass
        else:
            raise LineSplitException(f"书签行分割异常,行数为{lineIndex}")
        # 判断缩进数量
        if cls.__isMatchNoneIndentationPattern(index):
            return BookmarkLine(0, index, parts[1], page)
        elif cls.__isMatchOneIndentationPattern(index):
            return BookmarkLine(1, index, parts[1], page)
        elif cls.__isMatchTwoIndentationPattern(index):
            return BookmarkLine(2, index, parts[1], page)
        else:
            raise IndexMatchException("标签行索引与现有匹配规则不匹配，行数为{lineIndex}")

    # 按照匹配规则对书签进行替换
    @classmethod
    def replaceBookmarkByPattern(cls, pattern, bookmark):
        pass

    @classmethod
    def supplementPageOfBookmarkByInteractive(cls, bookmarkLines):
        """
        通过交互的方式补充书签的页面信息
        :param bookmarkLines:
        :return:
        """
        index = 0
        while index < len(bookmarkLines):
            # 获取对应行
            bookmarkLine = bookmarkLines[index]
            # 打印对应行信息
            logging.info(
                f"【old】这是书签行信息：行数为{index}，{bookmarkLine.index + bookmarkLine.content + bookmarkLine.page}")
            print(
                "对应页码直接输入数字，跳过请直接回车，展示书签行信息输入'ls -n num/all -d'(-d为可选参数表明输出后面的）,跳转至指定的书签行重新输入jp -n num")
            reiceive_command = input()

            # 进行解析
            def parseCommand(command):
                pass

            def handleSkipCommand(command):
                pass

            def handleShowCommand(command):
                pass

            def handleJumpCommand(command):
                pass

            def InvalidCommand(command):
                pass

            if bookmarkLine.page == -1:
                print("请输入书签的页面信息")
                bookmarkLine.page = input()
                print("输入书签的页面信息为：" + bookmarkLine.page)
            index += 1
        for bookmarkLine in bookmarkLines:
            if bookmarkLine.page == -1:
                print("请输入书签的页面信息")
                bookmarkLine.page = input()
                print("输入书签的页面信息为：" + bookmarkLine.page)

    # 对书签页面进行偏移
    @classmethod
    def offsetPageOfBookmark(cls, bookmark):
        pass

    @classmethod
    def __isMatchNoneIndentationPattern(cls, s):
        for pattern in cls.NONE_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                return True
        return False

    @classmethod
    def __isMatchOneIndentationPattern(cls, s):
        for pattern in cls.ONE_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                return True
        return False

    @classmethod
    def __isMatchTwoIndentationPattern(cls, s):
        for pattern in cls.TWO_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                return True
        return False
