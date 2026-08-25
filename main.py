import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo

API_KEY = os.environ["GEMINI_API_KEY"]

MODEL = "gemini-3.5-flash-lite"

JST = ZoneInfo("Asia/Tokyo")
now = datetime.now(JST)

weekday_themes = {
    0: "共感系。月曜日の仕事の憂鬱、仕事に行きたくない気持ちに寄り添う。求人の宣伝は弱めにする。",
    1: "収入系。今より少し収入を増やしたい、副業や転職を考える人に向ける。",
    2: "未経験系。警備未経験でも始められること、最初の不安を減らす内容にする。",
    3: "会社・人柄系。KAMBOの若いメンバー、雰囲気、人柄重視の採用について伝える。",
    4: "転職系。今の仕事を続けるか迷っている人、環境を変えたい人に向ける。",
    5: "働き方系。Wワーク、副業、働き方の選択肢をテーマにする。",
    6: "共感系。日曜の夜に明日からの仕事を考えて憂鬱になっている人へ寄り添う。強い求人訴求は避ける。"
}

theme = weekday_themes[now.weekday()]

prompt = f"""
あなたは株式会社KAMBOのSNS採用担当です。

今日の日付：
{now.strftime('%Y年%m月%d日')}

今日のテーマ：
{theme}

目的：
神奈川県、特に川崎市・横浜市周辺で仕事を探している人や、
今の仕事に悩んでいる人に自然に興味を持ってもらうこと。

会社・求人情報：
・株式会社KAMBO
・川崎市を中心に警備業を行っている
・主に工事現場などでの交通誘導警備
・勤務エリアは川崎市、横浜市周辺が中心
・未経験歓迎
・未経験者 日給11,000円〜
・経験者 日給13,000円〜
・比較的若いメンバーが多い
・経験や職歴だけではなく人柄も重視

投稿方針：
・毎回「求人募集です」という広告文にしない
・今日のテーマを最優先する
・共感系の日は、求人紹介よりも共感を中心にする
・仕事あるある、転職への迷い、収入、働き方、職場の雰囲気など切り口を変える
・読んだ人が「少し気になる」と思える自然な流れにする
・押し売り感、営業感を出さない
・事実確認できない内容は書かない
・存在しない福利厚生、待遇、制度は作らない
・「絶対」「必ず稼げる」などの断定は禁止
・過度に煽らない
・前向きで親しみやすい敬語
・堅すぎない文章
・親しみやすさを出すため、😄✨👍💡📣🇯🇵🤣✊🥰などの絵文字を各投稿に1〜3個程度、自然に使用する。使いすぎは禁止。

Threads：
・求人広告感を強くしすぎない
・最初の1〜2行で共感または興味を引く
・自然な会話調と段落
・3〜6段落程度
・最後はコメント、DM、プロフィール確認など自然な行動につなげる
・ハッシュタグは2〜4個程度
・毎回同じ書き出しや構成にしない

X：
・Threadsとは別の文章にする
・簡潔で読みやすくする
・。が来たら改行
・川崎、横浜、仕事、転職など検索されやすい語を自然に含める
・求人情報を入れる場合も詰め込みすぎない
・ハッシュタグは2〜4個程度
・過度な煽り表現は禁止

出力は必ず次の形式だけにしてください。

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
    "maxOutputTokens": 1200
}
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP STATUS:", e.code)
    print("ERROR BODY:")
    print(e.read().decode("utf-8"))
    raise
text = result["candidates"][0]["content"]["parts"][0]["text"]

print("===== KAMBO SNS POST =====")
print(text)

summary_path = os.environ.get("GITHUB_STEP_SUMMARY")

if summary_path:
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write("# KAMBO SNS 投稿案\n\n")
        f.write(text)
        f.write("\n")
