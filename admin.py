from __future__ import division, print_function
from flask import Blueprint,g, render_template, request, redirect, url_for,flash, session, jsonify
from flask_restful import Resource, Api


from package.model import conn



import sys
import os
import glob
import re
from pathlib import Path



# Import fast.ai Library
from fastai import *
from fastai.vision import *


# Flask utils
from flask import Flask, redirect, g, url_for, request, render_template
from werkzeug.utils import secure_filename



admin1 = Blueprint("admin", __name__, static_folder='static', template_folder='templates')

admin1.secret_key = "duyennguyen"




path = Path("path")
classes = ['bacteria','normal', 'virus']
data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
learn = create_cnn(data2, models.resnet50)
learn.load('x_ray_3class')


patientID = 0


@admin1.route('/', methods=["GET"])
def admin():
    getPatientCount = conn.execute("SELECT COUNT(*) AS patient FROM patient").fetchone()
    getDoctorCount = conn.execute("SELECT COUNT(*) AS doctor FROM doctor").fetchone()
    getAppointmentCount = conn.execute("SELECT COUNT(*) AS appointment FROM appointment").fetchone()
    print("++++++")
    print(session['user'])
    print(getAppointmentCount['appointment'])
    return render_template('admin/index.html',  numPat=getPatientCount['patient'], numDoc=getDoctorCount['doctor'], numAppoint=getAppointmentCount['appointment'])



### Patient Page

@admin1.route('/patient', methods=["GET"])
def patient():

    data = conn.execute("SELECT * FROM patient  ORDER BY pat_id ASC").fetchall()
    # print(data)
    return render_template('admin/patient.html', patients=data)


@admin1.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        pat_first_name = request.form['pat_first_name']
        pat_last_name = request.form['pat_last_name']
        pat_insurance_no = request.form['pat_insurance_no']
        pat_ph_no = request.form['pat_ph_no']
        pat_address = request.form['pat_address']

        print("***")
        print (pat_first_name )
        print( pat_last_name)
        conn.execute('''INSERT INTO patient(pat_first_name,pat_last_name,pat_insurance_no,pat_ph_no,pat_address)
                   VALUES(?,?,?,?,?)''',
                     (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address)).lastrowid
        conn.commit()
        flash("Patient Added Successfully!")

        return redirect(url_for("admin.patient"))


@admin1.route('/update', methods=['GET','POST'])
def update():
    if request.method == "POST":

        pat_id = request.form['pat_id']
        pat_first_name = request.form['pat_first_name']
        pat_last_name = request.form['pat_last_name']
        pat_insurance_no = request.form['pat_insurance_no']
        pat_ph_no = request.form['pat_ph_no']
        pat_address = request.form['pat_address']
        conn.execute(
            "UPDATE patient SET pat_first_name=?,pat_last_name=?,pat_insurance_no=?,pat_ph_no=?,pat_address=? WHERE pat_id=?",
            (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address, pat_id))
        conn.commit()
        flash("Updated Successfully")

        return redirect((url_for("admin.patient")))


@admin1.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    conn.execute("DELETE FROM patient WHERE pat_id=?", (id,))
    conn.commit()
    flash('Deleted Successfully!')
    return redirect((url_for("admin.patient")))

@admin1.route('/view/<id>/', methods = ['GET','POST'])
def view(id):
    global patientID
    patientID = id
    print("<---->")
    print(patientID)
    pat = conn.execute("SELECT * FROM patient WHERE pat_id=?", (id,)).fetchall()
    print(pat)


    return render_template('mlmodel/profile.html', patient=pat)

@admin1.route('/addpredict', methods = ['GET', 'POST'])
def add_predict():
    global patientID
    id = patientID
    print("---->")
    print(id)
    if request.method == 'POST':
        diagnose = request.form['predict']
        conn.execute('''INSERT INTO diagnosis(pat_id, prediction)
                             VALUES(?,?)''',
                     (id, diagnose)).lastrowid
        conn.commit()
        return  jsonify({'predict': diagnose})
    return jsonify({'error': 'Missing data!'})

def model_predict(img_path):
    """
       model_predict will return the preprocessed image
    """

    img = open_image(img_path)
    pred_class, pred_idx, outputs = learn.predict(img)
    print(pred_class)
    return pred_class



@admin1.route('/predict', methods=['GET', 'POST'])
def upload():
    print("Function is called!")
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        # print(basepath)
        file_path = os.path.join(
            basepath, 'static/uploads', secure_filename(f.filename))

        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)
        print(preds)
        return str(preds).lower()
    return None


### Doctor page

@admin1.route('/doctor', methods=["GET"])
def doctor():
    doc = conn.execute("SELECT * FROM doctor ORDER BY doc_id ASC").fetchall()
    return render_template('admin/doctor.html', doctors=doc)


@admin1.route('/updatedoc', methods=['GET','POST'])
def insertdoc():
    if request.method == "POST":


        doc_first_name = request.form['doc_first_name']
        doc_last_name = request.form['doc_last_name']
        doc_ph_no = request.form['doc_ph_no']
        doc_address = request.form['doc_address']
        conn.execute('''INSERT INTO doctor(doc_first_name,doc_last_name,doc_ph_no,doc_address)
                    VALUES(?,?,?,?)''', (doc_first_name, doc_last_name, doc_ph_no, doc_address)).lastrowid
        conn.commit()
        flash("Doctor Updated Successfully")

        return redirect((url_for("admin.doctor")))


@admin1.route('/deletedoc/<id>/', methods = ['GET', 'POST'])
def deletedoc(id):
    conn.execute("DELETE FROM doctor WHERE doc_id=?", (id,))
    conn.commit()
    flash('Doctor Deleted Successfully!')
    return redirect((url_for("admin.doctor")))




### Appointment Page

@admin1.route('/appointment', methods=["GET"])
def appointment():
    app = conn.execute(
        "SELECT p.*,d.*,a.* from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id ORDER BY appointment_date DESC").fetchall()
    return render_template('admin/appointment.html', appointments = app)


@admin1.route('/deleteappoint/<id>/', methods = ['GET', 'POST'])
def deleteappoint(id):
    conn.execute("DELETE FROM appointment WHERE app_id=?", (id,))
    conn.commit()
    flash('Doctor Deleted Successfully!')
    return redirect((url_for("admin.appointment")))