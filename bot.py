from requests import post, get
from rich.console import Console
from rich.table import Table
from rich.live import Live
import requests, os, re, uuid
import time
import random
from colorist import Color
from rich.text import Text
from datetime import datetime
from flask import Flask
import threading

expiration_date = datetime(2028, 12, 31)

if datetime.now() > expiration_date:
    print("\033[1;32mTool Disabled by 777 \033[0m")
    exit()

uid = str(uuid.uuid4())
console = Console()

def header():
    os.system("cls" if os.name == "nt" else "clear")
    console.print("By @Sir.oskaar", style="bold blue", justify="left")

class TextColor:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

def Report_Instagram(target_id, sessionid, csrftoken, reportType):
    try:
        r3 = post(
            f"https://i.instagram.com/users/{target_id}/flag/",
            headers={
                "User-Agent": "Mozilla/5.0",
                "Host": "i.instagram.com",
                "cookie": f"sessionid={sessionid}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=f"source_name=&reason_id={reportType}&frx_context=",
            allow_redirects=False,
        )

        return r3.status_code
    except Exception as e:
        return str(e)

def Post_Report(sessionid, csrftoken, media_id, reason_id):
    try:
        report_url = f"https://i.instagram.com/media/{media_id}/flag/"
        report = post(
            report_url,
            headers={
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "cookie": f"sessionid={sessionid}",
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=f"reason_id={reason_id}&source_name=profile",
        )

        return report.status_code
    except Exception as e:
        return str(e)

def starter():
    console.print(Text("Welcome to the Team 777 System!", style="bold underline"))
    user = input("\033[1;32mEnter Your Username : \033[0m")
    if user == "":
        console.print("[!] You must write the username")
        exit()
    pess = input("\033[1;32mEnter Your Password : \033[0m")
    if pess == "":
        console.print("[!] You must write the password")
        exit()

    r1 = post(
        "https://i.instagram.com/api/v1/accounts/login/",
        headers={
            "User-Agent": "Instagram 114.0.0.38.120 Android",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "i.instagram.com",
        },
        data={
            "_uuid": uid,
            "password": pess,
            "username": user,
            "device_id": uid,
            "from_reg": "false",
            "_csrftoken": "missing",
            "login_attempt_count": "0",
        },
        allow_redirects=True,
    )

    if "logged_in_user" in r1.text:
        console.print("✅ Logged in [bold green]successfully[/bold green]")
        sessionid = r1.cookies["sessionid"]
        csrftoken = r1.cookies["csrftoken"]

        console.print("\nChoose Report Type:")
        console.print("1 - Report Account")
        console.print("2 - Report Post(s)")
        choice = input(f"{TextColor.OKGREEN}Enter your choice (1 or 2): {TextColor.ENDC}")

        if choice == "1":
            target_id = input(f"\033[1;36mTarget User ID: \033[0m")
            print(f"{TextColor.HEADER}Choose Report Reason:{TextColor.ENDC}")
            reasons = [
                "1 - Spam", "2 - Self-Injury", "3 - Drugs", "4 - Nudity",
                "5 - Violence", "6 - Hate Speech", "7 - Bullying",
                "8 - Impersonation", "9 - Underage"
            ]
            for reason in reasons:
                print(f"{TextColor.OKCYAN}{reason}{TextColor.ENDC}")
            reportType = int(input(f"{TextColor.OKGREEN}Choose: {TextColor.ENDC}"))

            counter = 0
            with Live(refresh_per_second=4) as live:
                while True:
                    counter += 1
                    delay = random.uniform(2.5, 6.5)
                    status = Report_Instagram(target_id, sessionid, csrftoken, reportType)

                    table = Table(title="📣 Instagram Report Bot", expand=True)
                    table.add_column("Target User ID", justify="center")
                    table.add_column("Reports Sent", justify="center")
                    table.add_column("Last Delay (sec)", justify="center")
                    table.add_column("Status", justify="center")

                    status_str = f"[green]{status}[/green]" if str(status) == "200" else f"[red]{status}[/red]"
                    table.add_row(target_id, str(counter), f"{delay:.2f}", status_str)
                    live.update(table)
                    time.sleep(delay)

        elif choice == "2":
            post_input = input(f"{TextColor.OKCYAN}Enter post link or shortcode: {TextColor.ENDC}").strip()
            match = re.search(r"instagram\.com/p/([a-zA-Z0-9_-]+)/", post_input)
            shortcode = match.group(1) if match else post_input

            url = f"https://i.instagram.com/api/v1/media/shortcode/{shortcode}/info/"
            headers = {
                "User-Agent": "Instagram 114.0.0.38.120 Android",
                "cookie": f"sessionid={sessionid}",
            }

            res = get(url, headers=headers)
            if res.status_code != 200:
                console.print(f"{TextColor.FAIL}Failed to get media ID. Check shortcode/link.{TextColor.ENDC}")
                exit()

            media_id = res.json()["items"][0]["id"]

            print(f"{TextColor.HEADER}Choose Report Reason:{TextColor.ENDC}")
            reasons = [
                "1 - Spam", "2 - Nudity", "3 - Violence", "4 - Hate Speech",
                "5 - Bullying", "6 - False Information"
            ]
            for reason in reasons:
                print(f"{TextColor.OKCYAN}{reason}{TextColor.ENDC}")
            reason_id = int(input(f"{TextColor.OKGREEN}Choose: {TextColor.ENDC}"))

            counter = 0
            with Live(refresh_per_second=4) as live:
                while True:
                    counter += 1
                    delay = random.uniform(2.5, 6.5)
                    status = Post_Report(sessionid, csrftoken, media_id, reason_id)

                    table = Table(title="📣 Instagram Post Reporter", expand=True)
                    table.add_column("Post", justify="center")
                    table.add_column("Reports Sent", justify="center")
                    table.add_column("Last Delay (sec)", justify="center")
                    table.add_column("Status", justify="center")

                    status_str = f"[green]{status}[/green]" if str(status) == "200" else f"[red]{status}[/red]"
                    table.add_row(shortcode, str(counter), f"{delay:.2f}", status_str)
                    live.update(table)
                    time.sleep(delay)

        else:
            console.print(f"{TextColor.FAIL}Invalid choice. Exiting...{TextColor.ENDC}")
            exit()
    else:
        console.print("- [bold red]Login Failed![/bold red]")
        exit()

# إنشاء تطبيق Flask للويب
app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Report Bot is Running!"

@app.route('/health')
def health():
    return 'OK', 200

def run_flask():
    """تشغيل خادم Flask في خيط منفصل"""
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

if __name__ == "__main__":
    # تشغيل خادم الويب في خيط منفصل
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # تشغيل الأداة الرئيسية
    header()
    starter()
