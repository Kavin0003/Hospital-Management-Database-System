from flask import Blueprint, request, jsonify
from routes.db_config import get_db_connection
from utils.auth import token_required

patients = Blueprint('patients', __name__)

@patients.route("/", methods=['GET'])
@token_required
def patient_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients ORDER BY id DESC")
        patient_data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'patients': patient_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients.route("/", methods=['POST'])
@token_required
def add_patient():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'gender', 'contact', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO patients (name, age, gender, contact, address, email, medical_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['name'],
            data['age'],
            data['gender'],
            data['contact'],
            data['address'],
            data.get('email', ''),
            data.get('medical_history', '')
        ))
        
        conn.commit()
        patient_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Patient added successfully',
            'patient_id': patient_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients.route("/<int:patient_id>", methods=['GET'])
@token_required
def get_patient(patient_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify({
            'success': True,
            'patient': patient
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients.route("/<int:patient_id>", methods=['PUT'])
@token_required
def update_patient(patient_id):
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Patient not found'}), 404
        
        # Update patient
        cursor.execute("""
            UPDATE patients 
            SET name = %s, age = %s, gender = %s, contact = %s, 
                address = %s, email = %s, medical_history = %s
            WHERE id = %s
        """, (
            data.get('name'),
            data.get('age'),
            data.get('gender'),
            data.get('contact'),
            data.get('address'),
            data.get('email', ''),
            data.get('medical_history', ''),
            patient_id
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Patient updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients.route("/<int:patient_id>", methods=['DELETE'])
@token_required
def delete_patient(patient_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if patient exists
        cursor.execute("SELECT id FROM patients WHERE id = %s", (patient_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Patient not found'}), 404
        
        # Delete patient
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Patient deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients.route("/add", methods=["GET", "POST"])
def add_patient():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        address = request.form.get("address")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, age, gender, contact, address))
            conn.commit()
            flash("Patient added successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error adding patient: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for("patients.patient_list"))  # Redirect to patient list

    return render_template("add_patient.html")

@patients.route('/view/<int:id>')
def view_patient(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        flash("Patient not found", "danger")
        return redirect(url_for("patients.patient_list"))

    return render_template("view_patient.html", patient=patient)

@patients.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        address = request.form.get("address")

        try:
            cursor.execute("""
                UPDATE patients 
                SET name=%s, age=%s, gender=%s, contact=%s, address=%s
                WHERE id=%s
            """, (name, age, gender, contact, address, id))
            conn.commit()
            flash("Patient updated successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error updating patient: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for("patients.view_patient", id=id))

    # GET request - show edit form
    try:
        cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
        patient = cursor.fetchone()
        
        if not patient:
            flash("Patient not found", "danger")
            return redirect(url_for("patients.patient_list"))
            
        return render_template("edit_patient.html", patient=patient)
    finally:
        cursor.close()
        conn.close()

@patients.route('/delete/<int:id>')
def delete_patient(id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM patients WHERE id = %s", (id,))
        conn.commit()
        flash("Patient deleted successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting patient: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("patients.patient_list"))