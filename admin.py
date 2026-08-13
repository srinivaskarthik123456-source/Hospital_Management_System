from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# ==================================================
# SECRET KEY
# ==================================================

app.secret_key = "city-care-hospital-admin"


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_database():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    return connection


# ==================================================
# ADMIN LOGIN
# ==================================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    connection = get_database()

    # ---------------- PATIENTS ----------------

    patients = connection.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """).fetchall()

    # ---------------- APPOINTMENTS ----------------

    appointments = connection.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """).fetchall()

    # ---------------- COUNTS ----------------

    patient_count = connection.execute("""
        SELECT COUNT(*)
        FROM patients
    """).fetchone()[0]

    appointment_count = connection.execute("""
        SELECT COUNT(*)
        FROM appointments
    """).fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        patients=patients,
        appointments=appointments,
        patient_count=patient_count,
        appointment_count=appointment_count,
        search=""
    )


# ==================================================
# PATIENT SEARCH
# ==================================================

@app.route("/admin/search-patient")
def search_patient():

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    search = request.args.get(
        "search",
        ""
    ).strip()

    connection = get_database()

    # Search by name or phone

    if search:

        patients = connection.execute("""
            SELECT *
            FROM patients
            WHERE name LIKE ?
               OR phone LIKE ?
            ORDER BY id DESC
        """, (
            "%" + search + "%",
            "%" + search + "%"
        )).fetchall()

    else:

        patients = connection.execute("""
            SELECT *
            FROM patients
            ORDER BY id DESC
        """).fetchall()

    # Get appointments

    appointments = connection.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """).fetchall()

    # Get counts

    patient_count = connection.execute("""
        SELECT COUNT(*)
        FROM patients
    """).fetchone()[0]

    appointment_count = connection.execute("""
        SELECT COUNT(*)
        FROM appointments
    """).fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        patients=patients,
        appointments=appointments,
        patient_count=patient_count,
        appointment_count=appointment_count,
        search=search
    )


# ==================================================
# EDIT PATIENT - GET
# ==================================================

@app.route("/admin/edit-patient/<int:patient_id>")
def edit_patient(patient_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    connection = get_database()

    patient = connection.execute("""
        SELECT *
        FROM patients
        WHERE id = ?
    """, (
        patient_id,
    )).fetchone()

    connection.close()

    if patient is None:

        return "Patient not found."

    return render_template(
        "edit_patient.html",
        patient=patient
    )


# ==================================================
# UPDATE PATIENT - POST
# ==================================================

@app.route(
    "/admin/update-patient/<int:patient_id>",
    methods=["POST"]
)
def update_patient(patient_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")
    problem = request.form.get("problem")
    doctor = request.form.get("doctor")
    appointment_date = request.form.get(
        "appointment_date"
    )

    connection = get_database()

    connection.execute("""
        UPDATE patients

        SET
            name = ?,
            age = ?,
            gender = ?,
            phone = ?,
            email = ?,
            address = ?,
            problem = ?,
            doctor = ?,
            appointment_date = ?

        WHERE id = ?

    """, (
        name,
        age,
        gender,
        phone,
        email,
        address,
        problem,
        doctor,
        appointment_date,
        patient_id
    ))

    connection.commit()

    connection.close()

    return redirect("/admin")


# ==================================================
# DELETE PATIENT
# ==================================================

@app.route("/admin/delete-patient/<int:patient_id>")
def delete_patient(patient_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    connection = get_database()

    connection.execute("""
        DELETE FROM patients
        WHERE id = ?
    """, (
        patient_id,
    ))

    connection.commit()

    connection.close()

    return redirect("/admin")


# ==================================================
# EDIT APPOINTMENT - GET
# ==================================================

@app.route("/admin/edit-appointment/<int:appointment_id>")
def edit_appointment(appointment_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    connection = get_database()

    appointment = connection.execute("""
        SELECT *
        FROM appointments
        WHERE id = ?
    """, (
        appointment_id,
    )).fetchone()

    connection.close()

    if appointment is None:

        return "Appointment not found."

    return render_template(
        "edit_appointment.html",
        appointment=appointment
    )


# ==================================================
# UPDATE APPOINTMENT - POST
# ==================================================

@app.route(
    "/admin/update-appointment/<int:appointment_id>",
    methods=["POST"]
)
def update_appointment(appointment_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    patient_name = request.form.get(
        "patient_name"
    )

    phone = request.form.get(
        "phone"
    )

    doctor = request.form.get(
        "doctor"
    )

    appointment_date = request.form.get(
        "appointment_date"
    )

    appointment_time = request.form.get(
        "appointment_time"
    )

    reason = request.form.get(
        "reason"
    )

    connection = get_database()

    connection.execute("""
        UPDATE appointments

        SET
            patient_name = ?,
            phone = ?,
            doctor = ?,
            appointment_date = ?,
            appointment_time = ?,
            reason = ?

        WHERE id = ?

    """, (
        patient_name,
        phone,
        doctor,
        appointment_date,
        appointment_time,
        reason,
        appointment_id
    ))

    connection.commit()

    connection.close()

    return redirect("/admin")


# ==================================================
# DELETE APPOINTMENT
# ==================================================

@app.route(
    "/admin/delete-appointment/<int:appointment_id>"
)
def delete_appointment(appointment_id):

    if not session.get("admin_logged_in"):

        return redirect("/admin-login")

    connection = get_database()

    connection.execute("""
        DELETE FROM appointments
        WHERE id = ?
    """, (
        appointment_id,
    ))

    connection.commit()

    connection.close()

    return redirect("/admin")


# ==================================================
# ADMIN LOGOUT
# ==================================================

@app.route("/admin-logout")
def admin_logout():

    session.clear()

    return redirect("/admin-login")


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )