import base64
import boto3
import json
import requests
import time

"""
適宜変更してください
"""
is_local = True
YOUR_BUCKET_NAME = ''
PATH_TO_JPG = ''
YOUR_PROFILE_NAME = ''
LAMBDA_FUNCTION_NAME = ''


s = time.time()
if is_local:
    url = 'http://localhost:9000/2015-03-31/functions/function/invocations'
    r = requests.post(url, json.dumps({'bucket': 'YOUR_BUCKET_NAME', 's3_path': 'path/to/jpg'}))
    j = r.json()
    if j['result']:
        decoded = base64.b64decode(j['body'])
        with open("output.jpg", 'wb') as f:
            f.write(decoded)
    else:
        print(j)
        print("FAIL!!")
else:

    l = boto3.Session(profile_name=YOUR_PROFILE_NAME).client('lambda').invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse', # Event or RequestResponse
        Payload=json.dumps({'bucket': YOUR_BUCKET_NAME, 's3_path': PATH_TO_JPG})
    )
    j = json.loads(l['Payload'].read())
    decoded = base64.b64decode(j['body'])
    with open("output.jpg", 'wb') as f:
        f.write(decoded)

print(f"実行時間は、約{int(time.time() - s)}秒でした。")
