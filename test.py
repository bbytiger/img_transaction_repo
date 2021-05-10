import requests
from PIL import Image
import io

### first endpoint for creating an image

f = open('test.png', 'rb')
k = f.read()

url = "http://localhost:8000/data/create_image/"

headers = {
    'Authorization': 'Token 62ed705fa9520373cdf8562c8ff45e206d347149'
}

img_body = {
    'img': k
}

body = {
    'public': True,
    'img_name': 'djnawjkdnawkjd'
}

r = requests.post(url, headers=headers, files=img_body, data=body)
print(r)
print(r.json())
 

### second endpoint is for downloading an image

url2 = "http://localhost:8000/data/dl_image/"

body = {
    'id': str(r.json()['id'])
}

headers2 = {
    'Authorization': 'Token 62ed705fa9520373cdf8562c8ff45e206d347149'
}

r2 = requests.post(url2, headers=headers2, json=body)
print("response status: ", r2)
print("type of data returned: ", type(r2.content))

image = Image.open(io.BytesIO(r2.content))
image.show()
wait = input("enter to finish the test...")
