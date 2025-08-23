# 🤖 ConsumerFi Automation Bot

This bot automates **reward claiming**, **daily claiming**, and **thumbs up/down answering** on the [ConsumerFi](https://www.consumerfi.ai/app) platform using Bearer tokens from each account.

---

## 🧰 Features

- ✅ Automatic reward claim (`interval-rewards`)  
- 🗓️ Automatic daily claim (`daily-rewards`)  
- 👍 Auto-answer thumbs up/down  
- 🧑‍🤝‍🧑 Multi-account support (multiple tokens)  
- ⏱️ Delay between accounts  
- 🧾 Logs success/failure results  

---

## 📁 File Structure

```
.
├── main.py           # Main script
├── tokens.txt        # Account tokens
└── README.md         # This documentation
```

---

## 📝 `tokens.txt` Format

Each line should contain **one token only** (without `Bearer`), for example:

```
eyJhbGciOi...
eyJ0eXAiOi...
```

> ⚠️ Important: You don’t need to include `Bearer`. The script will add it automatically.

---

## 🚀 How to Run

1. Install Python (version 3.8 or higher)  
2. Install dependencies:  
   ```bash
   pip install requests
   ```
3. Run the bot:  
   ```bash
   python bot.py
   ```

---

## 🔁 Bot Workflow

For each account:

1. ✅ Send **interval reward** claim  
2. 🗓️ Send **daily reward** claim  
3. 👍 Answer all thumbs up/down questions  
4. ⏱️ Wait 3 seconds, then continue to the next account  

---

## ❗ Common Errors

| Issue | Cause | Solution |
|-------|-------|----------|
| `JWS Protected Header is invalid` | Invalid/expired token | Make sure the token is valid and not expired |
| Status 401 / 403 | Unauthorized or blocked account | Replace with a valid token |
| No success response | Server downtime or endpoint changes | Check the API endpoints and request format |

---
