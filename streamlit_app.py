from datetime import datetime
import streamlit as st

# --- Page Setup ---
st.set_page_config(
    page_title="Minecraft Server Hub", page_icon="⛏️", layout="centered"
)

# --- Initialize Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Default Status: "Online", "Offline", or "Under Maintenance"
if "server_status" not in st.session_state:
    st.session_state.server_status = "Online"

# Initial Maintenance Logs
if "maintenance_logs" not in st.session_state:
    st.session_state.maintenance_logs = [
        {
            "date": "2026-03-20 14:00",
            "msg": "Server updated to Modpack v1.2! Added new tech mods and bug fixes.",
        },
        {
            "date": "2026-03-15 10:30",
            "msg": "Routine maintenance completed. World backup created.",
        },
    ]

# Server Details (Change these to your actual details)
SERVER_IP = "play.yourserver.com"
SERVER_PORT = "25565"
MODPACK_LINK = "https://your-modpack-download-link.com/modpack.zip"

# --- Sidebar Admin Panel ---
with st.sidebar.expander("🔒 Admin Panel", expanded=not st.session_state.authenticated):
    if not st.session_state.authenticated:
        st.write("Sign in to manage status and post logs.")
        with st.form("admin_login_form"):
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            if st.form_submit_button("Log In"):
                try:
                    # Authenticate against st.secrets
                    secret_user = st.secrets["admin_credentials"]["username"]
                    secret_pass = st.secrets["admin_credentials"]["password"]

                    if user_input == secret_user and pass_input == secret_pass:
                        st.session_state.authenticated = True
                        st.success("Authenticated!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                except KeyError:
                    st.error("Admin secrets missing in `.streamlit/secrets.toml`!")
    else:
        st.write("🟢 **Logged in as Admin**")

        # 1. Server Status Selector
        st.divider()
        st.write("### ⚙️ Update Server Status")
        status_options = ["Online", "Offline", "Under Maintenance"]
        selected_status = st.selectbox(
            "Current State:",
            options=status_options,
            index=status_options.index(st.session_state.server_status),
        )
        if selected_status != st.session_state.server_status:
            st.session_state.server_status = selected_status
            st.toast(f"Status changed to {selected_status}!")
            st.rerun()

        # 2. Add Maintenance Log Entry
        st.divider()
        st.write("### 📝 Post Maintenance Log")
        log_input = st.text_area("Log Message", placeholder="e.g. Updating plugins and restarting server...")
        if st.button("Post Log"):
            if log_input.strip():
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.maintenance_logs.insert(
                    0, {"date": now_str, "msg": log_input.strip()}
                )
                st.success("Log entry posted!")
                st.rerun()
            else:
                st.warning("Please enter a log message first.")

        # 3. Log Out
        st.divider()
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.rerun()

# --- Main App Interface ---
st.title("⛏️ Minecraft Server Hub")
st.caption("Official server dashboard, modpack download, and maintenance tracker.")
st.divider()

# Section 1: Server IP & Status
st.subheader("🌐 Server Address & Live Status")

col_ip, col_port = st.columns([3, 1])
with col_ip:
    st.code(SERVER_IP, language="text")
with col_port:
    st.code(SERVER_PORT, language="text")

current_status = st.session_state.server_status

if current_status == "Online":
    st.success("### Status: 🟢 ONLINE")
    st.write("The server is live! You can connect right now.")
elif current_status == "Under Maintenance":
    st.warning("### Status: 🛠️ UNDER MAINTENANCE")
    st.info("The server is currently down for maintenance or updates. Check the logs below!")
else:
    st.error("### Status: 🔴 OFFLINE")
    st.write("The server is currently offline.")

st.divider()

# Section 2: Modpack Download
st.subheader("📦 Download Server Modpack")
st.write("Download the required modpack file to connect and join the world.")

st.link_button("📥 Download Modpack (.zip)", MODPACK_LINK, use_container_width=True)

st.divider()

# Section 3: Maintenance & Update Logs
st.subheader("📋 Maintenance Logs & Updates")

if st.session_state.maintenance_logs:
    for entry in st.session_state.maintenance_logs:
        with st.container():
            st.markdown(f"**`[{entry['date']}]`**")
            st.info(entry["msg"])
else:
    st.write("No maintenance logs recorded yet.")

st.divider()
st.caption("Tip: Admins can log in using the sidebar panel to change status and publish update logs.")