from flask import Flask, request, jsonify
import sqlite3
import datetime

import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hello World"

def insert_crowd_data(gate,count):
    conn = sqlite3.connect('crowd_data.db')
    cursor = conn.cursor()
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO crowd (gate, count, timestamp) VALUES (?, ?, ?)", (gate, count, timestamp))
    conn.commit()
    conn.close()


@app.route('/update_crowd', methods=['POST'])
def update_crowd():
    data=request.get_json()
    gate=data.get("gate")
    count=data.get("count")
    if gate is None or count is None:
        return jsonify({"error":"Invalid Data"}), 400
    insert_crowd_data(gate,count)
    return jsonify({"message":"Data Inserted"}), 200

@app.route('/show_crowd', methods=['GET'])
def show_crowd():
    conn=sqlite3.connect("crowd_data.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM crowd ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()

    return jsonify(data)

# @app.route('/optimize', methods=['GET'])
# def show_optimize():
#     limit_A=380
#     limit_B=380
#     conn=sqlite3.connect("crowd_data.db")
#     cursor=conn.cursor()
#     cursor.execute("SELECT count from crowd WHERE gate='Gate A' ORDER BY timestamp DESC LIMIT 1")
#     gate_A=cursor.fetchone()
#     cursor.execute("SELECT count from crowd WHERE gate='Gate B' ORDER BY timestamp DESC LIMIT 1")
#     gate_B=cursor.fetchone()
#     conn.close()

#     gate_A=gate_A[0] if gate_A else 0
#     gate_B=gate_B[0] if gate_B else 0
#     if gate_A>=limit_A and gate_B>=limit_B:
#         msg="Warning! Both gates are congested. Notify authorities."

#     if gate_A>=limit_A and gate_B<limit_B:
#         msg="Redirecting traffic from Gate A to Gate B"

#     if gate_B>=limit_B and gate_A<limit_A:
#         msg="Redirecting traffic from Gate B to Gate A"

#     return render_template("optimize.html", )

if __name__ == '__main__':
    app.run(debug=True)



