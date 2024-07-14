# -*- coding: utf-8 -*-

class LineSplitException(Exception):
    """
    书签行分割异常
    """
    def __init__(self, message="书签行分割异常"):
        super().__init__(message)
