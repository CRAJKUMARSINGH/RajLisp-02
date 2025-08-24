import io

import ezdxf
import streamlit as st


def page_bridge():
    st.title("🌉 Bridge - GAD DXF Export")
    st.markdown("Generate a placeholder Bridge GAD DXF. (Full detailing can be integrated later.)")

    with st.form("bridge_gad_form"):
        output_dxf_name = st.text_input("Output DXF filename", value="bridge_design.dxf")
        title_text = st.text_input("Title", value="BRIDGE GENERAL ARRANGEMENT")
        submitted = st.form_submit_button("📐 Generate DXF", type="primary")

    if submitted:
        with st.spinner("Creating DXF..."):
            try:
                doc = ezdxf.new('R2010')
                msp = doc.modelspace()
                msp.add_text(title_text, dxfattribs={'height': 250}).set_pos((0, 0))

                # Simple axes and frame as placeholder
                msp.add_line((-5000, 0), (5000, 0))
                msp.add_line((0, -2000), (0, 2000))
                msp.add_lwpolyline([(-6000, -1500), (6000, -1500), (6000, 1500), (-6000, 1500), (-6000, -1500)])

                dxf_io = io.BytesIO()
                doc.write(dxf_io)
                st.success("DXF created.")
                st.download_button("Download DXF", data=dxf_io.getvalue(), file_name=output_dxf_name, mime="application/dxf")
            except Exception as e:
                st.error(f"Failed to create DXF: {e}")