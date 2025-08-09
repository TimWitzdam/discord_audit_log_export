<div align="center">
    <h1 align="center">Discord Audit Log Exporter</a></h1>
    <p align="center">This bot helps you to export the audit log of your server in JSON or/and CSV format.</p>
  <a target="_blank" align="center">
    <img src="https://legende.cc/ss/3t0BMa8EtO.png" alt="Theme preview" width="975"/>
</a>
</div>
<br />

## 🚀 Getting started (Discord Bot)

1. Invite the bot to your server: [Invite](https://discord.com/oauth2/authorize?client_id=544944976853729300&permissions=2147485824&integration_type=0&scope=bot)
2. Use the /export command to export the audit log of your server

## 🖥️ Getting started (Selfhosted)

1. Prerequisites

Make sure you have Docker and Docker Compose installed

2. Clone/download the repo

```
git clone https://github.com/TimWitzdam/discord_audit_log_export.git
cd discord_audit_log_export
```

3. Create .env file

```
# Example .env file

BOT_TOKEN=your_bot_token
BOT_INVITE=https://example.com
DEFAULT_LIMIT=1000
MAX_LIMIT=10000
```

4. Start the bot

```
docker compose up
```

## 🧞 Commands

All commands that are available for the bot.

| Command                             | Action                                                        |
| :---------------------------------- | :------------------------------------------------------------ |
| `/export [data_type] [(opt) limit]` | Exports your audit log to the desired data type (JSON or CSV) |
| `/help`                             | Returns all commands of the bot                               |
| `/invite`                           | Sends the invite link configured in the .env                  |

## 👀 Any questions or problems?

Feel free to open an issue or even contribute by fixing a problem.

I'm also available via mail: [contact@witzdam.com](mailto:contact@witzdam.com)
