import streamlit as st
import sqlite3
import pandas as pd
import time

def get_latest_data():
    conn=sqlite3.connect("crowd_data.db")
    cursor=conn.cursor()
    query="SELECT gate, count, timestamp FROM crowd ORDER BY timestamp DESC LIMIT 10"
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df

st.title("Attendance - Gate Optimization Dashboard")

st.subheader("Live Crowd Data")
placeholder=st.empty()

while True:
    data=get_latest_data()
    placeholder.dataframe(data)

    latest_A = data[data["gate"] == "Gate A"]["count"].iloc[0] if not data[data["gate"] == "Gate A"].empty else 0
    latest_B = data[data["gate"] == "Gate B"]["count"].iloc[0] if not data[data["gate"] == "Gate B"].empty else 0

    if latest_A >= 350:
        st.error("⚠️ Gate A is congested! Open Gate B.")
    if latest_B >= 380:
        st.error("⚠️ Gate B is congested! Open Gate A.")
    if latest_A >= 350 and latest_B >= 380:
        st.error("🚨 Warning! Both gates are overloaded. Notify authorities.")

    time.sleep(5)


