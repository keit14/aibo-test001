# file name is "execute_action_api.py"
import json
import sys
import time
import urllib.request

headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExMSJ9.eyJzdWIiOiIwYjQ2Zjg0OC1lNmQ0LTQ2NjQtOGI5Yy0zODZiMzAyMzRkOWEiLCJleHAiOjE2ODA1MTIwMjksImlzcyI6Imh0dHBzOi8vcHVibGljLmFwaS5haWJvLmNvbSIsImF1ZCI6IjQ1LjU0NzA2MTA2NzUyMDgxOTIiLCJqdGkiOiI3YTY3N2U1OC04ZTQxLTQyMGMtYTcxMC04ZjRlODEzOTQzMDciLCJpYXQiOjE2ODA0MjU2Mjl9.biwkDdDT8gQxyrznmnf1fZm3JEJvwyLHXHb9MrcuxgqzNS2th33vbR-ukctMfzShxTMhS9FHPX2RVqj0E-cLL--IuRY4uD3wVnWKxM27vo6vSg0ftffMndW_rw_M2InvI-vYV0ssRB7RWGk2yoyusQEkJ6DiDE3xWGtoi_fDv8DhoKrBJWf4xD2FhOJ3n2NUZzMC1aJdnMnTiJab4GM-r1264YpvHnqpKlfq0GHPsadHRgdFtkDgzFGaGt8LO9O65whamSpJlDZ-dN-EOk9XrdbMOrdSvNIxbU7cqvPjK9wlxgfdVXPukxZmwN4JSU4aMmMz84IPChKA3_-_bg6eIA',
}

BASE_PATH = 'https://public.api.aibo.com/v1'
DEVICE_ID = "6d5d1ea7-7e41-4d35-a3a5-a309310bad81"
TIME_OUT_LIMIT = 10

def do_action(api_name, arguments):
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/' + api_name + '/execute'
    data = '{"arguments":' + arguments + '}'

    # POST API
    req = urllib.request.Request(post_url, data.encode(), headers=headers, method='POST')
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
    executionId = post_result["executionId"]

    # Get Result of API execution
    get_result_url = BASE_PATH + '/executions/' + executionId
    TimeOut = 0
    while True:
        req = urllib.request.Request(get_result_url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as res:
            response = res.read()
        get_result = json.loads(response)
        get_status = get_result["status"]

        if get_status == "SUCCEEDED":
            print(get_result)
            break
        elif get_status == "FAILED":
            print(get_result)
            break

        TimeOut += 1
        if TimeOut > TIME_OUT_LIMIT:
            print("Time out")
            break

        time.sleep(1)

if __name__ == '__main__':
    length = len(sys.argv)
    if length == 3:
        do_action(sys.argv[1], sys.argv[2])
    else :
        print("execute_action_api.py <action api name> <parameters>")
        exit(1)

do_action('play_motion','{"Category":"highFive","Mode":"NONE"}');
do_action('play_motion','{"Category":"belch","Mode":"NONE"}');