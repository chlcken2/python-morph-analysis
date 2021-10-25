import docx
from regex_function import *
import pandas as pd
from nltk.tokenize import sent_tokenize
import re

# Todo: word_to_en과 연결된 파일입니다.
# 1. word 불러오기
doc = docx.Document('20210122_op20210011us-영어번역문 (2).docx')

# 2. object 형식인 word파일을 text형식으로 풀어주고 리스트 담기
full_list = []
for i in doc.paragraphs:
    full_list.append(i.text.strip())
# print(full_list)

# 4. 마지막 인덱스 구하기
def find_last_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        check = re.compile(regex)
        check_word = check.search(whole_list[idx].strip())
        if bool(check_word):
            last_idx = idx
            continue
    return last_idx


# 4-1. 메인 로직
def header_point_idx(whole_list, last_idx):
    modified_result = []
    for idx in range(len(whole_list)):
        if idx <= last_idx:  # first_idx = 1
            modified_result.append('')
        else:
            modified_result.append(whole_list[idx])
    return modified_result


def footer_point_idx(whole_list, last_idx):
    modified_result = []
    for idx in range(len(whole_list)):
        if idx >= last_idx:  # first_idx = 1
            modified_result.append('')
        else:
            modified_result.append(whole_list[idx])
    return modified_result


def del_header(keywords, regexes):
    for regex in regexes:
        if regex in full_list:
            # print(regex + "---------------")
            last_idx = find_last_index(keywords, regex)
            modified_result = header_point_idx(keywords, last_idx)
            return modified_result
    return full_list  # header 날린 값 / last_idx


def del_footer(keywords, regexes):
    for regex in regexes:
        # print('-------',regex)
        if regex in pure_main_footer:
            # print('----',regex)
            last_idx = find_last_index(keywords, regex)
            modified_result = footer_point_idx(keywords, last_idx)
            return modified_result
    return pure_main_footer

# footer 부분 지우고 합친 뒤 청구항 빼내기

def footer_tmp(whole_list, last_idx):
    tmp_footer = []
    for idx in range(len(whole_list)):
        if idx > last_idx:  # first_idx = 1
            tmp_footer.append(whole_list[idx])
    return tmp_footer


def find_footer(keywords, regexes_list):
    for regex in regexes_list:
        if regex in pure_main_footer:
            last_idx = find_last_index(keywords, regex)
            footer_result = footer_tmp(keywords, last_idx)
            return footer_result
    return pure_main_footer


# 4-2. 지울 header, footer 담기
pure_main_footer = del_header(full_list, ['BACKGROUND'])
mod_header_footer = del_footer(pure_main_footer, ['WHAT IS CLAIMED IS:'])
footer_tmp_list_en = find_footer(pure_main_footer, ['WHAT IS CLAIMED IS:'])  # footer 부분 따로 빼냄
# print(footer_tmp_list)
# print(mod_header_footer)
# TODO 만약 문단 오류가 날 경우 체크해 볼 곳
# 문단 나누기
#
# print(footer_tmp_list)
def split_para(whole_list, para_regexes_list):
    for regex in para_regexes_list:
        find_regex = re.compile(regex)
        check_word = find_regex.search(" ".join(whole_list))
        if bool(check_word):
            return re.split(regex, " ".join(whole_list))
        else:
            return whole_list

# print(split_sentence)
# [1234], 【1234】로 나누기
para_regexes = [r'[[][\d]{4,4}[]]', r'([【][\d]{4,4}[】])']

split_sentence = split_para(mod_header_footer, para_regexes)
# print(split_sentence)
modified_pdf_eng = []  # 함수돌고나온거
for sentence in split_sentence:

    sentence = delete_sub_eng(sentence)

    sentence = need_not_middle_bracket(sentence)
    # sentence = delete_etc_bracket(sentence)  # ( ) 안 제거

    sentence = delete_start_etc_bracket_(sentence.strip())  # 숫자) 시작 제거

    sentence = delete_num_dash_num(sentence)  # 1뒤에 위치

    # sentence = delete_semicolon(sentence)

    sentence = delete_eng_small_header(sentence)

    sentence = delete_page_footer(sentence)

    sentence = delete_eng_page_num(sentence)

    sentence = delete_eng_only_num(sentence)

    sentence = address_no(sentence)

    # sentence = delete_sub(sentence)

    sentence = delete_sent_about_num_(sentence)

    sentence = delete_multi_space(sentence)  # 맨 마지막에 위치

    modified_pdf_eng.append(sentence.strip())

# print(modified_pdf_eng)
modified_pdf_eng = [v for v in modified_pdf_eng if v]
# print(footer_tmp_list_en)
result_footer_en = []
for sentence in footer_tmp_list_en:
    sentence = sentence.replace('\t', '')
    find_word = re.compile('[a-zA-Z]+')
    search_word = find_word.search(sentence)
    if bool(search_word):
        result_footer_en.append(sentence)

    else:
        result_footer_en.append('-------------------------------------')
        result_footer_en.append(sentence)

result_footer_en = [v for v in result_footer_en if v]



# result_list_eng = []  # result_list_eng에 문단단위 + nltk + '-----------'들어가있음
# for sentence_eng in modified_pdf_eng:  # 만약 ko, eng를 문단 단위로 묶으려면 여기서 작업 시작
#     sentence_eng = sentence_eng.replace('Fig. ', '-Fig.')
#     result_list_eng.append('-------------------------------------')
#     eng_list = para_nltk_sentence(sentence_eng)
#
#     for eng in eng_list:
#         result_list_eng.append(eng)

# print(no_list)
# print(comment_eng)

# print(result_list_eng)
