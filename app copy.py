import streamlit as st

st.title("🎓 Auxiliador de Estudos com IA")

# -------------------------
# 🧠 MEMÓRIA
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# ⚙️ SIDEBAR (PROFISSIONAL)
# -------------------------
with st.sidebar:
    st.header("⚙️ Configurações")

    modo = st.radio(
        "Modo de uso",
        ["Documentos (RAG)", "Internet", "YouTube", "Ferramentas"]
    )

    url = st.text_input("Link (opcional)")

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
    # 🧠 BACKEND BASEADO NO MODO
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

    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta
    })

    st.rerun()