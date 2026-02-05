<!-- omit in toc -->
# Minecraft Server Status -- Discord Bot

A Python-based Discord bot that monitors a Minecraft Java server in real time and posts live status updates to a Discord channel. The bot shows whether the server is online or offline, displays the number of players online, and lists their usernames.

> [!NOTE]
> This project is forked from: <https://github.com/ayankhanakaak/Minecraft-Server-Status-Discord-Bot>
>
> I've made many improvements over that version, such as optional settings, slash commands, and migrating to `nextcord` over `discord.py`.
>
> See [License](#license).

<!-- omit in toc -->
## Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the bot](#running-the-bot)
- [Screenshots](#screenshots)
- [License](#license)


## Features

- [x] :alarm_clock: **Real-time status updates**: Checks server status every 30 seconds.
- [x] :green_circle: **Online/Offline/Empty detection**: Shows different embed colors and messages based on server state.
- [x] :memo: **Player list display**: Lists the names of online players, if available.
- [x] :framed_picture: **Server icon support**: Optionally displays the Minecraft server's icon (or any image) in the embed.
- [x] :hourglass_flowing_sand: **Efficient updates**: Two modes for updating the status message:
   - Only update when something changes (status, player count, player list, or icon).
   - Post an update whenever possible.
- [x] :round_pushpin: **"Last edited" timestamp**: Option to include a timestamp with every update. Crucial if your bot has downtime (eg, it runs on your local computer, which you shut off every night), because it allows everyone to see exactly when the bot's inactive.

## How it works

1. The bot connects to your specified Discord channel.
2. It posts an embed message with the current Minecraft server status.
3. Every 30 seconds, it pings the server:
   - If the server is offline: Red embed with "Offline".
   - If the server is online with no players: Purple embed with "Online".
   - If the server is online with players: Green embed with "Online" -- lists the players if possible.

   Also changes the bot's status message and online status.

## Requirements

- Python 3.12+
- Minecraft server IP and port
- Discord bot token
- Discord channel ID
- Message ID (optional -- for editing the same message, otherwise the bot will create a new message on each run)
- Server icon file (optional -- for adding a thumbnail image to the embed)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/silvncr/mcss.git
   cd mcss
   ```

2. Install dependencies:

   Create `venv`, if necessary.

   ```sh
   python -m venv .venv
   ```

   (Ensure `venv` is active, if created.)

   
   ```sh
   pip install -r requirements.txt
   ```

3. If you want to use an icon, place it in the folder (with `bot.py`):

   Example:

   ```sh
   cp ~/Pictures/server-icon.png ./server-icon.png
   ```

4. Create a `.env` file with the following structure:

   ```env
   TOKEN=
   SERVER_IP=
   SERVER_NAME=
   SERVER_ICON_FILE=
   CHANNEL_ID=
   MESSAGE_ID=
   MODE_ALWAYS_UPDATE=
   MODE_INCLUDE_CHANGE_TIMESTAMP=
   MODE_INCLUDE_MESSAGE_TIMESTAMP=
   TIMEZONE_OFFSET_HOURS=
   TIMEZONE_OFFSET_MINUTES=
   ```

   - `TOKEN` (str): Discord bot token.

   - `SERVER_IP` (str): Minecraft server IP  with port in `ip:port` format. Can include text or numbers.

     Examples:
     - `play.example.com:1234`
     - `192.52.0.0:25565`

   - `SERVER_NAME` (str): Minecraft server name -- doesn't have to match, it can be anything. It only exists to be shown in the status message.
   - `SERVER_ICON_FILE` (str): Local path to your server icon. In the example from Step 3, this would be `SERVER_ICON_FILE=server-icon.png`.

   - `CHANNEL_ID` (int): Discord channel ID where status should be posted.
   - `MESSAGE_ID` (int): Discord message ID for the status message. Leave this empty on the first run. When the first message is posted, copy its ID and write it here to use the same message on future runs.

   - `MODE_ALWAYS_UPDATE` (str > bool): Whether to update the message every 30 seconds, or only when a change is detected. Does not affect logs. **Either `true` or empty.**

   - `MODE_INCLUDE_CHANGE_TIMESTAMP` (str > bool) and `MODE_INCLUDE_MESSAGE_TIMESTAMP` (str > bool): Whether to include a relative timestamp in the embed message -- each one serves a different purpose:
     - `CHANGE`: last time the server status changed.
     - `MESSAGE`: last time the status message was sent/edited.

     Does not affect logs. **Either `true` or empty.**

     > [!NOTE]
     > `CHANGE` timestamp will not appear until the bot runs long enough to actually see a change.

     > [!TIP]
     > If `MODE_ALWAYS_UPDATE` is false, `CHANGE` and `MESSAGE` will be the same timestamp, so don't use both. In this case, the wording of `CHANGE` is clearer, so use that.

   - `TIMEZONE_OFFSET_HOURS` (int) and `TIMEZONE_OFFSET_MINUTES` (int): Timezone to which timestamps should be converted. Doesn't affect the bot's messages, only logs. (Discord uses Unix timestamps which are timezone-independent.)

     Can be positive, negative, `0`, or empty (implicit `0`).

     Both numbers should be positive or negative, not mixed. Or one can be `0`. In `(HOURS, MINUTES)`:
     - `UTC+9:30` would be `(9, 30)`.
     - `UTC-1:15` would be `(-1, -15)`.

> [!NOTE]
> Logs are printed whenever the server is checked (I think), which is every 30 seconds. This should be regardless of your settings, and regardless of when updates are sent to Discord.

> [!NOTE]
> To other devs -- regarding images:
> 
> ```py
> # In discord.py (from upstream version):
> await msg.edit(embed=embed, attachments=[discord.File(...)])
>
> # In nextcord, either:
> await msg.edit(embed=embed, files=[nextcord.File(...)])
> await msg.edit(embed=embed, file=nextcord.File(...))
> ```
>
> See also: <https://github.com/nextcord/nextcord/issues/400>

## Running the bot

(Ensure `venv` is active, if created.)

```bash
python bot.py
```

The bot will create or update a status message in the given Discord channel, and continue to run indefinitely, updating every 30 seconds. Ctrl+C to terminate.

## Screenshots

> These screenshots are from before my fork, and not accurate to the updated version.

<table>
<tr>
<td>
<img width="458" height="197" alt="Screenshot 2025-08-15 174950" src="https://github.com/user-attachments/assets/8f10baff-7ddb-4193-a5a8-cf1b628d0453" />
</td>
</tr>
<tr>
<td>
<img width="458" height="254" alt="Screenshot 2025-08-15 175340" src="https://github.com/user-attachments/assets/5ee4534c-e3d5-473f-9536-7e1a29f48bb3" />
</td>
</tr>
<tr>
<td>
<img width="458" height="317" alt="Screenshot 2025-08-15 183136" src="https://github.com/user-attachments/assets/500638f4-06ec-48b3-b4d8-c113dedb799d" />
</td>
</tr>
</table>

## License

[GPL-3.0 License](LICENSE), complicit with the [upstream GPL-3.0 License](https://github.com/ayankhanakaak/Minecraft-Server-Status-Discord-Bot/blob/main/LICENSE).
