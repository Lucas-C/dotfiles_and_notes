#!/usr/bin/env python
import json, os, requests, sys

# USAGE:
#   export $(xargs < .httpsms_env)
#   cat msg.txt | ./send_text_msg_with_httpsms.py $tel_num1 [$tel_num2]

API_ENDPOINT = "https://api.httpsms.com/v1"
FREE_MSGS = 200

def main():
    api_key, from_number = os.environ['HTTPSMS_API_KEY'], os.environ['HTTPSMS_FROM']
    get_usage(api_key)
    print()
    # get_user_and_phones(api_key)
    if len(sys.argv) < 2:
        raise ValueError('Missing destination number arg')
    if any(not num.startswith('+') for num in sys.argv[1:]):
        raise ValueError('Phone numbers must start with a +')
    message = sys.stdin.read()
    for dest_number in sys.argv[1:]:
        send_message(api_key, from_number, dest_number, message)
        # get_messages(api_key, from_number, dest_number)

def send_message(api_key, from_number, dest_number, message):
    resp = requests.post(f"{API_ENDPOINT}/messages/send",
                         headers={"x-api-Key": api_key},
                         json={
                            "from": from_number,
                            "to": dest_number,
                            "content": message,
                         })
    status = resp.json()["data"]
    print(json.dumps(status, indent=2))
    resp.raise_for_status()

def get_usage(api_key):
    resp = requests.get(f"{API_ENDPOINT}/billing/usage",
                         headers={"x-api-Key": api_key})
    usage = resp.json()["data"]
    messages = usage["sent_messages"] + usage["received_messages"]
    print(f"Current free tier usage: {messages*100/FREE_MSGS:.0f}% ({messages}/{FREE_MSGS})")
    resp.raise_for_status()

def get_user_and_phones(api_key):
    resp = requests.get(f"{API_ENDPOINT}/users/me",
                         headers={"x-api-Key": api_key})
    user = resp.json()["data"]
    print(json.dumps(user, indent=2))
    resp = requests.get(f"{API_ENDPOINT}/phones",
                         headers={"x-api-Key": api_key})
    phones = resp.json()["data"]
    print(json.dumps(phones, indent=2))

def get_messages(api_key, from_number, dest_number):
    resp = requests.get(f"{API_ENDPOINT}/messages",
                         headers={"x-api-Key": api_key},
                         params={
                            "owner": from_number,
                            "contact": dest_number,
                         })
    msgs = resp.json()["data"]
    print("Messages successfully sent to:", dest_number)
    for msg in reversed(msgs):
        if msg["sent_at"]:
            print(msg["sent_at"], ":", msg["content"])

if __name__ == '__main__':
    main()
