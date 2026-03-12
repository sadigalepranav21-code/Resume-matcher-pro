import streamlit as st
import PyPDF2
from engine import calculate_similarity, analyze_keywords
from datetime import datetime

st.set_page_config(page_title="AI Resume Optimizer Pro", layout="wide")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in pdf_reader.pages])

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Resume Optimizer Pro")
st.caption("Deployment-Ready NLP System for Career Optimization")

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.subheader("📋 Input Details")
    job_description = st.text_area("Job Description", height=200, placeholder="Paste the job requirements here...")
    
    st.markdown("---")
    input_type = st.radio("Resume Input Method", ["Upload PDF", "Paste Text"])
    
    resume_text = ""
    if input_type == "Upload PDF":
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = st.text_area("Paste Resume Content", height=200)

if st.button("Analyze My Compatibility"):
    if resume_text and job_description:
        with st.spinner("Analyzing semantics and keywords..."):
            score = calculate_similarity(resume_text, job_description)
            found, missing = analyze_keywords(resume_text, job_description)
            
            with col_out:
                st.subheader("📊 Analysis Results")
                st.metric(label="Overall Match Score", value=f"{score}%")
                
                # Visual Match Bar
                if score > 70:
                    st.success("Strong Match! You're ready to apply.")
                elif score > 40:
                    st.warning("Average Match. Consider adding missing keywords.")
                else:
                    st.error("Low Match. This resume needs significant optimization.")

                # Skills Breakdown
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**✅ Skills Found**")
                    for s in found: st.write(f"✔️ {s}")
                with c2:
                    st.write("**❌ Skills Missing**")
                    for m in missing: st.write(f"✖️ {m}")

                # Report Generation
                report = f"Date: {datetime.now()}\nMatch: {score}%\nMissing: {', '.join(missing)}"
                st.download_button("📥 Download Summary Report", data=report, file_name="analysis.txt")
    else:
        st.error("Please provide both inputs to continue.")