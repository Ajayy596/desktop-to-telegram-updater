import sys
import os
import getpass
import asyncio

# --- ENFORCE PYTHON 3.14 GLOBAL PATHS ---
user_name = getpass.getuser()
global_packages = rf"C:\Users\{user_name}\AppData\Local\Programs\Python\Python314\Lib\site-packages"
if global_packages not in sys.path:
    sys.path.insert(0, global_packages)

try:
    asyncio.get_event_loop()
except RuntimeError:
    mock_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(mock_loop)

try:
    import pyrotgcrypto as tgcrypto
    sys.modules['tgcrypto'] = tgcrypto
    crypto_status = "[✓] High-speed cryptographic engine successfully initialized."
except ImportError:
    crypto_status = "[!] Native crypto accelerator missing. Running in standard compliance mode."

import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyrogram import Client
from pyrogram.errors import FloodWait

# =========================================================================
# ⚙️ SYSTEM CONFIGURATION (Replace placeholders below with your credentials)
# =========================================================================
API_ID = 12345678                          # YOUR NUMERICAL API_ID HERE (As an integer)
API_HASH = "YOUR_API_HASH_HERE"            # YOUR 32-CHARACTER API_HASH HERE (As a string)
WATCH_FOLDER = r"C:\Path\To\Your\Folder"   # The local folder path you want to watch
CHAT_TARGET = "me"                         # "me" for Saved Messages, or a custom group ID
LOG_FILE = "uploaded_files.txt"
REPORT_FILE = "backup_report.md"
# =========================================================================

app = Client("windows_backup_session", api_id=API_ID, api_hash=API_HASH)

def load_uploaded_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def log_uploaded_file(file_id_string):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(file_id_string + "\n")

def generate_markdown_report(status, summary, items):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📊 Telegram Auto-Backup Session Report\n\n")
        f.write(f"- **Timestamp:** {timestamp}\n")
        f.write(f"- **Status:** {status}\n")
        f.write(f"- **Summary:** {summary}\n\n")
        f.write(f"## 📝 Processed Files Log\n\n")
        f.write(f"| File Name | Status | Details |\n")
        f.write(f"| :--- | :--- | :--- |\n")
        for item in items:
            f.write(f"| {item['name']} | {item['status']} | {item['detail']} |\n")

uploaded_history = load_uploaded_log()
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mkv', '.mov', '.avi', '.pdf', '.docx', '.xlsx', '.zip')
last_logged_percent = {}

def upload_progress(current, total, file_name):
    global last_logged_percent
    if total <= 0:
        return
    percent = (current / total) * 100
    milestone = int(percent // 25) * 25
    
    if file_name not in last_logged_percent:
        last_logged_percent[file_name] = -1
        
    if milestone > last_logged_percent[file_name] and milestone <= 100:
        last_logged_percent[file_name] = milestone
        mb_sent = current / (1024 * 1024)
        mb_total = total / (1024 * 1024)
        print(f"    -> Progress for {file_name}: {milestone}% uploaded ({mb_sent:.1f}MB / {mb_total:.1f}MB)", flush=True)

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop
        super().__init__()

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        
        if file_name.lower().endswith(VALID_EXTENSIONS):
            try:
                file_size = os.path.getsize(file_path)
                file_signature = f"{file_name}|{file_size}"
                
                if file_signature not in uploaded_history:
                    time.sleep(3) 
                    app.loop.call_soon_threadsafe(
                        lambda: asyncio.create_task(self.async_upload(file_path, file_name, file_signature))
                    )
            except Exception:
                pass

    async def async_upload(self, file_path, file_name, file_signature):
        retries = 3
        while retries > 0:
            try:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    async with asyncio.timeout(300):
                        await app.send_document(
                            chat_id=CHAT_TARGET, 
                            document=file_path, 
                            caption=f"🚀 Auto-backed up: {file_name}",
                            progress=upload_progress,
                            progress_args=(file_name,)
                        )
                    uploaded_history.add(file_signature)
                    log_uploaded_file(file_signature)
                    print(f"[✓] Successfully uploaded live file: {file_name}\n", flush=True)
                    return
            except FloodWait as e:
                print(f"[!] Throttled by Telegram. Waiting {e.value} seconds...", flush=True)
                await asyncio.sleep(e.value)
            except Exception as e:
                retries -= 1
                print(f"[X] Upload failed for {file_name}. Retries remaining: {retries}. Error: {e}", flush=True)
                await asyncio.sleep(5)

async def scan_existing_files():
    print(f"[*] Scanning folder for existing files...", flush=True)
    if not os.path.exists(WATCH_FOLDER):
        print(f"[X] Error: Target WATCH_FOLDER can't be reached on this device architecture.", flush=True)
        return

    all_files = [f for f in os.listdir(WATCH_FOLDER) if f.lower().endswith(VALID_EXTENSIONS)]
    files_to_upload = []
    for f in all_files:
        path = os.path.join(WATCH_FOLDER, f)
        try:
            sig = f"{f}|{os.path.getsize(path)}"
            if sig not in uploaded_history:
                files_to_upload.append((f, path, sig))
        except Exception:
            continue
            
    total = len(files_to_upload)
    if total == 0:
        print("[✓] All existing folder items are already backed up!", flush=True)
        return

    try:
        await app.send_message(CHAT_TARGET, f"📦 **Backup Scan Complete**\nFound `{total}` historical items requiring upload. Starting bulk process...")
    except Exception:
        pass
    
    print(f"[!] Found {total} items requiring backup. Starting bulk sequential upload...", flush=True)
    session_items = []
    success_count = 0
    
    for idx, (file_name, file_path, file_signature) in enumerate(files_to_upload, 1):
        print(f"\n[*] Processing item {idx}/{total}: {file_name}", flush=True)
        retries = 3
        uploaded = False
        error_msg = "Unknown error"
        
        while retries > 0:
            try:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    async with asyncio.timeout(300):
                        await app.send_document(
                            chat_id=CHAT_TARGET, 
                            document=file_path, 
                            caption=f"𗟴 Historical Backup: {file_name}",
                            progress=upload_progress,
                            progress_args=(file_name,)
                        )
                    uploaded_history.add(file_signature)
                    log_uploaded_file(file_signature)
                    success_count += 1
                    uploaded = True
                    break
            except FloodWait as e:
                print(f"[!] Throttled. Waiting {e.value} seconds...", flush=True)
                await asyncio.sleep(e.value)
            except Exception as e:
                retries -= 1
                error_msg = str(e)
                await asyncio.sleep(3)
        
        if uploaded:
            session_items.append({"name": file_name, "status": "🟢 SUCCESS", "detail": "Uploaded perfectly."})
            print(f"[✓] Completed item {idx}/{total}: {file_name}", flush=True)
        else:
            session_items.append({"name": file_name, "status": "🔴 FAILED", "detail": error_msg})
            print(f"[X] Skipped item {idx}/{total} after exhaustive failure strategy.", flush=True)
            
        await asyncio.sleep(1.0)
            
    summary_text = f"Uploaded {success_count} out of {total} files successfully."
    generate_markdown_report("COMPLETED", summary_text, session_items)
    try:
        await app.send_message(CHAT_TARGET, f"✅ **Bulk Backup Completed**\n{summary_text}\nA session tracking report has been saved locally as `{REPORT_FILE}`.")
    except Exception:
        pass
    print(f"\n[✓] Existing history backup complete!", flush=True)

async def main():
    print(f"[*] Connecting to Telegram...", flush=True)
    print(f"[*] {crypto_status}", flush=True)
    await app.start()
    
    try:
        await app.send_message(CHAT_TARGET, "🖥️ **Windows Backup System Online**\nMonitoring service initiated successfully.")
    except Exception:
        pass
    
    await scan_existing_files()
    
    print(f"[*] Transitioning to live folder watcher on: {WATCH_FOLDER}", flush=True)
    print("[*] Press Ctrl+C to stop safely.", flush=True)
    
    event_handler = NewFileHandler(app.loop)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        print("\n[*] Stopping observer and disconnecting session...", flush=True)
        observer.stop()
        observer.join()
        await app.stop()


if __name__ == "__main__":
    try:
        app.loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass

