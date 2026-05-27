from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, db
import pickle, os
from datetime import datetime

app = Flask(__name__)

# ── FIREBASE ──
cred = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://roadwatch-system-default-rtdb.firebaseio.com/'   # paste from your Notepad
})

# ── ML MODEL ──
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# ════════════════════════════════════
#  PAGE ROUTES
# ════════════════════════════════════

@app.route('/')
def index():
    return render_template('login.html')   # role-select is now home

@app.route('/user')
def user_portal():
    return render_template('user.html')

@app.route('/driver')
def driver_portal():
    return render_template('driver.html')

@app.route('/toll')
def toll_portal():
    return render_template('toll.html')

@app.route('/admin')
def admin_portal():
    return render_template('admin.html')

# ════════════════════════════════════
#  API ROUTES
# ════════════════════════════════════

@app.route('/potholes')
def get_potholes():
    ref  = db.reference('potholes')
    data = ref.get() or {}
    result = []
    for key, val in data.items():
        val['id'] = key
        result.append(val)
    return jsonify(result)


@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    ref  = db.reference('potholes')
    ref.push({
        'latitude':        data.get('latitude'),
        'longitude':       data.get('longitude'),
        'severity':        data.get('severity', 'Medium'),
        'timestamp':       data.get('timestamp', datetime.now().isoformat()),
        'status':          'active',
        'confirmed_count': data.get('confirmed_count', 1),
        'source':          data.get('source', 'manual'),
        'description':     data.get('description', ''),
        'reporter':        data.get('reporter', 'Anonymous'),
    })
    return jsonify({'success': True})


@app.route('/resolve', methods=['POST'])
def resolve():
    data   = request.get_json()
    pot_id = data.get('id')
    status = data.get('status', 'resolved')   # supports 'forwarded' too
    if not pot_id:
        return jsonify({'error': 'No ID'}), 400
    db.reference(f'potholes/{pot_id}').update({'status': status})
    return jsonify({'success': True})


@app.route('/delete', methods=['POST'])
def delete_pothole():
    data   = request.get_json()
    pot_id = data.get('id')
    if not pot_id:
        return jsonify({'error': 'No ID'}), 400
    db.reference(f'potholes/{pot_id}').delete()
    return jsonify({'success': True})


@app.route('/detect', methods=['POST'])
def detect():
    data       = request.get_json()
    bbox_area  = data.get('bbox_area', 0)
    features   = [[
        bbox_area,
        data.get('depth_estimate', 0),
        data.get('pothole_width_px', 0),
        data.get('brightness_diff', 0),
        data.get('road_type', 0)
    ]]
    severity = model.predict(features)[0]
    db.reference('potholes').push({
        'latitude':        data.get('latitude', 16.5062),
        'longitude':       data.get('longitude', 80.6480),
        'severity':        severity,
        'timestamp':       datetime.now().isoformat(),
        'status':          'active',
        'confirmed_count': 1,
        'source':          'cctv',
    })
    return jsonify({'severity': severity})


@app.route('/classify', methods=['POST'])
def classify():
    data     = request.get_json()
    features = [[
        data.get('crack_area_px', 0),
        data.get('depth_estimate', 0),
        data.get('pothole_width_px', 0),
        data.get('brightness_diff', 0),
        data.get('road_type', 0)
    ]]
    severity = model.predict(features)[0]
    return jsonify({'severity': severity})


# ════════════════════════════════════
if __name__ == '__main__':
    app.run(debug=True)