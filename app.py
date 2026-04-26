import streamlit as st
import json
import re
from job_analyzer import analyze_job
from resume_generator import generate_resume, save_resume_to_word

st.set_page_config(page_title="AI Job Agent", layout="wide")

st.title("🚀 AI Job Application Agent - Sreekanth")

job_desc = st.text_area("📌 Paste Job Description Here")

# Load resume
resume = open("resume_master.txt", encoding="utf-8").read()

# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Job"):

    if job_desc.strip() == "":
        st.warning("Please paste a job description")

    else:
        result = analyze_job(job_desc, resume)

        try:
            # Clean AI response
            cleaned = result.strip()
            cleaned = re.sub(r"```json|```", "", cleaned).strip()

            data = json.loads(cleaned)

            # 🎯 Match Score
            st.subheader("🎯 Match Score")
            st.metric("Fit", f"{data.get('match_score', 'N/A')}%")

            # 📌 Decision
            st.subheader("📌 Apply Decision")
            st.write(f"**{data.get('decision', 'N/A')}**")
            st.write(data.get("reason", ""))

            # ✅ Matching Experience
            st.subheader("✅ Matching Experience")
            for item in data.get("matching_experience", []):
                st.write("- ", item)

            # ⚠️ Gaps
            st.subheader("⚠️ Gaps")
            for gap in data.get("gaps", []):
                st.write("- ", gap)

            # 🚀 Strategy
            st.subheader("🚀 Positioning Strategy")
            for item in data.get("positioning_strategy", []):
                st.write("- ", item)

            # 📄 Resume Suggestions
            st.subheader("📄 Resume Improvements")
            for item in data.get("resume_suggestions", []):
                st.write("- ", item)

        except Exception as e:
            st.error("⚠️ Could not parse AI response. Showing raw output:")
            st.write(result)
            st.text(f"Error: {e}")

# ---------------- RESUME GENERATOR BUTTON ----------------
if st.button("Generate Tailored Resume"):

    if job_desc.strip() == "":
        st.warning("Please paste a job description")

    else:
        with st.spinner("Generating tailored resume..."):
            analysis = analyze_job(job_desc, resume)
            generated = generate_resume(job_desc, resume, analysis)
            
        st.subheader("📄 Tailored Resume")
        st.text_area("Edit before download", generated, height=400)

        # Save as Word file
        file_path = save_resume_to_word(generated)

        # Download button
        with open(file_path, "rb") as file:
            st.download_button(
                label="⬇️ Download Resume (Word)",
                data=file,
                file_name="Sreekanth_Tailored_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )