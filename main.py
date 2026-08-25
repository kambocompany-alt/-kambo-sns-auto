import os
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = os.environ["GEMINI_API_KEY"]

MODEL = "gemini-2.5-flash"

JST = ZoneInfo("Asia/Tokyo")
now = datetime.now(JST)

weekday_themes = {
    0: "月曜日。仕事に行きたくない気持ちや、転職を考える人への共感",
    1: "火曜日。給与・収入・今より少し収入を増やしたい人向け",
    2: "水曜日。未経験から始められる仕事への不安解消",
    3: "木曜日。会社の雰囲気・若い会社・人柄を重視する採用",
    4: "金曜日。転職を迷っている人、仕事を変えたい人への訴求",
    5: "土曜日。副業・Wワーク・働き方の選択肢",
    6: "日曜日。明日からの仕事が憂鬱な人への共感"
}

theme = weekday_themes[now.weekday()]

prompt = f"""
あなたは株式会社KAMBOのSNS採用担当です。

今日の日付：
{now.strftime('%Y年%m月%d日')}

今日のテーマ：
{theme}

目的：
神奈川県、特に川崎市・横浜市周辺の求職者や転職を考えている人に
株式会社KAMBOを知ってもらうこと。

会社・求人情報：
・株式会社KAMBO
・川崎市を中心に警備業を行っている
・主に工事現場などでの交通誘導警備
・勤務地は川崎市、横浜市周辺が中心
・未経験歓迎
・未経験者 日給11,000円〜
・経験者 日給13,000円〜
・比較的若いメンバーが多い
・経験や職歴だけではなく人柄も重視

Threads用とX用の投稿をそれぞれ1本作成してください。

【Threads】
・求人広告感を強くしすぎない
・親しみやすい敬語
・元気で自然な口調
・共感や会話を重視
・最初の2行で興味を引く
・川崎周辺の人に届きやすい内容
・最後はコメントやDMにつながる自然な一言
・ハッシュタグを2〜4個程度
・同じ表現の繰り返しを避ける

【X】
・Threadsとは別の文章にする
・簡潔で分かりやすい
・川崎、横浜、仕事、転職など検索されやすい語を自然に入れる
・求人情報も分かるようにする
・ハッシュタグを2〜4個程度
・過度な煽り表現は禁止

【絶対に禁止】
・存在しない待遇や福利厚生を書く
・必ず稼げるなどの断定
・架空の実績
・差別的な募集条件
・事実確認できない内容

次の形式だけで出力してください。

THREADS:
（Threads投稿文）

X:
（X投稿文）
"""

url = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent?key={API_KEY}"
)

data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ],
    "generationConfig": {
        "temperature": 1.0,
        "maxOutputTokens": 1200
    }
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

text = result["candidates"][0]["content"]["parts"][0]["text"]

print("===== KAMBO SNS POST =====")
print(text)
