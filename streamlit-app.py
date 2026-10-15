import streamlit as st
from models.deep_learning_model import get_classifier

st.set_page_config(page_title="VeritasAI - Fake News Detection", page_icon="⚡", layout="wide")

st.title("⚡ VeritasAI: Fake News & Misinformation Detector")
st.write("Deep Learning NLP Intelligence Platform by Sricharan Surakanti")

classifier = get_classifier()

text_input = st.text_area("Enter News Article / Headline to Analyze:", height=150)

if st.button("Analyze News Content", type="primary"):
    if text_input.strip():
        with st.spinner("Analyzing linguistic patterns & neural weights..."):
            result = classifier.predict(text_input)
            
            is_fake = result.get("is_fake", False)
            confidence = result.get("confidence", 0.0)
            
            if is_fake:
                st.error(f"🚨 Verdict: High Risk Misinformation ({confidence:.1f}% confidence)")
            else:
                st.success(f" Verified Credible News ({confidence:.1f}% confidence)")
                
            st.json(result)
    else:
        st.warning("Please enter some text to analyze.")
