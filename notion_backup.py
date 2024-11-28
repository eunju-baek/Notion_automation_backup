import requests
import os

# Notion API 설정
headers = {
    'Authorization': 'Bearer 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',
    'Notion-Version': '2022-06-28',
    'Content-Type':'application/json'
}

# 데이터베이스 쿼리
database_id = '134d13da8dfa80a29232e955d7482ade'
url = f'https://api.notion.com/v1/databases/{database_id}/query'
response = requests.post(url, headers=headers)
data = response.json()

# 백업 폴더 생성
backup_folder = 'notion_backup'
os.makedirs(backup_folder, exist_ok=True)

# 페이지 및 파일 백업
for page in data['results']:
    page_id = page['id']
    page_title = page['properties']['Name']['title'][0]['plain_text']
    
    # 페이지 내용 저장
    with open(f'{backup_folder}/{page_title}.json', 'w') as f:
        f.write(str(page))
    
    # 파일 다운로드
    if 'Files' in page['properties']:
        for file in page['properties']['Files']['files']:
            file_url = file['file']['url']
            file_name = file['name']
            file_response = requests.get(file_url)
            
            with open(f'{backup_folder}/{file_name}', 'wb') as f:
                f.write(file_response.content)

print("Backup complete.")