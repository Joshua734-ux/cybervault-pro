import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- JOSHUA-MAXWELL STEALTH CONFIG ---
COMMISSION_RATE = 0.10  # Your 10% Cut
PAYOUT_NUMBER = "0708725402"  # Your Payout Bridge
VAULT_VERSION = "1.0.0-Stealth"

@app.route('/')
def index():
    return f"<h1>Maxwell Vault Active</h1><p>System Status: {VAULT_VERSION}</p>"

@app.route('/process-transaction', methods=['POST'])
def process_transaction():
    data = request.get_json()
    total_amount = float(data.get('amount', 0))
    
    # The 10% Logic
    joshua_cut = total_amount * COMMISSION_RATE
    client_payout = total_amount - joshua_cut
    
    return jsonify({
        "status": "Success",
        "total": total_amount,
        "joshua_commission": joshua_cut,
        "payout_to": PAYOUT_NUMBER,
        "client_amount": client_payout
    })

# --- SECURITY FIREWALL ---
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)