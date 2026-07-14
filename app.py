import streamlit as st
from openai import OpenAI

# -----------------------------
# Configure API
# -----------------------------
client = OpenAI(
    base_url=st.secrets["BASE_URL"],
    api_key=st.secrets["NVIDIA_API_KEY"]
)

system_prompt = st.secrets["SYSTEM_PROMPT"]

MODEL = "openai/gpt-oss-20b"

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="Odoo XML Migration Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Odoo XML Migration Assistant")
st.caption("AI-powered Odoo XML migration and compatibility assistant.")
# -----------------------------
# Session State
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# XML Input
# -----------------------------
xml_code = st.text_area(
    "Odoo XML Source",
    height=450,
    placeholder="""Paste your Odoo XML here..."""
)

# -----------------------------
# Convert Button
# -----------------------------
convert = st.button(
    "🚀 Migrate to Odoo 19",
    type="primary",
    use_container_width=True,
    disabled=not xml_code.strip()
)

if convert:


    user_prompt = f"""
Convert the following XML to Odoo v19.

{xml_code}
"""

    with st.spinner("🤖 AI is migrating your XML..."):

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.2,
            )

            answer = response.choices[0].message.content

        except Exception as e:
            answer = f"❌ {e}"

    st.session_state.history.insert(
        0,
        {
            "input": xml_code,
            "output": answer
        }
    )

# -----------------------------
# Output
# -----------------------------
if st.session_state.history:

    st.divider()

    latest = st.session_state.history[0]

    st.subheader("Migration Result")

    st.markdown(latest["output"])