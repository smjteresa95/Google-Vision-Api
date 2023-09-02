import mysql.connector
from dbsetup import get_connection

def __init__(self):
    self.conn = self.get_connection()
    self.cursor = self.conn.cursor()


#영양성분 이미지Url 가져오기
def fetch_nutri_facts_from_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = f'SELECT product_id, nutri_image FROM {table_name}'
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#영양성분 이미지에서 뽑아온 데이터로 성분 컬럼 채우기
#data는 다음과 같은 형식으로 
# data = {
#     'column1': 'new_value1',
#     'column2': 'new_value2'
# }
def update_nutri_facts(table_name, product_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    #SET(변경할 값) 구문 
    set_clause = ', '.join([f"{key} = %s" for key, value in data.items()])

    query = f'''
    UPDATE {table_name}
    SET {set_clause}
    WHERE id = %s
    '''

    #data에서 value 꺼내오기
    values = list(data.values()) + [product_id]

    cursor.execute(query, values)
    conn.commit()
    conn.close()


def close(self):
    self.conn.close()



