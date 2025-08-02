import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_l_beam_capacity

def page_l_beam():
    st.title("📏 L-Beam Designer")
    st.markdown("Design reinforced concrete L-beams for edge beams and spandrel applications")

    with st.form("l_beam_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 L-Beam Dimensions")
            span = st.number_input("Span (mm)", min_value=2000, max_value=12000, value=5000, step=500,
                                 help="Clear span of L-beam")
            
            st.markdown("**Vertical Web**")
            web_width = st.number_input("Web Width (mm)", min_value=200, max_value=400, value=300, step=25,
                                      help="Thickness of vertical web")
            web_height = st.number_input("Web Height (mm)", min_value=300, max_value=800, value=500, step=50,
                                       help="Height of vertical web")
            
            st.markdown("**Horizontal Flange**")
            flange_width = st.number_input("Flange Width (mm)", min_value=200, max_value=1000, value=400, step=50,
                                         help="Width of horizontal flange")
            flange_thickness = st.number_input("Flange Thickness (mm)", min_value=100, max_value=300, value=150, step=25,
                                             help="Thickness of horizontal flange")

        with col2:
            st.subheader("🔩 Web Reinforcement")
            web_main_dia = st.selectbox("Web Main Bar ⌀ (mm)", [16, 20, 25, 32], index=1,
                                      help="Main tension bars in web")
            num_web_bars = st.slider("Number of Web Bars", min_value=3, max_value=8, value=4, step=1,
                                   help="Main bars in vertical web")
            
            web_top_dia = st.selectbox("Web Top Bar ⌀ (mm)", [12, 16, 20], index=1,
                                     help="Top bars in web")
            num_web_top = st.slider("Number of Web Top Bars", min_value=2, max_value=6, value=3, step=1,
                                  help="Compression bars in web")
            
            st.markdown("**Flange Reinforcement**")
            flange_main_dia = st.selectbox("Flange Main Bar ⌀ (mm)", [12, 16, 20, 25], index=1,
                                         help="Main bars in flange")
            flange_bar_spacing = st.number_input("Flange Bar Spacing (mm)", min_value=150, max_value=300, value=200, step=25,
                                                help="Spacing of bars in flange")

        with col3:
            st.subheader("🔧 Shear & Distribution")
            stirrup_dia = st.selectbox("Stirrup Diameter (mm)", [8, 10, 12], index=1,
                                     help="Diameter of stirrups")
            stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=75, max_value=250, value=150, step=25,
                                            help="Spacing of stirrups")
            
            dist_bar_dia = st.selectbox("Distribution Bar ⌀ (mm)", [8, 10, 12], index=1,
                                      help="Distribution bars in flange")
            dist_bar_spacing = st.number_input("Distribution Spacing (mm)", min_value=150, max_value=300, value=200, step=25,
                                             help="Spacing of distribution bars")
            
            st.subheader("🏗️ Materials & Loading")
            concrete_grade = st.selectbox("Concrete Grade", ["M25", "M30", "M35"], index=1)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500"], index=1)
            clear_cover = st.number_input("Clear Cover (mm)", min_value=25, max_value=50, value=40, step=5)
            
            # Loading
            dead_load = st.number_input("Dead Load (kN/m)", min_value=0, max_value=80, value=25, step=5)
            live_load = st.number_input("Live Load (kN/m)", min_value=0, max_value=40, value=15, step=5)

        submitted = st.form_submit_button("🔄 Design L-Beam", type="primary")

    if submitted:
        with st.spinner("🔄 Designing L-beam..."):
            try:
                # Calculate design parameters
                total_depth = max(web_height, flange_thickness)
                total_load = dead_load + live_load
                design_moment = total_load * (span/1000)**2 / 8  # kNm
                design_shear = total_load * (span/1000) / 2  # kN
                
                # Self weight calculation
                web_volume = (web_width * web_height) / 1e6  # m²
                flange_volume = (flange_width * flange_thickness) / 1e6  # m²
                self_weight = 25 * (web_volume + flange_volume)  # kN/m
                
                # Perform L-beam design calculations
                results = calculate_l_beam_capacity(
                    web_width, web_height, flange_width, flange_thickness,
                    concrete_grade, steel_grade, web_main_dia, num_web_bars,
                    flange_main_dia, design_moment
                )

                # Create DXF drawing
                doc = create_l_beam_dxf(
                    span, web_width, web_height, flange_width, flange_thickness,
                    web_main_dia, num_web_bars, web_top_dia, num_web_top,
                    flange_main_dia, flange_bar_spacing, stirrup_dia, stirrup_spacing,
                    dist_bar_dia, dist_bar_spacing, clear_cover
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ L-beam design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**L-Beam Dimensions**")
                            st.write(f"• Span: {span} mm")
                            st.write(f"• Web: {web_width} × {web_height} mm")
                            st.write(f"• Flange: {flange_width} × {flange_thickness} mm")
                            st.write(f"• Total Depth: {total_depth} mm")
                            
                            # Effective depth calculation
                            effective_depth = web_height - clear_cover - stirrup_dia - web_main_dia/2
                            st.write(f"• Effective Depth: {effective_depth:.0f} mm")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement Summary**")
                            st.write(f"• Web Main: {num_web_bars}-⌀{web_main_dia}mm")
                            st.write(f"• Web Top: {num_web_top}-⌀{web_top_dia}mm")
                            
                            web_steel_area = num_web_bars * np.pi * (web_main_dia/2)**2
                            st.write(f"• Web Steel Area: {web_steel_area:.0f} mm²")
                            
                            # Number of flange bars
                            num_flange_bars = int(flange_width / flange_bar_spacing) + 1
                            st.write(f"• Flange Bars: {num_flange_bars}-⌀{flange_main_dia}mm")
                            st.write(f"• Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm")

                    # Load analysis
                    with st.expander("📊 Load Analysis", expanded=True):
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
                            
                            # L-beam section properties
                            section_modulus = results.get('section_modulus', 0)
                            st.write(f"• Section Modulus: {section_modulus:.2e} mm³")

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
                                st.markdown("**L-Beam Properties**")
                                neutral_axis = results.get('neutral_axis_depth', 0)
                                
                                st.write(f"• Neutral Axis: {neutral_axis:.0f} mm from top")
                                
                                # Check section behavior
                                if neutral_axis <= flange_thickness:
                                    st.info("ℹ️ Neutral axis in flange")
                                else:
                                    st.info("ℹ️ Neutral axis in web")
                                
                                # Steel percentage check
                                gross_area = web_width * web_height + flange_width * flange_thickness
                                total_steel = web_steel_area + num_flange_bars * np.pi * (flange_main_dia/2)**2
                                steel_percent = (total_steel / gross_area) * 100
                                
                                st.write(f"• Total Steel %: {steel_percent:.2f}%")
                                
                                if 0.85 <= steel_percent <= 4.0:
                                    st.success("✅ Steel % within limits")
                                else:
                                    st.warning("⚠️ Check steel percentage limits")

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
                        file_name=f"l_beam_{span}_{web_width}x{web_height}_{flange_width}x{flange_thickness}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_l_beam_report(
                        span, web_width, web_height, flange_width, flange_thickness,
                        concrete_grade, steel_grade, web_main_dia, num_web_bars,
                        total_with_self, actual_moment, actual_shear, results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"l_beam_design_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_l_beam_dxf(span, web_width, web_height, flange_width, flange_thickness,
                     web_main_dia, num_web_bars, web_top_dia, num_web_top,
                     flange_main_dia, flange_bar_spacing, stirrup_dia, stirrup_spacing,
                     dist_bar_dia, dist_bar_spacing, clear_cover):
    """Create DXF drawing for L-beam"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Cross-section view
    # L-beam outline
    l_beam_outline = [
        (0, 0),  # Bottom left of flange
        (flange_width, 0),  # Bottom right of flange
        (flange_width, flange_thickness),  # Top right of flange
        (web_width, flange_thickness),  # Junction point
        (web_width, web_height),  # Top right of web
        (0, web_height),  # Top left of web
        (0, 0)  # Back to start
    ]
    msp.add_lwpolyline(l_beam_outline)
    
    # Web reinforcement
    # Bottom bars in web
    web_bottom_y = clear_cover + stirrup_dia + web_main_dia/2
    web_bar_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_web_bars*web_main_dia) / (num_web_bars - 1) if num_web_bars > 1 else 0
    
    for i in range(num_web_bars):
        x_pos = clear_cover + stirrup_dia + web_main_dia/2 + i * (web_bar_spacing + web_main_dia)
        msp.add_circle(center=(x_pos, web_bottom_y), radius=web_main_dia/2)
    
    # Top bars in web
    web_top_y = web_height - clear_cover - stirrup_dia - web_top_dia/2
    web_top_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_web_top*web_top_dia) / (num_web_top - 1) if num_web_top > 1 else 0
    
    for i in range(num_web_top):
        x_pos = clear_cover + stirrup_dia + web_top_dia/2 + i * (web_top_spacing + web_top_dia)
        msp.add_circle(center=(x_pos, web_top_y), radius=web_top_dia/2)
    
    # Flange reinforcement
    num_flange_bars = int(flange_width / flange_bar_spacing) + 1
    flange_y = clear_cover + flange_main_dia/2
    
    for i in range(num_flange_bars):
        x_pos = i * flange_bar_spacing
        if x_pos <= flange_width:
            msp.add_circle(center=(x_pos, flange_y), radius=flange_main_dia/2)
    
    # Distribution bars in flange
    num_dist_bars = int(flange_thickness / dist_bar_spacing) + 1
    for i in range(num_dist_bars):
        y_pos = i * dist_bar_spacing
        if y_pos <= flange_thickness:
            msp.add_line(
                (clear_cover, y_pos),
                (flange_width - clear_cover, y_pos),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Stirrups in web
    stirrup_outline = [
        (clear_cover + stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2),
        (web_width - clear_cover - stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2),
        (web_width - clear_cover - stirrup_dia/2, web_height - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, web_height - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, flange_thickness + clear_cover + stirrup_dia/2)
    ]
    msp.add_lwpolyline(stirrup_outline, dxfattribs={'linetype': 'DASHED'})
    
    # Elevation view (offset to right)
    elevation_x_offset = flange_width * 1.5
    
    # Simplified elevation - web only
    msp.add_lwpolyline([
        (elevation_x_offset, 0),
        (elevation_x_offset + web_width, 0),
        (elevation_x_offset + web_width, web_height),
        (elevation_x_offset, web_height),
        (elevation_x_offset, 0)
    ])
    
    # Show flange in elevation as top projection
    msp.add_lwpolyline([
        (elevation_x_offset, web_height),
        (elevation_x_offset + flange_width, web_height),
        (elevation_x_offset + flange_width, web_height + 50),  # Small projection
        (elevation_x_offset, web_height + 50),
        (elevation_x_offset, web_height)
    ], dxfattribs={'linetype': 'DASHED'})
    
    # Stirrups in elevation
    num_stirrups = int(span / stirrup_spacing) + 1
    for i in range(0, num_stirrups, 4):  # Show every 4th stirrup
        x_pos = elevation_x_offset + clear_cover + (i * stirrup_spacing / 20)  # Scaled
        if x_pos <= elevation_x_offset + web_width - clear_cover:
            msp.add_line(
                (x_pos, flange_thickness + clear_cover),
                (x_pos, web_height - clear_cover),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Plan view (offset below)
    plan_y_offset = -web_height - 300
    
    # L-beam in plan
    l_plan_outline = [
        (0, plan_y_offset),
        (flange_width, plan_y_offset),
        (flange_width, plan_y_offset + flange_thickness),
        (web_width, plan_y_offset + flange_thickness),
        (web_width, plan_y_offset + 1000),  # Extended length
        (0, plan_y_offset + 1000),
        (0, plan_y_offset)
    ]
    msp.add_lwpolyline(l_plan_outline)
    
    # Add dimensions
    add_dimensions(msp, [
        ((0, -100), (flange_width, -100), (flange_width/2, -150), f"{flange_width}"),
        ((0, -75), (web_width, -75), (web_width/2, -125), f"{web_width}"),
        ((-100, 0), (-100, flange_thickness), (-150, flange_thickness/2), f"{flange_thickness}"),
        ((-100, flange_thickness), (-100, web_height), (-150, (flange_thickness + web_height)/2), f"{web_height - flange_thickness}"),
        ((elevation_x_offset - 50, 0), (elevation_x_offset - 50, web_height), (elevation_x_offset - 100, web_height/2), f"{web_height}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"L-BEAM CROSS SECTION\nWEB: {web_width} x {web_height}mm\nFLANGE: {flange_width} x {flange_thickness}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, web_height + 150))
    
    msp.add_text(
        f"SPAN: {span}mm\nWEB REINFORCEMENT:\nMAIN: {num_web_bars}-⌀{web_main_dia}mm\nTOP: {num_web_top}-⌀{web_top_dia}mm\nFLANGE: ⌀{flange_main_dia}mm @ {flange_bar_spacing}mm",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((elevation_x_offset + web_width + 100, web_height/2))
    
    return doc

def generate_l_beam_report(span, web_width, web_height, flange_width, flange_thickness,
                          concrete_grade, steel_grade, web_main_dia, num_web_bars,
                          total_load, design_moment, design_shear, results):
    """Generate L-beam design report"""
    
    web_steel_area = num_web_bars * np.pi * (web_main_dia/2)**2
    gross_area = web_width * web_height + flange_width * flange_thickness
    
    report = f"""
L-BEAM DESIGN REPORT
====================

GEOMETRY:
- Span: {span} mm
- Web Dimensions: {web_width} x {web_height} mm
- Flange Dimensions: {flange_width} x {flange_thickness} mm
- Gross Section Area: {gross_area:.0f} mm²

MATERIALS:
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

LOADING:
- Total Applied Load: {total_load:.1f} kN/m
- Design Moment: {design_moment:.2f} kNm
- Design Shear: {design_shear:.1f} kN

WEB REINFORCEMENT:
- Main Bars: {num_web_bars} - ⌀{web_main_dia}mm
- Main Steel Area: {web_steel_area:.0f} mm²
- Steel Percentage (Web): {(web_steel_area/(web_width*web_height))*100:.2f}%

DESIGN VERIFICATION:
- Moment Capacity: {results.get('moment_capacity', 0):.2f} kNm
- Neutral Axis Depth: {results.get('neutral_axis_depth', 0):.0f} mm
- Applied/Capacity Ratio: {design_moment/results.get('moment_capacity', 1):.2f}
- Design Status: {'SAFE' if design_moment <= results.get('moment_capacity', 0) else 'REVIEW REQUIRED'}

L-BEAM CHARACTERISTICS:
- Section Type: L-shaped (Edge beam/Spandrel)
- Effective Flange Width: {flange_width} mm
- Unsymmetrical section properties considered
- Torsional effects may need separate analysis

DESIGN CONSIDERATIONS:
1. L-beam behavior with unsymmetrical section
2. Lateral-torsional buckling check required
3. Effective flange width as per IS 456:2000
4. Proper connection between web and flange
5. Adequate lateral support required

CONSTRUCTION NOTES:
1. Ensure proper consolidation at web-flange junction
2. Provide adequate lateral bracing
3. Consider construction sequence effects
4. Proper anchorage of flange reinforcement

Generated by RajLisp Structural Design Suite
"""
    return report
