# Retispec REST API
An API for working with Patient and corresponding Acquisition data developed using Flask

## Setup
- Please clone the repo to an empty folder
- This API has been developed on `Python 3.9.1`, mainly for `f-string` compatibility
- Create a virtual environment using `python -m venv venv` and activate using `venv\Scripts\activate` if on Windows and `source venv/Scripts/activate` if on Unix
- Install package dependencies by running `pip install -r requirements.txt`

## Initialize and running the application
- Navigate to the application folder `cd application`
- Initiate the database by running `flask shell` and `db.create_all()`. This will create a folder called `instance` and inside a file called `database.db` that will store the SQLite database. Exit the flask shell with `quit()`.
- Run the app with `flask run` or `python app.py`

## Testing the application
- The `test.py` script can be used to generate various requests and some dummy data has been provided (while the app runs, please use a second terminal to run the `python test.py` script).
- Various portions of the code can be uncommented to run the requests
- One can modify the request URL to get, delete (etc.) various patients according to id. Ex: `requests.get(url=BASE+"/patient/1")` will query patient 1 and `requests.get(url=BASE+"/patient/2")` will query patient 2.
- Similar requests can be made via applications such as [Postman](https://www.postman.com).
- One test image has been provided: `test_imgs/rice.png`.
- To download an image from a patient's acquisition, one can navigate in a web browser to the corresponding URL. Ex: patient 1, acquisition 1 = `http://127.0.0.1:5000/patient/1/acquisition/1/download`
- To close the application, please press `CTRL+C`

## Notes
- Dates are represented as `dd-mm-yyyy`
- Date range filter is `dd-mm-yyyy~dd-mm-yyyy`, please note the tildae `~` between the two dates
- When creating an acquisition, the images are saved in a folder called `patient_images` and the image file names are `patient[id1]_acquisition[id2].png` where `id1` is the patient id and `id2` is the acquisition id for that patient.
- When adding a patient acquisition, the acquisition object will also store the patient id in a specified column.
- When deleting a patient, it will also delete that patient's acquisition data and the related images
