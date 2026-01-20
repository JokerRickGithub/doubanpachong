import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def crawl_douban_top250():
    """爬取豆瓣电影TOP250"""
    wb = Workbook()
    ws = wb.active
    ws.append(["排名", "电影名", "评分", "导演/主演", "简介"])
    base_url = "https://movie.douban.com/top250"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for page in range(10):  # 共10页，每页25条
        url = base_url + f"?start={page*25}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        movies = soup.find_all("div", class_="item")
        for movie in movies:
            rank = movie.find("em", class_="").text
            name = movie.find("span", class_="title").text
            score = movie.find("span", class_="rating_num").text
            info = movie.find("p", class_="").text.strip()
            intro = movie.find("span", class_="inq").text if movie.find("span", class_="inq") else "无简介"
            ws.append([rank, name, score, info, intro])
            print(f"✅ 爬取成功：{rank}. {name} - {score}分")
    wb.save("豆瓣电影TOP250.xlsx")
    print("🎉 全部爬取完成！已保存为Excel文件")

if __name__ == "__main__":
    crawl_douban_top250()