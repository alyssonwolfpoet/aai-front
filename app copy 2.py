import streamlit as st
import requests

# -------------------------
# 🔗 CONFIG
# -------------------------
API_URL = "http://localhost:8000/api/v1/auth"

st.set_page_config(layout="wide")

# -------------------------
# 🧠 STATE
# -------------------------
if "logado" not in st.session_state:
    st.session_state.logado = False

if "token" not in st.session_state:
    st.session_state.token = None

# -------------------------
# 🔐 FUNÇÕES
# -------------------------
def login_user(email, senha):
    return requests.post(
        f"{API_URL}/login-token",
        params={  # ✅ CORRETO
            "email": email,
            "password": senha
        }
    )

def register_user(email, senha):
    return requests.post(
        f"{API_URL}/register",
        json={
            "email": email,
            "password": senha
        }
    )

# -------------------------
# 🔐 LOGIN / REGISTRO
# -------------------------
if not st.session_state.logado:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🎓 Acesso")

        tab1, tab2 = st.tabs(["Login", "Registrar"])

        # -------------------------
        # LOGIN
        # -------------------------
        with tab1:
            email = st.text_input("Email", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")

            if st.button("Entrar"):
                res = login_user(email, senha)

                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.logado = True
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error(res.text)

        # -------------------------
        # REGISTRO
        # -------------------------
        with tab2:
            email = st.text_input("Novo email", key="reg_email")
            senha = st.text_input("Nova senha", type="password", key="reg_senha")

            if st.button("Registrar"):
                res = register_user(email, senha)

                if res.status_code == 200:
                    st.success("Conta criada!")
                else:
                    st.error(res.json().get("detail", "Erro"))

# -------------------------
# 💬 CHAT
# -------------------------
else:

    st.title("💬 Chat com IA")

    st.success("Você está logado!")

    with st.sidebar:
        st.write("🔐 Token ativo")
        st.caption(st.session_state.token[:30] + "...")

        if st.button("🚪 Sair"):
            st.session_state.logado = False
            st.session_state.token = None
            st.rerun()

    pergunta = st.text_input("Digite sua pergunta")

    if pergunta:
        st.write(f"Você disse: {pergunta}")