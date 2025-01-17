from get_blog_id import get_blog_ids_and_posts
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Chromium 실행 (수동 로그인 후 작업 시작)
    browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])  # 자동화 탐지 우회

    # 브라우저 컨텍스트 생성: 더 자연스러운 환경을 만들기 위해 context 사용
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.818.66",
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1.0,  # 실제 디스플레이와 유사한 해상도
        locale="ko",  # 언어 설정
        timezone_id="Asia/Seoul"  # 시간대 설정
    )
    
    page = context.new_page()

    # URL로 이동
    page.goto('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/')

    # 수동 로그인 대기: 로그인 후 '로그인 완료' 메시지를 확인하거나 특정 요소가 나타날 때까지 기다리기
    print("로그인 후 'Enter' 키를 눌러 계속 진행하세요...")
    input("로그인 완료 후 계속 진행하려면 'Enter'를 눌러주세요.")

    # 블로그 URL 리스트 가져오기
    result = get_blog_ids_and_posts("오징어")
    # 각 블로그 URL에 대해 작업 수행
    for url in result:
        try:  
            print(f"현재 처리 중인 URL: {url}")
        
            # 블로그로 이동
            time.sleep(1)
            page.goto(url)
        
            # 이웃 추가 버튼 클릭 (새 탭이 열릴 가능성 있음)
            with page.expect_popup() as popup_info:  # 새 탭 열릴 때까지 대기
                page.click(".btn_buddy")
        
            # 새로 열린 팝업 탭을 다루기
            popup = popup_info.value
            popup.wait_for_selector("#each_buddy_add", timeout=1000)  # 새 탭에서 요소가 나타날 때까지 대기
            
            # label을 클릭
            buddy_add_label = popup.locator('label[for="each_buddy_add"]')
            if not buddy_add_label.is_enabled():
                popup.close()  # 팝업 닫기
                time.sleep(1)
                print(f"비활성화된 '서로이웃 추가' 버튼을 건너뜁니다: {url}")
                continue  # 비활성화된 버튼이 있으면 해당 URL 건너뛰기
            
            popup.click('label[for="each_buddy_add"]')

            # next 다음 클릭
            popup.click('a.button_next')

            # 이름 가져오기
            name_buddy = popup.locator('.text_buddy_add strong.name_buddy').text_content()
            print(f"서로이웃 추가 요청 대상: {name_buddy}")

            # 메시지 입력
            popup.locator('#message').fill(f"안녕하세요! {name_buddy}님 서로이웃 신청 드립니다. 잘 부탁드려요 😊")

            # 최종 버튼 클릭
            popup.click('a.button_next')
            popup.close()  # 팝업 닫기

        except Exception as e:
            print(f"오류 발생: {e}, URL: {url}")
            popup.close()
            continue

    # 브라우저 종료
    browser.close()
