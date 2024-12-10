import sys
import csv
import os
from optparse import OptionParser
import requests
from requests.auth import HTTPBasicAuth
import json
parser = OptionParser()
parser.add_option("--username", dest="username", help="API username")
parser.add_option("--password", dest="password", help="API password")
parser.add_option("--url", dest="weburl", help="Endpoint hostname")
parser.add_option("--input-file", dest="INPUT_FILE", help="CSV values of emailAddress name displayName")
parser.add_option("--csv-delimiter", dest="dlimit", help="CSV seperator used")
(options, args) = parser.parse_args()

if not options.INPUT_FILE:
        parser.error("INPUT_FILE must be specified")
if not options.username or not options.weburl or not options.password or not options.dlimit :
        parser.error("--username <username> --password <password> --url <endpoint uri> --input-file <input csv file with header emailAddress name displayName> --csv-delimiter <; or ,>")

url = "https://"+options.weburl+"/jira/rest/api/2/user"
auth = HTTPBasicAuth(options.username, options.password)
headers = {"Accept": "application/json", "Content-Type": "application/json"}
with open(options.INPUT_FILE) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=options.dlimit)
    for row in reader:
        emailAddress = row['emailAddress']
        displayName = row['displayName']
        name = row['name']
        password = row['password']
        payload = json.dumps( {"emailAddress": emailAddress, "displayName": displayName, "name": name, "password": password } )
        response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))