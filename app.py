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

# ---------------- Routes ----------------

@app.route("/")
def home():
    return render_template("index.html")
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

# ---------------- Run App ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
