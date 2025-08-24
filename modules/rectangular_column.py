import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import add_dimensions
from utils.calculations import calculate_rectangular_column_capacity

def page_rectangular_column():
    st.title("⬜ Rectangular Column Designer")
    st.markdown("Design rectangular reinforced concrete columns with detailed reinforcement layout")

    with st.form("rectangular_column_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Column Dimensions")
            width = st.number_input("Width (mm)", min_value=200, max_value=2000, value=300, step=50,
                                  help="Column width (shorter dimension)")
            depth = st.number_input("Depth (mm)", min_value=200, max_value=2000, value=450, step=50,
                                  help="Column depth (longer dimension)")
            height = st.number_input("Height (mm)", min_value=1000, max_value=10000, value=3000, step=100,
                                   help="Column height")
            clear_cover = st.number_input("Clear Cover (mm)", min_value=20, max_value=75, value=40, step=5,
                                        help="Concrete cover to reinforcement")

        with col2:
            st.subheader("🔩 Reinforcement Layout")
            main_bars_dia = st.selectbox("Main Bar Diameter (mm)", [12, 16, 20, 25, 32, 40], index=2)
            
            # Bars along width and depth
            bars_width = st.slider("Bars along Width", min_value=2, max_value=8, value=3, step=1,
                                 help="Number of bars along width direction")
            bars_depth = st.slider("Bars along Depth", min_value=2, max_value=8, value=4, step=1,
                                 help="Number of bars along depth direction")
            
            tie_dia = st.selectbox("Tie Diameter (mm)", [6, 8, 10, 12], index=1)
            tie_spacing = st.number_input("Tie Spacing (mm)", min_value=75, max_value=300, value=150, step=25)

        with col3:
            st.subheader("🏗️ Materials & Loading")
            concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40", "M45"], index=2)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
            
            st.markdown("**Applied Loads**")
            axial_load = st.number_input("Axial Load (kN)", min_value=0, value=1200, step=50)
            moment_x = st.number_input("Moment about X (kNm)", min_value=0, value=75, step=10,
                                     help="Moment about width axis")
            moment_y = st.number_input("Moment about Y (kNm)", min_value=0, value=50, step=10,
                                     help="Moment about depth axis")

        submitted = st.form_submit_button("🔄 Generate Column Design", type="primary")

    if submitted:
        with st.spinner("🔄 Generating rectangular column design..."):
            try:
                # Calculate total number of bars
                total_bars = 2 * (bars_width + bars_depth) - 4  # Corner bars not double counted
                
                # Perform design calculations
                steel_area = total_bars * np.pi * (main_bars_dia/2)**2
                @st.cache_data(show_spinner=False)
                def _calc_rect(w, d, h, c, s, ast):
                    return calculate_rectangular_column_capacity(w, d, h, c, s, ast)
                results = _calc_rect(
                    width, depth, height, concrete_grade, steel_grade, steel_area
                )

                # Create DXF drawing
                doc = create_rectangular_column_dxf(
                    width, depth, height, main_bars_dia, bars_width, bars_depth, 
                    tie_dia, tie_spacing, clear_cover
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Column design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Column Geometry**")
                            st.write(f"• Width: {width} mm")
                            st.write(f"• Depth: {depth} mm")
                            st.write(f"• Height: {height} mm")
                            st.write(f"• Cross-sectional Area: {width * depth / 1000:.1f} cm²")
                            st.write(f"• Clear Cover: {clear_cover} mm")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement Details**")
                            st.write(f"• Total Bars: {total_bars} - ⌀{main_bars_dia} mm")
                            st.write(f"• Along Width: {bars_width} bars")
                            st.write(f"• Along Depth: {bars_depth} bars")
                            
                            steel_area = total_bars * np.pi * (main_bars_dia/2)**2
                            steel_percent = (steel_area / (width * depth)) * 100
                            st.write(f"• Steel Area: {steel_area:.0f} mm²")
                            st.write(f"• Steel %: {steel_percent:.2f}%")

                    # Material and loads
                    with st.expander("🏗️ Materials & Loading", expanded=False):
                        load_col1, load_col2 = st.columns(2)
                        
                        with load_col1:
                            st.markdown("**Materials**")
                            st.write(f"• Concrete Grade: {concrete_grade}")
                            st.write(f"• Steel Grade: {steel_grade}")
                            st.write(f"• Ties: ⌀{tie_dia} mm @ {tie_spacing} mm c/c")
                            
                        with load_col2:
                            st.markdown("**Applied Loads**")
                            st.write(f"• Axial Load: {axial_load} kN")
                            st.write(f"• Moment X: {moment_x} kNm")
                            st.write(f"• Moment Y: {moment_y} kNm")

                    # Design verification
                    if results:
                        with st.expander("🔍 Design Verification", expanded=True):
                            capacity_ratio = axial_load / max(results.get('capacity', 1), 1)
                            
                            st.write(f"**Design Capacity:** {results.get('capacity', 0):.0f} kN")
                            st.write(f"**Applied Load:** {axial_load} kN")
                            st.write(f"**Capacity Utilization:** {capacity_ratio*100:.1f}%")
                            
                            if capacity_ratio <= 1.0:
                                st.success(f"✅ Design is SAFE - Capacity Ratio: {capacity_ratio:.2f}")
                            else:
                                st.error("❌ Design UNSAFE - Increase section or reinforcement")
                                st.error(f"Capacity Ratio: {capacity_ratio:.2f} > 1.0")

                with col_download:
                    st.subheader("📥 Download")
                    st.markdown("**CAD Files**")
                    
                    # Save DXF to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                        doc.saveas(fp.name)
                        with open(fp.name, "rb") as f:
                            dxf_data = f.read()
                    
                    st.download_button(
                        label="📐 Download DXF",
                        data=dxf_data,
                        file_name=f"rect_column_{width}x{depth}x{height}.dxf",
                        mime="application/dxf",
                        help="Download CAD drawing file"
                    )
                    
                    # Generate design report
                    report_text = generate_column_report(
                        width, depth, height, concrete_grade, steel_grade,
                        main_bars_dia, total_bars, tie_dia, tie_spacing,
                        axial_load, moment_x, moment_y, results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report_text,
                        file_name=f"rect_column_{width}x{depth}_report.txt",
                        mime="text/plain",
                        help="Download design calculation report"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please verify your input parameters and try again.")

def create_rectangular_column_dxf(width, depth, height, main_bar_dia, bars_width, bars_depth, tie_dia, tie_spacing, clear_cover):
    """Create DXF drawing for rectangular column"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Column plan view
    msp.add_lwpolyline([
        (-width/2, -depth/2),
        (width/2, -depth/2),
        (width/2, depth/2),
        (-width/2, depth/2),
        (-width/2, -depth/2)
    ])
    
    # Add reinforcement bars in plan
    effective_width = width - 2 * (clear_cover + tie_dia + main_bar_dia/2)
    effective_depth = depth - 2 * (clear_cover + tie_dia + main_bar_dia/2)
    
    # Bars along width (top and bottom)
    for i in range(bars_width):
        x_pos = -effective_width/2 + i * (effective_width / (bars_width - 1)) if bars_width > 1 else 0
        # Top bars
        msp.add_circle(center=(x_pos, depth/2 - clear_cover - tie_dia - main_bar_dia/2), radius=main_bar_dia/2)
        # Bottom bars
        msp.add_circle(center=(x_pos, -depth/2 + clear_cover + tie_dia + main_bar_dia/2), radius=main_bar_dia/2)
    
    # Bars along depth (excluding corners already placed)
    for i in range(1, bars_depth - 1):
        y_pos = -effective_depth/2 + i * (effective_depth / (bars_depth - 1))
        # Left bars
        msp.add_circle(center=(-width/2 + clear_cover + tie_dia + main_bar_dia/2, y_pos), radius=main_bar_dia/2)
        # Right bars  
        msp.add_circle(center=(width/2 - clear_cover - tie_dia - main_bar_dia/2, y_pos), radius=main_bar_dia/2)
    
    # Add ties representation
    tie_outline = [
        (-width/2 + clear_cover + tie_dia/2, -depth/2 + clear_cover + tie_dia/2),
        (width/2 - clear_cover - tie_dia/2, -depth/2 + clear_cover + tie_dia/2),
        (width/2 - clear_cover - tie_dia/2, depth/2 - clear_cover - tie_dia/2),
        (-width/2 + clear_cover + tie_dia/2, depth/2 - clear_cover - tie_dia/2),
        (-width/2 + clear_cover + tie_dia/2, -depth/2 + clear_cover + tie_dia/2)
    ]
    msp.add_lwpolyline(tie_outline, dxfattribs={'linetype': 'DASHED'})
    
    # Add center lines
    msp.add_line((-width*0.75, 0), (width*0.75, 0), dxfattribs={'linetype': 'CENTER'})
    msp.add_line((0, -depth*0.75), (0, depth*0.75), dxfattribs={'linetype': 'CENTER'})
    
    # Column elevation view (offset to the right)
    elevation_x_offset = width * 2
    
    # Column outline in elevation
    msp.add_lwpolyline([
        (elevation_x_offset - width/2, 0),
        (elevation_x_offset + width/2, 0),
        (elevation_x_offset + width/2, height),
        (elevation_x_offset - width/2, height),
        (elevation_x_offset - width/2, 0)
    ])
    
    # Add ties in elevation
    num_ties = int(height / tie_spacing) + 1
    for i in range(num_ties):
        y_pos = i * tie_spacing
        if y_pos <= height:
            msp.add_lwpolyline([
                (elevation_x_offset - width/2 + clear_cover, y_pos),
                (elevation_x_offset + width/2 - clear_cover, y_pos),
                (elevation_x_offset + width/2 - clear_cover, y_pos + tie_dia),
                (elevation_x_offset - width/2 + clear_cover, y_pos + tie_dia),
                (elevation_x_offset - width/2 + clear_cover, y_pos)
            ], dxfattribs={'linetype': 'DASHED'})
    
    # Add main bars in elevation (vertical lines)
    for i in range(bars_width):
        x_pos = elevation_x_offset - effective_width/2 + i * (effective_width / (bars_width - 1)) if bars_width > 1 else elevation_x_offset
        msp.add_line((x_pos, 0), (x_pos, height))
    
    # Add dimensions
    add_dimensions(msp, [
        ((-width/2, -depth*0.75), (width/2, -depth*0.75), (0, -depth*0.9), f"{width}"),
        ((-width*0.75, -depth/2), (-width*0.75, depth/2), (-width*0.9, 0), f"{depth}"),
        ((elevation_x_offset - width/2, -height*0.1), (elevation_x_offset + width/2, -height*0.1), (elevation_x_offset, -height*0.2), f"{width}"),
        ((elevation_x_offset + width*0.75, 0), (elevation_x_offset + width*0.75, height), (elevation_x_offset + width*0.9, height/2), f"{height}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"RECTANGULAR COLUMN\n{width}mm x {depth}mm x {height}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, -depth*1.2))
    
    total_bars = 2 * (bars_width + bars_depth) - 4
    msp.add_text(
        f"REINFORCEMENT:\n{total_bars}-⌀{main_bar_dia}mm MAIN BARS\n⌀{tie_dia}mm TIES @ {tie_spacing}mm C/C",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((elevation_x_offset, -depth*0.8))
    
    return doc

def generate_column_report(width, depth, height, concrete_grade, steel_grade, main_bar_dia, total_bars, 
                          tie_dia, tie_spacing, axial_load, moment_x, moment_y, results):
    """Generate detailed design calculation report"""
    
    report = f"""
RECTANGULAR COLUMN DESIGN REPORT
================================

PROJECT DETAILS:
- Column Size: {width}mm x {depth}mm x {height}mm
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

REINFORCEMENT DETAILS:
- Main Bars: {total_bars} - ⌀{main_bar_dia}mm
- Ties: ⌀{tie_dia}mm @ {tie_spacing}mm c/c
- Steel Area: {total_bars * np.pi * (main_bar_dia/2)**2:.0f} mm²
- Steel Percentage: {(total_bars * np.pi * (main_bar_dia/2)**2 / (width * depth)) * 100:.2f}%

APPLIED LOADS:
- Axial Load: {axial_load} kN
- Moment about X-axis: {moment_x} kNm  
- Moment about Y-axis: {moment_y} kNm

DESIGN VERIFICATION:
- Design Capacity: {results.get('capacity', 0):.0f} kN
- Capacity Utilization: {(axial_load / max(results.get('capacity', 1), 1)) * 100:.1f}%
- Design Status: {'SAFE' if axial_load <= results.get('capacity', 0) else 'UNSAFE'}

REINFORCEMENT LAYOUT:
- Clear Cover: 40mm (assumed)
- Bar Spacing: As per IS 456:2000
- Minimum Steel: 0.8% of gross area
- Maximum Steel: 4.0% of gross area

Note: This is a preliminary design. Detailed analysis should be carried out
for critical structures considering all relevant load combinations as per
IS 456:2000 and IS 1893:2016.

Generated by RajLisp Structural Design Suite
"""
    return report
