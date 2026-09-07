import os
import requests
from google import genai

# Geminiクライアントの初期化
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 1. Gemini APIによるリサーチ＆記事執筆
prompt = """
あなたはnoteで人気のAI・テクノロジー系クリエイターです。
「AIツール比較・実践検証」をテーマに、読者が思わずスキを押したくなるような実用的なnote記事を作成してください。

条件:
- タイトルは冒頭に「# 」をつけて記載してください。
- 読者がすぐに使える具体的な比較データや、AIツール（Gemini、ChatGPT、Claudeなど）の使い分けのコツを盛り込んでください。
- 専門用語ばかりにせず、初心者にも分かりやすいトーン＆マナーで書いてください。
- Markdown形式で出力してください。
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)

article_content = response.text
discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# 2. Discordの2000文字制限対策：長文を分割して連投する関数
def send_to_discord(webhook_url, text):
    max_length = 1900
    # テキストを1900文字ごとにスライスしてリスト化
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    # 最初に通知ヘッダーを送信
    requests.post(webhook_url, json={"content": "【本日のnote自動生成記事（確認・手動投稿用）】"})
    
    # 分割したテキストを順番に送信（連投）
    for index, chunk in enumerate(chunks):
        payload = {"content": f"```markdown\n{chunk}\n```"}
        requests.post(webhook_url, json=payload)

# Discordへ分割送信を実行
send_to_discord(discord_webhook_url, article_content)
print("Successfully sent to Discord in chunks!")
