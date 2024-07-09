from word_to_en210727 import *
import re
from itertools import zip_longest

# TODO : ko_word file 파싱 로직, word_to_en과 연결되어, 헤더푸터 삭제, 문단 나누기, 정규식, nltk, 문장단위 파싱 결과 값으로 엑셀을 만듬.

# 1. word파일 불러오기
doc = docx.Document("OP20190261US_Korean Spec.docx")

# 2. object 형식인 word파일을 text형식으로 풀어주고 리스트 담기
full_list = []
for i in doc.paragraphs:
    full_list.append(i.text.strip())

# print(full_list)
# 4. 마지막 인덱스 구하기
def find_last_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        checked_regex = re.compile(regex)
        is_possible_checked_obj = checked_regex.search(whole_list[idx].strip())
        if bool(is_possible_checked_obj):
            last_idx = idx
    return last_idx


def find_first_index(whole_list, regex):
    last_idx = -1
    for idx in range(len(whole_list)):
        checked_regex = re.compile(regex)
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
            modified_result.append(whole_list[idx].strip())
    return modified_result


def footer_point_idx(whole_list, last_idx):
    modified_result = []
    for idx in range(len(whole_list)):
        if idx > last_idx:  # first_idx = 1
            modified_result.append('')
        else:
            modified_result.append(whole_list[idx])
    return modified_result


def del_header(keywords, regexes_list):
    for regex in regexes_list:
        if regex in keywords:
            last_idx = find_last_index(keywords, regex)
            modified_result = header_point_idx(keywords, last_idx)
            return modified_result
    return keywords  # header 날린 값 / last_idx


def del_footer(keywords, regexes_list):
    for regex in regexes_list:
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
        elif idx > last_idx:  # first_idx = 1
            extracted_footer_list.append(whole_list[idx])
    return extracted_footer_list


def find_footer(keywords, regexes_list):
    for regex in regexes_list:
        if regex in keywords:
            last_idx = find_first_index(keywords, regex)
            footer_result = pick_particular_footer_list(keywords, last_idx)
            return footer_result
    return keywords


# 4-2. 지울 header, footer 담기
pure_main_footer = del_header(full_list,
                              ['발명의 명칭', '발명영역', 'TECHNICAL FIELD', '【기술분야】', '비밀유지 계약서', '발명영역'])  # 삭제 header 추가
mod_header_footer = del_footer(pure_main_footer,
                               ['청구범위', '염기서열', 'WE CLAIM', '클레임(Claims)', '【청구의 범위】', '【청구범위】', '【청구항 1】',
                                '【특허청구범위】'])  # 삭제 footer 추가
footer_tmp_list = find_footer(pure_main_footer,
                              ['청구범위', '염기서열', 'WE CLAIM', '클레임(Claims)', '【청구의 범위】', '【청구범위】', '【청구항 1】',
                               '【특허청구범위】'])  # footer 부분 따로 빼냄




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

    sentence = delete_small_bracket(sentence)

    sentence = need_not_middle_bracket(sentence)  # 맨 앞 위치 소제목 제거

    sentence = delete_num_dash_num(sentence)  # 1-1제거

    # sentence = delete_etc_bracket(sentence)  # ()안에있는 무의미 단어 삭제

    sentence = delete_semicolon(sentence)

    sentence = delete_start_etc_bracket_(sentence.strip())

    sentence = delete_page_footer(sentence)

    sentence = delete_eng_only_num(sentence)  #

    sentence = delete_sub(sentence)

    sentence = address_no(sentence)

    sentence = delete_sent_about_num(sentence)

    sentence = delete_multi_space(sentence)  # 맨 마지막에 위치

    modified_pdf_ko.append(sentence.strip())

modified_pdf_ko = [v for v in modified_pdf_ko if v]

# footer 부분 【】 , 숫자.시작 빈문자열 만들기
del_point_para_footer = []
for sentence in footer_tmp_list:
    checked_word_middle_bracket = re.compile(r'[【][가-힣\s\d]+[】]')
    checked_word_no = re.compile(r'^\d.$') #숫자. 으로만 문단 먹는 경우
    is_possible_search_bracket = checked_word_middle_bracket.search(sentence)
    is_possible_search_no = checked_word_no.search(sentence)

    if bool(is_possible_search_bracket):
        sub_word = re.sub(checked_word_middle_bracket, '', sentence)
        del_point_para_footer.append(sub_word)

    elif bool(is_possible_search_no):
        sub_word = re.sub(checked_word_no, '', sentence)
        del_point_para_footer.append(sub_word)
    else:
        del_point_para_footer.append(sentence)


# footer 부분 빈 문자열 두개 이상일 때 하나 삭제하기 로직
empty_str_idx_list = []

for i, v in enumerate(del_point_para_footer):
    if i == len(del_point_para_footer) - 1 and v == '':
        continue

    elif v == '' and del_point_para_footer[i+1] != '':
        empty_str_idx_list.append('')
    elif v == '' and del_point_para_footer[i+1] == '':
        # del_point_para_footer[i+1] == False
        continue
    else:
        empty_str_idx_list.append(v)
# print(empty_str_idx_list)
# footer 부분 대쉬 추가하기
result_footer = ['-------------------------------------']
# TODO 청구항 부분 맨 앞에 빈 문자열일 경우 대쉬가 들어가므로 대쉬 삭제 or 추가
for sentence in empty_str_idx_list:
    checked_word = re.compile('[【][가-힣\s\d]+[】]')
    is_possible_search_word = checked_word.search(sentence)
    if bool(is_possible_search_word):
        sub_word = re.sub(checked_word, '-------------------------------------', sentence)  # TODO 대쉬 두개들어갈 때 체크할 곳
        result_footer.append(sub_word)
    elif bool(sentence):
        result_footer.append(sentence)
    else:
        result_footer.append('-------------------------------------')
        result_footer.append(sentence)
result_footer = [v for v in result_footer if v]


# 대쉬 기준으로 footer 부분 문단 구하기 로직
# 1-1. dash들어가 있는 idx 구하기
def find_dash_idx(footer_sentence):
    idx_list = []
    for idx in range(len(footer_sentence)):
        checked_dash = re.compile('-------------------------------------')
        is_possible_searching_dash = checked_dash.search(footer_sentence[idx])
        if bool(is_possible_searching_dash):
            idx_list.append(idx)
            dash_last_idx = idx
            continue
    return idx_list, dash_last_idx


# 1-2 전체 dash에 대한 idx 와 dash_last값
dash_idx, dash_last_idx = find_dash_idx(result_footer)  # dash의 idx가 담겨있는 리스트

# 1-3 para_footer_list에 앞, 중간, 끝 값 넣기
para_footer_list = []  # result_footer_en[:dash_idx[0]]    문단 단위로 담겨 있는 footer
for j in range(len(dash_idx) - 1):
    para_footer_list.append(result_footer[dash_idx[j]:dash_idx[j + 1]])  # 대쉬 사이 내용 더하기

para_footer_list.append(result_footer[dash_last_idx:])  # 대쉬 뒤 내용 더하기

# 1-4 para_footer 와 para_footer_list_en zip_longest 사용하여 문단 맞추기(이중 리스트 형태)
para_ko = []
para_en = []

for zip_ko, zip_en in zip_longest(para_footer_list, para_footer_list_en, fillvalue='-'):
    for ko, en in zip_longest(zip_ko, zip_en, fillvalue='-'):
        para_ko.append(ko)
        para_en.append(en)




# footer를 제외한 윗 부분 zip만들기 로직(문장내 문장 나누기, 국문, 영문 문단 매치)
ko_result = []  # '------' + 문장 + '-' 으로 이루어짐
eng_result = []  # '------' + 문장 + '-'
for sentence_ko, sentence_eng in zip_longest(modified_pdf_ko, modified_pdf_eng, fillvalue='-'):
    ko_result.append('-------------------------------------')
    eng_result.append('-------------------------------------')
    split_sentence_in_sentence = []

    sentence_eng = sentence_eng.replace('Fig. ', 'Fig.')
    sentence_ko = sentence_ko.replace('-', ' ')
    sentence_eng = sentence_eng.replace('FIG. ', 'FIG.')
    sentence_eng = sentence_eng.replace('FIGS. ', 'FIGS.')
    sentence_eng = sentence_eng.replace('NO. ', 'NO.')
    sentence_eng = sentence_eng.replace('No. ', 'No.')

    kor_list = para_nltk_sentence(str(sentence_ko))  # kor_list = list
    eng_list = para_nltk_sentence(str(sentence_eng))

    for sentence in eng_list:
        sent = split_upper_eng_dot_space(sentence)  # 영문문장 내 문장 분리 M.과 같은
        split_sentence_in_sentence.extend(sent)
    print(kor_list)
    for zip_ko_sentence, zip_eng_sentence in zip_longest(kor_list, split_sentence_in_sentence, fillvalue='-'):
        ko_result.append(zip_ko_sentence)
        eng_result.append(zip_eng_sentence)

# footer 윗 부분 빈문자열 제거
ko_result = [v for v in ko_result if v]
eng_result = [v for v in eng_result if v]


# header + footer 더하기
ko_footer_result = ko_result + para_ko
en_footer_result = eng_result + para_en

# comment 부분
comment_ko = []
for sentence in ko_footer_result:
    bracket_ko = find_bracket(str(sentence))
    comment_ko.append(" ".join(bracket_ko))

no_list = []
comment_eng = []
for i, sentence in enumerate(en_footer_result):
    no_list.append(i + 1)
    bracket_ko = find_bracket(str(sentence))
    comment_eng.append(" ".join(bracket_ko))

# # 8. 엑셀 만들기
zipped = zip_longest(no_list, ko_footer_result, comment_ko, en_footer_result, comment_eng, fillvalue='-')

a = []
b = []
c = []
d = []
e = []
for aa, bb, cc, dd, ee in list(zipped):
    a.append(aa)
    b.append(bb)
    c.append(cc)
    d.append(dd)
    e.append(ee)


# # 8. 엑셀 만들기
df = pd.DataFrame({'NO': a, '국문': b, '국문병기': c, '영문': d, '영문병기': e})
df_i = df.set_index('NO', inplace=True)

# result
df.to_excel('PR2.2_OP20190261US_Korean Spec.docx.xlsx')
