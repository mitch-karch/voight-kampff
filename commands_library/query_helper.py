import http.client
import json
import requests

headers = {
    "cache-control": "no-cache",
}


def query_request(url, suburl, requestType="GET", raw_return=False):
    conn = http.client.HTTPSConnection(url)
    conn.request(requestType, suburl, headers=headers)
    if raw_return:
        return conn.getresponse().read().decode("utf-8")
    else:
        try:
            json_response = json.loads(conn.getresponse().read().decode("utf-8"))
        except json.decoder.JSONDecodeError:
            return False

        return json_response


def payload_post(url, suburl, payload, requestType="POST", raw_return=False):
    conn = http.client.HTTPSConnection(url)
    conn.request(requestType, suburl, headers=headers, params=payload)
    if raw_return:
        return conn.getresponse().read().decode("utf-8")
    else:
        json_response = json.loads(conn.getresponse().read().decode("utf-8"))
        return json_response


def payload_request(url, payload={}):
    return requests.request("GET", url, params=payload).json()


def headers_request(url, headers):
    return requests.get(url, headers=headers).json()
