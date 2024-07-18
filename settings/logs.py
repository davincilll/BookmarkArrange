# 配置默认的logger
from nb_log import get_logger

# 这个是交互式部分的日志配置
# 打印一般的书页行信息是用info等级，其他的采用warning等级，这里注意一下
nb_logger = get_logger("interactive", formatter_template=12)
# 配置一下日志格式，这里将前缀全部都不要
# 这个是用来debug的日志，上面一个用来debug日志信息会很少
debug_logger = get_logger("debug")
