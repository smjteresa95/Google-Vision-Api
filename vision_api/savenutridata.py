from dbquery import fetch_nutri_facts_from_table
from visionapi import detect_text, extract_report_num, extract_serving_size, extract_kcal, extract_nutri_data


#fetch nutrition facts image from DB

products = fetch_nutri_facts_from_table('ssg_data')

for product in products:
    #받아온 이미지 링크(출력형태: id, image_url)에서 텍스트 뽑아 품목번호만 출력 
    product_id, url = product
    try:
        if url:
            data = detect_text(url)

            print(f"Product {product_id}")
            print(f"전체데이터: {data}")

            #품목보고번호
            report_num = extract_report_num(data)
            print(f"unique item number: {report_num}")

            #내용량
            serving_size = extract_serving_size(data)
            print(f"serving size: {serving_size}")

            #칼로리
            kcal = extract_kcal(data)
            print(f"kcal: {kcal}")

            #영양성분
            nutri_keywords = ['나트륨', '탄수화물', '당류', '지방', '트랜스지방', '포화지방', '콜레스테롤', '단백질']
            extracted_nutri_list = []
            for keyword in nutri_keywords:
                result = extract_nutri_data(data, keyword)
                extracted_nutri_list.append(result)

            print(f"영양성분: {extracted_nutri_list}")

            print("-------------------------------")

        else:
            print(f"Product {product_id} has no nutrition facts image")
    except Exception as e:
        print(f"Error processing product with ID {product_id} and URL {url}: {e}")