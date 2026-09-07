import os
import requests
from google import genai

# Geminiクライアントの初期化 (Google GenAI SDKを使用)
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
    model="gemini-3.6-flash",  # または用途に合わせたモデル
    contents=prompt,
)

article_content = response.text

# 2. DiscordへのWebhook送信
discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# Discordのメッセージ制限（2000文字）対策として、分割または冒頭部分の通知にする場合もありますが、
# Webhook経由で長文を送るための処理
payload = {"content": f"【本日のnote自動生成記事（要確認・手動投稿用）】\n\n{article_content}"}

# Discordは2000文字制限があるため、超える場合は分割して送るか、ファイル添付にするのが安全です
if len(article_content) > 1900:
  # 長い場合はファイルとして送信、あるいは分割送信
  payload = {
      "content": "【本日のnote自動生成記事】\n文字数が多いため、ファイルとして生成されました。（または一部抜粋）"
  }
  # 簡易的にテキストファイルとして送信する場合の処理などへの拡張も可能です

response_discord = requests.post(discord_webhook_url, json=payload)

if response_discord.status_code == 204 or response_discord.status_code == 200:
  print("Successfully sent to Discord!")
else:
  print(f"Failed to send to Discord: {response_discord.text}")
