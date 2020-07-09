from flask import Blueprint, render_template, g, request, redirect, url_for,flash,session,jsonify
from flask_restful import Resource, Api
import os


from package.model import conn

doctor1 = Blueprint("doctor", __name__, static_folder='static', template_folder='templates')

PATIENT_IMAGES = os.path.join('static', 'uploads')



patientID = 0

@doctor1.route('/', methods=["GET"])
def doctor():
    print("++++++")
    print(session['user'])
    username = session['user']
    user = conn.execute("SELECT * FROM user WHERE username=?", (username,)).fetchall()
    docID = user[0]['user_id']
    getPatientCount = conn.execute("SELECT COUNT(*) AS patient from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id WHERE a.doc_id = ?",(docID,)).fetchone()
    getAppointmentCount = conn.execute("SELECT COUNT(*) AS appointment from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id WHERE a.doc_id = ?",(docID,)).fetchone()

    #print(getAppointmentCount['appointment'])
    return render_template('doctor/doctor.html',  numPat=getPatientCount['patient'], numAppoint=getAppointmentCount['appointment'], user=session['user'])


@doctor1.route('/patient', methods=["GET"])
def patient():
  username = session['user']
  user = conn.execute("SELECT * FROM user WHERE username=?", (username,)).fetchall()
  docID = user[0]['user_id']
  pats = conn.execute(
        "SELECT p.*,d.*,a.* from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id WHERE a.doc_id = ?",(docID,)).fetchall()

  print(pats)
  return render_template('doctor/patient.html', patients = pats, user=session['user'])

@doctor1.route('/view/<id>/')
def view(id):
    global patientID
    patientID = id
    print("<---->")
    print(patientID)
    pat = conn.execute("SELECT * FROM patient WHERE pat_id=?", (id,)).fetchall()
    diag = conn.execute("SELECT * FROM diagnosis WHERE pat_id=?", (id,)).fetchall()
    print(diag)
    #print(pat)

    full_filename = os.path.join('/',PATIENT_IMAGES, 'patient_' + patientID+'.jpeg')
    print(full_filename)
    return render_template('doctor/patientInfo.html', patients = pat, pat_image = full_filename, result = diag[0]['prediction'], therapy=diag[0]['note'], user=session['user'])



@doctor1.route('/savepatientinfo', methods = ['GET', 'POST'])
def add_predict():
    global patientID
    id = patientID
    print("---->")
    print(id)
    if request.method == 'POST':
        diagnose = request.form['predict']
        therapy = request.form['suggestion']

        conn.execute(
            "UPDATE diagnosis SET prediction=?, note=? WHERE pat_id=?",
            (diagnose, therapy, id))
        conn.commit()
        return  jsonify({'success':'update successfully!'})
    return jsonify({'error': 'Missing data!'})

@doctor1.route('/appointment', methods=["GET"])
def appointment():
    username = session['user']
    user = conn.execute("SELECT * FROM user WHERE username=?", (username,)).fetchall()
    docID = user[0]['user_id']
    data = conn.execute(
        "SELECT p.*,d.*,a.* from appointment a LEFT JOIN patient p ON a.pat_id = p.pat_id LEFT JOIN doctor d ON a.doc_id = d.doc_id WHERE a.doc_id = ?",
        (docID,)).fetchall()

    return render_template('doctor/appointment.html', appointments = data, user=session['user'])


