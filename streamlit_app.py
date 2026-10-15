import os
import streamlit as st
from predict_news import predict_news_article, load_artifacts

st.set_page_config(
    page_title='VeritasAI - Fake News Detection',
    page_icon='⚡',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('⚡ VeritasAI: Fake News & Misinformation Intelligence Platform')
st.markdown('### Deep Learning NLP Architecture — Sricharan Surakanti')
st.markdown('Accurately identify fabricated stories, clickbait anomalies, and verified journalistic reports using trained sequence neural networks.')

@st.cache_resource
def get_cached_artifacts():
    return load_artifacts()

try:
    model, tokenizer = get_cached_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.warning(f'Note: Deep Learning weights loading error: {e}')

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader('📰 Input News Article or Headline')
    preset_text = st.selectbox(
        'Or select a sample news headline:',
        [
            'Custom Input...',
            'SHOCKING CONSPIRACY: Secret government leaked memo confirms 5G radiation towers are secretly controlling daily global weather and mind waves! Mainstream media is desperately trying to hide this truth from the public!',
            'NASA Perseverance Rover Detects Organic Molecules in Ancient Jezero Crater Lakebed on Mars according to peer-reviewed research published in Nature.',
            'Big Pharma Hiding Miracle 24-Hour Cancer Cure In Common Lemon Peels, corrupt executives furious this leaked out!',
            'The Federal Reserve concluded its two-day policy meeting by voting unanimously to maintain benchmark interest rates amid moderating inflation.'
        ]
    )

    default_val = '' if preset_text == 'Custom Input...' else preset_text
    news_input = st.text_area('News Content to Analyze:', value=default_val, height=180)

    if st.button('🚀 Analyze News Authenticity', type='primary'):
        if news_input.strip() and model_loaded:
            with st.spinner('Processing sequences through trained neural network...'):
                res = predict_news_article(news_input, model, tokenizer)
                verdict = res['verdict']
                conf = res['confidence'] * 100

                st.markdown('---')
                if verdict == 'Real News':
                    st.success(f'✅ Verified Credible News (Confidence: {conf:.1f}%)')
                else:
                    st.error(f'🚨 High Risk Misinformation / Fake News (Confidence: {conf:.1f}%)')

                st.progress(res['real_probability'])
                st.write(f'**Real Probability:** {res["real_probability"] * 100:.1f}% | **Fake Probability:** {res["fake_probability"] * 100:.1f}%')
        elif not news_input.strip():
            st.warning('Please enter or select news text to analyze.')

with col2:
    st.subheader('📊 System Telemetry')
    st.metric(label='Model Architecture', value='BiLSTM + 1D-CNN')
    st.metric(label='Validation Accuracy', value='96.2%')
    st.metric(label='Max Sequence Length', value='200 Tokens')
    st.info('VeritasAI evaluates linguistic patterns, sensational phrasing, and syntactic anomalies to output an objective probabilistic veracity score.')
