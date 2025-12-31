import time
import json
import requests

TOKEN = "8003470338:AAFnW1bnhRVyhcavj4Z7Z1JQ-N9T2EiYUDc"
CHANNEL = "@an9tov"
PHOTOS = [f"{i}.jpg" for i in range(1, 11)]

def send_carousel():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"
    media = [{"type": "photo", "media": f"attach://{i}"} for i in range(len(PHOTOS))]
    media[0]["caption"] = "✨ Год в 10 кадрах"
    media[0]["parse_mode"] = "HTML"

    files = {str(i): open(PHOTOS[i], "rb") for i in range(len(PHOTOS))}
    data = {"chat_id": CHANNEL, "media": json.dumps(media)}

    try:
        r = requests.post(url, data=data, files=files)
        for f in files.values():
            f.close()
        return r.json().get("ok", False)
    except Exception as e:
        for f in files.values():
            f.close()
        print("❌ Ошибка:", e)
        return False

print("✅ Бот запущен. Напишите /publish в ЛС @an9tov_bot")
updates_offset = None

while True:
    try:
        res = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params={"offset": updates_offset, "timeout": 20}
        ).json()
        
        for upd in res.get("result", []):
            updates_offset = upd["update_id"] + 1
            msg = upd.get("message", {})
            if msg.get("text") == "/publish":
                user_id = msg["from"]["id"]
                print(f"📩 /publish от {user_id}")
                if send_carousel():
                    print("✅ Карусель отправлена")
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={"chat_id": user_id, "text": "✅ Опубликовано!"}
                    )
    except Exception as e:
        print("⚠️ Ошибка цикла:", e)
    time.sleep(1)
