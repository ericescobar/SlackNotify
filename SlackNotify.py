import requests
import socket
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read('config.txt')  # Ensure this path is correct
description = config['DEFAULT']['Description']
webhook_url = config['DEFAULT'].get('Slack_Webhook_URL')

if not webhook_url:
    raise ValueError("Slack Webhook URL not provided in configuration. Please include it in config.txt.")

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except requests.RequestException:
        print("Failed to obtain public IP.")
        exit(1)  # Exit with an error code to let systemd handle the retry.

def get_local_ips():
    local_ips = {}
    for interface in os.listdir('/sys/class/net/'):
        if interface == 'lo':
            continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                if ip:
                    local_ips[interface] = ip
        except Exception:
            continue
    return local_ips

def send_slack_notification(public_ip, local_ips):
    message = f"{description}\nPublic IP: {public_ip}\nLocal IPs: {local_ips}"
    try:
        response = requests.post(webhook_url, json={'text': message})
        if response.status_code != 200:
            print(f"Failed to send Slack notification: {response.text}")
            exit(1)  # Exit with an error code to let systemd handle the retry.
    except requests.RequestException as e:
        print(f"Error: {e}")
        exit(1)  # Exit with an error code to let systemd handle the retry.

if __name__ == "__main__":
    public_ip = get_public_ip()
    local_ips = get_local_ips()
    send_slack_notification(public_ip, local_ips)
