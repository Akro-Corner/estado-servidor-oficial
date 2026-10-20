from datetime import datetime
import streamlit as st

# --- Page Setup ---
st.set_page_config(
    page_title="Estado Actual Servidor", page_icon="⛏️", layout="centered"
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
            "date": "20/10/26 18:18",
            "msg": "Servidor apagado debido a mantenimiento y uso del servidor para actividades extracurriculares.",
        },
    ]

# Server Details (Change these to your actual details)
SERVER_IP = "practically-xii.tun.ply.gg"
SERVER_PORT = "25565"
MODPACK_LINK = "lo tienes en el Whatsapp."

# --- Sidebar Admin Panel ---
with st.sidebar.expander("🔒 Admin Panel", expanded=not st.session_state.authenticated):
    if not st.session_state.authenticated:
        st.write("Incio de sesión")
        with st.form("admin_login_form"):
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            if st.form_submit_button("Iniciar Sesión"):
                try:
                    # Authenticate against st.secrets
                    secret_user = st.secrets["admin_credentials"]["username"]
                    secret_pass = st.secrets["admin_credentials"]["password"]

                    if user_input == secret_user and pass_input == secret_pass:
                        st.session_state.authenticated = True
                        st.success("Autenticado")
                        st.rerun()
                    else:
                        st.error("Contraseña inválida")
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
st.title("Monitor Servidor")
st.caption("Monitor del servidor.")
st.divider()

# Section 1: Server IP & Status
st.subheader("🌐 Estado y IP")

col_ip, col_port = st.columns([3, 1])
with col_ip:
    st.code(SERVER_IP, language="text")
with col_port:
    st.code(SERVER_PORT, language="text")

current_status = st.session_state.server_status

if current_status == "Online":
    st.success("### Status: 🟢 ONLINE")
    st.write("Encendido y listo para entrar.")
elif current_status == "Under Maintenance":
    st.warning("### Status: 🛠️ BAJO MANTENIMIENTO")
    st.info("Servidor bajo mantenimiento, mirar registros para la hora de retorno.")
else:
    st.error("### Status: 🔴 OFFLINE")
    st.write("Servidor apagado.")

st.divider()

# Section 2: Modpack Download
st.subheader("📦 Descargar Modpack Servidor")
st.write("Download the required modpack file to connect and join the world.")

st.write("*GRUPO DE WHATSAPP*")

st.divider()

# Section 3: Maintenance & Update Logs
st.subheader("📋 Mantenimiento y registros")

if st.session_state.maintenance_logs:
    for entry in st.session_state.maintenance_logs:
        with st.container():
            st.markdown(f"**`[{entry['date']}]`**")
            st.info(entry["msg"])
else:
    st.write("Ningún registro de mantenimiento publicado.")

st.divider()
st.caption("Tip: Admins can log in using the sidebar panel to change status and publish update logs.")