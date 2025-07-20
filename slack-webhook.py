import os
import psycopg2
import select
import requests
import json
import dotenv

dotenv.load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_to_slack(message):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, headers=headers, json={'text': message})
        if response.status_code != 200:
            print(f"Slack error: {response.status_code} - {response.text}")
        else:
            print("✅ Slack message sent")
    except Exception as e:
        print(f"Slack send error: {e}")

def format_slack_message(data):
    action = data.get("action")
    table = data.get("table")

    if action == "INSERT":
        return f"🟢 *INSERT* into `{table}`:\n```{json.dumps(data.get('new'), indent=2)}```"
    elif action == "UPDATE":
        old = json.dumps(data.get("old"), indent=2)
        new = json.dumps(data.get("new"), indent=2)
        return f"🟡 *UPDATE* on `{table}`:\n*Before:*\n```{old}```\n*After:*\n```{new}```"
    elif action == "DELETE":
        return f"🔴 *DELETE* from `{table}`:\n```{json.dumps(data.get('old'), indent=2)}```"
    else:
        return f"❓ Unknown action on `{table}`: {json.dumps(data)}"

# Connect to DB and listen
conn = psycopg2.connect("dbname=audit_demo user=admin password=adminpass host=localhost")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("LISTEN audit_channel;")
print("🔍 Listening for audit events...")

# Event loop
while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        notify = conn.notifies.pop(0)
        try:
            data = json.loads(notify.payload)
            msg = format_slack_message(data)
            send_to_slack(msg)
        except Exception as e:
            print(f"Error processing message: {e}")
