import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_sunshade():
    st.title("🌞 Sunshade Designer")
    st.markdown("Design cantilever sunshades with supporting beam and reinforcement details")

    with st.form("sunshade_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🔧 Beam Dimensions")
            web_width = st.number_input("Web Width (mm)", min_value=200, max_value=1000, value=300, step=10,
                                      help="Width of the supporting beam")
            total_depth = st.number_input("Beam Depth (mm)", min_value=200, max_value=1000, value=450, step=10,
                                        help="Total depth of the supporting beam")

            st.subheader("📏 Sunshade Dimensions")
            projection = st.number_input("Projection (mm)", min_value=500, max_value=3000, value=1000, step=50,
                                       help="Horizontal projection of the sunshade")
            support_thickness = st.number_input("Thickness at Support (mm)", min_value=100, max_value=300, value=150, step=10,
                                              help="Thickness where sunshade meets the wall")
            edge_thickness = st.number_input("Thickness at Edge (mm)", min_value=50, max_value=200, value=100, step=5,
                                           help="Thickness at the outer edge of sunshade")

        with col2:
            st.subheader("🔩 Beam Reinforcement")
            bottom_bar_dia = st.selectbox("Bottom Bar Diameter (mm)", [8, 10, 12, 16, 20, 25, 32], index=3,
                                        help="Diameter of bottom reinforcement bars")
            num_bottom_bars = st.slider("Number of Bottom Bars", min_value=2, max_value=10, value=4, step=1,
                                      help="Number of bars at the bottom of the beam")
            top_bar_dia = st.selectbox("Top Bar Diameter (mm)", [8, 10, 12, 16, 20, 25], index=2,
                                     help="Diameter of top reinforcement bars")
            num_top_bars = st.slider("Number of Top Bars", min_value=2, max_value=8, value=2, step=1,
                                   help="Number of bars at the top of the beam")
            stirrup_dia = st.selectbox("Stirrup Diameter (mm)", [6, 8, 10, 12], index=1,
                                     help="Diameter of shear reinforcement stirrups")
            stirrup_spacing = st.slider("Stirrup Spacing (mm)", min_value=50, max_value=300, value=150, step=10,
                                      help="Spacing between stirrups")

        with col3:
            st.subheader("🌞 Sunshade Reinforcement")
            main_bar_dia = st.selectbox("Main Bar Diameter (mm)", [8, 10, 12, 16], index=1,
                                      help="Diameter of main reinforcement bars in sunshade")
            dist_bar_dia = st.selectbox("Distribution Bar Diameter (mm)", [6, 8, 10, 12], index=1,
                                      help="Diameter of distribution bars in sunshade")
            dist_bar_spacing = st.slider("Distribution Bar Spacing (mm)", min_value=100, max_value=300, value=150, step=10,
                                       help="Spacing between distribution bars")

            st.subheader("⚙️ Drawing Settings")
            scale = st.slider("Drawing Scale (1:?)", min_value=10, max_value=100, value=25, step=5,
                            help="Scale factor for the drawing")
            sunshade_num = st.text_input("Sunshade Number", value="01",
                                       help="Identifier for this sunshade design")

        submitted = st.form_submit_button("🔄 Generate Sunshade Design", type="primary")

    if submitted:
        with st.spinner("🔄 Generating Sunshade Design..."):
            try:
                # Generate the DXF drawing
                doc = create_sunshade_dxf(
                    web_width, total_depth, projection, support_thickness, edge_thickness,
                    bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                    stirrup_dia, stirrup_spacing, main_bar_dia, dist_bar_dia,
                    dist_bar_spacing, scale, sunshade_num
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Sunshade design generated successfully!")

                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)

                        with summary_col1:
                            st.markdown("**Sunshade Dimensions**")
                            st.write(f"• Projection: {projection} mm")
                            st.write(f"• Thickness at Support: {support_thickness} mm")
                            st.write(f"• Thickness at Edge: {edge_thickness} mm")
                            
                            # Calculate sunshade area and volume
                            avg_thickness = (support_thickness + edge_thickness) / 2
                            sunshade_area = projection * 1000  # Assuming 1m width
                            sunshade_volume = sunshade_area * avg_thickness / 1e9  # m³
                            
                            st.write(f"• Average Thickness: {avg_thickness:.1f} mm")
                            st.write(f"• Volume (per m width): {sunshade_volume:.3f} m³")

                        with summary_col2:
                            st.markdown("**Supporting Beam**")
                            st.write(f"• Width: {web_width} mm")
                            st.write(f"• Depth: {total_depth} mm")
                            st.write(f"• Bottom: {num_bottom_bars}⌀{bottom_bar_dia}mm")
                            st.write(f"• Top: {num_top_bars}⌀{top_bar_dia}mm")
                            st.write(f"• Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm c/c")

                    # Reinforcement details
                    with st.expander("🔩 Reinforcement Details", expanded=True):
                        reinf_col1, reinf_col2 = st.columns(2)
                        
                        with reinf_col1:
                            st.markdown("**Sunshade Reinforcement**")
                            st.write(f"• Main Bars: ⌀{main_bar_dia}mm")
                            st.write(f"• Distribution Bars: ⌀{dist_bar_dia}mm @ {dist_bar_spacing}mm c/c")
                            
                            # Calculate reinforcement quantities
                            main_steel_area = np.pi * (main_bar_dia/2)**2
                            dist_bars_per_meter = 1000 / dist_bar_spacing
                            dist_steel_per_meter = dist_bars_per_meter * np.pi * (dist_bar_dia/2)**2
                            
                            st.write(f"• Main Steel Area: {main_steel_area:.1f} mm²/bar")
                            st.write(f"• Dist Steel: {dist_steel_per_meter:.0f} mm²/m")
                        
                        with reinf_col2:
                            st.markdown("**Beam Reinforcement**")
                            bottom_steel_area = num_bottom_bars * np.pi * (bottom_bar_dia/2)**2
                            top_steel_area = num_top_bars * np.pi * (top_bar_dia/2)**2
                            beam_gross_area = web_width * total_depth
                            
                            st.write(f"• Bottom Steel: {bottom_steel_area:.0f} mm²")
                            st.write(f"• Top Steel: {top_steel_area:.0f} mm²")
                            st.write(f"• Total Steel: {bottom_steel_area + top_steel_area:.0f} mm²")
                            
                            steel_percentage = ((bottom_steel_area + top_steel_area) / beam_gross_area) * 100
                            st.write(f"• Steel %: {steel_percentage:.2f}%")

                    # Design calculations
                    with st.expander("🧮 Design Calculations", expanded=False):
                        st.markdown("**Load Estimation**")
                        
                        # Self weight calculation
                        concrete_density = 25  # kN/m³
                        sunshade_self_weight = sunshade_volume * concrete_density * 1000  # N/m
                        live_load_sunshade = 1.5 * projection  # kN/m (1.5 kN/m² assumed)
                        
                        st.write(f"• Sunshade Self Weight: {sunshade_self_weight:.1f} N/m")
                        st.write(f"• Live Load on Sunshade: {live_load_sunshade:.1f} N/m")
                        st.write(f"• Total Load: {sunshade_self_weight + live_load_sunshade:.1f} N/m")
                        
                        # Moment calculation
                        total_load = (sunshade_self_weight + live_load_sunshade) / 1000  # kN/m
                        moment = total_load * (projection/1000)**2 / 2  # kNm/m
                        
                        st.write(f"• Design Moment: {moment:.2f} kNm/m")
                        
                        st.markdown("**Note:** These are preliminary calculations. Detailed analysis should consider wind loads, thermal effects, and other factors as per IS 456:2000.")

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
                        file_name=f"sunshade_ss_{sunshade_num}.dxf",
                        mime="application/dxf",
                        help="Download the DXF file for this design"
                    )
                    
                    # Generate design report
                    report = generate_sunshade_report(
                        web_width, total_depth, projection, support_thickness, edge_thickness,
                        bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                        stirrup_dia, stirrup_spacing, main_bar_dia, dist_bar_dia,
                        dist_bar_spacing, sunshade_num
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"sunshade_ss_{sunshade_num}_report.txt",
                        mime="text/plain",
                        help="Download detailed design report"
                    )

            except Exception as e:
                st.error(f"❌ Error generating drawing: {str(e)}")
                st.error("Please check your input values and try again.")

def create_sunshade_dxf(web_width, total_depth, projection, support_thickness, edge_thickness,
                       bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                       stirrup_dia, stirrup_spacing, main_bar_dia, dist_bar_dia,
                       dist_bar_spacing, scale, sunshade_num):
    """Create comprehensive DXF drawing for sunshade"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Scale factor for drawing
    scale_factor = 1.0 / scale
    
    # Main elevation view
    # Supporting beam
    beam_points = [
        (0, 0),
        (web_width, 0),
        (web_width, total_depth),
        (0, total_depth),
        (0, 0)
    ]
    msp.add_lwpolyline([(x * scale_factor, y * scale_factor) for x, y in beam_points])
    
    # Sunshade profile (cantilever)
    sunshade_points = [
        (0, total_depth),
        (projection, total_depth),
        (projection, total_depth + edge_thickness),
        (0, total_depth + support_thickness),
        (0, total_depth)
    ]
    msp.add_lwpolyline([(x * scale_factor, y * scale_factor) for x, y in sunshade_points])
    
    # Add reinforcement in beam elevation
    clear_cover = 40  # mm
    
    # Bottom reinforcement
    bottom_y = clear_cover + stirrup_dia + bottom_bar_dia/2
    bottom_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_bottom_bars*bottom_bar_dia) / (num_bottom_bars - 1) if num_bottom_bars > 1 else 0
    
    for i in range(num_bottom_bars):
        x_pos = clear_cover + stirrup_dia + bottom_bar_dia/2 + i * (bottom_spacing + bottom_bar_dia)
        msp.add_circle(center=(x_pos * scale_factor, bottom_y * scale_factor), radius=(bottom_bar_dia/2) * scale_factor)
    
    # Top reinforcement
    top_y = total_depth - clear_cover - stirrup_dia - top_bar_dia/2
    top_spacing = (web_width - 2*clear_cover - 2*stirrup_dia - num_top_bars*top_bar_dia) / (num_top_bars - 1) if num_top_bars > 1 else 0
    
    for i in range(num_top_bars):
        x_pos = clear_cover + stirrup_dia + top_bar_dia/2 + i * (top_spacing + top_bar_dia)
        msp.add_circle(center=(x_pos * scale_factor, top_y * scale_factor), radius=(top_bar_dia/2) * scale_factor)
    
    # Stirrups
    num_stirrups = int(projection / stirrup_spacing) + 2
    stirrup_points = [
        (clear_cover + stirrup_dia/2, clear_cover + stirrup_dia/2),
        (web_width - clear_cover - stirrup_dia/2, clear_cover + stirrup_dia/2),
        (web_width - clear_cover - stirrup_dia/2, total_depth - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, total_depth - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, clear_cover + stirrup_dia/2)
    ]
    
    for i in range(num_stirrups):
        x_offset = i * stirrup_spacing if i * stirrup_spacing <= projection else projection
        offset_stirrup = [(x + x_offset, y) for x, y in stirrup_points]
        msp.add_lwpolyline([(x * scale_factor, y * scale_factor) for x, y in offset_stirrup], 
                          dxfattribs={'linetype': 'DASHED'})
    
    # Sunshade reinforcement
    # Main reinforcement bars (longitudinal)
    num_main_bars_sunshade = int((support_thickness + edge_thickness) / 2 / 50) + 2  # Estimate based on thickness
    
    for i in range(num_main_bars_sunshade):
        y_spacing = (support_thickness - 2*clear_cover) / (num_main_bars_sunshade - 1) if num_main_bars_sunshade > 1 else 0
        y_pos = total_depth + clear_cover + main_bar_dia/2 + i * y_spacing
        
        # Tapered bar length
        start_x = clear_cover
        end_x = projection - clear_cover
        
        msp.add_line(
            (start_x * scale_factor, y_pos * scale_factor),
            (end_x * scale_factor, y_pos * scale_factor)
        )
    
    # Distribution bars (transverse)
    num_dist_bars = int(projection / dist_bar_spacing) + 1
    for i in range(num_dist_bars):
        x_pos = i * dist_bar_spacing
        if x_pos <= projection:
            # Calculate thickness at this position
            thickness_at_pos = support_thickness - (support_thickness - edge_thickness) * (x_pos / projection)
            y_start = total_depth + clear_cover
            y_end = total_depth + thickness_at_pos - clear_cover
            
            msp.add_line(
                (x_pos * scale_factor, y_start * scale_factor),
                (x_pos * scale_factor, y_end * scale_factor),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Plan view (offset below)
    plan_y_offset = -(total_depth + support_thickness + 500) * scale_factor
    
    # Beam plan
    beam_plan_points = [
        (0, 0),
        (web_width, 0),
        (web_width, 1000),  # Assuming 1m length for plan
        (0, 1000),
        (0, 0)
    ]
    msp.add_lwpolyline([(x * scale_factor, y * scale_factor + plan_y_offset) for x, y in beam_plan_points])
    
    # Sunshade plan
    sunshade_plan_points = [
        (0, 0),
        (projection, 0),
        (projection, 1000),
        (0, 1000),
        (0, 0)
    ]
    msp.add_lwpolyline([(x * scale_factor, y * scale_factor + plan_y_offset) for x, y in sunshade_plan_points])
    
    # Add dimensions
    dimension_offset = 200 * scale_factor
    
    # Horizontal dimensions
    msp.add_text(
        f"{web_width}",
        dxfattribs={'height': 50 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((web_width/2 * scale_factor, -dimension_offset))
    
    msp.add_text(
        f"{projection}",
        dxfattribs={'height': 50 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((projection/2 * scale_factor, (total_depth + support_thickness + 100) * scale_factor))
    
    # Vertical dimensions
    msp.add_text(
        f"{total_depth}",
        dxfattribs={'height': 50 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((-dimension_offset, total_depth/2 * scale_factor))
    
    msp.add_text(
        f"{support_thickness}",
        dxfattribs={'height': 30 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((-dimension_offset/2, (total_depth + support_thickness/2) * scale_factor))
    
    # Title and annotations
    title_y = (total_depth + support_thickness + 300) * scale_factor
    msp.add_text(
        f"SUNSHADE SS-{sunshade_num}\nSCALE 1:{scale}",
        dxfattribs={'height': 100 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((0, title_y))
    
    # Reinforcement schedule
    schedule_x = (projection + 500) * scale_factor
    schedule_text = f"""REINFORCEMENT SCHEDULE:
    
BEAM:
- BOTTOM: {num_bottom_bars}-⌀{bottom_bar_dia}mm
- TOP: {num_top_bars}-⌀{top_bar_dia}mm  
- STIRRUPS: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm C/C

SUNSHADE:
- MAIN: ⌀{main_bar_dia}mm LONGITUDINAL
- DISTRIBUTION: ⌀{dist_bar_dia}mm @ {dist_bar_spacing}mm C/C

NOTES:
- ALL DIMENSIONS IN MM
- CONCRETE GRADE M25
- STEEL GRADE Fe500
- CLEAR COVER 40MM"""
    
    msp.add_text(
        schedule_text,
        dxfattribs={'height': 40 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((schedule_x, 0))
    
    return doc

def generate_sunshade_report(web_width, total_depth, projection, support_thickness, edge_thickness,
                           bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                           stirrup_dia, stirrup_spacing, main_bar_dia, dist_bar_dia,
                           dist_bar_spacing, sunshade_num):
    """Generate detailed sunshade design report"""
    
    # Calculate quantities
    beam_volume = (web_width * total_depth * 1000) / 1e9  # m³ per meter length
    avg_sunshade_thickness = (support_thickness + edge_thickness) / 2
    sunshade_volume = (projection * avg_sunshade_thickness * 1000) / 1e9  # m³ per meter width
    
    bottom_steel_area = num_bottom_bars * np.pi * (bottom_bar_dia/2)**2
    top_steel_area = num_top_bars * np.pi * (top_bar_dia/2)**2
    total_beam_steel = bottom_steel_area + top_steel_area
    
    report = f"""
SUNSHADE DESIGN REPORT - SS-{sunshade_num}
==========================================

GEOMETRY:
- Projection: {projection} mm
- Support Thickness: {support_thickness} mm
- Edge Thickness: {edge_thickness} mm
- Average Thickness: {avg_sunshade_thickness:.1f} mm

SUPPORTING BEAM:
- Width: {web_width} mm
- Depth: {total_depth} mm
- Volume: {beam_volume:.3f} m³/m length

REINFORCEMENT DETAILS:

BEAM REINFORCEMENT:
- Bottom Bars: {num_bottom_bars} - ⌀{bottom_bar_dia}mm
- Top Bars: {num_top_bars} - ⌀{top_bar_dia}mm
- Total Steel Area: {total_beam_steel:.0f} mm²
- Steel Percentage: {(total_beam_steel/(web_width*total_depth))*100:.2f}%
- Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm c/c

SUNSHADE REINFORCEMENT:
- Main Bars: ⌀{main_bar_dia}mm (Longitudinal)
- Distribution Bars: ⌀{dist_bar_dia}mm @ {dist_bar_spacing}mm c/c

MATERIAL QUANTITIES (PER METER WIDTH):
- Concrete Volume: {beam_volume + sunshade_volume:.3f} m³
- Beam Steel: {total_beam_steel * 1000 / 1e6:.3f} kg/m (approx.)
- Sunshade Steel: To be calculated based on detailed analysis

DESIGN LOADS (PRELIMINARY):
- Self Weight: {(beam_volume + sunshade_volume) * 25:.1f} kN/m
- Live Load: {1.5 * projection/1000:.1f} kN/m (@ 1.5 kN/m²)
- Design Moment: {((beam_volume + sunshade_volume) * 25 + 1.5 * projection/1000) * (projection/1000)**2 / 2:.2f} kNm/m

DESIGN STANDARDS:
- IS 456:2000 - Code of Practice for Plain and Reinforced Concrete
- IS 1893:2016 - Earthquake Resistant Design of Structures
- IS 875:1987 - Code of Practice for Design Loads

NOTES:
1. Design is preliminary and based on standard assumptions
2. Wind loads and seismic effects should be considered separately
3. Detailed analysis required for critical applications
4. Thermal expansion joints may be required for long spans
5. Waterproofing and drainage details to be provided
6. Construction joints and lift positions to be planned

DISCLAIMER:
This is a computer-generated design based on input parameters.
Professional engineering review and approval required before construction.

Generated by: RajLisp Structural Design Suite
Design Code: SS-{sunshade_num}
Scale: As specified in drawing
"""
    
    return report
