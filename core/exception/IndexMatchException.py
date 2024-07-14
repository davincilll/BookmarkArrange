# -*- coding: utf-8 -*-

class IndexMatchException(Exception):
    """
    标题与现有匹配规则不匹配
    """

    def __init__(self, message="标签行索引与现有匹配规则不匹配"):
        super().__init__(message)
