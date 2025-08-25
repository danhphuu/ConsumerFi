import requests
import time
import os

url_base = "https://p2a-gateway.up.railway.app"
log_file = "quest_log.txt"

# Hàm nhận phần thưởng
def claim(headers):
    url = f"{url_base}/api/v1/compute-units/user/interval-rewards/claim"
    response = requests.post(url, headers=headers)

    if response.status_code == 401:
        print("⚠️ Token hết hạn hoặc không hợp lệ.")
        return False

    if response.status_code == 200:
        data = response.json()
        if data.get("success", False):
            print("✅ Checkin thành công!")
            return True
        else:
            print("❌ Checkin thất bại:", data)
            return False
    else:
        print("⚠️ Không thể nhận thưởng:", response.status_code, response.text)
        return False

# Lấy questId tự động từ API hoặc từ file log
def load_quests(headers):
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            quests = [{"questionId": line.strip(), "thumbsUp": True} for line in f if line.strip()]
        print(f"📌 Đã load {len(quests)} questId từ file log.")
        return quests

    url = f"{url_base}/api/v1/quest/user/thumbs-questions/daily"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            print("⚠️ Token hết hạn hoặc không hợp lệ (khi lấy quest).")
            return []
        if response.status_code == 200:
            data = response.json()
            quests = []
            questions = data.get("data", {}).get("questions", [])
            with open(log_file, "w") as f_log:
                for q in questions:
                    questionId = q.get("id")
                    if questionId:
                        quests.append({"questionId": questionId, "thumbsUp": True})
                        f_log.write(questionId + "\n")
            print(f"📌 Lấy {len(quests)} questId từ API và lưu vào file log.")
            return quests
        else:
            print("⚠️ Không lấy được quest từ API:", response.status_code, response.text)
            return []
    except Exception as e:
        print("❌ Lỗi khi gọi API quest:", e)
        return []

# Hàm làm nhiệm vụ
def task(headers, questionId, thumbsUp):
    url = f"{url_base}/api/v1/quest/user/thumbs-questions/answer"
    payload = {"questionId": questionId, "thumbsUp": thumbsUp}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 401:
        print(f"⚠️ Token hết hạn khi làm nhiệm vụ {questionId}.")
        return

    data = response.json()
    if response.status_code == 200 and data.get("success", False):
        print(f"🎯 Nhiệm vụ {questionId} hoàn thành.")
    else:
        print(f"❌ Lỗi khi làm nhiệm vụ {questionId}: {data}")

# Chạy cho 1 token
def chay_cho_mot_token(token, idx):
    headers = {
        "Authorization": "Bearer " + token.strip(),
        "Content-Type": "application/json"
    }
    print(f"\n🔑 Đang chạy cho tài khoản {idx+1}...")

    # Nhận thưởng
    if not claim(headers):
        print(f"⏩ Bỏ qua tài khoản {idx+1} do token không hợp lệ.")
        return

    # Lấy questId từ file log hoặc API
    quests = load_quests(headers)

    # Thực hiện nhiệm vụ với delay 4s mỗi quest
    for q in quests:
        task(headers, q["questionId"], q["thumbsUp"])
        time.sleep(4)

# Hàm chính
def main():
    with open("tokens.json", "r") as f:
        tokens = f.readlines()

    for idx, token in enumerate(tokens):
        try:
            chay_cho_mot_token(token, idx)
            time.sleep(3)  # nghỉ 3s giữa các account
        except Exception as e:
            print(f"⚠️  Lỗi với token {idx+1}: {e}")

# Run
if __name__ == "__main__":
    try:
        while True:
            main()
            print("\n✅ Hoàn thành tất cả tài khoản, chờ 24h trước khi chạy lại...")
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        print("⏹️ Dừng bởi người dùng.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
