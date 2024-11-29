import os
import json
import pandas as pd

# JSON 파일이 저장된 폴더 경로
folder_path = 'notion_backup'
# 결과를 저장할 CSV 파일 경로
output_csv = 'notion_backup.csv'

# 모든 JSON 데이터를 저장할 리스트
data_list = []

# 폴더 내의 모든 JSON 파일을 읽기
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 필요한 데이터 추출 (예: 제목과 내용)
                page_data = {
                    'id': data.get('id'),
                    'title': data.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', ''),
                    'content': json.dumps(data)  # 전체 내용을 문자열로 저장
                }
                data_list.append(page_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

# DataFrame 생성 후 CSV로 저장
if data_list:  # 데이터가 있을 경우에만 CSV로 저장
    df = pd.DataFrame(data_list)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"CSV 파일이 '{output_csv}'로 저장되었습니다.")
else:
    print("No valid data found to convert.")
    
