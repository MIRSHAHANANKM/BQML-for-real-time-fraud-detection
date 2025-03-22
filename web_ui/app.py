import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random


# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Route for dashboard
@app.route('/')
def index():
    return render_template('index.html')


# Background function to emit fake fraud alerts every few seconds
def emit_fake_fraud_alerts():
    while True:
        alert = generate_fake_alert()
        print("🚨 Sending alert:", alert)
        socketio.emit('fraud_update', alert)
        time.sleep(3)


# Utility function to generate a fake alert
def generate_fake_alert():
    return {
        "transaction_id": random.randint(1000, 9999),
        "amount": round(random.uniform(50, 5000), 2),
        "risk_score": round(random.uniform(0, 1), 2),
        "user_behavior": round(random.uniform(0, 1), 2),
        "device_trust": round(random.uniform(0, 1), 2),
        "signup_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "purchase_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "device_id": f"device_{random.randint(100, 999)}",
        "browser": random.choice(["Chrome", "Firefox", "Safari"]),
        "source": random.choice(["ad", "organic", "referral"]),
        "age": random.randint(18, 60)
    }


# Start background thread for emitting alerts
def start_background_thread():
    alert_thread = threading.Thread(target=emit_fake_fraud_alerts)
    alert_thread.daemon = True
    alert_thread.start()


# Entry point
if __name__ == '__main__':
    start_background_thread()
    print(" Real-time fraud alert server running on http://127.0.0.1:5000")
    socketio.run(app, host='127.0.0.1', port=5000)



