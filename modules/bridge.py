import io
import os

import ezdxf
import pandas as pd
import streamlit as st

from attached_assets.bridge_gad_app_1754174198163 import generate_tender_report


def page_bridge():
    st.title("🌉 Bridge - Tender & GAD Utilities")
    st.markdown("Upload an Excel to generate a Tender Analysis PDF. Optionally export a placeholder DXF.")

    with st.form("bridge_tender_form"):
        col1, col2 = st.columns(2)
        with col1:
            excel_file = st.file_uploader("Upload Bid Summary Excel", type=["xlsx"], accept_multiple_files=False)
            output_pdf_name = st.text_input("Output PDF filename", value="tender_analysis.pdf")
        with col2:
            export_dxf = st.checkbox("Also export placeholder GAD DXF", value=False)
            output_dxf_name = st.text_input("Output DXF filename", value="bridge_design.dxf")

        submitted = st.form_submit_button("🔄 Generate", type="primary")

    if submitted:
        if not excel_file:
            st.error("Please upload an Excel file with a 'Bid Summary' sheet.")
            return

        with st.spinner("Generating tender analysis PDF..."):
            try:
                # Read uploaded Excel to a temporary file for the generator
                with st.spinner("Reading Excel..."):
                    df = pd.read_excel(excel_file, sheet_name='Bid Summary')

                # Build PDF in memory using reportlab via generate_tender_report; write to temp path first
                tmp_dir = st.experimental_get_query_params().get("tmp_dir", ["."])[0]
                os.makedirs(tmp_dir, exist_ok=True)
                tmp_input = os.path.join(tmp_dir, "_upload.xlsx")
                tmp_output_pdf = os.path.join(tmp_dir, "_tender.pdf")

                # Save uploaded excel to tmp_input
                with open(tmp_input, "wb") as f:
                    f.write(excel_file.getbuffer())

                # Call existing function
                generate_tender_report(tmp_input, tmp_output_pdf)

                # Return PDF to user
                with open(tmp_output_pdf, "rb") as f:
                    pdf_bytes = f.read()
                st.success("Tender Analysis PDF generated.")
                st.download_button("📄 Download Tender PDF", data=pdf_bytes, file_name=output_pdf_name, mime="application/pdf")
            except Exception as e:
                st.error(f"Failed to generate PDF: {e}")
                return

        if export_dxf:
            with st.spinner("Creating placeholder DXF..."):
                try:
                    doc = ezdxf.new('R2010')
                    msp = doc.modelspace()
                    msp.add_text("BRIDGE GAD PLACEHOLDER", dxfattribs={'height': 250}).set_pos((0, 0))

                    dxf_io = io.BytesIO()
                    doc.write(dxf_io)
                    st.success("DXF created.")
                    st.download_button("📐 Download DXF", data=dxf_io.getvalue(), file_name=output_dxf_name, mime="application/dxf")
                except Exception as e:
                    st.error(f"Failed to create DXF: {e}")