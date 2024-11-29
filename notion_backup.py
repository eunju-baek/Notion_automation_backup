import requests
import os
import json  # json 모듈 추가

# Notion API 설정
headers = {
    'Authorization': 'Bearer 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',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

# 데이터베이스 쿼리
database_id = '134d13da8dfa80a29232e955d7482ade'
url = f'https://api.notion.com/v1/databases/{database_id}/query'
response = requests.post(url, headers=headers)
if response.status_code != 200:
    print(f"Error: API request failed with status code {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

data = response.json()
if 'results' not in data:
    print("Error: 'results' key not found in API response")
    print(f"Response: {data}")
    exit(1)

# 백업 폴더 생성
backup_folder = 'notion_backup'
os.makedirs(backup_folder, exist_ok=True)

# 페이지 및 파일 백업
for page in data['results']:
    page_id = page['id']
    page_title = page['properties']['Name']['title'][0]['plain_text']
    
    # 페이지 내용 저장 (올바른 JSON 형식으로 저장)
    with open(f'{backup_folder}/{page_title}.json', 'w', encoding='utf-8') as f:
        json.dump(page, f, ensure_ascii=False, indent=4)  # json.dump() 사용
    
    # 파일 다운로드
    if 'Files' in page['properties']:
        for file in page['properties']['Files']['files']:
            file_url = file['file']['url']
            file_name = file['name']
            file_response = requests.get(file_url)
            
            with open(f'{backup_folder}/{file_name}', 'wb') as f:
                f.write(file_response.content)

print("Backup complete.")
