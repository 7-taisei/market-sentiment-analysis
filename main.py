import os
import sqlite3 # 追加：SQLを使うための道具
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def save_to_db(articles):
    # 1. データベースファイルを作成（または開く）
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    # 2. テーブル（表）を作成する。すでに存在する場合はスキップ。
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            published_at TEXT,
            url TEXT
        )
    ''')

    # 3. 取得したニュースを1件ずつ保存する
    for article in articles:
        cursor.execute('''
            INSERT INTO articles (title, published_at, url)
            VALUES (?, ?, ?)
        ''', (article['title'], article['publishedAt'], article['url']))

    # 4. 変更を確定して閉じる
    conn.commit()
    conn.close()
    print("--- データベースへの保存が完了しました ---")

def get_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "経済 OR 株価",
        "language": "jp",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] == "ok":
        articles = data["articles"]
        # 保存用関数を呼び出す
        save_to_db(articles)
        
        for article in articles:
            print(f"タイトル: {article['title']}")
    else:
        print("エラーが発生しました。")

if __name__ == "__main__":
    get_news()