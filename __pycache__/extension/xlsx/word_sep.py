import pandas as pd
from konlpy.tag import Okt
from collections import Counter

# NOTE: 엑셀파일 특정행을 타겟한 뒤 단어 | 숫자 형식으로 count하는 함수 
def extract_column(input_file, column_name):
    # 엑셀 파일을 읽어옵니다.
    df = pd.read_excel(input_file, engine='openpyxl')
    
    # 특정 열의 값을 추출합니다.
    column_data = df[column_name]
    
    return column_data

def analyze_text(text_list):
    okt = Okt()
    word_list = []
    
    for text in text_list:
        # 형태소 분석을 통해 명사만 추출합니다.
        text = str(text)
        nouns = okt.nouns(text)
        word_list.extend(nouns)
    
    # 단어 빈도수를 계산합니다.
    word_freq = Counter(word_list)
    
    return word_freq

def save_to_excel(word_freq, output_file):
    # 단어 빈도수를 데이터프레임으로 변환합니다.
    df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
    df = df.dropna()
    # 엑셀 파일로 저장합니다.
    df.to_excel(output_file, index=False)

if __name__ == '__main__':
    input_file = ''  # NOTE 입력 파일 경로
    column_name = 'content'  # NOTE 추출할 열 이름
    output_file = 'word_frequency.xlsx'  # NOTE 출력 파일 경로
    
    # 특정 열의 값을 추출합니다.
    content_values = extract_column(input_file, column_name)

    print('target Value: ',content_values)
    
    # 형태소 분석을 통해 단어 빈도수를 계산합니다.
    word_freq = analyze_text(content_values)
    
    # 단어 빈도수를 엑셀 파일로 저장합니다.
    save_to_excel(word_freq, output_file)