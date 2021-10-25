import docx
import nltk
# import pdftotext
from regex_function import *
import pandas as pd
from word_to_en import *
from nltk.tokenize import sent_tokenize
import re
from itertools import zip_longest

# TODO : ko_word file 파싱 로직, word_to_en과 연결되어, 헤더푸터 삭제, 문단 나누기, 정규식, nltk, 문장단위 파싱 결과 값으로 엑셀을 만듬.

# 1. word파일 불러오기
doc = docx.Document("20210122_OP20210011US_국문명세서 (2).docx")

# 2. object 형식인 word파일을 text형식으로 풀어주고 리스트 담기
full_list = []
for i in doc.paragraphs:
    full_list.append(i.text.strip())


# print(full_list)

# 4. 마지막 인덱스 구하기
def find_last_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        check = re.compile(regex, re.IGNORECASE)
        check_word = check.search(whole_list[idx])
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
    tmp_footer = []
    for idx in range(len(whole_list)):
        if idx >= last_idx:  # first_idx = 1
            modified_result.append('')

        else:
            modified_result.append(whole_list[idx])
    return modified_result, tmp_footer


def del_header(keywords, regexes_list):
    for regex in regexes_list:
        if regex in keywords:
            print(regex + "---------------")
            last_idx = find_last_index(keywords, regex)
            modified_result = header_point_idx(keywords, last_idx)
            return modified_result
    return full_list  # header 날린 값 / last_idx


def del_footer(keywords, regexes_list):
    for regex in regexes_list:
        if regex in pure_main_footer:
            last_idx = find_last_index(keywords, regex)
            modified_result = footer_point_idx(keywords, last_idx)
            return modified_result
    return pure_main_footer


# footer 부분 지우고 합친 뒤 청구항 빼내기

def footer_tmp(whole_list, last_idx):
    tmp_footer = []
    for idx in range(len(whole_list)):
        if idx >= last_idx:  # first_idx = 1
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

pure_main_footer = del_header(full_list, ['【기술분야】'])  # 삭제 header 추가

mod_header_footer = del_footer(pure_main_footer, ['【청구항 1】'])  # 삭제 footer 추가
footer_tmp_list = find_footer(pure_main_footer, ['【청구항 1】'])  # footer 부분 따로 빼냄

print(mod_header_footer)
# TODO 만약 문단 오류가 날 경우 체크해 볼 곳
# 문단 나누기
def split_para(whole_list, para_regexes_list):
    for regex in para_regexes_list:
        find_regex = re.compile(regex)
        check_word = find_regex.search(" ".join(whole_list))

        if bool(check_word):
            return re.split(regex, " ".join(whole_list))
        else:
            return whole_list


# [1234], 【1234】로 나누기
para_regexes = [r'[[][\d]+[]]', r'([【][\d]{4,4}[】])']

split_sentence = split_para(mod_header_footer, para_regexes)

modified_pdf_ko = []  # 함수돌고나온거
for sentence in split_sentence:
    # print(sentence)

    # sentence = need_not_middle_bracket(sentence)  # 맨 앞 위치 소제목 제거

    sentence = delete_num_dash_num(sentence)  # 1-1제거

    # sentence = delete_etc_bracket(sentence)  # ()안에있는 무의미 단어 삭제

    # sentence = delete_etc_bracket(sentence)  # 숫자) 시작 제거

    sentence = delete_start_etc_bracket_(sentence.strip())

    # sentence = delete_semicolon(sentence)  # 세미콜론 삭제

    sentence = delete_page_footer(sentence)

    sentence = delete_eng_only_num(sentence)  #

    # sentence = delete_sub(sentence)

    sentence = address_no(sentence)

    sentence = delete_sent_about_num_(sentence)

    sentence = delete_multi_space(sentence)  # 맨 마지막에 위치

    modified_pdf_ko.append(sentence.strip())

modified_pdf_ko = [v for v in modified_pdf_ko if v]

print(modified_pdf_ko)

ko_result = []  # '------' + 문장 + '-' 으로 이루어짐
eng_result = []  # '------' + 문장 + '-'
for sentence_ko, sentence_eng in zip_longest(modified_pdf_ko, modified_pdf_eng, fillvalue='-'):
    ko_result.append('-------------------------------------')
    eng_result.append('-------------------------------------')

    sentence_eng = sentence_eng.replace('Fig. ', 'Fig.')
    sentence_eng = sentence_eng.replace('FIG. ', 'FIG.')
    sentence_eng = sentence_eng.replace('FIGS. ', 'FIGS.')
    sentence_eng = sentence_eng.replace('NO. ', 'NO.')
    sentence_eng = sentence_eng.replace('No. ', 'No.')

    kor_list = para_nltk_sentence(str(sentence_ko))  # kor_list = list
    eng_list = para_nltk_sentence(str(sentence_eng))

    for zip_ko_sentence, zip_eng_sentence in zip_longest(kor_list, eng_list, fillvalue='-'):
        ko_result.append(zip_ko_sentence)
        eng_result.append(zip_eng_sentence)
# print(ko_result)
comment_ko = []
for sentence in ko_result:
    bracket_ko = find_bracket(str(sentence))
    comment_ko.append(" ".join(bracket_ko))

no_list = []
comment_eng = []
for i, sentence in enumerate(eng_result):
    no_list.append(i + 1)
    bracket_ko = find_bracket(str(sentence))
    comment_eng.append(" ".join(bracket_ko))

# # # 8. 엑셀 만들기
# zipped = zip_longest(no_list, ko_result, comment_ko, eng_result, comment_eng, fillvalue='-')
#
# a = []
# b = []
# c = []
# d = []
# e = []
# for aa, bb, cc, dd, ee in list(zipped):
#     a.append(aa)
#     b.append(bb)
#     c.append(cc)
#     d.append(dd)
#     e.append(ee)
#
# # print(b)
# # # 8. 엑셀 만들기
# df = pd.DataFrame({'NO': a, '국문': b, '국문병기': c, '영문': d, '영문병기': e})
# df_i = df.set_index('NO', inplace=True)
#
# df.to_excel('test20210122_OP20210011US_국문명세서 (2).docx.xlsx')



#
#
# sentence_footer_tmp = re.split('[【][가-힣\s\d]+[】]', " ".join(footer_tmp_list))
# # print(sentence_footer_tmp)
# sentence_footer_tmp = [v for v in sentence_footer_tmp if v]
# # print(sentence_footer_tmp)
# result_footer = []
# for sentence in sentence_footer_tmp:
#     result_footer.append('---------------')
#     check_word = re.compile(r'[가-힣]+')
#     change_one_space = check_word.search(sentence)
#     # print(change_one_space)
#     if bool(change_one_space):
#         result_footer.append(sentence)
# # print(result_footer)
#
# modified_pdf_ko_list = modified_pdf_ko + result_footer
