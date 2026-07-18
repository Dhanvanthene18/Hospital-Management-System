from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:DG%401847@localhost/hospital_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- Patient Model ----------------

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    blood_group = db.Column(db.String(5))
    disease = db.Column(db.String(100))
    doctor = db.Column(db.String(100))
    admission_date = db.Column(db.Date)
    status = db.Column(db.String(20))
class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    consultation_fee = db.Column(db.Float)
    availability = db.Column(db.String(50))
# Add this below the Doctor model
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    appointment_id = db.Column(db.String(20), unique=True, nullable=False)

    patient_name = db.Column(db.String(100), nullable=False)

    doctor_name = db.Column(db.String(100), nullable=False)

    appointment_date = db.Column(db.Date, nullable=False)

    appointment_time = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), nullable=False)

# ---------------- Routes ----------------

@app.route("/")
def home():

    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()

    return render_template(
        "index.html",
        total_patients=total_patients,
        total_doctors=total_doctors
    )
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
@app.route("/patients/add", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        patient = Patient(
            patient_id=request.form["patient_id"],
            name=request.form["name"],
            age=request.form["age"],
            gender=request.form["gender"],
            phone=request.form["phone"],
            address=request.form["address"],
            blood_group=request.form["blood_group"],
            disease=request.form["disease"],
            doctor=request.form["doctor"],
            admission_date=datetime.strptime(
                request.form["admission_date"], "%Y-%m-%d"
            ),
            status=request.form["status"]
        )

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("patients"))

    return render_template("add_patient.html")

@app.route("/patients")
def patients():
    patients = Patient.query.all()      # Step 1
    return render_template("patients.html", patients=patients)   # Step 2
@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "POST":
        patient.patient_id = request.form["patient_id"]
        patient.name = request.form["name"]
        patient.age = request.form["age"]
        patient.gender = request.form["gender"]
        patient.phone = request.form["phone"]
        patient.address = request.form["address"]
        patient.blood_group = request.form["blood_group"]
        patient.disease = request.form["disease"]
        patient.doctor = request.form["doctor"]

        patient.admission_date = datetime.strptime(
            request.form["admission_date"],
            "%Y-%m-%d"
        ).date()

        patient.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("patients"))

    return render_template("edit_patient.html", patient=patient)
@app.route("/delete_patient/<int:id>")
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect(url_for("patients"))
@app.route("/doctors")
def doctors():

    doctors = Doctor.query.all()

    return render_template(
        "doctors.html",
        doctors=doctors
    )
from flask import request, redirect, url_for

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():

    if request.method == "POST":

        doctor = Doctor(

            doctor_id=request.form["doctor_id"],
            name=request.form["name"],
            specialization=request.form["specialization"],
            qualification=request.form["qualification"],
            experience=request.form["experience"],
            phone=request.form["phone"],
            email=request.form["email"],
            consultation_fee=request.form["consultation_fee"],
            availability=request.form["availability"]

        )

        db.session.add(doctor)
        db.session.commit()

        return redirect(url_for("doctors"))

    return render_template("add_doctor.html")
@app.route("/edit_doctor/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":

        doctor.doctor_id = request.form["doctor_id"]
        doctor.name = request.form["name"]
        doctor.specialization = request.form["specialization"]
        doctor.qualification = request.form["qualification"]
        doctor.experience = request.form["experience"]
        doctor.phone = request.form["phone"]
        doctor.email = request.form["email"]
        doctor.consultation_fee = request.form["consultation_fee"]
        doctor.availability = request.form["availability"]

        db.session.commit()

        return redirect(url_for("doctors"))

    return render_template(
        "edit_doctor.html",
        doctor=doctor
    )
@app.route("/delete_doctor/<int:id>")
def delete_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    db.session.delete(doctor)
    db.session.commit()

    return redirect(url_for("doctors"))
# ---------------- Run App ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
