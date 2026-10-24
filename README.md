# 🚀 Desktop to Telegram Auto-Updater & Folder Backup

An optimized, asynchronous background folder backup service built specifically for Windows architectures. This tool monitors any designated local folder (e.g., photo pools, device camera back-ups, or storage dumps) and streams modifications natively to your designated personal Telegram vault (`Saved Messages` or a target group) with zero taskbar window clutter.

---

## ✨ Features

- **Asynchronous Data Pipelines:** Built natively over true Python `asyncio` loop frameworks to prevent thread block stalls.
- **High-Speed Crypto Acceleration:** Pre-configured to utilize compiled native `PyroTgCrypto` engines for up to 10x faster local file encryption over standard pure-Python execution blocks.
- **Smart Duplication Guard:** Tracks unique file name and file size structural keys inside a local runtime log (`uploaded_files.txt`) to bypass previously uploaded assets instantly upon restart.
- **Fail-Safe Auto Recovery:** Dynamically intercepts Telegram API `FloodWait` throttling limits, automatically pausing and safely resuming sequences when tracking large batch loads.
- **Session Reporting:** Automatically outputs structured logs to a Markdown document (`backup_report.md`) detailing success/failure rates after bulk history processing.
- **Completely Invisible Background Operation:** Hidden execution wrapper scripts ensure it operates silently on Windows startup without leaving command prompts open on your taskbar.

---

## 🛠️ Prerequisite Configuration

Before initiating setup, you must obtain client connectivity endpoints directly from the Telegram gateway infrastructure.

### 1. Generating API Credentials
1. Navigate to the official portal: [https://telegram.org](https://telegram.org)
2. Enter your account number in complete international format (e.g., `+91XXXXXXXXXX`) and authenticate using the validation pin sent to your Telegram application client.
3. Click on **API development tools**.
4. Enter an application title and short identifier name of your choice, then select **Create application**.
5. Copy your unique numerical integer (**App api_id**) and string identifier (**App api_hash**). Keep these completely private!

### 2. Finding a Target Chat ID (Optional)
By default, the script forwards data straight into your personal **Saved Messages** conversation space (referenced internally as `"me"`). If routing files to a separate channel or private storage vault:
1. Invite [IDBot (@username_to_id_bot)](https://t.me) into your chat workspace.
2. Direct-message or forward a piece of text out of your target vault to the bot.
3. It will return a numerical tracking signature (e.g., `-100XXXXXXXXXX`). Copy this value to use as your alternative chat container destination.

---

## 🚀 Execution & Setup Deployment Guide

### Step 1: Environment Packages Installation
Open your Windows **Command Prompt** (cmd) as an administrator and run the following deployment strings:

```cmd
py -3.14 -m pip install --upgrade pip
py -3.14 -m pip install watchdog pyrogram
py -3.14 -m pip install PyroTgCrypto
```

### Step 2: Configure Local Script Overrides
1. Open the file `TelegramBackup.py` using your preferred local text configuration utility (such as Python IDLE, Notepad++, or VS Code).
2. Modify the **`SYSTEM CONFIGURATION`** variables to match your personal ecosystem keys:
   ```python
   API_ID = 12345678                          # Input your numerical api_id integer
   API_HASH = "YOUR_API_HASH_HERE"            # Input your 32-character api_hash string
   WATCH_FOLDER = r"C:\Path\To\Your\Folder"   # Target Windows local file tracking folder path
   CHAT_TARGET = "me"                         # "me" for Saved Messages or target numerical chat ID
   ```
3. Save your file changes.

### Step 3: Run the Initialization Lifecycle
1. Open your configured script file within **Python IDLE** and press **F5**.
2. **First-Run Verification:** Because it uses an underlying user account framework, the shell profile will explicitly prompt you to write out your verified account **Phone number** and **Confirmation login token** inside the console window.
3. Once completed, Pyrogram compiles a local authorization lock database (`windows_backup_session.session`). **You do not need to do this step again!**

---

## 🥷 Running Invisibly in the Background on Windows Startup

To make the process run silently behind your standard system apps without keeping a terminal tracking page visible on your screen layout:

1. Inside your active workspace folder (e.g., `C:\Script\Backup_python\`), create a text file named **`run_backup.bat`** containing:
   ```batch
   @echo off
   py -3.14 "C:\Script\Backup_python\TelegramBackup.py"
   ```
2. Create an additional accompanying text file named **`launch_invisible.vbs`** containing:
   ```vbs
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run chr(34) & "C:\Script\Backup_python\run_backup.bat" & chr(34), 0, False
   ```
3. Trigger the Windows Run prompt utility by pressing **Windows Key + R**, write out **`shell:startup`**, and hit **Enter**.
4. Right-click your local `launch_invisible.vbs` file, select **Copy**, then go straight to the newly opened Windows Startup directory window, right-click inside the workspace, and select **Paste shortcut**.

The updater engine will now quietly initiate in the background the moment your machine cycles on!

---

## 📋 File Compatibility Rules

- **Standard Assets Support:** Supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.mp4`, `.mkv`, `.mov`, `.avi`, `.pdf`, `.docx`, `.xlsx`, and `.zip` extensions naturally out of the box.
- **Uncompressed Pipeline Storage:** Files are passed natively using streaming structural endpoints, ensuring Telegram preserves the raw capture quality of your items without server compression.
- **File System Limits:** Standard user configurations restrict total standalone items to a maximum cap of **2 GB per file**. Items surpassing this threshold will write a warning line inside your diagnostic outputs.

---

## 📄 License
Distributed under open-source project standards. Feel free to copy, fork, and adapt to custom deployment environments!
