import openpyxl
import pandas as pd
import requests
from bs4 import BeautifulSoup

data = []

# 1부터 4까지 4개 페이지 수집
for i in range(1, 5):
    # 수정 1: URL 앞에 f를 붙여서 page=1, page=2 ... 가 적용되도록 수정
    response = requests.get(
        f"https://startcoding.pythonanywhere.com/basic?page={i}"
    )
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    items = soup.select(".product")

    for item in items:
        # 카테고리
        category = item.select_one(".product-category").text.strip()

        # 상품명
        category_name = item.select_one(".product-name").text.strip()

        # 수정 2: 가격 처리 (replace를 먼저 수행한 후 '원' 제거 및 공백 정리)
        price = (
            item.select_one(".product-price")
            .text.replace(",", "")
            .replace("원", "")
            .strip()
        )

        # 상세페이지 링크
        category_link = item.select_one(".product-name > a").attrs["href"]

        # 데이터 저장
        data.append([category, category_name, category_link, price])
        print(category, category_name, category_link, price)

# Excel 파일 저장
df = pd.DataFrame(data, columns=["카테고리", "상품명", "상세페이지링크", "가격"])
df.to_excel("data.xlsx", index=False)
print("엑셀 저장 완료!")    