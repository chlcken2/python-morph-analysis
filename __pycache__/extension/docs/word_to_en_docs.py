import docx
from regex_function import *
import re

# Todo: word_to_en과 연결된 파일입니다.
# 1. word 불러오기
doc = docx.Document('op20190261US_EN.docx')

# 2. object 형식인 word파일을 text형식으로 풀어주고 리스트 담기
full_list = []
for i in doc.paragraphs:
    full_list.append(i.text.strip())




# 4. 마지막 인덱스 구하기
def find_last_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        checked_regex = re.compile(regex)
        is_possible_checked_obj = checked_regex.search(whole_list[idx].strip())
        if bool(is_possible_checked_obj):
            last_idx = idx
            continue
    return last_idx


def find_first_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        checked_regex = re.compile(regex)  # IGNORE 사용 경우 문장에 있는 regex와 걸리는 경우 발생
        is_possible_checked_obj = checked_regex.search(whole_list[idx].strip())
        if bool(is_possible_checked_obj):
            last_idx = idx
            break
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
        if regex in keywords:
            last_idx = find_last_index(keywords, regex)
            modified_result = header_point_idx(keywords, last_idx)
            return modified_result
    return keywords  # header 날린 값 / last_idx


def del_footer(keywords, regexes):
    for regex in regexes:
        if regex in keywords:
            last_idx = find_first_index(keywords, regex)
            modified_result = footer_point_idx(keywords, last_idx)
            return modified_result
    return keywords


# footer 부분 지우고 합친 뒤 청구항 빼내기

def pick_particular_footer_list(whole_list, last_idx):
    extracted_footer_list = []
    for idx in range(len(whole_list)):
        if idx == last_idx:
            extracted_footer_list.append('')
        elif idx > last_idx:  # first_idx = 1              #footer의 기준이 되는 값 빈 문자열 만들기.
            extracted_footer_list.append(whole_list[idx].strip())
    return extracted_footer_list


def find_footer(keywords, regexes_list):
    for regex in regexes_list:
        if regex in keywords:
            last_idx = find_first_index(keywords, regex)
            footer_result = pick_particular_footer_list(keywords, last_idx)
            return footer_result
    return keywords


# 4-2. 지울 header, footer 담기
pure_main_footer = del_header(full_list, ['Technical Field', 'Photographic objective', 'TECHNICAL FIELD',
                                          'BACKGROUND OF THE INVENTION', 'Field of the Invention',
                                          'CROSS-REFERENCE TO RELATED APPLICATIONS', 'BACKGROUND',
                                          'CROSS-REFERENCE TO RELATED APPLICATIONS'])
mod_header_footer = del_footer(pure_main_footer,
                               ['300: user interface\nWHAT IS CLAIMED IS:', 'CLAIMED', 'CLAIMS', 'Claims', '[Claim 1]',
                                'WHAT IS CLAIMED IS:', 'PATENT CLAIMS'])
footer_tmp_list_en = find_footer(pure_main_footer,
                                 ['300: user interface\nWHAT IS CLAIMED IS:', 'CLAIMED', 'CLAIMS', 'Claims',
                                  '[Claim 1]', 'WHAT IS CLAIMED IS:', 'PATENT CLAIMS'])  # footer 부분 따로 빼냄


delete_small_sub = []
for sentence in mod_header_footer:
    delete_eng_small_sub = re.compile(r'(^[A-Z][a-z]+$)|(^[A-Z][a-z]+[\s][A-Z][a-z]+)')
    check_small_sub = re.sub(delete_eng_small_sub, '', sentence)
    delete_small_sub.append(check_small_sub)


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
para_regexes = [r'[[][\d]{4,4}[]]', r'([【][\d]{4,4}[】])']

split_sentence = split_para(delete_small_sub, para_regexes)


modified_pdf_eng = []  # 함수돌고나온거
for sentence in split_sentence:

    sentence = need_not_middle_bracket(sentence)

    # sentence = delete_etc_bracket(sentence)  # ( ) 안 제거

    sentence = delete_start_etc_bracket_(sentence.strip())  # 숫자) 시작 제거

    sentence = delete_num_dash_num(sentence)  # 1뒤에 위치

    # sentence = delete_eng_small_header(sentence)

    sentence = delete_page_footer(sentence)

    sentence = delete_eng_page_num(sentence)

    sentence = delete_eng_only_num(sentence.strip())

    sentence = delete_sub_eng(sentence.strip())

    # sentence = delete_sub(sentence)

    sentence = delete_sent_about_num(sentence)

    sentence = delete_multi_space(sentence)  # 맨 마지막에 위치

    modified_pdf_eng.append(sentence.strip())

# print(modified_pdf_eng)
modified_pdf_eng = [v for v in modified_pdf_eng if v]

# 기준이 없어 문단이 나눠지지 않는 경우 숫자. 기준으로 빈 문자열 추가하기
added_empty_sentence = []
for sentence in footer_tmp_list_en:
    sentence = delete_square_bracket(sentence) #[]삭제
    checked_word_no = re.compile(r'^\d.')  # 숫자.로 시작하는 문장
    is_possible_search_no = checked_word_no.search(sentence)

    if bool(is_possible_search_no):
        added_empty_sentence.append('')
        added_empty_sentence.append(sentence)
    else:
        added_empty_sentence.append(sentence)


# footer 부분 빈 문자열 두개 이상일 때 하나 삭제하기 로직
empty_str_idx_list = []

for i, v in enumerate(added_empty_sentence):
    if i == len(added_empty_sentence) - 1 and v == '':
        empty_str_idx_list.append('')

    elif v == '' and added_empty_sentence[i+1] != '':
        empty_str_idx_list.append('')

    elif v == '' and added_empty_sentence[i+1] == '':
        # del_point_para_footer[i+1] == False
        continue

    elif v == 'Abstract' or v == '【DRAWINGS】' or v == 'ABSTRACT' or v == '【DRAWING】':
        empty_str_idx_list.append('')

    else:
        empty_str_idx_list.append(v)
# print(empty_str_idx_list)

# print(empty_str_idx_list)
# footer 부분 대쉬 추가하기
result_footer_en = []
# TODO 청구항 부분 맨 앞에 빈 문자열일 경우 대쉬가 들어가므로 대쉬 삭제 or 추가
result_footer_en.append('-------------------------------------')
for sentence in empty_str_idx_list:
    sentence = sentence.replace('\t', '')
    find_word = re.compile('[a-zA-Z]+|[【][a-zA-Z\.\s\d]+[】]')
    search_word = find_word.search(sentence)
    if bool(search_word):
        result_footer_en.append(sentence)
    else:
        result_footer_en.append('-------------------------------------')
        result_footer_en.append(sentence)

result_footer_en = [v for v in result_footer_en if v]


# 대쉬 기준으로 footer 부분 문단 구하기 로직
# 1-1. dash들어가 있는 idx 구하기
def find_dash_idx(footer_sentence):
    idx_list = []
    for idx in range(len(footer_sentence)):
        check_dash = re.compile('-------------------------------------')
        search_dash = check_dash.search(footer_sentence[idx])
        if bool(search_dash):
            idx_list.append(idx)
            dash_last_idx = idx
            continue
    return idx_list, dash_last_idx


# 1-2 전체 dash에 대한 idx 와 dash_last값
dash_idx, dash_last_idx = find_dash_idx(result_footer_en)  # dash의 위치에 대한 idx가 담겨있는 리스트

# 1-3 para_footer_list에 앞, 중간, 끝 값 넣기
para_footer_list_en = []  # result_footer_en[:dash_idx[0]] 문단 단위로 담겨 있는 footer
for j in range(len(dash_idx) - 1):
    para_footer_list_en.append(result_footer_en[dash_idx[j]:dash_idx[j + 1]])  # 대쉬 사이 내용 더하기


para_footer_list_en.append(result_footer_en[dash_last_idx:])  # 대쉬 뒤 내용 더하기

# ...word_to_ko210727로 연결되어 결과 반환
