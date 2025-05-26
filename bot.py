import os
import json
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from data_load import data
import random

# Dictionary to track last message IDs per thread
last_message_ids = {}

def filter_messages(username: str, password: str, session_file: str = 'session.json'):
    cl = Client()

    if os.path.exists(session_file) and os.path.getsize(session_file) > 0:
        try:
            cl.load_settings(session_file)
        except json.JSONDecodeError:
            print("Invalid session file. Will re-login.")
    else:
        print("No valid session file. Will re-login.")

    try:
        cl.login(username, password)
        cl.dump_settings(session_file)
    except LoginRequired:
        cl.login(username, password)
        cl.dump_settings(session_file)

    threads = cl.direct_threads(amount=5)

    for thread in threads:
        thread_id = thread.id
        last_seen_msg_id = last_message_ids.get(thread_id)

        new_messages = []
        for msg in thread.messages:
            if last_seen_msg_id is None or msg.id > last_seen_msg_id:
                new_messages.append(msg)

        new_messages.sort(key=lambda m: m.timestamp)

        for msg in new_messages:
            if msg.text and f"@{username}" in msg.text:
                # Extract text after the mention
                mention_index = msg.text.find(f"@{username}")
                command_text = msg.text[mention_index + len(f"@{username}"):].strip()

                print("NEW mention found:", msg.text)
                print("Command extracted:", command_text)

                respond_message(cl, thread_id, command_text)  # Pass extracted command

        if thread.messages:
            last_message_ids[thread_id] = thread.messages[0].id




def respond_message(cl: Client, thread_id: str, command_text: str):
    founded_data = [row for row in data if row['poet'].lower() == command_text.lower()]

    if founded_data:
        selected_row = random.choice(founded_data)
        message = f"{selected_row['misra1']} {selected_row['misra2']}"
        cl.direct_send(message, thread_ids=[thread_id])
    else:
        cl.direct_send("No poetry found for this poet.", thread_ids=[thread_id])