import requests
import re

# 네이버 API 키 설정
CLIENT_ID = ''
CLIENT_SECRET = ''

# 네이버 블로그 검색 API를 호출하는 함수
def get_blog_ids_and_posts(query, display=10, start=1):
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    
    params = {
        "query": query,  # 검색할 키워드
        "display": display,  # 한 번에 반환할 블로그 포스트 수
        "start": start  # 검색 결과의 시작 페이지
    }
    
    # API 호출
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        blog_info = []
        
        # 블로그 URL에서 ID와 포스트 번호 추출
        for item in data.get("items", []):
            blog_url = item.get("link")
            
            # URL에서 블로그 ID와 포스트 ID 추출 (예: blog.naver.com/{blog_id}/{post_id})
            match = re.search(r"blog\.naver\.com/([^/]+)/(\d+)", blog_url)
            if match:
                blog_id = match.group(1)
                post_id = match.group(2)
                blog_info.append(f"https://blog.naver.com/PostView.naver?blogId={blog_id}&logNo={post_id}&redirect=Dlog&widgetTypeCall=true&noTrackingCode=true&directAccess=false")
        
        return blog_info
    else:
        print(f"API 요청 실패: {response.status_code} {response}")
        return []


