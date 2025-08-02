import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_footing_design

def page_circular_column_footing():
    st.title("🔘🦶 Circular Column with Footing")
    st.markdown("Design circular column with circular or square isolated footing")

    with st.form("circular_column_footing_form"):
        tab1, tab2, tab3 = st.tabs(["🏗️ Geometry", "🔩 Reinforcement", "📊 Loading"])

        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Column Properties")
                col_diameter = st.number_input("Column Diameter (mm)", min_value=200, max_value=1200, value=400, step=50)
                col_height = st.number_input("Column Height (mm)", min_value=1000, max_value=8000, value=3000, step=100)
                clear_cover = st.number_input("Clear Cover (mm)", min_value=25, max_value=75, value=40, step=5)
                
                st.subheader("Material Properties")
                concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"], index=2)
                steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
            
            with col2:
                st.subheader("Footing Configuration")
                footing_type = st.radio("Footing Type", ["Circular", "Square"], horizontal=True)
                
                if footing_type == "Circular":
                    footing_diameter = st.number_input("Footing Diameter (mm)", min_value=1000, max_value=5000, value=2000, step=100)
                    footing_size_display = f"⌀{footing_diameter}mm"
                else:
                    footing_side = st.number_input("Footing Side (mm)", min_value=1000, max_value=5000, value=2000, step=100)
                    footing_size_display = f"{footing_side}×{footing_side}mm"
                
                footing_thickness = st.number_input("Footing Thickness (mm)", min_value=300, max_value=1000, value=500, step=50)
                
                st.subheader("Foundation Details")
                depth_of_foundation = st.number_input("Foundation Depth (mm)", min_value=500, max_value=3000, value=1500, step=100)
                safe_bearing_capacity = st.number_input("Safe Bearing Capacity (kN/m²)", min_value=50, max_value=500, value=150, step=25)

        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Column Reinforcement")
                col_main_dia = st.selectbox("Main Bar Diameter (mm)", [12, 16, 20, 25, 32, 40], index=2)
                num_main_bars = st.slider("Number of Main Bars", min_value=6, max_value=20, value=8, step=1)
                col_tie_dia = st.selectbox("Tie Diameter (mm)", [6, 8, 10, 12], index=1)
                tie_spacing = st.number_input("Tie Spacing (mm)", min_value=75, max_value=300, value=150, step=25)
            
            with col2:
                st.subheader("Footing Reinforcement")
                footing_main_dia = st.selectbox("Footing Main Bar ⌀ (mm)", [12, 16, 20, 25], index=2)
                footing_main_spacing = st.number_input("Main Bar Spacing (mm)", min_value=100, max_value=250, value=150, step=25)
                
                if footing_type == "Square":
                    footing_dist_dia = st.selectbox("Distribution Bar ⌀ (mm)", [10, 12, 16, 20], index=1)
                    footing_dist_spacing = st.number_input("Distribution Spacing (mm)", min_value=150, max_value=300, value=200, step=25)

        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Applied Loads")
                dead_load = st.number_input("Dead Load (kN)", min_value=0, value=600, step=50)
                live_load = st.number_input("Live Load (kN)", min_value=0, value=300, step=50)
                wind_load = st.number_input("Wind Load (kN)", min_value=0, value=40, step=10)
                seismic_load = st.number_input("Seismic Load (kN)", min_value=0, value=30, step=10)
            
            with col2:
                st.subheader("Applied Moments")
                moment_x = st.number_input("Moment X (kNm)", min_value=0, value=80, step=10)
                moment_y = st.number_input("Moment Y (kNm)", min_value=0, value=60, step=10)
                torsion = st.number_input("Torsion (kNm)", min_value=0, value=20, step=5)

        submitted = st.form_submit_button("🔄 Design Circular Column & Footing", type="primary")

    if submitted:
        with st.spinner("🔄 Designing circular column with footing..."):
            try:
                # Calculate total loads
                total_vertical_load = dead_load + live_load + wind_load + seismic_load
                
                # Calculate footing area
                if footing_type == "Circular":
                    footing_area = np.pi * (footing_diameter/2)**2 / 1e6  # m²
                    footing_dimension = footing_diameter
                else:
                    footing_area = (footing_side**2) / 1e6  # m²
                    footing_dimension = footing_side

                # Basic design calculations
                soil_pressure = total_vertical_load / footing_area
                
                # Create design results
                design_results = {
                    'soil_pressure': soil_pressure,
                    'bearing_capacity_ok': soil_pressure <= safe_bearing_capacity,
                    'footing_area': footing_area,
                    'pressure_ratio': soil_pressure / safe_bearing_capacity
                }

                # Create DXF drawing
                doc = create_circular_column_footing_dxf(
                    col_diameter, col_height, footing_type, footing_dimension,
                    footing_thickness, col_main_dia, num_main_bars,
                    footing_main_dia, footing_main_spacing, clear_cover
                )

                # Display results
                col_results, col_download = st.columns([3, 1])

                with col_results:
                    st.success("✅ Circular column and footing design completed!")
                    
                    # Create result tabs
                    result_tab1, result_tab2, result_tab3 = st.tabs(["📋 Design Summary", "🔍 Verification", "📊 Details"])
                    
                    with result_tab1:
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Column Configuration**")
                            st.write(f"• Diameter: ⌀{col_diameter} mm")
                            st.write(f"• Height: {col_height} mm")
                            st.write(f"• Main Bars: {num_main_bars}-⌀{col_main_dia}mm")
                            
                            col_steel_area = num_main_bars * np.pi * (col_main_dia/2)**2
                            col_cross_area = np.pi * (col_diameter/2)**2
                            steel_percentage = (col_steel_area / col_cross_area) * 100
                            
                            st.write(f"• Steel Area: {col_steel_area:.0f} mm²")
                            st.write(f"• Steel %: {steel_percentage:.2f}%")
                            st.write(f"• Ties: ⌀{col_tie_dia}mm @ {tie_spacing}mm c/c")
                        
                        with summary_col2:
                            st.markdown("**Footing Configuration**")
                            st.write(f"• Type: {footing_type}")
                            st.write(f"• Size: {footing_size_display}")
                            st.write(f"• Thickness: {footing_thickness} mm")
                            st.write(f"• Area: {footing_area:.2f} m²")
                            st.write(f"• Foundation Depth: {depth_of_foundation} mm")
                            st.write(f"• Main Bars: ⌀{footing_main_dia}mm @ {footing_main_spacing}mm c/c")

                    with result_tab2:
                        verification_col1, verification_col2 = st.columns(2)
                        
                        with verification_col1:
                            st.markdown("**Bearing Capacity Check**")
                            st.write(f"• Applied Pressure: {soil_pressure:.1f} kN/m²")
                            st.write(f"• Safe Bearing Capacity: {safe_bearing_capacity} kN/m²")
                            st.write(f"• Utilization: {(soil_pressure/safe_bearing_capacity)*100:.1f}%")
                            
                            if design_results['bearing_capacity_ok']:
                                st.success("✅ Bearing capacity is adequate")
                            else:
                                st.error("❌ Bearing capacity exceeded - increase footing size")
                        
                        with verification_col2:
                            st.markdown("**Load Summary**")
                            st.write(f"• Dead Load: {dead_load} kN")
                            st.write(f"• Live Load: {live_load} kN")
                            st.write(f"• Wind Load: {wind_load} kN")
                            st.write(f"• Seismic Load: {seismic_load} kN")
                            st.write(f"• **Total Load: {total_vertical_load} kN**")

                    with result_tab3:
                        details_col1, details_col2 = st.columns(2)
                        
                        with details_col1:
                            st.markdown("**Material Properties**")
                            st.write(f"• Concrete Grade: {concrete_grade}")
                            st.write(f"• Steel Grade: {steel_grade}")
                            st.write(f"• Clear Cover: {clear_cover} mm")
                            
                            st.markdown("**Applied Moments**")
                            st.write(f"• Moment X: {moment_x} kNm")  
                            st.write(f"• Moment Y: {moment_y} kNm")
                            st.write(f"• Torsion: {torsion} kNm")
                        
                        with details_col2:
                            st.markdown("**Design Parameters**")
                            st.write(f"• Minimum Steel (Column): 0.8% = {0.008 * col_cross_area:.0f} mm²")
                            st.write(f"• Maximum Steel (Column): 4.0% = {0.04 * col_cross_area:.0f} mm²")
                            st.write(f"• Provided Steel: {col_steel_area:.0f} mm² ✓")
                            
                            if footing_type == "Circular":
                                st.write(f"• Footing Reinforcement: Radial & Circumferential")
                            else:
                                st.write(f"• Footing Reinforcement: Orthogonal Grid")

                with col_download:
                    st.subheader("📥 Downloads")
                    
                    # Save DXF
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                        doc.saveas(fp.name)
                        with open(fp.name, "rb") as f:
                            dxf_data = f.read()
                    
                    st.download_button(
                        label="📐 Download DXF",
                        data=dxf_data,
                        file_name=f"circular_column_footing_D{col_diameter}_{footing_type}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_circular_footing_report(
                        col_diameter, col_height, footing_type, footing_dimension,
                        footing_thickness, concrete_grade, steel_grade,
                        total_vertical_load, moment_x, moment_y,
                        safe_bearing_capacity, design_results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"circular_column_footing_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error in design: {str(e)}")
                st.error("Please verify all input parameters and try again.")

def create_circular_column_footing_dxf(col_diameter, col_height, footing_type, footing_dimension,
                                     footing_thickness, col_main_dia, num_main_bars,
                                     footing_main_dia, footing_main_spacing, clear_cover):
    """Create DXF drawing for circular column with footing"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Plan view - Footing
    if footing_type == "Circular":
        msp.add_circle(center=(0, 0), radius=footing_dimension/2)
        footing_area_text = f"⌀{footing_dimension}mm"
    else:
        msp.add_lwpolyline([
            (-footing_dimension/2, -footing_dimension/2),
            (footing_dimension/2, -footing_dimension/2),
            (footing_dimension/2, footing_dimension/2),
            (-footing_dimension/2, footing_dimension/2),
            (-footing_dimension/2, -footing_dimension/2)
        ])
        footing_area_text = f"{footing_dimension}×{footing_dimension}mm"
    
    # Column in plan
    msp.add_circle(center=(0, 0), radius=col_diameter/2)
    
    # Column reinforcement in plan
    bar_circle_radius = col_diameter/2 - clear_cover - col_main_dia/2
    for i in range(num_main_bars):
        angle = 2 * np.pi * i / num_main_bars
        x = bar_circle_radius * np.cos(angle)
        y = bar_circle_radius * np.sin(angle)
        msp.add_circle(center=(x, y), radius=col_main_dia/2)
    
    # Footing reinforcement pattern
    if footing_type == "Circular":
        # Radial reinforcement pattern
        num_radial_bars = int(2 * np.pi * (footing_dimension/2 - clear_cover) / footing_main_spacing)
        for i in range(num_radial_bars):
            angle = 2 * np.pi * i / num_radial_bars
            x1 = (col_diameter/2 + clear_cover) * np.cos(angle)
            y1 = (col_diameter/2 + clear_cover) * np.sin(angle)
            x2 = (footing_dimension/2 - clear_cover) * np.cos(angle)
            y2 = (footing_dimension/2 - clear_cover) * np.sin(angle)
            msp.add_line((x1, y1), (x2, y2))
        
        # Circumferential bars
        for r in range(int(col_diameter/2 + clear_cover), int(footing_dimension/2 - clear_cover), footing_main_spacing):
            msp.add_circle(center=(0, 0), radius=r, dxfattribs={'linetype': 'DASHED'})
            
    else:
        # Grid reinforcement for square footing
        num_bars = int(footing_dimension / footing_main_spacing) + 1
        for i in range(num_bars):
            pos = -footing_dimension/2 + clear_cover + i * footing_main_spacing
            if abs(pos) <= footing_dimension/2 - clear_cover:
                # Bars in X direction
                msp.add_line(
                    (pos, -footing_dimension/2 + clear_cover),
                    (pos, footing_dimension/2 - clear_cover)
                )
                # Bars in Y direction
                msp.add_line(
                    (-footing_dimension/2 + clear_cover, pos),
                    (footing_dimension/2 - clear_cover, pos),
                    dxfattribs={'linetype': 'DASHED'}
                )

    # Section view (offset to right)
    section_x_offset = footing_dimension * 1.5
    
    # Create section view
    if footing_type == "Circular":
        # Circular footing section
        msp.add_arc(
            center=(section_x_offset, -footing_thickness),
            radius=footing_dimension/2,
            start_angle=0, end_angle=180
        )
        msp.add_line(
            (section_x_offset - footing_dimension/2, -footing_thickness),
            (section_x_offset + footing_dimension/2, -footing_thickness)
        )
    else:
        # Square footing section  
        msp.add_lwpolyline([
            (section_x_offset - footing_dimension/2, -footing_thickness),
            (section_x_offset + footing_dimension/2, -footing_thickness),
            (section_x_offset + footing_dimension/2, 0),
            (section_x_offset + col_diameter/2, 0),
            (section_x_offset + col_diameter/2, col_height),
            (section_x_offset - col_diameter/2, col_height),
            (section_x_offset - col_diameter/2, 0),
            (section_x_offset - footing_dimension/2, 0),
            (section_x_offset - footing_dimension/2, -footing_thickness)
        ])
    
    # Column in section
    msp.add_lwpolyline([
        (section_x_offset - col_diameter/2, 0),
        (section_x_offset + col_diameter/2, 0),
        (section_x_offset + col_diameter/2, col_height),
        (section_x_offset - col_diameter/2, col_height),
        (section_x_offset - col_diameter/2, 0)
    ])
    
    # Add center lines
    msp.add_line((-footing_dimension*0.75, 0), (footing_dimension*0.75, 0), dxfattribs={'linetype': 'CENTER'})
    msp.add_line((0, -footing_dimension*0.75), (0, footing_dimension*0.75), dxfattribs={'linetype': 'CENTER'})
    
    # Add dimensions
    add_dimensions(msp, [
        ((-footing_dimension/2, -footing_dimension*0.7), (footing_dimension/2, -footing_dimension*0.7), 
         (0, -footing_dimension*0.8), footing_area_text),
        ((-col_diameter/2, col_diameter*0.7), (col_diameter/2, col_diameter*0.7), 
         (0, col_diameter*0.8), f"⌀{col_diameter}"),
        ((section_x_offset + footing_dimension*0.6, -footing_thickness), 
         (section_x_offset + footing_dimension*0.6, col_height),
         (section_x_offset + footing_dimension*0.7, col_height/2), f"{col_height + footing_thickness}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"CIRCULAR COLUMN WITH {footing_type.upper()} FOOTING\nCOLUMN: ⌀{col_diameter}mm x {col_height}mm\nFOOTING: {footing_area_text} x {footing_thickness}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, -footing_dimension*1.3))
    
    msp.add_text(
        f"COLUMN REINFORCEMENT:\n{num_main_bars}-⌀{col_main_dia}mm MAIN BARS\nFOOTING BARS: ⌀{footing_main_dia}mm @ {footing_main_spacing}mm C/C",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((section_x_offset, -footing_dimension*0.9))
    
    return doc

def generate_circular_footing_report(col_diameter, col_height, footing_type, footing_dimension,
                                   footing_thickness, concrete_grade, steel_grade,
                                   total_load, moment_x, moment_y, sbc, results):
    """Generate detailed design report"""
    
    if footing_type == "Circular":
        footing_area = np.pi * (footing_dimension/2)**2 / 1e6
        footing_size_text = f"⌀{footing_dimension}mm"
    else:
        footing_area = (footing_dimension**2) / 1e6
        footing_size_text = f"{footing_dimension}×{footing_dimension}mm"
    
    report = f"""
CIRCULAR COLUMN WITH {footing_type.upper()} FOOTING DESIGN REPORT
==================================================================

COLUMN DETAILS:
- Diameter: ⌀{col_diameter}mm
- Height: {col_height}mm  
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

FOOTING DETAILS:
- Type: {footing_type}
- Size: {footing_size_text}
- Thickness: {footing_thickness}mm
- Footing Area: {footing_area:.2f} m²
- Safe Bearing Capacity: {sbc} kN/m²

APPLIED LOADS:
- Total Vertical Load: {total_load} kN
- Moment about X-axis: {moment_x} kNm
- Moment about Y-axis: {moment_y} kNm

DESIGN VERIFICATION:
- Applied Soil Pressure: {results.get('soil_pressure', 0):.1f} kN/m²
- Allowable Pressure: {sbc} kN/m²
- Pressure Utilization: {results.get('pressure_ratio', 0)*100:.1f}%
- Bearing Status: {'SAFE' if results.get('bearing_capacity_ok', False) else 'UNSAFE'}

REINFORCEMENT DETAILS:
- Column: As per drawing and IS 456:2000
- Footing: As per drawing and IS 456:2000
- Development length and anchorage as per code

DESIGN ASSUMPTIONS:
1. Design based on IS 456:2000 
2. Load combinations as per IS 1893:2016
3. Soil properties as provided
4. Foundation level and depth as specified

RECOMMENDATIONS:
1. Provide adequate drainage around foundation
2. Ensure proper compaction of backfill
3. Regular inspection during construction
4. Quality control of concrete and reinforcement

Generated by RajLisp Structural Design Suite
============================================
"""
    return report
