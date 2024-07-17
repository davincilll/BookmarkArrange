import re

from core.BookmarkLine import BookmarkLine
from core.Commands import CommandParser
from core.exception.CommandParseException import CommandParseException
from core.exception.IndexMatchException import IndexMatchException
from settings.logs import nb_logger

WITHOUT_PAGEINFO_LENGTH = 2
WITH_PAGEINFO_LENGTH = 3


class BookmarkUtil:
    # 一级标题匹配
    NONE_INDENTATION_PATTERNS = [r"^第[0-9]+章"]
    # 二级标题匹配
    ONE_INDENTATION_PATTERNS = [r'^[0-9]+\.[0-9]+(?!\.[0-9]+)']
    # 三级标题匹配
    TWO_INDENTATION_PATTERNS = [r"^[0-9]+\.[0-9]+\.[0-9]+(?!\.[0-9]+)"]

    @classmethod
    def acquireBookmarkLine(cls, line, lineIndex):
        """按照匹配模式分割书签行，lineIndex为书签行在文件中的行号"""
        # 1. 使用标题匹配分割得到三部分
        parts = re.split(r'[\s\t]+', line)
        bookmarkIndex = parts[0]
        page = -1
        # 这里生成page信息，以及对parts进行重组（中间可能含有空格的情况）
        if len(parts) == WITH_PAGEINFO_LENGTH:
            # 最后一页是否为空,为空则进行更新parts，不为空则设置page
            if parts[2].isdigit():
                page = parts[2]
            else:
                merged_parts = "".join(parts[1:])
                parts = [parts[0], merged_parts]
        elif len(parts) == WITHOUT_PAGEINFO_LENGTH:
            pass
        else:
            if parts[-1].isdigit():
                # 将中间的部分进行合并
                merged_parts = "".join(parts[1:-1])
                parts = [parts[0], merged_parts, parts[-1]]
            else:
                merged_parts = "".join(parts[1:])
                parts = [parts[0], merged_parts]
            # logger.info(parts)
            # raise LineSplitException(f"书签行分割异常,行数为{lineIndex}")
        # 判断缩进数量
        if page != -1:
            nb_logger.debug(f"page 为 {page}")
        if cls.__isMatchNoneIndentationPattern(bookmarkIndex):
            return BookmarkLine(0, bookmarkIndex, parts[1], page)
        elif cls.__isMatchOneIndentationPattern(bookmarkIndex):
            return BookmarkLine(1, bookmarkIndex, parts[1], page)
        elif cls.__isMatchTwoIndentationPattern(bookmarkIndex):
            return BookmarkLine(2, bookmarkIndex, parts[1], page)
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
        nb_logger.info("【命令行提示】进入交互式输入页数模式")
        bookmarkLinesWithIndex = {
            "index": 0,
            "bookmarkLines": bookmarkLines
        }
        while bookmarkLinesWithIndex["index"] < len(bookmarkLinesWithIndex["bookmarkLines"]):
            _index = bookmarkLinesWithIndex["index"]
            bookmarkLine = bookmarkLinesWithIndex["bookmarkLines"][_index]
            nb_logger.warning(
                "\n1.对应页码直接输入数字\n2. 跳过请直接回车\n3. 展示书签行信息输入'ls -n num -d'(-d为可选参数表明输出后面的,不输入-n则默认输出全部）\n4. 跳转至指定的书签行重新输入jp num")
            nb_logger.info(
                f"【default】【old】这是书签行信息：行数为{_index + 1}，{bookmarkLine.index + bookmarkLine.content}\t{str(bookmarkLine.page)}")
            reiceive_command = input()
            try:
                commonCommand = CommandParser.parse2Command(reiceive_command)
                # changeIndex(bookmarkLinesWithIndex=bookmarkLinesWithIndex)
                nb_logger.debug(f"当前书签行索引为{bookmarkLinesWithIndex['index']}")
                commonCommand.execute(bookmarkLinesWithIndex=bookmarkLinesWithIndex)
                nb_logger.debug(f"当前书签行索引为{bookmarkLinesWithIndex['index']}")
            except CommandParseException:
                nb_logger.warning("命令行输入错误，请重新输入")

        nb_logger.info("执行完毕")

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

# # 设置书的偏移用的
# def setPageOffset(text, offset):
#     lines = text.split('\n')
#     index = 0
#     while index < len(lines):
#         line = lines[index]
#         parttern = r"\b[0-9]+\b$"
#         # 输入页码数
#         m = re.search(parttern, line)
#         if not m:
#             logger.info("有问题的line:" + line)
#         original = int(m.group())
#         realPage = original + offset
#         if m:
#             line = re.sub(parttern, str(realPage), line)
#             lines[index] = line
#             index += 1
#     indent_text = '\n'.join(lines)
#     return indent_text
