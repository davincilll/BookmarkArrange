# 这是一个示例 Python 脚本。
import re

from loguru import logger


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# todo:后面用配置加载和命令模式以及工作流进行重构
def indent_text(text):
    lines = text.split('\n')
    indented_lines = []
    # 1.1.1的表达式
    parttern1 = r"^[0-9]+\.[0-9]+\.[0-9]+"
    # 1.1的表达式我目前还不会实现
    # 带有章节的表达式
    parttern2 = r"^第[0-9]+章"
    for line in lines:
        # 去除空行
        if re.match(r"^\n", line) or line == '' or line == ' ':

            continue
        # 字符串格式化
        line = line.strip()
        # 识别出三部分
        parts = re.split(r'[\s\t]+', line)
        # 这里打一个补丁吧
        if len(parts) == 2:
            indented_line = '\t' + parts[0] + ' ' + parts[1]
            indented_lines.append(indented_line)
            continue
        print(parts)
        number = parts[0]
        content = parts[1]
        page = parts[2]
        number = number.strip()
        content = content.strip()
        page = page.strip()
        # 拼接
        pre_result = str(number) +' '+ str(content) +"\t"+ str(page)
        #print(pre_result)
        # 判断行是否是章节标题
        if re.match(parttern2, number):
            indented_line = pre_result
            indented_lines.append(indented_line)
        # 匹配模式1.1.1
        elif re.match(parttern1, number):
            indented_line = '\t\t' + pre_result
            indented_lines.append(indented_line)
        # 匹配模式1.1
        else:
            indented_line = '\t' + pre_result
            indented_lines.append(indented_line)
        print(indented_line)
    # 对每一个indented_line回车后拼接
    indent_text = '\n'.join(indented_lines)
    return indent_text


# 添加书页用的
def addPageNum(text):
    lines = text.split('\n')
    index = 0
    while index < len(lines):
        line = lines[index]
        parttern = r"\b[0-9]+\b$"
        # 输入页码数
        m = re.search(parttern, line)
        if m:
            print("原始的line：" + line)
            line = re.sub(parttern, '', line)
        input_text = input('请输入' + line + '的页码（直接回车重新输入，输入"<"重新设置上一个循环体的页数）: ')
        if input_text == '':
            # 回车，重新输入
            continue
        if input_text == '<':
            index -= 1
            continue
        try:
            page = int(input_text)
            indented_line = line + str(page)
            lines[index] = indented_line
            index += 1  # 保存当前页数作为上一个循环体的页数
            continue
        except ValueError:
            print('输入无效，请重新输入有效的页码数。')
    indent_text = '\n'.join(lines)
    return indent_text


# 设置书的偏移用的
def setPageOffset(text, offset):
    lines = text.split('\n')
    index = 0
    while index < len(lines):
        line = lines[index]
        parttern = r"\b[0-9]+\b$"
        # 输入页码数
        m = re.search(parttern, line)
        if not m:
            logger.info("有问题的line:" + line)
        original = int(m.group())
        realPage = original + offset
        if m:
            line = re.sub(parttern, str(realPage), line)
            lines[index] = line
            index += 1
    indent_text = '\n'.join(lines)
    return indent_text


def main1():
    # 读入文本文件
    with open("input.txt", "r", encoding="utf-8") as file:
        text = file.read()

    indented_text = indent_text(text)

    #   输出文本文件
    with open("temp.txt", "w", encoding="utf-8") as file:
        file.write(indented_text)


def main2():
    with open("temp.txt", "r", encoding="utf-8") as file:
        text = file.read()
    indented_text = addPageNum(text)
    #   输出文本文件
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(indented_text)


def main3():
    with open("output.txt", "r", encoding="utf-8") as file:
        text = file.read()
    indented_text = setPageOffset(text, -386)
    #   输出文本文件
    with open("output1.txt", "w", encoding="utf-8") as file:
        file.write(indented_text)


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
if __name__ == '__main__':
    main1()
