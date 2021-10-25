import docx
from regex_function import *
import pandas as pd
from nltk.tokenize import sent_tokenize
import re

# Todo: 영어문장 내
# 1. word 불러오기
doc = docx.Document('20190829_description 12871,1000.docx')

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
            last_idx = find_last_index(keywords, regex)
            modified_result = header_point_idx(keywords, last_idx)
            return modified_result
    return full_list  # header 날린 값 / last_idx


def del_footer(keywords, regexes):
    for regex in regexes:
        if regex in pure_main_footer:
            # print('----',regex)
            last_idx = find_last_index(keywords, regex)
            modified_result = footer_point_idx(keywords, last_idx)
            return modified_result
    return pure_main_footer


# 4-2. 지울 header, footer 담기
pure_main_footer = del_header(full_list, ['BACKGROUND OF THE INVENTION','CROSS-REFERENCE TO RELATED APPLICATIONS','TECHNICAL FIELD', 'BACKGROUND'])
mod_header_footer = del_footer(pure_main_footer, [])


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

    # sentence = delete_eng_small_header(sentence)

    sentence = delete_page_footer(sentence)

    sentence = delete_eng_page_num(sentence)

    sentence = delete_eng_only_num(sentence)

    # sentence = address_no(sentence)

    # sentence = delete_sub(sentence)

    sentence = delete_sent_about_num(sentence)

    sentence = delete_multi_space(sentence)  # 맨 마지막에 위치

    modified_pdf_eng.append(sentence.strip())

modified_pdf_eng = [v for v in modified_pdf_eng if v]

# result_list_eng = []  # result_list_eng에 문단단위 + nltk + '-----------'들어가있음
# for sentence_eng in modified_pdf_eng:  # 만약 ko, eng를 문단 단위로 묶으려면 여기서 작업 시작
#     sentence_eng = sentence_eng.replace('Fig. ', '-Fig.')
#     result_list_eng.append('-------------------------------------')
#     eng_list = para_nltk_sentence(sentence_eng)
#
#     for eng in eng_list:
#         result_list_eng.append(eng)
#
# print(no_list)
# print(comment_eng)
#
# print(result_list_eng)
