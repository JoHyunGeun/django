import base64
import urllib.request
import json
import time


class Magellan:

    def __init__(self, sex):
        if sex == 'male':
            self.blocks_designer = 'ysmr3104blocksboard06adb5a1'
            self.blocks_flow = 'modelM'
            self.headers = {"Content-Type": "application/json",
                            "Authorization": "Bearer a31a3475f4c36444087958e69d4e5ff6268c2ac40a089a2808a610c84218d6af"}
        elif sex == 'female':
            self.blocks_designer = 'ysmr3104blocksboard038ea854'
            self.blocks_flow = 'modelF'
            self.headers = {"Content-Type": "application/json",
                            "Authorization": "Bearer 77c64136f3a5efb72215cafc4ca28646538d669ba1ce4ec10e5919168348b49c"}
        self.job_id = ""
        self.json_data = ""
        self.status = ""

    def decision(self, result):
        if result == 'c_stage1':
            return 'Initial circular hair loss is suspected. Please visit a nearby hospital for further diagnosis.'
        elif result == 'c_stage2':
            return 'A round hair loss is already in progress. Please visit a nearby hospital for further diagnosis.'
        elif result == 'c_stage3':
            return 'You have severe round hair loss. Please visit the nearest hospital as soon as possible.'
        elif result == 'm_normal':
            return 'Your hair looks normal. But please visit the hospital for further diagnosis.'
        elif result == 'm_stage1':
            return 'Initial M-shaped hair loss is suspected. Please visit a nearby hospital for further diagnosis.'
        elif result == 'm_stage2':
            return 'M-shaped hair loss is already in progress. Please visit a nearby hospital for further diagnosis.'
        elif result == 'm_stage3':
            return 'You have severe M-shaped hair loss. Please visit the nearest hospital as soon as possible.'
        elif result == 'normal':
            return 'Your hair looks normal. But please visit the hospital for further diagnosis.'
        elif result == 'total':
            return 'A total hair loss is suspected. Please visit a nearby hospital for further diagnosis.'

    def image_to_base64(self, image_str):
        b64 = base64.encodebytes(open(image_str, 'rb').read())
        blocks_json = {'_': {'key': image_str, 'image': {'b64': b64.decode('utf8')}}}
        self.json_data = json.dumps(blocks_json).encode('utf-8')

    def start_flow(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + ".json"
        method = "POST"
        headers = self.headers
        request = urllib.request.Request(url, data=self.json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            json_obj = json.loads(response_body)
            result = json_obj['result']
            self.job_id = json_obj['job_id']
            if result is True:
                print("flow starting is successed.")
            else:
                print("flow starting is failed.")

    def check_status(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + "/jobs/" + str(
            self.job_id) + "/status.json"
        method = "GET"
        headers = self.headers
        request = urllib.request.Request(url, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            json_obj = json.loads(response_body)
            self.status = json_obj['status']
            print(self.status)

    def check_result(self):
        url = "https://" + self.blocks_designer + ".magellanic-clouds.net/flows/" + self.blocks_flow + "/jobs/" + str(
            self.job_id) + "/variable.json"
        method = "GET"
        headers = self.headers
        request = urllib.request.Request(url, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            json_obj = json.loads(response_body)
            result = json_obj['predictions'][0]['label']
            print(self.decision(result))
            return self.decision(result)

    def predict(self, image_str):
        self.image_to_base64(image_str)
        self.start_flow()
        while True:
            time.sleep(1)
            self.check_status()
            if self.status in ['finished', 'failed', 'canceled']:
                return self.check_result()