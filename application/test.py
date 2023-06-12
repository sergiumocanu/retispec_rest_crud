import requests, json, base64

BASE = "http://127.0.0.1:5000"

##### testing Patient API
patient1 = {"first_name": "Albert", "last_name": "Einstein", "date_of_birth": "14-03-1879", "sex": "male"}
patient2 = {"first_name": "Leonhard", "last_name": "Euler", "date_of_birth": "15-04-1707", "sex": "female"}

### adding patients
# response = requests.post(url=BASE+"/patient", json=patient1)
# print(response.json())
# response = requests.post(url=BASE+"/patient", json=patient2)
# print(response.json())

### getting a patient
# response = requests.get(url=BASE+"/patient/2")
# print(response.json())

### getting a patient by first_name and last_name
# params = {"first_name": "Albert", "last_name": "Einstein"}
# response = requests.get(url=BASE+"/patient", params=params)
# print(response.json())

### deleting a patient
# response = requests.delete(url=BASE+"/patient/1")
# print(response.json())

##### testing Acquistion API
acquisition1 = {"eye": "right", "view": "disk", "site_name": "Toronto", "date_taken": "01-05-2020", "operator_name": "John Doe"}
img = "../test_imgs/rice.png"
with open(img, "rb") as f:
    im_bytes = f.read()        
im_b64 = base64.b64encode(im_bytes).decode("utf8")
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

acquisition1 = json.dumps({"eye": "right", "view": "disk", "site_name": "Toronto", "date_taken": "01-05-2020", "operator_name": "John Doe", "image_data": im_b64})
acquisition2 = json.dumps({"eye": "left", "view": "fovea", "site_name": "London", "date_taken": "01-06-2020", "operator_name": "John Doe", "image_data": im_b64})

### adding an acquisition for patient 1
# response = requests.post(url=BASE+"/patient/1/acquisition", data=acquisition1, headers=headers)
# print(response.json())
# response = requests.post(url=BASE+"/patient/1/acquisition", data=acquisition2, headers=headers)
# print(response.json())

### getting all acquisitions for a patient
# response = requests.get(url=BASE+"/patient/1/acquisition")
# print(response.json())

### list all acquisitions according to filter: eye
# params = {"eye": "left"}
# response = requests.get(url=BASE+"/patient/1/acquisition", params=params)
# print(response.json())

### list all acquisitions according to filter: view
# params = {"view": "fovea"}
# response = requests.get(url=BASE+"/patient/1/acquisition", params=params)
# print(response.json())

### list all acquisitions according to filter: site_name
# params = {"site_name": "Toronto"}
# response = requests.get(url=BASE+"/patient/1/acquisition", params=params)
# print(response.json())

### list all acquisitions according to filter: date_range
# params = {"date_range": "01-05-2020~10-06-2020"}
# response = requests.get(url=BASE+"/patient/1/acquisition", params=params)
# print(response.json())

### getting a specific patient acquisition
# response = requests.get(url=BASE+"/patient/1/acquisition/1")
# print(response.json())

### deleting a patient acquisition
# response = requests.delete(url=BASE+"/patient/1/acquisition/3")
# print(response.json())

### download an image from an acquisition
# in browser navigate to "http://127.0.0.1:5000/patient/1/acquisition/1/download"
