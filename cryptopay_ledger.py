import streamlit as st
import hashlib
from datetime import datetime

# --- App Configuration ---
st.set_page_config(page_title="CryptoPay Ledger", page_icon="💸", layout="wide")

# --- Initialize state ---
if "ledger" not in st.session_state:
    st.session_state.ledger = []

# --- Sidebar Input ---
st.sidebar.title("💰 Create New Payment")

col1 = st.sidebar.text_input("From")
col2 = st.sidebar.text_input("To")
col3 = st.sidebar.number_input("Amount (in coins)", min_value=0.0, step=0.01)

if st.sidebar.button("Add Payment"):
    if not col1 or not col2 or col3 == 0:
        st.sidebar.warning("All fields are required.")
    else:
        # Data and hash generation
        payload = f"{col1}->{col2}:{col3}-{datetime.now()}"
        unique_id = hashlib.sha256(payload.encode()).hexdigest()

        st.session_state.ledger.append({
            "from": col1,
            "to": col2,
            "amount": col3,
            "hash": unique_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.sidebar.success("Payment successfully recorded!")

# --- Main Area ---
st.title("💳 CryptoPay Ledger")
st.caption("A minimal blockchain-inspired transaction visualizer")

if st.session_state.ledger:
    for index, record in enumerate(reversed(st.session_state.ledger), 1):
        color_bg = "#f0ffe0" if index % 2 == 0 else "#e6f3ff"
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color:{color_bg};
                    padding:12px 15px;
                    border-left:5px solid #4CAF50;
                    border-radius:8px;
                    margin-bottom:8px;
                ">
                    <b>From:</b> {record['from']} <br>
                    <b>To:</b> {record['to']} <br>
                    <b>Amount:</b> {record['amount']} coins<br>
                    <b>Timestamp:</b> {record['timestamp']}<br>
                    <b>Tx Hash:</b> <code>{record['hash'][:32]}...</code>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("No payments recorded yet. Start by adding one from the sidebar!")
