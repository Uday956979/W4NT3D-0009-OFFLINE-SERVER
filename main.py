import os
import time
import json
from instagrapi import Client

USERNAME = "WANTED"              # тЖР рдЕрдкрдирд╛ username
PASSWORD = "1234"             # тЖР рдЕрдкрдирд╛ password
GROUP_NAME = "JUST CHILL ЁЯШО"     # тЖР рдЕрдкрдирд╛ group title
REPLY_TEXT = "ЁЯдЦ Auto reply from bot!"

SESSION_FILE = "session.json"
cl = Client()

def login():
    if os.path.exists(SESSION_FILE):
        print("ЁЯФД Loading session...")
        try:
            with open(SESSION_FILE, "r") as f:
                settings = json.load(f)
                cl.set_settings(settings)
            cl.login(WANTED, 1234)
        except Exception as e:
            print("тЪая╕П Session failed, logging fresh:", e)
            cl.login(WANTED, 1234)
            with open(SESSION_FILE, "w") as f:
                json.dump(cl.get_settings(), f)
    else:
        print("ЁЯФР Logging in fresh...")
        cl.login(WANTED, 1234)
        with open(SESSION_FILE, "w") as f:
            json.dump(cl.get_settings(), f)
        print("тЬЕ Session saved!")

def get_group_thread_id(group_name):
    try:
        result = cl.private_request("direct_v2/inbox/", {})
        for thread in result.get("inbox", {}).get("threads", []):
            title = thread.get("thread_title", "")
            if title == group_name:
                return thread.get("thread_id")
    except Exception as e:
        print("тЭМ Error getting thread:", e)
    return None

def welcome_new_members(thread_id, seen_users):
    try:
        thread = cl.direct_thread(thread_id)
        for user in thread.users:
            if user.pk not in seen_users and user.username != WANTED:
                cl.direct_send(f"ЁЯСЛ Welcome @{user.username}!", thread_ids=[thread_id])
                seen_users.add(user.pk)
                print(f"тЬЕ Welcomed @{user.WANTED}")
    except Exception as e:
        print("тЪая╕П Welcome error:", e)

def reply_to_messages(thread_id, seen_msgs):
    try:
        thread = cl.direct_thread(thread_id)
        for item in thread.messages:
            if item.id not in seen_msgs and item.user.username != WANTED:
                cl.direct_send(REPLY_TEXT, thread_ids=[thread_id])
                print(f"ЁЯТм Replied to @{item.user.WANTED}")
                seen_msgs.add(item.id)
    except Exception as e:
        print("тЪая╕П Reply error:", e)

if __name__ == "__main__":
    login()
    thread_id = get_group_thread_id(GROUP_NAME)
    if not thread_id:
        print("тЭМ Group not found. Check GROUP_NAME")
        exit()

    print(f"ЁЯдЦ Bot started in group: {GROUP_NAME}")
    seen_users = set()
    seen_msgs = set()

    while True:
        try:
            welcome_new_members(thread_id, seen_users)
            reply_to_messages(thread_id, seen_msgs)
            time.sleep(15)
        except Exception as e:
            print("тЭМ Main error:", e)
            time.sleep(30)
            
