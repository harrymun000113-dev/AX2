import openpyxl
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 네이버 금융 차단을 완전히 우회하기 위한 완벽한 브라우저 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.naver.com/",
}

data = []

# 1페이지부터 3페이지까지 수집
for page in range(1, 4):
    url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page={page}"

    # requests로 데이터 요청
    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")

    # 모든 종목명이 포함된 a 태그 직접 타겟팅 (a.tlt.i 클래스)
    items = soup.select("a.tlt.i")

    print(f"--- {page}페이지 읽는 중... (찾은 종목 수: {len(items)}개) ---")

    for a_tag in items:
        # a 태그의 부모 tr(행) 찾기
        tr = a_tag.find_parent("tr")
        tds = tr.select("td")

        # 데이터 추출
        name = a_tag.text.strip()
        link = "https://finance.naver.com" + a_tag["href"]
        price = tds[2].text.replace(",", "").strip()  # 현재가
        market_cap = tds[6].text.replace(",", "").strip()  # 시가총액

        data.append([name, price, market_cap, link])
        print(f"[{name}] 현재가: {price} | 시가총액: {market_cap}억")

# 수집된 데이터가 있는지 확인 후 엑셀 저장
if len(data) > 0:
    df = pd.DataFrame(
        data, columns=["종목명", "현재가", "시가총액(억)", "상세페이지링크"]
    )
    df.to_excel("naver_finance.xlsx", index=False)
    print(f"\n총 {len(data)}개 데이터 수집 성공! 'naver_finance.xlsx' 저장 완료.")
else:
    print(
        "\n데이터를 가져오지 못했습니다. 네트워크 상태나 네이버 차단 여부를 확인하세요."
    )