from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from routes.dashboard import dashboard
from routes.patients import patients
from routes.doctors import doctors
from routes.appointments import appointments
from routes.billing import billing
from routes.feedback import feedback
from routes.inventory import inventory
from routes.medical_records import medical_records
from routes.staff import staff

app = Flask(__name__)
app.secret_key = "ad826e665c7e73fc236ee542ee08c0bee72bc7786d7c765bfecd3005169a504d"

# Enable CORS for React frontend
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173'])

# Register Blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(dashboard, url_prefix='/api/dashboard')  
app.register_blueprint(patients, url_prefix='/api/patients')    
app.register_blueprint(doctors, url_prefix='/api/doctors')
app.register_blueprint(appointments, url_prefix='/api/appointments')
app.register_blueprint(billing, url_prefix='/api/billing')
app.register_blueprint(feedback, url_prefix='/api/feedback')
app.register_blueprint(inventory, url_prefix='/api/inventory')
app.register_blueprint(medical_records, url_prefix='/api/medical')
app.register_blueprint(staff, url_prefix='/api/staff')

@app.route('/')
def home():
    return jsonify({
        'message': 'Hospital Management System API',
        'version': '2.0',
        'endpoints': [
            '/api/auth/login',
            '/api/auth/register',
            '/api/dashboard',
            '/api/patients',
            '/api/doctors',
            '/api/appointments',
            '/api/billing',
            '/api/feedback',
            '/api/inventory',
            '/api/medical',
            '/api/staff'
        ]
    })

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': 'now'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
