import requests
import json

HUBSPOT_API_KEY = "your-key"
HEADERS = {"Authorization": f"Bearer {HUBSPOT_API_KEY}", "Content-Type": "application/json"}

def publish_blog(title, body, meta_description):
    payload = {
        "name": title,
        "html_title": title,
        "body": body,
        "meta_description": meta_description,
        "publish_date": "now",
        "state": "PUBLISHED"
    }
    r = requests.post("https://api.hubapi.com/content/api/v4/pages/blog-posts", headers=HEADERS, json=payload)
    return r.json()

# Usage: parse markdown blog output → extract title/body/meta → call function
