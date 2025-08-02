import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_t_beam_capacity

def page_t_beam():
    st.title("📐 T-Beam Designer")
    st.markdown("Design reinforced concrete T-beams with flange and web reinforcement")

    with st.form("t_beam_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 T-Beam Dimensions")
            span = st.number_input("Span (mm)", min_value=2000, max_value=15000, value=6000, step=500,
                                 help="Clear span of T-beam")
            
            st.markdown("**Flange Dimensions**")
            flange_width = st.number_input("Flange Width (mm)", min_value=500, max_value=3000, value=1200, step=100,
                                         help="Total width of flange")
            flange_thickness = st.number_input("Flange Thickness (mm)", min_value=75, max_value=200, value=125, step=25,
                                             help="Thickness of compression flange")
            
            st.markdown("**Web Dimensions**")
            web_width = st.number_input("Web Width (mm)", min_value=200, max_value=500, value=300, step=25,
                                      help="Width of web")
            web_depth = st.number_input("Web Depth (mm)", min_value=300, max_value=1200, value=600, step=50,
                                      help="Depth of web below flange")

        with col2:
            st.subheader("🔩 Main Reinforcement")
            bottom_bar_dia = st.selectbox("Bottom Bar Diameter (mm)", [16, 20, 25, 32, 40], index=2,
                                        help="Diameter of tension reinforcement")
            num_bottom_bars = st.slider("Number of Bottom Bars", min_value=3, max_value=12, value=6, step=1,
                                      help="Number of tension bars in web")
            
            top_bar_dia = st.selectbox("Top Bar Diameter (mm)", [12, 16, 20, 25], index=1,
                                     help="Diameter of compression bars")
            num_top_bars = st.slider("Number of Top Bars", min_value=2, max_value=8, value=4, step=1,
                                   help="Number of compression bars")
            
            st.markdown("**Flange Reinforcement**")
            flange_bar_dia = st.selectbox("Flange Bar Diameter (mm)", [10, 12, 16], index=1,
                                        help="Diameter of flange distribution bars")
            flange_bar_spacing = st.number_input("Flange Bar Spacing (mm)", min_value=150, max_value=300, value=200, step=25,
                                                help="Spacing of distribution bars in flange")

        with col3:
            st.subheader("🔧 Shear Reinforcement")
            stirrup_dia = st.selectbox("Stirrup Diameter (mm)", [8, 10, 12, 16], index=1,
                                     help="Diameter of stirrups")
            stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=75, max_value=300, value=150, step=25,
                                            help="Spacing of stirrups")
            
            st.subheader("🏗️ Materials & Loading")
            concrete_grade = st.selectbox("Concrete Grade", ["M25", "M30", "M35", "M40"], index=1)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
            clear_cover = st.number_input("Clear Cover (mm)", min_value=25, max_value=50, value=40, step=5)
            
            st.markdown("**Design Loads**")
            dead_load = st.number_input("Dead Load (kN/m)", min_value=0, max_value=100, value=20, step=5,
                                      help="Dead load including self weight")
            live_load = st.number_input("Live Load (kN/m)", min_value=0, max_value=50, value=15, step=5,
                                      help="Live load on beam")

        submitted = st.form_submit_button("🔄 Design T-Beam", type="primary")

    if submitted:
        with st.spinner("🔄 Designing T-beam..."):
            try:
                # Calculate design parameters
                total_depth = flange_thickness + web_depth
                total_load = dead_load + live_load
                design_moment = total_load * (span/1000)**2 / 8  # kNm for simply supported
                design_shear = total_load * (span/1000) / 2  # kN
                
                # Self weight check
                flange_volume = (flange_width * flange_thickness) / 1e6  # m²
                web_volume = (web_width * web_depth) / 1e6  # m²
                self_weight = 25 * (flange_volume + web_volume)  # kN/m
                
                # Perform T-beam design calculations
                results = calculate_t_beam_capacity(
                    flange_width, flange_thickness, web_width, web_depth,
                    concrete_grade, steel_grade, bottom_bar_dia, num_bottom_bars,
                    design_moment
                )

                # Create DXF drawing
                doc = create_t_beam_dxf(
                    span, flange_width, flange_thickness, web_width, web_depth,
                    bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                    flange_bar_dia, flange_bar_spacing, stirrup_dia, stirrup_spacing, clear_cover
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ T-beam design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**T-Beam Dimensions**")
                            st.write(f"• Span: {span} mm")
                            st.write(f"• Total Depth: {total_depth} mm")
                            st.write(f"• Flange: {flange_width} × {flange_thickness} mm")
                            st.write(f"• Web: {web_width} × {web_depth} mm")
                            
                            # Calculate section properties
                            effective_depth = total_depth - clear_cover - stirrup_dia - bottom_bar_dia/2
                            st.write(f"• Effective Depth: {effective_depth:.0f} mm")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement Summary**")
                            st.write(f"• Bottom Bars: {num_bottom_bars}-⌀{bottom_bar_dia}mm")
                            st.write(f"• Top Bars: {num_top_bars}-⌀{top_bar_dia}mm")
                            
                            bottom_steel_area = num_bottom_bars * np.pi * (bottom_bar_dia/2)**2
                            st.write(f"• Bottom Steel: {bottom_steel_area:.0f} mm²")
                            
                            web_area = web_width * total_depth
                            steel_percentage = (bottom_steel_area / web_area) * 100
                            st.write(f"• Steel %: {steel_percentage:.2f}%")
                            
                            st.write(f"• Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm")

                    # Load analysis
                    with st.expander("📊 Load & Moment Analysis", expanded=True):
                        load_col1, load_col2 = st.columns(2)
                        
                        with load_col1:
                            st.markdown("**Applied Loads**")
                            st.write(f"• Dead Load: {dead_load} kN/m")
                            st.write(f"• Live Load: {live_load} kN/m")
                            st.write(f"• Self Weight: {self_weight:.1f} kN/m")
                            total_with_self = total_load + self_weight
                            st.write(f"• **Total Load: {total_with_self:.1f} kN/m**")
                            
                        with load_col2:
                            st.markdown("**Design Forces**")
                            actual_moment = total_with_self * (span/1000)**2 / 8
                            actual_shear = total_with_self * (span/1000) / 2
                            
                            st.write(f"• Design Moment: {actual_moment:.2f} kNm")
                            st.write(f"• Design Shear: {actual_shear:.1f} kN")
                            
                            # Span to depth ratio
                            span_depth_ratio = span / total_depth
                            st.write(f"• Span/Depth Ratio: {span_depth_ratio:.1f}")
                            
                            limiting_ratio = 20 if concrete_grade in ["M20", "M25"] else 26
                            if span_depth_ratio <= limiting_ratio:
                                st.success(f"✅ Span/Depth OK (limit: {limiting_ratio})")
                            else:
                                st.warning(f"⚠️ Check deflection (limit: {limiting_ratio})")

                    # Design verification
                    if results:
                        with st.expander("🔍 Design Verification", expanded=True):
                            verify_col1, verify_col2 = st.columns(2)
                            
                            with verify_col1:
                                st.markdown("**Moment Capacity**")
                                moment_capacity = results.get('moment_capacity', 0)
                                moment_ratio = actual_moment / moment_capacity if moment_capacity > 0 else 1
                                
                                st.write(f"• Moment Capacity: {moment_capacity:.2f} kNm")
                                st.write(f"• Applied Moment: {actual_moment:.2f} kNm")
                                st.write(f"• Utilization: {moment_ratio*100:.1f}%")
                                
                                if moment_ratio <= 1.0:
                                    st.success(f"✅ Design SAFE - Ratio: {moment_ratio:.2f}")
                                else:
                                    st.error(f"❌ Design UNSAFE - Ratio: {moment_ratio:.2f}")
                            
                            with verify_col2:
                                st.markdown("**Section Properties**")
                                neutral_axis = results.get('neutral_axis_depth', 0)
                                lever_arm = results.get('lever_arm', 0)
                                
                                st.write(f"• Neutral Axis Depth: {neutral_axis:.0f} mm")
                                st.write(f"• Lever Arm: {lever_arm:.0f} mm")
                                
                                # Check if neutral axis is in flange
                                if neutral_axis <= flange_thickness:
                                    st.info("ℹ️ Neutral axis in flange - Rectangular beam behavior")
                                else:
                                    st.info("ℹ️ Neutral axis in web - T-beam behavior")

                with col_download:
                    st.subheader("📥 Download")
                    
                    # Save DXF
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                        doc.saveas(fp.name)
                        with open(fp.name, "rb") as f:
                            dxf_data = f.read()
                    
                    st.download_button(
                        label="📐 Download DXF",
                        data=dxf_data,
                        file_name=f"t_beam_{span}_{flange_width}x{total_depth}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_t_beam_report(
                        span, flange_width, flange_thickness, web_width, web_depth,
                        concrete_grade, steel_grade, bottom_bar_dia, num_bottom_bars,
                        total_with_self, actual_moment, actual_shear, results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"t_beam_design_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_t_beam_dxf(span, flange_width, flange_thickness, web_width, web_depth,
                     bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                     flange_bar_dia, flange_bar_spacing, stirrup_dia, stirrup_spacing, clear_cover):
    """Create DXF drawing for T-beam"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    total_depth = flange_thickness + web_depth
    
    # Cross-section view
    # T-beam outline
    t_beam_outline = [
        (0, 0),
        (flange_width, 0),
        (flange_width, flange_thickness),
        ((flange_width + web_width)/2, flange_thickness),
        ((flange_width + web_width)/2, total_depth),
        ((flange_width - web_width)/2, total_depth),
        ((flange_width - web_width)/2, flange_thickness),
        (0, flange_thickness),
        (0, 0)
    ]
    msp.add_lwpolyline(t_beam_outline)
    
    # Reinforcement in cross-section
    web_start_x = (flange_width - web_width) / 2
    web_end_x = (flange_width + web_width) / 2
    
    # Bottom bars
    bottom_y = total_depth - clear_cover - stirrup_dia - bottom_bar_dia/2
    bottom_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_bottom_bars*bottom_bar_dia) / (num_bottom_bars - 1) if num_bottom_bars > 1 else 0
    
    for i in range(num_bottom_bars):
        x_pos = web_start_x + clear_cover + stirrup_dia + bottom_bar_dia/2 + i * (bottom_spacing + bottom_bar_dia)
        msp.add_circle(center=(x_pos, bottom_y), radius=bottom_bar_dia/2)
    
    # Top bars
    top_y = clear_cover + stirrup_dia + top_bar_dia/2
    top_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_top_bars*top_bar_dia) / (num_top_bars - 1) if num_top_bars > 1 else 0
    
    for i in range(num_top_bars):
        x_pos = web_start_x + clear_cover + stirrup_dia + top_bar_dia/2 + i * (top_spacing + top_bar_dia)
        msp.add_circle(center=(x_pos, top_y), radius=top_bar_dia/2)
    
    # Flange distribution bars
    num_flange_bars = int(flange_width / flange_bar_spacing) + 1
    flange_bar_y = clear_cover + flange_bar_dia/2
    
    for i in range(num_flange_bars):
        x_pos = i * flange_bar_spacing
        if x_pos <= flange_width:
            msp.add_circle(center=(x_pos, flange_bar_y), radius=flange_bar_dia/2)
    
    # Stirrups
    stirrup_outline = [
        (web_start_x + clear_cover + stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2),
        (web_end_x - clear_cover - stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2),
        (web_end_x - clear_cover - stirrup_dia/2, total_depth - clear_cover - stirrup_dia/2),
        (web_start_x + clear_cover + stirrup_dia/2, total_depth - clear_cover - stirrup_dia/2),
        (web_start_x + clear_cover + stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2)
    ]
    msp.add_lwpolyline(stirrup_outline, dxfattribs={'linetype': 'DASHED'})
    
    # Elevation view (offset to right)
    elevation_x_offset = flange_width * 1.5
    
    # Simplified elevation showing web only
    msp.add_lwpolyline([
        (elevation_x_offset, 0),
        (elevation_x_offset + web_width, 0),
        (elevation_x_offset + web_width, total_depth),
        (elevation_x_offset, total_depth),
        (elevation_x_offset, 0)
    ])
    
    # Stirrups in elevation
    num_stirrups = int(span / stirrup_spacing) + 1
    for i in range(0, num_stirrups, 3):  # Show every 3rd stirrup for clarity
        x_pos = elevation_x_offset + clear_cover + i * stirrup_spacing/10  # Scaled for drawing
        if x_pos <= elevation_x_offset + web_width - clear_cover:
            msp.add_line(
                (x_pos, clear_cover),
                (x_pos, total_depth - clear_cover),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Main bars in elevation
    msp.add_line(
        (elevation_x_offset + clear_cover + stirrup_dia + bottom_bar_dia/2, bottom_y),
        (elevation_x_offset + web_width - clear_cover - stirrup_dia - bottom_bar_dia/2, bottom_y)
    )
    
    msp.add_line(
        (elevation_x_offset + clear_cover + stirrup_dia + top_bar_dia/2, top_y),
        (elevation_x_offset + web_width - clear_cover - stirrup_dia - top_bar_dia/2, top_y),
        dxfattribs={'linetype': 'DASHED'}
    )
    
    # Plan view (offset below)
    plan_y_offset = -total_depth - 500
    
    # Flange in plan
    msp.add_lwpolyline([
        (0, plan_y_offset),
        (flange_width, plan_y_offset),
        (flange_width, plan_y_offset + 1000),  # 1m length shown
        (0, plan_y_offset + 1000),
        (0, plan_y_offset)
    ])
    
    # Web in plan
    msp.add_lwpolyline([
        (web_start_x, plan_y_offset),
        (web_end_x, plan_y_offset),
        (web_end_x, plan_y_offset + 1000),
        (web_start_x, plan_y_offset + 1000),
        (web_start_x, plan_y_offset)
    ], dxfattribs={'linetype': 'DASHED'})
    
    # Add dimensions
    add_dimensions(msp, [
        ((0, -100), (flange_width, -100), (flange_width/2, -150), f"{flange_width}"),
        ((web_start_x, -75), (web_end_x, -75), ((web_start_x + web_end_x)/2, -125), f"{web_width}"),
        ((-100, 0), (-100, flange_thickness), (-150, flange_thickness/2), f"{flange_thickness}"),
        ((-100, flange_thickness), (-100, total_depth), (-150, (flange_thickness + total_depth)/2), f"{web_depth}"),
        ((elevation_x_offset - 50, 0), (elevation_x_offset - 50, total_depth), (elevation_x_offset - 100, total_depth/2), f"{total_depth}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"T-BEAM CROSS SECTION\nFLANGE: {flange_width} x {flange_thickness}mm\nWEB: {web_width} x {web_depth}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, total_depth + 200))
    
    msp.add_text(
        f"SPAN: {span}mm\nREINFORCEMENT:\nBOTTOM: {num_bottom_bars}-⌀{bottom_bar_dia}mm\nTOP: {num_top_bars}-⌀{top_bar_dia}mm\nSTIRRUPS: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((elevation_x_offset + web_width + 100, total_depth/2))
    
    return doc

def generate_t_beam_report(span, flange_width, flange_thickness, web_width, web_depth,
                          concrete_grade, steel_grade, bottom_bar_dia, num_bottom_bars,
                          total_load, design_moment, design_shear, results):
    """Generate T-beam design report"""
    
    total_depth = flange_thickness + web_depth
    bottom_steel_area = num_bottom_bars * np.pi * (bottom_bar_dia/2)**2
    web_area = web_width * total_depth
    steel_percentage = (bottom_steel_area / web_area) * 100
    
    report = f"""
T-BEAM DESIGN REPORT
====================

GEOMETRY:
- Span: {span} mm
- Total Depth: {total_depth} mm
- Flange Width: {flange_width} mm
- Flange Thickness: {flange_thickness} mm
- Web Width: {web_width} mm
- Web Depth: {web_depth} mm

MATERIALS:
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

LOADING:
- Total Applied Load: {total_load:.1f} kN/m
- Design Moment: {design_moment:.2f} kNm
- Design Shear: {design_shear:.1f} kN

REINFORCEMENT:
- Bottom Bars: {num_bottom_bars} - ⌀{bottom_bar_dia}mm
- Bottom Steel Area: {bottom_steel_area:.0f} mm²
- Steel Percentage: {steel_percentage:.2f}%

DESIGN VERIFICATION:
- Moment Capacity: {results.get('moment_capacity', 0):.2f} kNm
- Neutral Axis Depth: {results.get('neutral_axis_depth', 0):.0f} mm
- Applied/Capacity Ratio: {design_moment/results.get('moment_capacity', 1):.2f}
- Design Status: {'SAFE' if design_moment <= results.get('moment_capacity', 0) else 'REVIEW REQUIRED'}

SECTION PROPERTIES:
- Span to Depth Ratio: {span/total_depth:.1f}
- Effective Flange Width: As per IS 456:2000 Cl. 23.1.2
- Moment of Resistance: Based on T-beam theory

DESIGN ASSUMPTIONS:
1. T-beam action considered
2. Effective flange width as per code
3. Balanced or under-reinforced section
4. Linear strain distribution assumed

CONSTRUCTION REQUIREMENTS:
1. Proper connection between flange and web
2. Adequate lateral support to compression flange
3. Minimum reinforcement as per IS 456:2000
4. Proper detailing at supports and mid-span

Generated by RajLisp Structural Design Suite
"""
    return report
