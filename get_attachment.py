import requests
import json
import configparser
import urllib3
import os


def req_get(url, auth, headers):
    response_get = requests.get(url=url, auth=auth, verify=False)
    return response_get

# Подавление ошибки проверки SSL-сертификатов
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


config = configparser.ConfigParser()
config.read('config_get.ini')

jira_user = config['auth']['user']
jira_pass = config['auth']['password']
base_url  = config['url']['url']
project   = config['project']['name']

auth = (jira_user, jira_pass)

headers = {
    "Content-Type": "application/json"
}

startAt = 0
total   = 0

while True:
    get_issues = '/rest/api/2/search?jql=project=' + \
        project + '&fields=*all&maxResults=1000&startAt=' + str(startAt)
    
    rest_req = base_url + get_issues

    response_get = req_get(url=rest_req, auth=auth, headers=headers)

    if response_get.status_code == 200:
        dict_resp = json.loads(response_get.text)
        total     = dict_resp['total']

        with open('json.json', 'w', encoding='UTF-8') as json_file:
            json_file.write(response_get.text)

        for issue in dict_resp['issues']:
            issue_key = issue['key']
            print(issue_key)
            issue_attachs = issue['fields']['attachment']
            if issue_attachs != []:
                if not os.path.isdir(project):
                    os.mkdir(project)
                for issue_attach in issue_attachs:
                    issue_attach_filename = issue_attach['filename']
                    issue_attach_link     = issue_attach['content']
                    issue_key_dir         = project + '/' + issue_key
                    if not os.path.isdir(issue_key_dir):
                        os.mkdir(issue_key_dir)
                    xyz = req_get(issue_attach_link, auth=auth, headers=headers)
                    if xyz.status_code == 200:
                        issue_attach_file_body = xyz.content
                        issue_attach_full_path = './' + issue_key_dir + '/' + issue_attach_filename
                        if not os.path.isfile(issue_attach_full_path):
                            with open(issue_attach_full_path, 'wb') as file_body:
                                file_body.write(issue_attach_file_body)
                                file_body.close()
    else:
        print(response_get.status_code)

    if total - startAt > 1000:
        startAt += 1000
    else:
        break