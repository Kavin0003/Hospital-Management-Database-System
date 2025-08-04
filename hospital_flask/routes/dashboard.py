from flask import Blueprint, jsonify, request
from routes.db_config import get_db_connection
from utils.auth import token_required

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/", methods=['GET'])
@token_required
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get statistics
        stats = {}
        
        # Count patients
        cursor.execute("SELECT COUNT(*) FROM patients")
        stats['total_patients'] = cursor.fetchone()[0]
        
        # Count doctors
        cursor.execute("SELECT COUNT(*) FROM doctors")
        stats['total_doctors'] = cursor.fetchone()[0]
        
        # Count staff
        cursor.execute("SELECT COUNT(*) FROM staff")
        stats['total_staff'] = cursor.fetchone()[0]
        
        # Count appointments today
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE DATE(date) = CURDATE()")
        stats['appointments_today'] = cursor.fetchone()[0]
        
        # Count total appointments
        cursor.execute("SELECT COUNT(*) FROM appointments")
        stats['total_appointments'] = cursor.fetchone()[0]
        
        # Recent appointments
        cursor.execute("""
            SELECT a.id, p.name as patient_name, d.name as doctor_name, 
                   a.date, a.time, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.date DESC, a.time DESC
            LIMIT 5
        """)
        recent_appointments = []
        for row in cursor.fetchall():
            recent_appointments.append({
                'id': row[0],
                'patient_name': row[1],
                'doctor_name': row[2],
                'date': str(row[3]),
                'time': str(row[4]),
                'status': row[5]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'user': request.current_user,
            'stats': stats,
            'recent_appointments': recent_appointments
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500