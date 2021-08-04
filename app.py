from locust import HttpUser, TaskSet, task, between
import json
import random
import sys
import random

headers = {
    'Content-Type': 'application/json',
}

objs = []
with open('data.json') as f:
  objs = json.load(f)

def run_request(locust, data, name):
    data["id"] = random.randint(0, sys.maxsize)
    with locust.client.post("", name=name, json=data, catch_response=True) as response:
        try:
            data = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            response.failure("Invalid JSON")
        else:
            if data.get("error", False):
                response.failure("Payload error: %s" % data.get("error"))
            elif data.get("id") != data["id"]:
                response.failure("Mismatched IDs")
            else: response.success()
        return response

class RunTest(TaskSet):
    @task()
    def eth_call1(locust):
        call = objs[random.randint(0,526238)]
        data = {"jsonrpc":"2.0","method":"eth_call","params":[{"to": call["to"], "data": call["data"]}, "latest"],"id":1}
        print(data)
        run_request(locust, data, name="eth_call")

class WebsiteUser(HttpUser):
    tasks = [RunTest]
    wait_time = between(1, 5)