import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions, new_dxf_doc
from utils.calculations import calculate_column_capacity

def page_circular_column():
    st.title("🔘 Circular Column Designer")
    st.markdown("Design circular reinforced concrete columns with detailed reinforcement")

    # Create form for inputs
    with st.form("circular_column_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🔧 Column Dimensions")
            diameter = st.number_input("Diameter (mm)", min_value=200, max_value=2000, value=400, step=50,
                                     help="Column diameter in millimeters")
            height = st.number_input("Height (mm)", min_value=1000, max_value=10000, value=3000, step=100,
                                   help="Column height in millimeters")
            clear_cover = st.number_input("Clear Cover (mm)", min_value=20, max_value=75, value=40, step=5,
                                        help="Concrete cover to reinforcement")

        with col2:
            st.subheader("🔩 Reinforcement Details")
            main_bars_dia = st.selectbox("Main Bar Diameter (mm)", [12, 16, 20, 25, 32, 40], index=2,
                                       help="Diameter of main longitudinal bars")
            num_bars = st.slider("Number of Main Bars", min_value=4, max_value=20, value=8, step=1,
                               help="Number of main longitudinal bars")
            tie_dia = st.selectbox("Tie Diameter (mm)", [6, 8, 10, 12], index=1,
                                 help="Diameter of lateral ties")
            tie_spacing = st.number_input("Tie Spacing (mm)", min_value=75, max_value=300, value=150, step=25,
                                        help="Center to center spacing of ties")

        with col3:
            st.subheader("🏗️ Material & Loads")
            concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40", "M45"], index=2)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
            
            st.markdown("**Design Loads**")
            axial_load = st.number_input("Axial Load (kN)", min_value=0, value=1000, step=50,
                                       help="Applied axial compression load")
            moment_x = st.number_input("Moment X (kNm)", min_value=0, value=50, step=10,
                                     help="Applied moment about X-axis")
            moment_y = st.number_input("Moment Y (kNm)", min_value=0, value=50, step=10,
                                     help="Applied moment about Y-axis")

        submitted = st.form_submit_button("🔄 Generate Column Design", type="primary")

    if submitted:
        with st.spinner("🔄 Generating circular column design..."):
            try:
                # Perform design calculations
                results = calculate_column_capacity(
                    'circular', diameter, diameter, height, concrete_grade, steel_grade,
                    main_bars_dia, num_bars, axial_load, moment_x, moment_y
                )

                # Create DXF drawing
                doc = create_circular_column_dxf(
                    diameter, height, main_bars_dia, num_bars, tie_dia, tie_spacing, clear_cover
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Column design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Column Details**")
                            st.write(f"• Diameter: {diameter} mm")
                            st.write(f"• Height: {height} mm") 
                            st.write(f"• Clear Cover: {clear_cover} mm")
                            st.write(f"• Concrete: {concrete_grade}")
                            st.write(f"• Steel: {steel_grade}")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement**")
                            st.write(f"• Main Bars: {num_bars} - ⌀{main_bars_dia} mm")
                            steel_area = num_bars * np.pi * (main_bars_dia/2)**2
                            steel_percent = (steel_area / (np.pi * (diameter/2)**2)) * 100
                            st.write(f"• Steel Area: {steel_area:.0f} mm²")
                            st.write(f"• Steel %: {steel_percent:.2f}%")
                            st.write(f"• Ties: ⌀{tie_dia} mm @ {tie_spacing} mm c/c")

                    # Capacity check
                    if results:
                        with st.expander("🔍 Design Check", expanded=True):
                            st.write(f"**Axial Capacity:** {results.get('axial_capacity', 0):.0f} kN")
                            st.write(f"**Applied Load:** {axial_load} kN")
                            
                            capacity_ratio = axial_load / results.get('axial_capacity', 1)
                            if capacity_ratio <= 1.0:
                                st.success(f"✅ Design OK - Capacity Ratio: {capacity_ratio:.2f}")
                            else:
                                st.error(f"❌ Design Inadequate - Capacity Ratio: {capacity_ratio:.2f}")

                with col_download:
                    st.subheader("📥 Download")
                    
                    # Save DXF to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                        doc.saveas(fp.name)
                        with open(fp.name, "rb") as f:
                            dxf_data = f.read()
                    
                    st.download_button(
                        label="📐 Download DXF",
                        data=dxf_data,
                        file_name=f"circular_column_D{diameter}_H{height}.dxf",
                        mime="application/dxf",
                        help="Download CAD file for AutoCAD/DraftSight"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_circular_column_dxf(diameter, height, main_bar_dia, num_bars, tie_dia, tie_spacing, clear_cover):
    """Create DXF drawing for circular column"""
    doc = new_dxf_doc()
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Column outline (plan view)
    radius = diameter / 2
    msp.add_circle(center=(0, 0), radius=radius)
    
    # Add main reinforcement bars
    bar_circle_radius = radius - clear_cover - tie_dia - main_bar_dia/2
    
    for i in range(num_bars):
        angle = 2 * np.pi * i / num_bars
        x = bar_circle_radius * np.cos(angle)
        y = bar_circle_radius * np.sin(angle)
        msp.add_circle(center=(x, y), radius=main_bar_dia/2)
    
    # Add ties representation
    tie_radius = radius - clear_cover - tie_dia/2
    msp.add_circle(center=(0, 0), radius=tie_radius, dxfattribs={'linetype': 'DASHED'})
    
    # Add center lines
    msp.add_line((-radius*1.5, 0), (radius*1.5, 0), dxfattribs={'linetype': 'CENTER'})
    msp.add_line((0, -radius*1.5), (0, radius*1.5), dxfattribs={'linetype': 'CENTER'})
    
    # Add dimensions
    add_dimensions(msp, [
        ((-radius, 0), (radius, 0), (0, radius*1.2), f"⌀{diameter}"),
        ((bar_circle_radius, 0), (bar_circle_radius, 0), (bar_circle_radius*1.3, 0), f"⌀{main_bar_dia}")
    ])
    
    # Add section view at different location
    section_x_offset = diameter * 2
    
    # Column section (elevation)
    section_width = diameter
    section_height = height
    
    # Column outline in section
    msp.add_lwpolyline([
        (section_x_offset - section_width/2, 0),
        (section_x_offset + section_width/2, 0),
        (section_x_offset + section_width/2, section_height),
        (section_x_offset - section_width/2, section_height),
        (section_x_offset - section_width/2, 0)
    ])
    
    # Add ties in elevation
    num_ties = int(height / tie_spacing) + 1
    for i in range(num_ties):
        y_pos = i * tie_spacing
        if y_pos <= height:
            msp.add_line(
                (section_x_offset - section_width/2 + clear_cover, y_pos),
                (section_x_offset + section_width/2 - clear_cover, y_pos),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Add main bars in elevation (simplified as lines at edges)
    msp.add_line(
        (section_x_offset - section_width/2 + clear_cover + main_bar_dia/2, 0),
        (section_x_offset - section_width/2 + clear_cover + main_bar_dia/2, section_height)
    )
    msp.add_line(
        (section_x_offset + section_width/2 - clear_cover - main_bar_dia/2, 0),
        (section_x_offset + section_width/2 - clear_cover - main_bar_dia/2, section_height)
    )
    
    # Add text annotations
    msp.add_text(
        f"CIRCULAR COLUMN\n⌀{diameter}mm x {height}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, -radius*2), align="MIDDLE_CENTER")
    
    msp.add_text(
        f"REINFORCEMENT:\n{num_bars}-⌀{main_bar_dia}mm MAIN BARS\n⌀{tie_dia}mm TIES @ {tie_spacing}mm C/C",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((section_x_offset, -radius), align="MIDDLE_CENTER")
    
    return doc
