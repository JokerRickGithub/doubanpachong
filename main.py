import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

def crawl_douban_top250():
    """豆瓣电影TOP250爬虫 - 修复反爬+容错判断 完整版"""
    # 创建Excel工作簿
    wb = Workbook()
    ws = wb.active
    ws.append(["排名", "电影名", "评分", "导演/主演/年份", "电影简介"])

    # 豆瓣TOP250地址
    base_url = "https://movie.douban.com/top250"
    # ✅ 重点修复：升级请求头，伪装成真实浏览器，彻底绕过豆瓣反爬
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://movie.douban.com/",
        "Cache-Control": "max-age=0"
    }

    # 爬取10页，每页25条，共250条
    for page in range(10):
        url = base_url + f"?start={page*25}"
        try:
            # 发送请求
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status() # 抛出请求错误
            soup = BeautifulSoup(res.text, "html.parser")
            movies = soup.find_all("div", class_="item")

            # 解析每一部电影
            for movie in movies:
                # ✅ 重点修复：所有find都加容错判断，找不到返回空字符串，不会报错
                rank_tag = movie.find("em", class_="")
                rank = rank_tag.text.strip() if rank_tag else "无排名"

                name_tag = movie.find("span", class_="title")
                movie_name = name_tag.text.strip() if name_tag else "无名"

                score_tag = movie.find("span", class_="rating_num")
                score = score_tag.text.strip() if score_tag else "0.0"

                info_tag = movie.find("p", class_="")
                movie_info = info_tag.text.strip().replace("\n", "").replace("  ", "") if info_tag else "无信息"

                intro_tag = movie.find("span", class_="inq")
                movie_intro = intro_tag.text.strip() if intro_tag else "无简介"

                # 写入Excel
                ws.append([rank, movie_name, score, movie_info, movie_intro])
                print(f"✅ 爬取成功：{rank}. {movie_name} - {score}分")
            
            # ✅ 友好爬取：每页爬完休眠1秒，降低服务器压力，避免被封IP
            time.sleep(1)

        except Exception as e:
            print(f"❌ 第{page+1}页爬取失败：{str(e)}")
            continue

    # 保存Excel文件
    wb.save("豆瓣电影TOP250.xlsx")
    print("\n🎉 全部爬取完成！已生成【豆瓣电影TOP250.xlsx】文件")

# 运行爬虫
if __name__ == "__main__":
    crawl_douban_top250()