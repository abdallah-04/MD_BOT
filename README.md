
# IEEE CS MD Assistant Telegram Bot 🤖

A Telegram bot designed to assist the **IEEE Computer Society Membership Development (MD) Team** in managing new member follow-ups, sending WhatsApp links, updating Google Sheets, and automating membership communication.

**By Abdallah Almuflah, MD Leader**

---

## 🔧 Features

- **Start Monitoring**: Automatically checks for new form entries and assigns them to MD members.
- **Send WhatsApp Links**: Automatically generates and sends WhatsApp links to new joiners.
- **Mention MD Members**: Notifies specific MD members when action is required.
- **Update Follow-Up Status**: Changes Google Sheet cell colors to indicate follow-up status.
- **Check for Delayed Responses**: Periodically checks for pending follow-ups and notifies the MD team.
- **Job Distribution**: Splits phone numbers among MD members and sends their task list.
- **Keyword-Based Auto Reply**: Replies with links and information based on detected keywords in the chat.
- **Sheet Integration**: Seamlessly interacts with Google Sheets using `gspread`.

---

## 🧠 Requirements

- Python 3.10+
- Google Sheets API credentials (`credentials.json`)
- A Telegram Bot Token
- `.env` file with the following variables:

```env
TOKEN=your_telegram_bot_token
BOT_USERNAME=@your_bot_username
SCOPES=https://www.googleapis.com/auth/spreadsheets
SHEET_ID=your_google_sheet_id
```

---

## 📦 Installation

1. Clone the repository
2. Create `.env` file as shown above
3. Place your `credentials.json` in the root directory
4. Install dependencies:

```bash
pip install python-telegram-bot gspread gspread-formatting google-auth python-dotenv
```

5. Run the bot:

```bash
python bot.py
```

---

## 🧪 Bot Commands

| Command       | Description                                         |
|---------------|-----------------------------------------------------|
| `/start`      | Starts the bot and begins checking for new entries |
| `/help`       | Shows help message                                  |
| `/update ID`  | Updates a user's status and colors their row green  |
| `/mention`    | Mentions all numbers in a dedicated sheet tab       |
| `/jop`        | Distributes WhatsApp links among MD members         |

---

## 📁 Sheet Structure

The main worksheet should include:

- Column **B**: Name
- Column **D**: Phone Number
- Column **K**: Assigned MD member
- Column **L**: Follow-up status (`B` for pending, `D` for done)
- Column **I**: Used for background color indicators

Other tabs like `jop_command`, `mention_command`, and `data fot the bot` support job distribution and keyword response features.

---

## 🙋‍♂️ Author

**By Abdallah Almuflah**, MD Leader of IEEE Computer Society - BAU.
**abdullah8almufleh@gmail.com**


Feel free to reach out for any improvements or issues.

---

## 📜 License

This project is private/internal for IEEE CS MD purposes. Distribution without permission is not allowed.
```
