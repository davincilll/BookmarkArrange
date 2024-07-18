import re

from core.BookmarkLine import BookmarkLine
from core.Commands import CommandParser
from core.exception.CommandParseException import CommandParseException
from core.exception.IndexMatchException import IndexMatchException
from settings.logs import nb_logger, debug_logger

WITHOUT_PAGEINFO_LENGTH = 2
WITH_PAGEINFO_LENGTH = 3
# 规定全都不匹配时的缩进数量
INDENTATIONCOUNTWITHOUTMATCH = 2


class BookmarkUtil:
    # 一级标题匹配
    NONE_INDENTATION_PATTERNS = [r"^第[0-9]+章", r"^第[一|二|三|四|五|六|七|八|九|十]部分"]
    # 二级标题匹配
    ONE_INDENTATION_PATTERNS = [r'^[0-9]+\.[0-9]+(?!\.[0-9]+)', r'^[0-9]+\b']
    # 三级标题匹配
    TWO_INDENTATION_PATTERNS = [r"^[0-9]+\.[0-9]+\.[0-9]+(?!\.[0-9]+)"]

    @classmethod
    def acquireBookmarkLine(cls, line, lineIndex):
        """按照匹配模式分割书签行，lineIndex为书签行在文件中的行号"""
        # 1. 使用标题匹配分割得到三部分
        parts = re.split(r'\s+', line)
        debug_logger.debug(f"分割后的结果为{parts}")
        # 去除可能存在的空字符串
        parts = [part for part in parts if part != ""]
        bookmarkIndex = ""
        # intentationCount = 0
        # content = None
        page = -1
        # 这里需要进行重构，检测头，检测尾
        hasIndex = cls.__isMatchPagePattern(parts[0])
        debug_logger.debug(f"分割的最后一位是{parts[-1]}")
        hasPage = parts[-1].isdigit()
        if hasIndex and hasPage:
            # 中间进行合并
            merged_parts = "".join(parts[1:-1])
            parts = [parts[0], merged_parts, parts[-1]]
            bookmarkIndex = parts[0]
            intentationCount = cls.__getIntentationCount(bookmarkIndex)
            content = parts[1]
            page = int(parts[2])
        elif hasIndex and not hasPage:
            merged_parts = "".join(parts[1:])
            parts = [parts[0], merged_parts]
            bookmarkIndex = parts[0]
            intentationCount = cls.__getIntentationCount(bookmarkIndex)
            content = parts[1]
        elif not hasIndex and hasPage:
            merged_parts = "".join(parts[0:-1])
            parts = [merged_parts, parts[-1]]
            intentationCount = INDENTATIONCOUNTWITHOUTMATCH
            content = parts[0]
            page = parts[1]
        # 没有索引也没有页数
        else:
            merged_parts = "".join(parts[0:])
            intentationCount = INDENTATIONCOUNTWITHOUTMATCH
            content = merged_parts
        debug_logger.debug(
            f"完成书签行分割,最后各个参数为intentationCount={intentationCount},bookmarkIndex={bookmarkIndex},content={content},page={page}")
        return BookmarkLine(intentationCount, bookmarkIndex, content, page)

    # 按照匹配规则对书签进行替换
    @classmethod
    def replaceBookmarkByPattern(cls, pattern, bookmark):
        pass

    # todo: 待完善
    @classmethod
    def OCRforPageofBookmark(cls, bookmarkLines):
        """
        通过OCR识别书签的页面信息
        :param bookmarkLines:
        :return:
        """
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
    def __getIntentationCount(cls, bookmarkIndex):
        if cls.__isMatchNoneIndentationPattern(bookmarkIndex):
            return 0
        if cls.__isMatchOneIndentationPattern(bookmarkIndex):
            return 1
        if cls.__isMatchTwoIndentationPattern(bookmarkIndex):
            return 2
        raise IndexMatchException(f"标签行索引与现有匹配规则不匹配")

    @classmethod
    def __isMatchNoneIndentationPattern(cls, s):
        for pattern in cls.NONE_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                debug_logger.debug(f"s 为 {s},match none indentation,pattern {pattern}")
                return True
        return False

    @classmethod
    def __isMatchOneIndentationPattern(cls, s):
        for pattern in cls.ONE_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                debug_logger.debug(f"s 为 {s},match one indentation,pattern {pattern}")
                return True
        return False

    @classmethod
    def __isMatchTwoIndentationPattern(cls, s):
        # 这里在没有四级标题的情况下始终返回true，即如果没有匹配的话就进入这个
        debug_logger.debug(f"s 为 {s},match two indentation")
        # return True
        for pattern in cls.TWO_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                return True
        return False

    @classmethod
    def __isNotMatchPattern(cls, s):
        for pattern in cls.NONE_INDENTATION_PATTERNS + cls.ONE_INDENTATION_PATTERNS + cls.TWO_INDENTATION_PATTERNS:
            if re.match(pattern, s):
                return False
        return True

    @classmethod
    def __isMatchPagePattern(cls, s):
        for pattern in cls.NONE_INDENTATION_PATTERNS + cls.ONE_INDENTATION_PATTERNS + cls.TWO_INDENTATION_PATTERNS:
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
