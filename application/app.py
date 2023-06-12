from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, date
import base64
from PIL import Image
import numpy as np
import io
import os
import glob

# instantiate flask app
app = Flask(__name__)

# set configs
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate db object
db = SQLAlchemy(app)

# create marshmallow object
ma = Marshmallow(app)

# create database
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return self.id
    
# create Patient schema
class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'sex')

# create instance of schema
patient_schema = PatientSchema(many=False)

# create/add a patient
@app.route("/patient", methods=["POST"])
def add_patient():
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        date_of_birth = request.json['date_of_birth']
        sex = request.json['sex']
        
        # convert DOB string to datetime object
        date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y').date()

        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            sex=sex
        )

        db.session.add(new_patient)
        db.session.commit()
        return patient_schema.jsonify(new_patient)
    except Exception as e:
        return jsonify({"Error": "Invalid request."})
    
# get patient by id
@app.route("/patient/<int:id>", methods=["GET"])
def get_patient_by_id(id):
    patient = Patient.query.get_or_404(int(id))
    return patient_schema.jsonify(patient)

# get patient by first and last name
@app.route("/patient/", methods=["GET"])
def get_patient_by_first_last():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    patient = Patient.query.filter_by(first_name=str(first_name), last_name=str(last_name)).first()
    return patient_schema.jsonify(patient)

# delete a patient by id
@app.route("/patient/<int:id>", methods=["DELETE"])
def delete_patient_by_id(id):
    patient = Patient.query.get_or_404(int(id))
    # also deleting any acquisitions a patient has
    acquisitions = Acquisition.query.filter_by(patient_id=int(id)).all()
    if acquisitions:
        patient_imgs = glob.glob(os.path.join("patient_imgs", f"*patient{id}*"))
        for i in range(len(acquisitions)):
            db.session.delete(acquisitions[i])
            os.remove(patient_imgs[i])
            

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"Success": "Patient deleted"})


class Acquisition(db.Model):
    ___tablename__ = "acquisitions"

    id = db.Column(db.Integer, primary_key=True)
    eye = db.Column(db.String(20), nullable=False)
    view = db.Column(db.String(20), nullable=False)
    site_name = db.Column(db.String(100), nullable=False)
    date_taken = db.Column(db.Date, nullable=False)
    operator_name = db.Column(db.String(100), nullable=False)
    image_data = db.Column(db.Text, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.id

# create acqusition schema
class AcquistionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'eye', 'view', 'site_name', 'date_taken', 'operator_name', 'patient_id')

# create instance of schemas
acquisition_schema = AcquistionSchema(many=False)
acquisitions_schema = AcquistionSchema(many=True)

# create/add an a patient acqusition
@app.route("/patient/<int:id>/acquisition", methods=["POST"])
def add_patient_acquisition(id):
    try:
        # print(request.json['eye'], "_____000000000000_______")
        # data = json.loads(request.form['data'])
        eye = request.json['eye']
        view = request.json['view']
        site_name = request.json['site_name']
        date_taken = request.json['date_taken']
        operator_name = request.json['operator_name']
        image_data = request.json['image_data']
        patient_id = id

        image_data = base64.b64decode(image_data.encode('utf-8'))
        image_data = Image.open(io.BytesIO(image_data))
        image_array = np.asarray(image_data)

        # convert date_taken from string to datetime object
        date_taken = datetime.strptime(date_taken, '%d-%m-%Y').date()

        new_acquisition = Acquisition(
            eye = eye,
            view = view,
            site_name = site_name,
            date_taken = date_taken,
            operator_name = operator_name,
            image_data = image_array,
            patient_id = patient_id
        )
        db.session.add(new_acquisition)
        db.session.commit()

        # saving image according to patient id and acquisition id
        acq_id = new_acquisition.id
        upload_dir = "patient_imgs"
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)
        image_data.save(f"{upload_dir}/patient{id}_acquisition{acq_id}.png")

        return acquisition_schema.jsonify(new_acquisition)
    except Exception as e:
        return jsonify({"Error": e})
    
# get all acquisitions
@app.route("/patient/<int:id>/acquisition", methods=["GET"])
def get_all_acqusitions_for_a_patient(id):
    eye = request.args.get('eye')
    view = request.args.get('view')
    site_name = request.args.get('site_name')
    date_range = request.args.get('date_range')
    
    # filter by eye, view, site_name
    if any([eye, view, site_name, date_range]):
        if eye:
            if eye.lower() not in ["left", "right"]:
                return jsonify({"Error": "eye should only be: 'left' or 'right'"})
            else:
                acquisitions = Acquisition.query.filter_by(eye=str(eye), patient_id=id).all()
                results_set = acquisitions_schema.dump(acquisitions)
                return jsonify(results_set)
        elif view:
            if view.lower() not in ["disk", "center", "fovea"]:
                return jsonify({"Error": "view should only be: 'disk', 'center', or 'fovea'"})
            else:
                acquisitions = Acquisition.query.filter_by(view=str(view), patient_id=id).all()
                results_set = acquisitions_schema.dump(acquisitions)
                return jsonify(results_set)
        elif site_name:
            acquisitions = Acquisition.query.filter_by(site_name=str(site_name), patient_id=id).all()
            results_set = acquisitions_schema.dump(acquisitions)
            return jsonify(results_set)
        elif date_range:
            date_range = date_range.split("~")
            first_date = datetime.strptime(date_range[0], '%d-%m-%Y').date()
            last_date = datetime.strptime(date_range[1], '%d-%m-%Y').date()
            acquisitions = Acquisition.query.filter(Acquisition.date_taken.between(first_date, last_date)).filter_by(patient_id=id).all()
            results_set = acquisitions_schema.dump(acquisitions)
            return jsonify(results_set)

    # view all acquisitions for a patient
    else:
        acqusitions = Acquisition.query.filter_by(patient_id=id).all()
        results_set = acquisitions_schema.dump(acqusitions)
        return jsonify(results_set)

# get specific acquisition
@app.route("/patient/<int:id>/acquisition/<int:acq_id>", methods=["GET"])
def get_one_acquisition_for_a_patient(id, acq_id):
    acquisition = Acquisition.query.filter_by(id=int(acq_id)).filter_by(patient_id=id).first()
    return acquisition_schema.jsonify(acquisition)

# delete an acquisition
@app.route("/patient/<int:id>/acquisition/<int:acq_id>", methods=["DELETE"])
def delete_acquisition_for_a_patient(id, acq_id):
    acquisition = Acquisition.query.filter_by(id=int(acq_id)).filter_by(patient_id=id).first()
    db.session.delete(acquisition)
    db.session.commit()
    image_path = os.path.join(os.getcwd(), f"patient_imgs/patient{id}_acquisition{acq_id}.png")
    if os.path.exists(image_path):
        os.remove(image_path)
    return jsonify({"Success": "Patient acquisition successfully deleted"})

# download an image by acquisition id
@app.route("/patient/<int:id>/acquisition/<int:acq_id>/download", methods=["GET"])
def download_an_image(id, acq_id):
    image_path = os.path.join(os.getcwd(), f"patient_imgs/patient{id}_acquisition{acq_id}.png")
    if os.path.exists(image_path):
        return send_file(image_path, as_attachment=True, download_name=f"patient{id}_acquisition_{acq_id}.png", mimetype="png")
    else:
        return jsonify({"Error": "Image does not exist for specified URL"})
if __name__ == "__main__":
    app.run(debug=True)