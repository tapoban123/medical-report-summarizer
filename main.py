import streamlit as st
from ai_methods.ai_summarizer import process_document
import tempfile
import os

if "report_path" not in st.session_state:
    st.session_state.report_path = None


st.title("Medical Report Summarizer")

report = st.file_uploader("Upload Report", type=[".pdf"])

if report is not None:
    file_bytes = report.getvalue()
    temp_file_path = ""

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(report.name)[1]
    ) as temp_file:
        temp_file.write(file_bytes)
        st.session_state.report_path = temp_file.name

    with st.status("Analyzing document..."):
        report_summary = process_document(st.session_state.report_path)

    st.markdown(report_summary)
