import streamlit as st
import mysql.connector
import re

# ---------- DATABASE CONNECTION ----------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",     
        password="1111", 
        database="user_management")


def is_strong(password):
    if len(password) < 8: return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"\d", password): return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False
    return True

# ---------- SIGNUP FUNCTION ----------

def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cur.fetchone():
        conn.close()
        return "Username already exists!"
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s,%s)",
                (username, password))  
    conn.commit()
    conn.close()
    return "Signup successful!"

# ---------- LOGIN FUNCTION ----------

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return "Username does not exist!"
    return "Login successful!" if row[0] == password else "Incorrect password!"

# ---------- UPDATE USER FUNCTION ----------

def update_user(old_username, new_username, new_password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=%s, password_hash=%s WHERE username=%s",
                (new_username, new_password, old_username))
    conn.commit()
    conn.close()
    return "Account updated successfully!"

# ---------- DELETE USER FUNCTION ----------

def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username=%s", (username,))
    conn.commit()
    conn.close()
    return "Account deleted!"



# ---------- STREAMLIT UI ----------


st.title("User Management System")

menu = ["Signup", "Login"]
choice = st.sidebar.selectbox("Menu", menu)


# ---------- SIGNUP PAGE ----------

if choice == "Signup":
    st.subheader("Signup")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    p2 = st.text_input("Retype Password", type="password")
    if st.button("Create Account"):
        if len(u) < 5:
            st.error("Username must be at least 5 characters long.")
        elif not is_strong(p):
            st.error("Password not strong enough.")
        elif p != p2:
            st.error("Passwords do not match.")
        else:
            st.success(signup(u, p))


# ---------- LOGIN PAGE ----------

elif choice == "Login":
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        msg = login(u, p)
        if msg == "Login successful!":
            st.session_state["user"] = u
            st.success(f"Welcome {u}")
        else:
            st.error(msg)


# ---------- USER DASHBOARD ----------

    if "user" in st.session_state:
        st.subheader("Welcome Page")
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        if st.button("Update Account"):
            st.success(update_user(st.session_state["user"], new_u, new_p))
            st.session_state["user"] = new_u
        if st.button("Delete Account"):
            st.warning(delete_user(st.session_state["user"]))
            del st.session_state["user"]

