from bing_translation_for_python import Translator, public, setting
from bing_translation_for_python.core import Semantic, get_token
from pyperclip import paste, copy

import argparse
import os


def parser(args) -> argparse.Namespace:
    a_p = argparse.ArgumentParser(
        prog='bin',
        usage='%(prog)s lang_tag [text] [optionals]',
    )
    # 位置参数 #
    # 语言类型
    a_p.add_argument('lang_tag', help='Target lang_tag')
    # 文本，接受多个参数
    a_p.add_argument('text', nargs='*', default=None, help='text')

    # 可选参数 #
    # 复制输出内容
    a_p.add_argument('-c', '--copy', action='store_true',
                     help='Write text to the clipboard')
    # 以当前指定语言模式列出所有语言标签
    a_p.add_argument('-l', '--list_all_ltgt', action='store_true',
                     help='List all supported languages')
    # de bug 模式
    a_p.add_argument('-d', '--debug', action='store_true',
                     help='DeBug Mode')

    return a_p.parse_args(args)


def translator(name_spece):
    lang_tag = name_spece.lang_tag.strip()
    # 分别从name_spece 和 paste中获取文本，name_space 优先
    reper_text = ' '.join(name_spece.text) or paste()

    try:
        text_obj = Translator(lang_tag).translator(reper_text)

        # copy选项仅复制翻译后的文本
        if name_spece.copy:
            copy(text_obj.text())

        # 如果文本是一个单词就能够获取到它的详细释义
        semantic = Semantic(text_obj, get_token())
        # 单词释义无效,返回文本
        if semantic:
            return F"{str(text_obj)}\n{'-='*20}\n{semantic.text()}"
        return text_obj.text()

    except public.errors.EmptyTextError:
        return "待翻译文本为空!"


def list_language_tag():
    lang_tag = setting.Config().tgt_lang

    formant_tags = [[tag, lang_tag[tag]['text']] for tag in lang_tag.keys()]
    return '\n'.join([item[1]+' ==> '+item[0] for item in formant_tags])


def default_help(argv):
    # 没有有效参数时,默认显示帮助信息
    if argv:
        return argv
    return ['-h']


def entrance(args: list = None):
    """翻译入口"""
    if not args:
        args = os.sys.argv[1:]
    name_spece = parser(default_help(args))

    # 列出所有语言标签
    if name_spece.list_all_ltgt:
        return list_language_tag()
    # 翻译给出的文本
    try:
        return translator(name_spece)
    except public.errors.TargetLanguageNotSupported:
        print(F"不支持的语言:'{name_spece.lang_tag}'")
        print("你可以使用‘-l’选项查看语言支持列表")
    finally:
        # debug mode
        if name_spece.debug:
            print(F'DeBugMode:\n\t{name_spece}\n\tArgs:{args}')
            print(F'\tRunningPath:{os.getcwd()}')
