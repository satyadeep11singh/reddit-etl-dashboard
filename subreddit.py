import requests
import json

url = "https://www.reddit.com/subreddits/popular.json?limit=100"
headers = {'User-agent': 'python-script'}

response = requests.get(url, headers=headers)
data = response.json()

subreddits = []
for sub in data['data']['children']:
    name = sub['data']['display_name_prefixed']
    subs = sub['data']['subscribers']
    title = sub['data']['title']
    subreddits.append({
        'name': name,
        'subscribers': subs,
        'title': title
    })
    print(f"{name}: {subs:,}")

# Save to JSON file for frontend to use
with open('subreddits.json', 'w') as f:
    json.dump(subreddits, f)