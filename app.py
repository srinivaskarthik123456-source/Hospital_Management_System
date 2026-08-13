from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ==================================================
# DATABASE
# ==================================================

def create_database():

    connection = sqlite3.connect("database.db")

    # ---------------- PATIENTS TABLE ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            problem TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL
        )
    """)

    # ---------------- APPOINTMENTS TABLE ----------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# PATIENT REGISTRATION
# ==================================================

@app.route("/patient-registration", methods=["GET", "POST"])
def patient_registration():

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        problem = request.form.get("problem")
        doctor = request.form.get("doctor")
        appointment_date = request.form.get("date")

        connection = sqlite3.connect("database.db")

        connection.execute("""
            INSERT INTO patients
            (
                name,
                age,
                gender,
                phone,
                email,
                address,
                problem,
                doctor,
                appointment_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            phone,
            email,
            address,
            problem,
            doctor,
            appointment_date
        ))

        connection.commit()
        connection.close()

        return redirect("/success")

    return render_template("patient_registration.html")


# ==================================================
# PATIENT REGISTRATION SUCCESS
# ==================================================

@app.route("/success")
def success():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Registration Successful</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f8fb;
                text-align: center;
                padding-top: 100px;
            }

            .box {
                background: white;
                width: 600px;
                max-width: 90%;
                margin: auto;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px #ccc;
            }

            h1 {
                color: green;
            }

            a {
                display: inline-block;
                margin: 12px;
                color: #0b6e8e;
                text-decoration: none;
                font-size: 17px;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>
                ✅ Patient Registered Successfully!
            </h1>

            <p>
                Patient details have been saved in the database.
            </p>

            <br>

            <a href="/patient-registration">
                Register Another Patient
            </a>

            <br>

            <a href="/">
                Back to Home
            </a>

        </div>

    </body>

    </html>
    """


# ==================================================
# PATIENT RECORDS
# ==================================================

@app.route("/patients")
def patients():

    connection = sqlite3.connect("database.db")

    connection.row_factory = sqlite3.Row

    patient_data = connection.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "patients.html",
        patients=patient_data
    )


# ==================================================
# DOCTORS PAGE
# ==================================================

@app.route("/doctors")
def doctors():

    return render_template("doctors.html")


# ==================================================
# APPOINTMENT BOOKING
# ==================================================

@app.route("/appointments", methods=["GET", "POST"])
def appointments():

    # ---------------- GET ----------------

    if request.method == "GET":

        return render_template("appointments.html")


    # ---------------- POST ----------------

    if request.method == "POST":

        patient_name = request.form.get("patient_name")
        phone = request.form.get("phone")
        doctor = request.form.get("doctor")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")
        reason = request.form.get("reason")


        # Check required fields

        if not patient_name:
            return "Patient Name is required."

        if not phone:
            return "Phone Number is required."

        if not doctor:
            return "Doctor is required."

        if not appointment_date:
            return "Appointment Date is required."

        if not appointment_time:
            return "Appointment Time is required."

        if not reason:
            return "Reason is required."


        # Save appointment

        connection = sqlite3.connect("database.db")

        connection.execute("""
            INSERT INTO appointments
            (
                patient_name,
                phone,
                doctor,
                appointment_date,
                appointment_time,
                reason
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_name,
            phone,
            doctor,
            appointment_date,
            appointment_time,
            reason
        ))

        connection.commit()
        connection.close()


        # Redirect to success page

        return redirect("/appointment-success")


# ==================================================
# APPOINTMENT SUCCESS
# ==================================================

@app.route("/appointment-success")
def appointment_success():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Appointment Successful</title>

        <style>

            * {
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }

            body {
                margin: 0;
                background: #f4f8fb;
            }

            header {
                background: #0b6e8e;
                color: white;
                padding: 20px;
                text-align: center;
            }

            .success-box {
                width: 650px;
                max-width: 90%;
                background: white;
                margin: 80px auto;
                padding: 50px;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0 4px 15px #ccc;
            }

            .icon {
                font-size: 60px;
            }

            h1 {
                color: green;
            }

            p {
                font-size: 18px;
                color: #333;
            }

            a {
                display: inline-block;
                background: #0b6e8e;
                color: white;
                text-decoration: none;
                padding: 13px 22px;
                margin: 10px;
                border-radius: 6px;
            }

            a:hover {
                background: #075b75;
            }

        </style>

    </head>

    <body>

        <header>

            <h2>
                🏥 City Care Hospital
            </h2>

        </header>


        <div class="success-box">

            <div class="icon">
                ✅
            </div>

            <h1>
                Appointment Booked Successfully!
            </h1>

            <p>
                Your appointment has been successfully booked.
            </p>

            <p>
                Appointment details have been saved in the database.
            </p>

            <br>

            <a href="/appointments">
                Book Another Appointment
            </a>

            <a href="/appointment-records">
                View Appointment Records
            </a>

            <a href="/">
                Back to Home
            </a>

        </div>

    </body>

    </html>
    """


# ==================================================
# APPOINTMENT RECORDS
# ==================================================

@app.route("/appointment-records")
def appointment_records():

    connection = sqlite3.connect("database.db")

    connection.row_factory = sqlite3.Row

    appointments = connection.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "appointment_records.html",
        appointments=appointments
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)