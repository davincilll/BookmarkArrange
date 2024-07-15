import logging
from abc import ABC, abstractmethod
from math import inf

from loguru import logger

from core.BookmarkLine import BookmarkLine
from core.exception.CommandParseException import CommandParseException


class AbstractReceiver(ABC):
    def handleCommand(self, options: dict, *args, **kwargs):
        pass


class BookmarLinePageInputReceiver(AbstractReceiver):

    def handleCommand(self, options: dict, **kwargs):
        bookmarkLinesWithIndex = kwargs.pop("bookmarkLinesWithIndex")
        bookmarkLines = bookmarkLinesWithIndex["bookmarkLines"]
        _index = bookmarkLinesWithIndex["index"]
        inputPage = options.pop("inputPage")
        bookmarkLines[_index].page = inputPage
        bookmarkLine = bookmarkLines[_index]
        logging.info(
            f"【default】【old】这是书签行信息：行数为{_index + 1}，{bookmarkLine.index + bookmarkLine.content + bookmarkLine.page}")


class BookmarkLineSkipReceiver(AbstractReceiver):
    # 注意这里是引用拷贝
    def handleCommand(self, options: dict, **kwargs):
        bookmarkLinesWithIndex = kwargs.pop("bookmarkLinesWithIndex")

        bookmarkLinesWithIndex["index"] += 1
        logger.info("【skip】pass")


class BookmarkLineJumpReceiver(AbstractReceiver):
    def handleCommand(self, options: dict, **kwargs):
        bookmarkLinesWithIndex = kwargs.pop("bookmarkLinesWithIndex")
        jumpRow = options.pop("jumpRow")
        bookmarkLinesWithIndex["index"] = jumpRow - 1
        logger.info(f"【jump】jump to {jumpRow} row")


class BookmarkShowReceiver(AbstractReceiver):
    _options = {
        "-n": inf,
        "-d": False
    }

    def handleCommand(self, options, **kwargs):
        bookmarkLinesWithIndex = kwargs.pop("bookmarkLinesWithIndex")
        # 合并选项
        commandOptions = self._options.copy()
        commandOptions.update(options)
        _index = bookmarkLinesWithIndex["index"]
        count = commandOptions["-n"]
        if commandOptions["-d"]:
            # 这个是当前所在的行，也是即将修改的行
            while _index < len(bookmarkLinesWithIndex["bookmarkLines"]) and count > 0:
                bookmarkLine = bookmarkLinesWithIndex["bookmarkLines"][_index]
                logging.info(
                    f"【show】这是书签行信息：行数为{_index + 1}，{bookmarkLine.index + bookmarkLine.content + bookmarkLine.page}")
                _index += 1
                count -= 1
        else:
            while _index > -1 and count > 0:
                bookmarkLine = bookmarkLinesWithIndex["bookmarkLines"][_index]
                logging.info(
                    f"【show】这是书签行信息：行数为{_index + 1}，{bookmarkLine.index + bookmarkLine.content + bookmarkLine.page}")
                _index -= 1
                count -= 1
        logging.info("【show】show done")


class CommonCommand:
    """
    采用命令模式来实现交互式补充书页信息
    """
    commandReceiver: AbstractReceiver
    commandOptions: dict

    def __init__(self, commandReceiver: AbstractReceiver, commandOptions: dict = None):
        if commandOptions is None:
            commandOptions = {}
        self.commandReceiver = commandReceiver
        self.commandOptions = commandOptions

    def execute(self, *args, **kwargs):
        self.commandReceiver.handleCommand(options=self.commandOptions, *args, **kwargs)


class CommandParser:
    # 交互式补充书页信息
    # 跳转指定行数书签行的命令输入
    JUMP_INDEX_COMMAND = "jp"
    # 展示书签行信息的命令输入
    SHOW_COMMAND = "ls"
    # 保持不变的命令输入
    KEEP_COMMAND = ""

    @classmethod
    def parse2Command(cls, inputRawCommand: str) -> CommonCommand:
        result = inputRawCommand.split()
        options = {}
        if inputRawCommand.startswith(cls.JUMP_INDEX_COMMAND) and len(result) == 2 and result[1].isdigit():
            # 放入 inputPage参数
            options["inputPage"] = int(result[1])
            return CommonCommand(BookmarkLineJumpReceiver(), options)
        elif inputRawCommand.startswith(cls.SHOW_COMMAND):
            result.remove(cls.SHOW_COMMAND)
            # 放入-n,-d参数
            if "-n" in result:
                # fixme 这里存在一个参数解析的bug，如果输入的是-n -d，那么就会导致-d被解析为-n的参数，这种情况应该有异常被抛出的
                options["-n"] = int(result[result.index("-n") + 1])
                result.remove(result[result.index("-n") + 1])
                result.remove("-n")
                pass
            if "-d" in result:
                options["-d"] = True
                result.remove("-d")
            if len(result) == 0:
                return CommonCommand(BookmarkShowReceiver(), options)
            else:
                raise CommandParseException(f"show命令解析错误，inputRawCommand:{inputRawCommand}")
        elif inputRawCommand == cls.KEEP_COMMAND:
            return CommonCommand(BookmarkLineSkipReceiver(), options)
        elif inputRawCommand.isdigit():
            # 放入page参数
            options["inputPage"] = int(inputRawCommand)
            return CommonCommand(BookmarLinePageInputReceiver(), options)
        else:
            raise CommandParseException(f"命令解析错误，inputRawCommand:{inputRawCommand}")
