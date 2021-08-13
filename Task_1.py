import requests
import json
username = 'eroticstaff'
url = 'https://api.github.com/users/'
response = requests.get(f"{url}{username}/repos")
data = response.json()
repos_list = [{'repository_name': repo['name'],'repository_url': repo['html_url']} for repo in data]
json_data = json.dumps(repos_list)
with open('repos.json','w') as f:
    f.write(json_data)
print("FINISH")
