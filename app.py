import streamlit as st
import requests

# -------------------------
# 🔗 CONFIG
# -------------------------
API_URL = "http://localhost:8000/api/v1/auth"
IAAPI_URL = "http://localhost:8000/api/v1/llm"

st.set_page_config(layout="wide")

# -------------------------
# 🧠 STATE
# -------------------------
if "logado" not in st.session_state:
    st.session_state.logado = False

if "token" not in st.session_state:
    st.session_state.token = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# 🔐 FUNÇÕES
# -------------------------
def login_user(email, senha):
    return requests.post(
        f"{API_URL}/login-token",
        params={
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

def chat(prompt):
    return requests.post(
        f"{IAAPI_URL}/llm",
        params={
            "prompt": prompt
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

        # LOGIN
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

        # REGISTRO
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
# 💬 CHAT (SÓ SE LOGADO)
# -------------------------
else:

    st.title("🎓 Auxiliador de Estudos com IA")

    # -------------------------
    # ⚙️ SIDEBAR
    # -------------------------
    with st.sidebar:
        st.header("⚙️ Configurações")

        modo = st.radio(
            "Modo de uso",
            ["Documentos (RAG)", "Internet", "YouTube", "Ferramentas"]
        )

        url = st.text_input("Link (opcional)")

        st.divider()
        st.write("🔐 Token ativo")
        st.caption(st.session_state.token[:30] + "...")

        if st.button("🚪 Sair"):
            st.session_state.logado = False
            st.session_state.token = None
            st.session_state.messages = []
            st.rerun()

    # -------------------------
    # 📜 CHAT
    # -------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -------------------------
    # ⌨️ INPUT
    # -------------------------
    pergunta = st.chat_input("Digite sua pergunta...")

    if pergunta:
        st.session_state.messages.append({
            "role": "user",
            "content": pergunta
        })

        # -------------------------
        # 🧠 BACKEND SIMULADO (SEUS MODOS)
        # -------------------------
        if modo == "Documentos (RAG)":
            resposta = f"[RAG] Respondendo com base nos seus arquivos: {pergunta}"

        elif modo == "Internet":
            resposta = f"[WEB] Buscando na internet: {pergunta}"

        elif modo == "YouTube":
            if url:
                resposta = f"[YOUTUBE] Resumindo vídeo: {url}"
            else:
                resposta = "Envie um link do YouTube"

        elif modo == "Ferramentas":
            resposta = f"[TOOLS] Executando ferramenta para: {pergunta}"

        # -------------------------
        # 💬 RESPOSTA
        # -------------------------

        resposta = chat(resposta)
        print(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": resposta.json()["response"]
        })

        print(resposta)

        st.rerun()