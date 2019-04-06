import http.client
import json
import requests

headers = {
    'cache-control': "no-cache",
}

def query_request(url, suburl, requestType="GET", raw_return=False):
    conn = http.client.HTTPSConnection(url)
    conn.request(requestType, suburl,headers=headers)
    if raw_return:
        return conn.getresponse().read().decode("utf-8")
    else:
        json_response = json.loads(conn.getresponse().read().decode("utf-8"))
        return json_response

def payload_request(url, payload):
    conn = http.client.HTTPSConnection("")
    return requests.get(url, params=payload).json()
