"""
AHRE Security Dashboard Backend API & Web Server (Member 3 Module)
"""

from flask import Flask, jsonify, render_template, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RISK_FILE = os.path.join(BASE_DIR, "data/processed/user_risk_scores.csv")

def get_risk_data():
    if os.path.exists(RISK_FILE):
        return pd.read_csv(RISK_FILE)
    return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/kpi')
def get_kpi():
    df = get_risk_data()
    if df.empty:
        return jsonify({"total_users": 0, "critical_threats": 0, "avg_risk": 0, "total_events": 0})
    
    total_users = df['user'].nunique()
    critical = df[df['risk_category'] == 'CRITICAL']['user'].nunique()
    avg_risk = round(df['risk_score'].mean(), 1)
    total_events = int(df['total_logons'].sum() + df['usb_connect_count'].sum())
    
    return jsonify({
        "total_users": total_users,
        "critical_threats": critical,
        "avg_risk": avg_risk,
        "total_events": total_events
    })

@app.route('/api/users')
def get_user_risk():
    df = get_risk_data()
    if df.empty:
        return jsonify([])
    
    # Get latest risk profile per user
    latest_df = df.sort_values(by=['day', 'risk_score'], ascending=[False, False]).groupby('user').first().reset_index()
    latest_df = latest_df.sort_values(by='risk_score', ascending=False)
    
    result = latest_df[['user', 'day', 'risk_score', 'risk_category', 'failed_logins', 'off_hours_logins', 'usb_connect_count', 'file_copy_count', 'explanation']].to_dict(orient='records')
    return jsonify(result)

@app.route('/api/user/<user_id>/timeline')
def get_user_timeline(user_id):
    df = get_risk_data()
    if df.empty:
        return jsonify([])
    
    user_df = df[df['user'] == user_id].sort_values(by='day')
    result = user_df[['day', 'risk_score', 'risk_category', 'failed_logins', 'usb_connect_count']].to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    print("Starting AHRE Security Dashboard on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
