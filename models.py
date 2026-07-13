from app import db

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