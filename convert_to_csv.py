import os
import json
import pandas as pd
from datetime import datetime  # datetime 모듈 추가

# JSON 파일이 저장된 폴더 경로
folder_path = 'notion_backup'

# 현재 날짜를 YYYYMMDD 형식으로 가져오기
current_date = datetime.now().strftime("%Y%m%d")

# 결과를 저장할 CSV 파일 경로 (엑셀 확장자로 변경)
output_csv = f'{current_date}_DBbackup.xlsx'

# 모든 JSON 데이터를 저장할 리스트
data_list = []

# 폴더 내의 모든 JSON 파일을 읽기
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # 필요한 데이터 추출
                page_data = {
                    'Name': data.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', ''),
                    'Tags': [tag['name'] for tag in data.get('properties', {}).get('Tags', {}).get('multi_select', [])],
                    '완료': data.get('properties', {}).get('완료', {}).get('checkbox', False),
                    '파일과 미디어': [file['name'] for file in data.get('properties', {}).get('파일과 미디어', {}).get('files', [])],
                    'Date': data.get('properties', {}).get('Date', {}).get('date', None),
                }
                data_list.append(page_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

# DataFrame 생성 후 엑셀로 저장
if data_list:  # 데이터가 있을 경우에만 CSV로 저장
    df = pd.DataFrame(data_list)
    df.to_excel(output_csv, index=False, encoding='utf-8-sig')  # to_excel() 사용
    print(f"엑셀 파일이 '{output_csv}'로 저장되었습니다.")
else:
    print("No valid data found to convert.")
