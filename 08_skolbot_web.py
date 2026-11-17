# ŠkolBot ve webovém prohlížeči
# Spuštění v terminálu:  streamlit run 08_skolbot_web.py
from pathlib import Path

import streamlit as st

from llm import MODEL, klient

SYSTEM = (Path(__file__).parent / "system_prompt.txt").read_text(encoding="utf-8")

st.title("ŠkolBot")
st.caption(f"Model: {MODEL}")

# st.session_state přežije překreslení stránky (Streamlit spouští skript
# při každé akci uživatele znovu od začátku)
if "zpravy" not in st.session_state:
    st.session_state.zpravy = [{"role": "system", "content": SYSTEM}]

if st.sidebar.button("Nová konverzace"):
    st.session_state.zpravy = [{"role": "system", "content": SYSTEM}]

# vykreslíme dosavadní konverzaci (bez systémové zprávy)
for zprava in st.session_state.zpravy[1:]:
    with st.chat_message(zprava["role"]):
        st.markdown(zprava["content"])

if dotaz := st.chat_input("Na co se chceš zeptat?"):
    st.session_state.zpravy.append({"role": "user", "content": dotaz})
    with st.chat_message("user"):
        st.markdown(dotaz)
    with st.chat_message("assistant"):
        proud = klient.chat.completions.create(
            model=MODEL, messages=st.session_state.zpravy, stream=True
        )
        odpoved = st.write_stream(proud)
    st.session_state.zpravy.append({"role": "assistant", "content": odpoved})
