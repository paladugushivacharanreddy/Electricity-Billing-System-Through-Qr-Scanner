from flask import Flask, request, jsonify, render_template
import mysql.connector
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import os

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="billing_user",
        password="password",
        database="billing_system"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        address = request.form['address']
        meter_number = request.form['meter_number']
        amount_due = float(request.form['amount_due'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, address, meter_number, amount_due) VALUES (%s, %s, %s, %s)',
                       (name, address, meter_number, amount_due))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        data = request.form['meter_number']
        img = qrcode.make(data)
        qr_code_path = f'static/qr_codes/{data}.png'
        img.save(qr_code_path)
        return jsonify({'message': 'QR code generated successfully!', 'qr_code': qr_code_path})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    try:
        file = request.files['qr_code']
        image = Image.open(file)
        decoded_objects = decode(image)
        if decoded_objects:
            meter_number = decoded_objects[0].data.decode('utf-8')
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE meter_number = %s', (meter_number,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return jsonify({'name': user['name'], 'address': user['address'], 'amount_due': user['amount_due']})
        return jsonify({'error': 'QR code not recognized or user not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    if not os.path.exists('static/qr_codes'):
        os.makedirs('static/qr_codes')
    app.run(debug=True)
