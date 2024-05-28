import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Article data
articles = [
    {
        "title": "經典雞尾酒的調製技巧",
        "content": "本文介紹了幾種經典雞尾酒的調製技巧，從馬提尼到舊式雞尾酒，每一步驟都詳細講解，讓你在家也能調出專業水準的飲品。",
        "publisher": "李俊雄",
        "date": "2024-06-01",
        "tag": "recipes"
    },
    {
        "title": "調酒與藝術的結合",
        "content": "調酒不僅僅是技術，更是一門藝術。探索如何通過調酒展現創意與風格，讓每一杯雞尾酒都成為一件藝術品。",
        "publisher": "王怡婷",
        "date": "2024-07-15",
        "tag": "cocktail-art"
    },
    {
        "title": "初學者的調酒指南",
        "content": "對於調酒初學者，了解基礎工具和材料是非常重要的。本文將介紹基本的調酒設備和一些簡單易學的雞尾酒配方。",
        "publisher": "陳建中",
        "date": "2024-03-20",
        "tag": "mixology"
    }
]

# Insert articles into the database
for article in articles:
    cursor.execute(
        'INSERT INTO article (title, content, publisher, tag, date) VALUES (?, ?, ?, ?, ?)',
        (article['title'], article['content'], article['publisher'], article['tag'], article['date'])
    )
    print(f"Article '{article['title']}' added successfully.")

# Commit the changes and close the connection
conn.commit()
conn.close()