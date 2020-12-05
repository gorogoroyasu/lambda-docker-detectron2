import base64
from datetime import datetime as dt
from demo import get_result
import json

def handler(event, context):
    if 's3_path' not in event or 'bucket' not in event:
        return {'result': False}

    get_result(event)
    with open("/tmp/output.jpg", 'rb') as f:
        img = base64.b64encode(f.read())
    base64_encoded_binary_data = img.decode("utf-8")
    return {
        'result': True,
        'isBase64Encoded'   : True,
        'statusCode'        : 200,
        'headers'           : { 'Content-Type': 'image/jpeg' },
        'body'              : base64_encoded_binary_data}
