import sqlite3
import time
# import request
window_size=5
limit_A=350
limit_B=380

def moving_average(gate):
    conn=sqlite3.connect("crowd_data.db")
    cursor=conn.cursor()
    cursor.execute("SELECT count FROM crowd WHERE gate = ? ORDER BY timestamp DESC LIMIT ?",(gate,window_size))
    data=cursor.fetchall()
    conn.close()

    count=[row[0] for row in data]

    if len(count)<window_size:
        return "Insufficient data"
    return sum(count)/len(count)

def predict_trend():
    avg_A=moving_average("Gate A")
    avg_B=moving_average("Gate B")

    if isinstance(avg_A,float) and isinstance(avg_B,float):
        print(f"Predicted trend: Gate A:{avg_A}, Gate B:{avg_B}")
        msg=f"Predicted trend: Gate A:{avg_A}, Gate B:{avg_B}"
    else:
        print("Insufficient data for prediction")
        msg="Insufficient data for prediction"

def optimize_gates():
    global latest_message
    conn=sqlite3.connect("crowd_data.db")
    cursor=conn.cursor()
    cursor.execute("SELECT count from crowd WHERE gate='Gate A' ORDER BY timestamp DESC LIMIT 1")
    gate_A=cursor.fetchone()
    cursor.execute("SELECT count from crowd WHERE gate='Gate B' ORDER BY timestamp DESC LIMIT 1")
    gate_B=cursor.fetchone()
    conn.close()

    gate_A=gate_A[0] if gate_A else 0
    gate_B=gate_B[0] if gate_B else 0
    if gate_A>=limit_A and gate_B>=limit_B:
        print("Warning! Both gates are congested. Notify authorities.")
        msg="Warning! Both gates are congested. Notify authorities."

    if gate_A>=limit_A and gate_B<limit_B:
        print(f"Gate A= {gate_A}: Redirecting traffic from Gate A to Gate B")
        msg=f"Gate A= {gate_A}: Redirecting traffic from Gate A to Gate B"

    if gate_B>=limit_B and gate_A<limit_A:
        print(f"Gate B= {gate_B}: Redirecting traffic from Gate B to Gate A")
        msg=f"Gate B= {gate_B}: Redirecting traffic from Gate B to Gate A"

    # try:
    #     request.post("http://127.0.0.1:5000/update_message",json={"message":msg})
    # except:
    #     print("Error sending data to server")
    # return msg

if __name__ == "__main__":
    while True:
        predict_trend() 
        optimize_gates()  
        print("\n------------------------\n")
        time.sleep(2)

