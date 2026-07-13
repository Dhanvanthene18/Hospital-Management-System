from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/patients")
def patients():
    return render_template("patients.html")

# ---------------- Run App ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
