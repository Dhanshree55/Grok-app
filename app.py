import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# ------------------ SETUP ------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = Groq(api_key=api_key)

st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="🧠",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
/* Full black background */
body {
    background-color: #0a0a0a;
}

/* Hide Streamlit default header/footer */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Center container */
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Title styling */
.title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ffffff, #888);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    color: #aaa;
    text-align: center;
    margin-bottom: 40px;
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 25px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* Text area */
textarea {
    background-color: #111 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="title">🧠 AI Notes Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate clean, structured notes instantly</div>', unsafe_allow_html=True)

# ------------------ INPUT UI ------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    topic = st.text_input("", placeholder="Ask anything...")
    mode = st.selectbox("Mode", ["Detailed", "Short"])

    generate = st.button("✨ Generate Notes")

# ------------------ FUNCTION ------------------
def generate_notes(topic, mode):
    if mode == "Short":
        detail = "Keep it concise."
    else:
        detail = "Provide detailed explanations with examples."

    prompt = f"""
Generate structured study notes on: {topic}

- Use headings and subheadings
- Use bullet points
- Add real-world examples
- {detail}
- Add summary at end
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ------------------ OUTPUT ------------------
if generate and topic:
    with st.spinner("Generating notes..."):
        notes = generate_notes(topic, mode)

    st.markdown("---")

    colA, colB, colC = st.columns([1,2,1])
    with colB:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(notes)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download Notes",
            data=notes,
            file_name=f"{topic}.txt",
            mime="text/plain"
        )

        # Copy button (simple)
        st.code(notes, language="markdown")

elif generate:
    st.warning("Please enter a topic first ⚠️")