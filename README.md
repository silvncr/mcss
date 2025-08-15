# Minecraft Server Status Discord Bot

A Python-based Discord bot that monitors a Minecraft Java server in real time and posts live status updates in a Discord channel. The bot shows whether the server is online or offline, displays the number of players online, lists their usernames, and attaches the server's icon.

## Features

- **Real-time status updates**: Checks server status every 30 seconds.
- **Online/Offline/Empty detection**: Shows different embed colors and messages based on server state.
- **Player list display**: Lists the names of online players (if available).
- **Server icon support**: Displays the Minecraft server's icon in the embed. Place your `server-icon.png` in root directory where `Minecraft_Server_Status_Discord_Bot.py` is located.
- **Efficient updates**: Only sends updates when something changes (status, player count, player list, or icon).

## How It Works

1. The bot connects to your specified Discord channel.
2. It posts an embed message with the current Minecraft server status.
3. Every 30 seconds, it pings the server:
   - If the server is offline → Red embed with "Server is Offline".
   - If the server is online with no players → Purple embed with "Server is Online".
   - If the server is online with players → Green embed listing the players.
4. Updates the embed only if something changes.
5. Uses the server icon.

## Requirements

- Python 3.8+
- [discord.py](https://pypi.org/project/discord.py/) (latest stable)
- [mcstatus](https://pypi.org/project/mcstatus/)
- A running Minecraft Java server
- Discord bot token

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/minecraft-server-status-bot.git
   cd minecraft-server-status-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the following files in the same directory:**
   - `TOKEN` → Your Discord bot token.
   - `MC_SERVER_IP` → Your Minecraft server IP (e.g., play.example.com:25565).
   - `CHANNEL_ID` → Discord channel ID where status should be posted.
   - `MESSAGE_ID` → Leave empty or `0` for first run (will be auto-filled).

4. **Optional:** Place your Minecraft server icon as `server-icon.png` in the bot's directory.

## Running the Bot

```bash
python Minecraft\ Server\ Status\ Discord\ Bot.py
```

The bot will create or update a status message in the given Discord channel.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Created by:** Ayan Khan  
**Version:** 15.08.2025-1  
**Email:** ayankhantnp786@gmail.com
