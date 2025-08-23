import requests
import time

url_base = "https://p2a-gateway.up.railway.app"

# Hàm nhận phần thưởng
def claim(headers):
    url = f"{url_base}/api/v1/compute-units/user/interval-rewards/claim"
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success", False):
            print("Checkin thành công:")
        else:
            print("Checkin thất bại:")
    else:
        print("Không thể nhận thưởng:", response.status_code, response.text)

# Danh sách các câu hỏi cần làm nhiệm vụ
question_list = [
    {"questionId": "cmel5sklx02sfo83xx8vs5snf", "thumbsUp": True},
    {"questionId": "cmel5se7702reo83xi1vofov5", "thumbsUp": True},
    {"questionId": "cmel5r5yu02nto83x582u70yk", "thumbsUp": True},
    {"questionId": "cmel5qx2602noo83xesoh5nkn", "thumbsUp": True},
    {"questionId": "cmel658p003kro83xl0hy9sha", "thumbsUp": True},
    {"questionId": "cmel64qc203k3o83xm8x6ib9y", "thumbsUp": True},
    {"questionId": "cmel64c9q015umg3x7f3muc5z", "thumbsUp": True},
    {"questionId": "cmel63yby03ioo83x3d2bvjuc", "thumbsUp": True},
    {"questionId": "cmel62xg403gno83xbtpfm55o", "thumbsUp": True},
    {"questionId": "cmel62j7z03g2o83xdyc8i4sk", "thumbsUp": True},
]

# Hàm làm nhiệm vụ (trả lời câu hỏi bằng cách bấm Like/Dislike)
def task(headers, questionId, thumbsUp):
    url = f"{url_base}/api/v1/quest/user/thumbs-questions/answer"
    payload = {
        "questionId": questionId,
        "thumbsUp": thumbsUp
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if response.status_code == 200 and response.json().get("success", False):
        print(f"Nhiệm vụ cho câu hỏi {questionId} hoàn thành thành công.")
    else:
        error_message = data.get( "Lỗi không xác định")
        print(f"{error_message}")

# Hàm xử lý cho một token (1 tài khoản)
def chay_cho_mot_token(token, idx):
    headers = {
        "Authorization": "Bearer " + token.strip(),  # Thêm "Bearer" tự động
        "Content-Type": "application/json"
    }  
    print(f"\n🔑 Đang chạy cho tài khoản {idx+1}...")
    # Nhận thưởng
    claim(headers)
    
    # Thực hiện các nhiệm vụ trong danh sách câu hỏi
    for question in question_list:
        task(headers, question["questionId"], question["thumbsUp"])

# Hàm chính, chạy cho nhiều token từ file tokens.json
def main():
    with open("tokens.json", "r") as f:
        tokens = f.readlines()

    for idx, token in enumerate(tokens):
        try:
            chay_cho_mot_token(token, idx)
            time.sleep(3)  # nghỉ 3 giây giữa các tài khoản (tùy chọn)
        except Exception as e:
            print(f"⚠️  Lỗi với token {idx+1}: {e}")

# Chạy chương trình chính
if __name__ == "__main__":
    try:
        while True:
            main()
            print("\n✅ Hoàn thành cho tất cả tài khoản, chờ 24 giờ trước khi chạy lại...")
            time.sleep(60 * 60 * 24)  # chờ 24 giờ
    except KeyboardInterrupt:
        print("⏹️ Chương trình đã bị dừng bởi người dùng.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")
