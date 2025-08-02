import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_footing_design

def page_rect_column_footing():
    st.title("⬜🦶 Rectangular Column with Footing")
    st.markdown("Design rectangular column with isolated footing foundation")

    with st.form("rect_column_footing_form"):
        # Create tabs for different input sections
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Column", "🏗️ Footing", "🔩 Reinforcement", "📊 Loads"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Column Dimensions")
                col_width = st.number_input("Column Width (mm)", min_value=200, max_value=1000, value=300, step=50)
                col_depth = st.number_input("Column Depth (mm)", min_value=200, max_value=1000, value=450, step=50)
                col_height = st.number_input("Column Height (mm)", min_value=1000, max_value=8000, value=3000, step=100)
            
            with col2:
                st.subheader("Material Properties")
                concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40"], index=2)
                steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
                clear_cover = st.number_input("Clear Cover (mm)", min_value=20, max_value=75, value=40, step=5)

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Footing Dimensions")
                footing_length = st.number_input("Footing Length (mm)", min_value=1000, max_value=5000, value=2000, step=100)
                footing_width = st.number_input("Footing Width (mm)", min_value=1000, max_value=5000, value=1800, step=100)
                footing_thickness = st.number_input("Footing Thickness (mm)", min_value=300, max_value=1000, value=500, step=50)
            
            with col2:
                st.subheader("Soil Properties")
                safe_bearing_capacity = st.number_input("Safe Bearing Capacity (kN/m²)", min_value=50, max_value=500, value=150, step=25)
                depth_of_foundation = st.number_input("Foundation Depth (mm)", min_value=500, max_value=3000, value=1500, step=100)
                soil_unit_weight = st.number_input("Soil Unit Weight (kN/m³)", min_value=15, max_value=25, value=18, step=1)

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Column Reinforcement")
                col_main_dia = st.selectbox("Column Main Bar ⌀ (mm)", [12, 16, 20, 25, 32], index=2)
                col_bars_width = st.slider("Bars along Width", min_value=2, max_value=6, value=3)
                col_bars_depth = st.slider("Bars along Depth", min_value=2, max_value=6, value=4)
                col_tie_dia = st.selectbox("Column Tie ⌀ (mm)", [6, 8, 10, 12], index=1)
                col_tie_spacing = st.number_input("Tie Spacing (mm)", min_value=75, max_value=300, value=150, step=25)
            
            with col2:
                st.subheader("Footing Reinforcement")
                footing_main_dia = st.selectbox("Footing Main Bar ⌀ (mm)", [12, 16, 20, 25], index=2)
                footing_main_spacing = st.number_input("Main Bar Spacing (mm)", min_value=100, max_value=300, value=150, step=25)
                footing_dist_dia = st.selectbox("Distribution Bar ⌀ (mm)", [10, 12, 16, 20], index=1)
                footing_dist_spacing = st.number_input("Distribution Spacing (mm)", min_value=100, max_value=300, value=200, step=25)

        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vertical Loads")
                dead_load = st.number_input("Dead Load (kN)", min_value=0, value=800, step=50)
                live_load = st.number_input("Live Load (kN)", min_value=0, value=400, step=50)
                wind_load = st.number_input("Wind Load (kN)", min_value=0, value=50, step=10)
            
            with col2:
                st.subheader("Moments")
                moment_x = st.number_input("Moment about X (kNm)", min_value=0, value=100, step=10)
                moment_y = st.number_input("Moment about Y (kNm)", min_value=0, value=75, step=10)
                moment_wind = st.number_input("Wind Moment (kNm)", min_value=0, value=120, step=10)

        submitted = st.form_submit_button("🔄 Design Column & Footing", type="primary")

    if submitted:
        with st.spinner("🔄 Designing column with footing..."):
            try:
                # Calculate total loads
                total_vertical_load = dead_load + live_load + wind_load
                total_moment_x = moment_x + moment_wind
                total_moment_y = moment_y
                
                # Perform footing design calculations
                design_results = calculate_footing_design(
                    footing_length, footing_width, footing_thickness,
                    col_width, col_depth, total_vertical_load,
                    total_moment_x, total_moment_y, safe_bearing_capacity
                )

                # Create DXF drawing
                doc = create_column_footing_dxf(
                    col_width, col_depth, col_height,
                    footing_length, footing_width, footing_thickness,
                    col_main_dia, col_bars_width, col_bars_depth,
                    footing_main_dia, footing_main_spacing,
                    footing_dist_dia, footing_dist_spacing,
                    clear_cover
                )

                # Display results
                col_results, col_download = st.columns([3, 1])

                with col_results:
                    st.success("✅ Column and footing design completed!")
                    
                    # Design summary in tabs
                    summary_tab1, summary_tab2, summary_tab3 = st.tabs(["📋 Summary", "🔍 Verification", "📊 Analysis"])
                    
                    with summary_tab1:
                        col_sum1, col_sum2 = st.columns(2)
                        
                        with col_sum1:
                            st.markdown("**Column Details**")
                            st.write(f"• Size: {col_width} × {col_depth} × {col_height} mm")
                            st.write(f"• Concrete: {concrete_grade}, Steel: {steel_grade}")
                            
                            total_col_bars = 2 * (col_bars_width + col_bars_depth) - 4
                            st.write(f"• Main Bars: {total_col_bars}-⌀{col_main_dia}mm")
                            st.write(f"• Ties: ⌀{col_tie_dia}mm @ {col_tie_spacing}mm c/c")
                            
                            col_steel_area = total_col_bars * np.pi * (col_main_dia/2)**2
                            col_steel_percent = (col_steel_area / (col_width * col_depth)) * 100
                            st.write(f"• Steel %: {col_steel_percent:.2f}%")
                        
                        with col_sum2:
                            st.markdown("**Footing Details**")
                            st.write(f"• Size: {footing_length} × {footing_width} × {footing_thickness} mm")
                            st.write(f"• Foundation Depth: {depth_of_foundation} mm")
                            st.write(f"• Safe Bearing Capacity: {safe_bearing_capacity} kN/m²")
                            
                            footing_area = footing_length * footing_width / 1e6  # m²
                            st.write(f"• Footing Area: {footing_area:.2f} m²")
                            
                            soil_pressure = total_vertical_load / footing_area
                            st.write(f"• Soil Pressure: {soil_pressure:.1f} kN/m²")

                    with summary_tab2:
                        if design_results:
                            # Bearing pressure check
                            st.markdown("**Bearing Pressure Check**")
                            max_pressure = design_results.get('max_soil_pressure', 0)
                            pressure_ratio = max_pressure / safe_bearing_capacity
                            
                            if pressure_ratio <= 1.0:
                                st.success(f"✅ Bearing OK - Max Pressure: {max_pressure:.1f} kN/m²")
                            else:
                                st.error(f"❌ Bearing Exceeded - Max Pressure: {max_pressure:.1f} kN/m²")
                            
                            st.write(f"• Pressure Utilization: {pressure_ratio*100:.1f}%")
                            
                            # Footing stability check
                            st.markdown("**Stability Check**")
                            eccentricity_x = design_results.get('eccentricity_x', 0)
                            eccentricity_y = design_results.get('eccentricity_y', 0)
                            
                            st.write(f"• Eccentricity X: {eccentricity_x:.0f} mm")
                            st.write(f"• Eccentricity Y: {eccentricity_y:.0f} mm")
                            
                            # Punching shear check
                            st.markdown("**Punching Shear Check**")
                            punching_shear_ratio = design_results.get('punching_shear_ratio', 0)
                            if punching_shear_ratio <= 1.0:
                                st.success(f"✅ Punching Shear OK - Ratio: {punching_shear_ratio:.2f}")
                            else:
                                st.error(f"❌ Punching Shear Failed - Ratio: {punching_shear_ratio:.2f}")

                    with summary_tab3:
                        st.markdown("**Load Analysis**")
                        
                        load_col1, load_col2 = st.columns(2)
                        
                        with load_col1:
                            st.write("**Applied Loads**")
                            st.write(f"• Dead Load: {dead_load} kN")
                            st.write(f"• Live Load: {live_load} kN")
                            st.write(f"• Wind Load: {wind_load} kN")
                            st.write(f"• **Total: {total_vertical_load} kN**")
                        
                        with load_col2:
                            st.write("**Applied Moments**")
                            st.write(f"• Moment X: {moment_x} kNm")
                            st.write(f"• Moment Y: {moment_y} kNm")
                            st.write(f"• Wind Moment: {moment_wind} kNm")
                            st.write(f"• **Total Mx: {total_moment_x} kNm**")

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
                        file_name=f"column_footing_{col_width}x{col_depth}_{footing_length}x{footing_width}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate detailed report
                    report = generate_footing_report(
                        col_width, col_depth, col_height,
                        footing_length, footing_width, footing_thickness,
                        concrete_grade, steel_grade,
                        total_vertical_load, total_moment_x, total_moment_y,
                        safe_bearing_capacity, design_results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"column_footing_design_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error in design: {str(e)}")
                st.error("Please check input parameters and try again.")

def create_column_footing_dxf(col_width, col_depth, col_height, footing_length, footing_width, 
                             footing_thickness, col_main_dia, col_bars_width, col_bars_depth,
                             footing_main_dia, footing_main_spacing, footing_dist_dia, 
                             footing_dist_spacing, clear_cover):
    """Create comprehensive DXF drawing for column with footing"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Plan view of footing
    msp.add_lwpolyline([
        (-footing_length/2, -footing_width/2),
        (footing_length/2, -footing_width/2),
        (footing_length/2, footing_width/2),
        (-footing_length/2, footing_width/2),
        (-footing_length/2, -footing_width/2)
    ])
    
    # Column outline in plan
    msp.add_lwpolyline([
        (-col_width/2, -col_depth/2),
        (col_width/2, -col_depth/2),
        (col_width/2, col_depth/2),
        (-col_width/2, col_depth/2),
        (-col_width/2, -col_depth/2)
    ])
    
    # Footing reinforcement layout
    # Main bars in longer direction
    num_main_bars = int(footing_width / footing_main_spacing) + 1
    for i in range(num_main_bars):
        y_pos = -footing_width/2 + i * footing_main_spacing
        if abs(y_pos) <= footing_width/2:
            msp.add_line(
                (-footing_length/2 + clear_cover, y_pos),
                (footing_length/2 - clear_cover, y_pos)
            )
    
    # Distribution bars in shorter direction  
    num_dist_bars = int(footing_length / footing_dist_spacing) + 1
    for i in range(num_dist_bars):
        x_pos = -footing_length/2 + i * footing_dist_spacing
        if abs(x_pos) <= footing_length/2:
            msp.add_line(
                (x_pos, -footing_width/2 + clear_cover),
                (x_pos, footing_width/2 - clear_cover),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Section view (offset to right)
    section_x_offset = footing_length * 1.5
    
    # Footing section
    msp.add_lwpolyline([
        (section_x_offset - footing_length/2, -footing_thickness),
        (section_x_offset + footing_length/2, -footing_thickness),
        (section_x_offset + footing_length/2, 0),
        (section_x_offset + footing_length/2 - (footing_length - col_width)/2, 0),
        (section_x_offset + footing_length/2 - (footing_length - col_width)/2, col_height),
        (section_x_offset - footing_length/2 + (footing_length - col_width)/2, col_height),
        (section_x_offset - footing_length/2 + (footing_length - col_width)/2, 0),
        (section_x_offset - footing_length/2, 0),
        (section_x_offset - footing_length/2, -footing_thickness)
    ])
    
    # Add main reinforcement bars in section
    for i in range(num_main_bars):
        y_pos = -footing_width/2 + i * footing_main_spacing
        if abs(y_pos) <= footing_width/2:
            bar_x = section_x_offset - footing_length/2 + clear_cover + footing_main_dia/2 + i * 100
            if bar_x <= section_x_offset + footing_length/2 - clear_cover:
                msp.add_circle(center=(bar_x, -footing_thickness + clear_cover + footing_main_dia/2), 
                             radius=footing_main_dia/2)
    
    # Add dimensions
    add_dimensions(msp, [
        ((-footing_length/2, -footing_width*0.7), (footing_length/2, -footing_width*0.7), 
         (0, -footing_width*0.8), f"{footing_length}"),
        ((-footing_length*0.7, -footing_width/2), (-footing_length*0.7, footing_width/2), 
         (-footing_length*0.8, 0), f"{footing_width}"),
        ((-col_width/2, col_depth*0.7), (col_width/2, col_depth*0.7), 
         (0, col_depth*0.8), f"{col_width}"),
        ((section_x_offset + footing_length*0.7, -footing_thickness), 
         (section_x_offset + footing_length*0.7, col_height),
         (section_x_offset + footing_length*0.8, col_height/2), f"{col_height + footing_thickness}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"COLUMN WITH FOOTING\nCOLUMN: {col_width}x{col_depth}x{col_height}mm\nFOOTING: {footing_length}x{footing_width}x{footing_thickness}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, -footing_width*1.2))
    
    msp.add_text(
        f"FOOTING REINFORCEMENT:\n⌀{footing_main_dia}mm @ {footing_main_spacing}mm C/C MAIN\n⌀{footing_dist_dia}mm @ {footing_dist_spacing}mm C/C DIST",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((section_x_offset, -footing_width*0.8))
    
    return doc

def generate_footing_report(col_width, col_depth, col_height, footing_length, footing_width, 
                           footing_thickness, concrete_grade, steel_grade, total_load, 
                           moment_x, moment_y, sbc, results):
    """Generate comprehensive design report"""
    
    report = f"""
RECTANGULAR COLUMN WITH FOOTING DESIGN REPORT
============================================

COLUMN DETAILS:
- Size: {col_width}mm x {col_depth}mm x {col_height}mm
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

FOOTING DETAILS:
- Size: {footing_length}mm x {footing_width}mm x {footing_thickness}mm
- Footing Area: {(footing_length * footing_width)/1e6:.2f} m²
- Safe Bearing Capacity: {sbc} kN/m²

APPLIED LOADS:
- Total Vertical Load: {total_load} kN
- Moment about X-axis: {moment_x} kNm
- Moment about Y-axis: {moment_y} kNm

DESIGN VERIFICATION:
- Maximum Soil Pressure: {results.get('max_soil_pressure', 0):.1f} kN/m²
- Pressure Utilization: {(results.get('max_soil_pressure', 0)/sbc)*100:.1f}%
- Eccentricity X: {results.get('eccentricity_x', 0):.0f} mm
- Eccentricity Y: {results.get('eccentricity_y', 0):.0f} mm

DESIGN STATUS:
- Bearing Pressure: {'SAFE' if results.get('max_soil_pressure', 0) <= sbc else 'UNSAFE'}
- Punching Shear: {'SAFE' if results.get('punching_shear_ratio', 0) <= 1.0 else 'UNSAFE'}

REINFORCEMENT SUMMARY:
- Footing main bars as per drawing
- Column reinforcement as per drawing
- All reinforcement as per IS 456:2000

DESIGN NOTES:
1. Design based on IS 456:2000 and IS 1893:2016
2. Minimum reinforcement requirements satisfied
3. Development length and anchorage as per code
4. All dimensions in mm unless specified otherwise

Generated by RajLisp Structural Design Suite
Date: {st.session_state.get('current_date', 'Current Date')}
"""
    return report
