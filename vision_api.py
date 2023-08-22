# Google Cloud에서 프로젝트 생성하고, 
# 해당 프로젝트에 대해서 service account를 만든다. 
# API key는 json파일로 받아서 잘 저장해둔다.
# 위의 과정은 gcloud CLI를 다운받아 콘솔 창에서 진행가능하다.

import io, os
import sys #한글을 읽어오게끔 하기 위한 라이브러리
import re #정규표현식을 사용하기 위한 라이브러리

from google.cloud import vision

# 한글이 깨져서 보이지 않게
# 파이썬의 표준 출력과 표준 에러 출력을 UTF-8 인코딩으로 변경하는 코드
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


#GOOGLE API KEY 경로 지정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\msong\Desktop\VisionAPI\kinni-396612-830c42e9beec.json'


# vision api로 이미지에서 텍스트만 추출
def detect_text(url):

    #이미지를 vision API가 읽을 수 있는 형태로 가공해 주는 과정

    #이 객체를 통해서 이미지에서 텍스트,레이블,얼굴 등 주석 생성가능
    client = vision.ImageAnnotatorClient()

    #Vision api에 제공할 이미지 객체
    image = vision.Image()

    # 이미지 객체의 'source' 속성의 'image_uri'에 인수로 받은 URL을 할당함으로서 
    # 지정된 URL에서 이미지를 불러 올 수 있게 된다.
    image.source.image_uri = url

    #한국어 잘 감지하도록 힌트를 준다.
    image_context = {"language_hints": ["ko"]}

    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    return texts[0].description





#이미지에서 추출한 데이터에서 원하는 정보만 얻어오기

#품목보고번호 가져오기
def extract_report_num(text):
    num_pattern = re.compile(
        r'품목보고번호 (\d+-\d+)', re.I
    )

    matches = num_pattern.search(text)
    if matches: 
        return matches.group()
    else:
        return "품목보고번호 가져오기 실패"





#내용량과 열량 가져오기
def extract_misc_data(text):
    
    kcal_pattern = re.compile(
        r'내용량\n(\d+ ?[g|mL])\n(\d+ ?kcal)', re.I)
    
    matches = kcal_pattern.search(text)
    if matches: 
            return matches.group()
    else:
        return "형식 잘못 입력한듯"
    



#영양성분 가져오기
def extract_nutri_data(text, keyword):

    nutri_patterns = [
        r'({}\s*\d+\.\s*\d+(?:g|mg))'.format(keyword),
        r'({}\s*\d+\s*\.\s*\d+(?:g|mg))'.format(keyword),
        r'({}\s*\d+\.\d+\s*(?:g|mg))'.format(keyword),
        r'({}\s*\d+\.\d+(?:g|mg))'.format(keyword),
        r'({}\s*\d+\s*(?:g|mg))'.format(keyword),
        r'({}\d+\s*(?:g|mg))'.format(keyword)
    ]

    for pattern in nutri_patterns:
        match = re.search(pattern, text)

        if match: 
            return match.group(1)
    else:
        return "일치하는 패턴이 없습니다."



# 한 이미지에 두 가지 이상의 상품이 있는지 확인
def contains_multiple_items(text, keyword):
    return text.count(keyword) >=2



data = detect_text(r'https://gi.esmplus.com/babyda/all_new_bb/grain/on_the_go/masala_red_curry_chicken/masala_red_curry_chicken_05.jpg')

nutri_keywords = ['나트륨', '탄수화물', '당류', '지방', '트랜스지방', '포화지방', '콜레스테롤', '단백질']

extracted_list = []


if contains_multiple_items(data, '탄수화물'):
    print("한 이미지에 두 상품이 포함되어있습니다.")
else:
    print("이미지에 하나의 상품만 포함되어있습니다.")




#품목보고번호
print(extract_report_num(data))
    

# 영양성분
for keyword in nutri_keywords:
    result = extract_nutri_data(data, keyword)
    extracted_list.append(result)

print(extracted_list)


#내용량, 열량 
print(extract_misc_data(data))
