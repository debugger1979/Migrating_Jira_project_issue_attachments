import requests
import configparser
import urllib3
import os
import mimetypes

# Подавление ошибки проверки SSL-сертификатов
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Забираем параметры авторизации и базовый URL из файла конфигурации
config = configparser.ConfigParser()
config.read('config_put.ini')

jira_user = config['auth']['user']
jira_pass = config['auth']['password']
base_url  = config['url']['url']
project   = config['project']['name']

auth = (jira_user, jira_pass)

headers = {
    "X-Atlassian-Token": "nocheck",
    "Accept": "application/json"
}

path = project

for root, dirs, files in os.walk(path):
    for name in files:
        full_path = os.path.join(root, name)
        issue_name = root.split('\\')[1]
        attach_mimetype = mimetypes.guess_type(full_path)[0]
        if attach_mimetype == None:
            attach_mimetype = 'application/octet-stream'
        attach_name = os.path.basename(full_path)


        attach_files = {'files': (attach_name, open(full_path, 'rb'), attach_mimetype)}

        post_issue = '/rest/api/2/issue' + issue_name + '/attachments'
        rest_req = base_url + post_issue

        response_post = requests.post(url=rest_req, auth=auth, files=attach_files, headers=headers, verify=False)

        print(issue_name, full_path, response_post.status_code)
        print()
