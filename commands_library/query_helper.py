import http.client
import json

headers = {
    'cache-control': "no-cache",
}

def query_request(url, suburl, requestType="GET"):
    conn = http.client.HTTPSConnection(url)
    conn.request(requestType, suburl,headers=headers)
    json_response = json.loads(conn.getresponse().read().decode("utf-8"))
    return json_response

