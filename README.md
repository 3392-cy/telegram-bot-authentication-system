# Telegram Token Access Bot 🤖🔐  
**by @gqpgqpg**

A lightweight **Telegram bot access-control system** that uses **time-based activation tokens** to grant or restrict user access to private services, tools, or bots.

This project is split into **two files**:
- `admin.py` → configuration & token duration logic
- `main.py` → Telegram bot, token validation, and user access handling

---

## ✨ Features

### 🔑 Token-Based Access System
- One-time activation tokens
- Token durations:
  - `7days`
  - `30days`
  - `lifetime`
- Tokens are **single-use**
- Each user can only have **one active token at a time**
- Automatic expiry handling

### 👤 User Management
- Authorized users stored automatically
- Persistent storage via `tokens.json`
- Access validation on every command
- Automatic re-authentication if token is still valid

### 🛡️ Admin Controls
- Admin-only token generation
- Duration-based token issuing
- Secure admin ID check
- Environment-variable token support

### 🤖 Telegram Bot Commands
- `/start` → Check access status
- `/activate` → Activate an access token
- `/gentoken` → *(Admin only)* Generate a token

├── admin.py # Admin config, token duration, paths
├── main.py # Telegram bot logic
├── tokens.json # Token storage (auto-created)

---

## 🧠 How It Works

1. Admin generates a token with a duration
2. User activates token via `/activate`
3. Token is:
   - Moved from `active` → `used`
   - Bound to the user's Telegram ID
4. Bot checks token validity on each interaction
5. Expired users automatically lose access

---

## 📦 Requirements

- Python **3.8+**
- Dependencies:
  ```bash
  pip install pyTelegramBotAPI


## 📁 Project Structure

