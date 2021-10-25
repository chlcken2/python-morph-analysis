import re
from nltk.tokenize import sent_tokenize


# [소제목] 이와 같은 형식으로 문장내 삽입 되어 있는경우가 있어서 문단 삭제 발생 -> [화학식1]이 삭제되는 경우도 있어서 제외 함
# 【국어단어】, [영어단어], [국어단어, 숫자포함x], [영어단어+공백]
def delete_sub(sentence):  #
    find_word = re.compile(
        r'([【]+[\s가-힣\d]+[】])|(^[A-Za-z]+$)|(^[[][가-힣]+[]])|(^[a-zA-Z\s]+$)')  # (^[[][a-zA-Z가-힣\d\s]+[]]+$)
    delete_word = re.sub(find_word, '', sentence.strip())
    return delete_word


# ^[A-Z][a-z]+$|^[A-Z][a-z]+[\s][A-Z][a-z]+

def address_no(sentence):
    find_word = re.compile(r'^[A-Z]+[\s][\d]+[-][\d]+[.]+$')
    delete_word = re.sub(find_word, '', sentence.strip())
    return delete_word


# def delete_big_bracket_sub_eng(sentence):
#     find_word = re.compile(r'^[[][a-zA-Z\s]+[]]+$')
#     delete_word = re.sub(find_word, '', sentence.strip())
#     return delete_word
def delete_num_dash_num(sentence):
    find_word = re.compile(r'^[\d]+[\-\d]+[\.]|^[\d][.]')
    delete_word = re.sub(find_word, '', sentence.strip())
    return delete_word


def delete_semicolon(sentence):
    find_word = re.compile(r'^;$')
    delete_word = re.sub(find_word, '', sentence)
    return delete_word


def delete_eng_page_num(sentence):
    find_word = re.compile(r'(\d+$)|(^[\d]+[\/][\d]+)')
    delete_word = re.sub(find_word, '', sentence)
    return delete_word


# 문단앞에 숫자로 시작하는 경우
def delete_eng_only_num(sentence):
    find_word = re.compile(r'(^\d+$)|(^\d[.])')  # (^\d+$)|(^\d[.])|(^\d)|(^[\d]+[\-\d]+[\.])
    delete_word = re.sub(find_word, '', sentence)
    return delete_word


def delete_eng_small_header(sentence):
    find_word = re.compile(r'(^[\d])[.][\s][a-zA-Z\s]+|^[\d]+[\s][a-zA-Z\s]+')
    delete_word = re.sub(find_word, '', sentence)
    return delete_word


def delete_page_footer(sentence):
    find_word = re.compile('MAPS Intellectual Property Law Firm|Strictly Confidential|MAPS Docket No DP20190715KR')
    delete_word = re.sub(find_word, '', sentence)
    return delete_word


# (숫자)삭제 / 숫자)는 삭제x
# def delete_etc_bracket(sentence):  # [(][\d\~a-zA-Z]{0,3}[)]|[(][SWC~\d]+[)]
#     check_word = re.compile(r'([(][\d\~a-zA-Z]{0,3}[)])|([(][A-Z~\d]+[)])')
#     delete_word = re.sub(check_word, '', sentence)
#     return delete_word

# 숫자) 시작
def delete_start_etc_bracket_(sentence):  # [(][\d\~a-zA-Z]{0,3}[)]|[(][SWC~\d]+[)]
    check_word = re.compile(r'(^[\d][\)])')
    delete_word = re.sub(check_word, '', sentence)
    return delete_word


def find_bracket(sentence):
    check_word = re.compile(r'[(][a-zA-Z\s\-\,\.\:]{2,}[)]')  # [(][a-zA-Z\s\-]+[)]
    append_word = check_word.findall(sentence)
    if not bool(append_word):
        return '-'
    else:
        return append_word


def delete_multi_space(sentence):
    check_word = re.compile(r'[\s]{2,}')
    change_one_space = re.sub(check_word, ' ', sentence)
    return change_one_space


# 필요없는 중괄호 삭제인데 간혹 [영어]로 문단 먹는 경우 문단 불일치 발생
def need_not_middle_bracket(sentence):
    check_word = re.compile(r'(\[\d+\])|([[][a-zA-Z]+\s\d[]]+)|([[][a-zA-Z]+[]]|[[][a\d\s]+[→][a\d\s]+[]])')
    delete_word = re.sub(check_word, '', sentence)
    return delete_word


def para_nltk_sentence(sentence):
    sent_tokens_list = sent_tokenize(sentence)

    return sent_tokens_list


# 영어로 시작해서 끝나는 문장, [중괄호] 삭제  ->  |([[][a-zA-Z\s]+[]])
def delete_sub_eng(sent_tokens):
    check_word = re.compile(r'(^[a-zA-Z\s]+$)|(^[A-Z][a-z]+$)|(^[A-Z][a-z]+[\s][A-Z][a-z]+)')
    delete_word = re.sub(check_word, '', sent_tokens.strip())
    return delete_word


# (a) 은, 는, 이, 가, 에 로 시작하는 문장은 포함/ 그외 (a)가 포함된 문장에 (a)삭제
def delete_small_bracket(sentence):
    checked_part_word = re.compile(r'(^[(][a-z\s][)])(\s)*(은|는|이|가|에)')
    added_checked_part_word = checked_part_word.search(sentence)

    if bool(added_checked_part_word):
        return sentence.strip()
    else:
        checked_word = re.compile(r'(^[(][a-z\s][)])')
        added_checked_word = re.sub(checked_word, '', sentence)
        return added_checked_word.strip()


# 약 + 숫자 조합이 6개 이상일 때 삭제
def delete_sent_about_num(sentence):
    check_word = re.compile(r'(약)|(about)|(approximately)', re.IGNORECASE)
    sentence_inspect = check_word.findall(sentence)
    if len(sentence_inspect) > 10:
        return ''
    else:
        return sentence


def delete_square_bracket(sentence):
    checked_word_square_bracket = re.compile(r'^[[][a-zA-Z\s\d]+[]]$')  # 숫자.로 시작하는 문장
    is_possible_search_square = re.sub(checked_word_square_bracket, '', sentence)
    return is_possible_search_square


def split_upper_eng_dot_space(sentence):
    checked_word_upper_dot_space = re.compile(r'[\s][A-Z][.][\s]')
    check_word = checked_word_upper_dot_space.search(sentence)
    check_word_str = checked_word_upper_dot_space.findall(sentence)
    d = " ".join(check_word_str)
    if bool(check_word):
        list_split_sentence = [e + d for e in sentence.split(d) if e]
        return list_split_sentence
    else:
        return [sentence]
