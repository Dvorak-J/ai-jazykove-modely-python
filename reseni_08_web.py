# Řešení: webový ŠkolBot s teplotou, počtem zpráv a stažením konverzace
# Spuštění v terminálu:  streamlit run reseni_08_web.py
import json
from pathlib import Path

import streamlit as st

from llm import MODEL, klient

SYSTEM = (Path(__file__).parent / "system_prompt.txt").read_text(encoding="utf-8")

st.title("ŠkolBot")
st.caption(f"Model: {MODEL}")

if "zpravy" not in st.session_state:
    st.session_state.zpravy = [{"role": "system", "content": SYSTEM}]

if st.sidebar.button("Nová konverzace"):
    st.session_state.zpravy = [{"role": "system", "content": SYSTEM}]

# 1) výběr teploty
teplota = st.sidebar.slider("Teplota", 0.0, 1.5, 0.7)

for zprava in st.session_state.zpravy[1:]:
    with st.chat_message(zprava["role"]):
        st.markdown(zprava["content"])

if dotaz := st.chat_input("Na co se chceš zeptat?"):
    st.session_state.zpravy.append({"role": "user", "content": dotaz})
    with st.chat_message("user"):
        st.markdown(dotaz)
    with st.chat_message("assistant"):
        proud = klient.chat.completions.create(
            model=MODEL, messages=st.session_state.zpravy,
            temperature=teplota, stream=True,
        )
        odpoved = st.write_stream(proud)
    st.session_state.zpravy.append({"role": "assistant", "content": odpoved})

# 2) počet zpráv (bez systémové) a 3) stažení konverzace
st.sidebar.write(f"Zpráv v konverzaci: {len(st.session_state.zpravy) - 1}")
st.sidebar.download_button(
    "Stáhnout konverzaci (JSON)",
    data=json.dumps(st.session_state.zpravy, ensure_ascii=False, indent=2),
    file_name="konverzace.json",
    mime="application/json",
)
