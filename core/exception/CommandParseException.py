# -*- coding: utf-8 -*-

class CommandParseException(Exception):
    """
        输入的命令解析错误
    """

    def __init__(self, message="输入的命令解析错误"):
        super().__init__(message)
