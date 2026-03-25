from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ml_model import detector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(200))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='sent')

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database ready!")

@app.route('/')
def home():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(5).all()
    return render_template('index.html', recent_alerts=alerts)

@app.route('/sos', methods=['POST'])
def sos_alert():
    """Handle SOS button press"""
    data = request.json
    
    # Get location from frontend
    location = data.get('location', 'Location unavailable')
    message = data.get('message', '🚨 EMERGENCY SOS ALERT 🚨')
    
    # Save to database
    alert = Alert(message=message, location=location)
    db.session.add(alert)
    db.session.commit()
    
    # SIMULATE SMS (Real Twilio can be added later)
    print("\n🚨" + "="*50)
    print(f"📱 EMERGENCY ALERT!")
    print(f"📍 Location: {location}")
    print(f"💬 Message: {message}")
    print(f"🕐 Time: {alert.timestamp}")
    print("="*50 + "\n")
    
    return jsonify({
        'status': 'success',
        'alert_id': alert.id,
        'message': 'Alert sent to emergency contacts!'
    })

@app.route('/voice-check', methods=['POST'])
def voice_check():
    """ML Distress Detection"""
    text = request.json.get('text', '')
    
    # ML Prediction
    is_distress, confidence = detector.predict(text)
    
    response = {
        'text': text,
        'is_distress': bool(is_distress),
        'confidence': float(confidence),
        'action': 'ALERT' if is_distress else 'OK'
    }
    
    print(f"🎤 Voice: '{text}' → Distress: {is_distress} ({confidence:.2f})")
    return jsonify(response)

@app.route('/history')
def history():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    return render_template('history.html', alerts=alerts)

@app.route('/test-ml')
def test_ml():
    """Test ML model - for demo"""
    tests = [
        "help me", "sos", "normal talk", "emergency", "hello", "save me"
    ]
    results = []
    for text in tests:
        is_distress, conf = detector.predict(text)
        results.append({'text': text, 'distress': is_distress, 'confidence': conf})
    return jsonify(results)

if __name__ == '__main__':
    print("🚀 Women Safety Alert System Starting...")
    print("📱 Open: http://localhost:5000")
    app.run(debug=True)