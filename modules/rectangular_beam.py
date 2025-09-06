import streamlit as st
import numpy as np
import ezdxf
import tempfile
import math
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_beam_capacity

def page_rectangular_beam():
    st.title("📏 Rectangular Beam Designer")
    st.markdown("Design reinforced concrete rectangular beams with detailed reinforcement layout")

    # Create form for inputs
    with st.form("rectangular_beam_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🔧 Beam Dimensions")
            beam_width = st.number_input("Beam Width (mm)", min_value=150, max_value=800, value=300, step=25,
                                       help="Width of the beam cross-section")
            beam_depth = st.number_input("Total Depth (mm)", min_value=200, max_value=1200, value=450, step=25,
                                       help="Total depth of the beam")
            beam_length = st.number_input("Beam Length (m)", min_value=2.0, max_value=15.0, value=6.0, step=0.5,
                                        help="Span length of the beam")
            
            clear_cover = st.number_input("Clear Cover (mm)", min_value=20, max_value=75, value=25, step=5,
                                        help="Concrete cover to reinforcement")

        with col2:
            st.subheader("🔩 Reinforcement Details")
            
            st.markdown("**Bottom (Tension) Reinforcement**")
            bottom_bar_dia = st.selectbox("Bottom Bar Diameter (mm)", [12, 16, 20, 25, 32], index=2,
                                        help="Diameter of bottom reinforcement bars")
            num_bottom_bars = st.number_input("Number of Bottom Bars", min_value=2, max_value=8, value=3, step=1,
                                            help="Number of bottom reinforcement bars")
            
            st.markdown("**Top (Compression) Reinforcement**")
            top_bar_dia = st.selectbox("Top Bar Diameter (mm)", [12, 16, 20, 25], index=1,
                                     help="Diameter of top reinforcement bars")
            num_top_bars = st.number_input("Number of Top Bars", min_value=2, max_value=6, value=2, step=1,
                                         help="Number of top reinforcement bars")
            
            st.markdown("**Shear Reinforcement**")
            stirrup_dia = st.selectbox("Stirrup Diameter (mm)", [6, 8, 10, 12], index=1,
                                     help="Diameter of shear stirrups")
            stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=75, max_value=300, value=150, step=25,
                                            help="Center to center spacing of stirrups")

        with col3:
            st.subheader("🏗️ Material & Loads")
            concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30", "M35", "M40", "M45"], index=2)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500", "Fe550"], index=1)
            
            st.markdown("**Loading**")
            dead_load = st.number_input("Dead Load (kN/m)", min_value=0.0, value=15.0, step=1.0,
                                      help="Distributed dead load including self weight")
            live_load = st.number_input("Live Load (kN/m)", min_value=0.0, value=10.0, step=1.0,
                                      help="Distributed live load")
            
            st.markdown("**Drawing Options**")
            drawing_scale = st.selectbox("Drawing Scale", ["1:10", "1:20", "1:25", "1:50"], index=2)
            beam_number = st.text_input("Beam Number", value="B1", help="Beam identification number")

        submitted = st.form_submit_button("🔄 Design Rectangular Beam", type="primary")

        if submitted:
            # Extract material properties
            fck = int(concrete_grade[1:])  # Extract concrete strength
            fy_dict = {"Fe415": 415, "Fe500": 500, "Fe550": 550}
            fy = fy_dict[steel_grade]
            
            # Calculate beam properties
            results = calculate_rectangular_beam(
                beam_width, beam_depth, beam_length, clear_cover,
                bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                stirrup_dia, stirrup_spacing, fck, fy, dead_load, live_load
            )
            
            # Display results
            display_beam_results(results, beam_width, beam_depth, beam_length)
            
            # Generate DXF drawing
            dxf_content = generate_rectangular_beam_dxf(
                beam_width, beam_depth, bottom_bar_dia, num_bottom_bars,
                top_bar_dia, num_top_bars, stirrup_dia, stirrup_spacing,
                beam_number, drawing_scale, results
            )
            
            # Download button
            scale_num = int(drawing_scale.split(':')[1])
            filename = f"rectangular_beam_{beam_number}_1_{scale_num}.dxf"
            
            st.download_button(
                label="📥 Download DXF Drawing",
                data=dxf_content,
                file_name=filename,
                mime="application/dxf",
                use_container_width=True
            )

def calculate_rectangular_beam(b, d, length, cover, dia_bottom, n_bottom, dia_top, n_top, 
                              stirrup_dia, stirrup_spacing, fck, fy, dl, ll):
    """
    Calculate rectangular beam design parameters
    Based on IS 456:2000 code provisions
    """
    results = {}
    
    # Effective depth
    d_eff = d - cover - stirrup_dia - dia_bottom/2
    results['d_effective'] = d_eff
    
    # Areas of reinforcement
    ast_bottom = n_bottom * math.pi * (dia_bottom/2)**2
    ast_top = n_top * math.pi * (dia_top/2)**2
    
    results['ast_bottom'] = ast_bottom
    results['ast_top'] = ast_top
    results['ast_total'] = ast_bottom + ast_top
    
    # Steel percentages
    pt_bottom = (100 * ast_bottom) / (b * d_eff)
    pt_top = (100 * ast_top) / (b * d_eff)
    pt_total = (100 * results['ast_total']) / (b * d_eff)
    
    results['pt_bottom'] = pt_bottom
    results['pt_top'] = pt_top  
    results['pt_total'] = pt_total
    
    # Check minimum and maximum steel
    pt_min = max(0.85/fy, 0.15) * 100  # IS 456 Cl. 26.5.1.1
    pt_max = 4.0  # IS 456 Cl. 26.5.1.1
    
    results['pt_min'] = pt_min
    results['pt_max'] = pt_max
    results['steel_check'] = "OK" if pt_min <= pt_total <= pt_max else "FAIL"
    
    # Load calculations
    total_udl = dl + ll
    factored_udl = 1.5 * total_udl  # Load factor as per IS 456
    
    # Maximum moment
    max_moment = factored_udl * length**2 / 8  # For simply supported beam
    max_shear = factored_udl * length / 2
    
    results['total_udl'] = total_udl
    results['factored_udl'] = factored_udl
    results['max_moment'] = max_moment
    results['max_shear'] = max_shear
    
    # Moment of resistance calculation
    xu_max = 0.48 * d_eff  # For Fe500, from IS 456
    if fy == 415:
        xu_max = 0.53 * d_eff
    elif fy == 550:
        xu_max = 0.46 * d_eff
        
    # Balanced section check
    Mr_lim = 0.36 * fck * b * xu_max * (d_eff - 0.42 * xu_max) / 1000000  # kNm
    results['Mr_lim'] = Mr_lim
    results['section_type'] = "Under-reinforced" if max_moment <= Mr_lim else "Over-reinforced"
    
    # Actual moment of resistance (simplified)
    # For under-reinforced section
    if max_moment <= Mr_lim:
        # Using ast_bottom only for moment resistance
        stress_factor = 0.87 * fy
        lever_arm = 0.9 * d_eff  # Approximation
        Mr_actual = (ast_bottom * stress_factor * lever_arm) / 1000000  # kNm
    else:
        Mr_actual = Mr_lim
    
    results['Mr_actual'] = Mr_actual
    results['moment_check'] = "OK" if Mr_actual >= max_moment else "FAIL"
    
    # Shear check
    # Design shear strength as per IS 456 Table 19
    tau_c = get_design_shear_strength(pt_bottom, fck)
    Vc = tau_c * b * d_eff / 1000  # kN
    
    results['tau_c'] = tau_c
    results['Vc'] = Vc
    results['shear_check'] = "OK" if Vc >= max_shear else "NEEDS SHEAR REINFORCEMENT"
    
    # Shear reinforcement calculation
    if max_shear > Vc:
        Vs_req = max_shear - Vc
        asv = 2 * math.pi * (stirrup_dia/2)**2  # Two-legged stirrup
        sv_req = (0.87 * fy * asv * d_eff) / (Vs_req * 1000)  # Required spacing
        
        results['Vs_required'] = Vs_req
        results['sv_required'] = sv_req
        results['stirrup_adequate'] = "OK" if stirrup_spacing <= sv_req else "REDUCE SPACING"
    else:
        results['Vs_required'] = 0
        results['sv_required'] = "Minimum"
        results['stirrup_adequate'] = "OK"
    
    # Deflection check (simplified)
    span_depth_basic = 20  # For simply supported beam
    modification_factor = get_deflection_modification_factor(pt_bottom, fy)
    span_depth_allowed = span_depth_basic * modification_factor
    span_depth_actual = (length * 1000) / d_eff
    
    results['span_depth_allowed'] = span_depth_allowed
    results['span_depth_actual'] = span_depth_actual
    results['deflection_check'] = "OK" if span_depth_actual <= span_depth_allowed else "INCREASE DEPTH"
    
    return results

def get_design_shear_strength(pt, fck):
    """Get design shear strength from IS 456 Table 19"""
    # Simplified lookup - in practice, use proper interpolation
    tau_c_values = {
        20: {0.15: 0.28, 0.25: 0.36, 0.50: 0.48, 0.75: 0.56, 1.00: 0.62},
        25: {0.15: 0.29, 0.25: 0.37, 0.50: 0.49, 0.75: 0.57, 1.00: 0.64},
        30: {0.15: 0.31, 0.25: 0.39, 0.50: 0.51, 0.75: 0.59, 1.00: 0.66}
    }
    
    # Get closest fck value
    if fck <= 20:
        fck_key = 20
    elif fck <= 25:
        fck_key = 25
    else:
        fck_key = 30
    
    # Get closest pt value  
    pt_values = list(tau_c_values[fck_key].keys())
    pt_key = min(pt_values, key=lambda x: abs(x - pt))
    
    return tau_c_values[fck_key][pt_key]

def get_deflection_modification_factor(pt, fy):
    """Get modification factor for deflection as per IS 456 Fig. 4"""
    # Simplified calculation
    fs = 0.58 * fy * (pt / 1.0)  # Approximate stress in steel
    
    if fs <= 200:
        return 2.0
    elif fs <= 240:
        return 1.6
    elif fs <= 280:
        return 1.33
    else:
        return 1.0

def display_beam_results(results, b, d, length):
    """Display beam design results in organized sections"""
    
    st.success("✅ Beam Design Completed")
    
    # Create tabs for different result categories
    tab1, tab2, tab3, tab4 = st.tabs(["📐 Geometry", "🔩 Steel Design", "💪 Strength Check", "📊 Summary"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Beam Width", f"{b} mm")
            st.metric("Total Depth", f"{d} mm")
            st.metric("Effective Depth", f"{results['d_effective']:.1f} mm")
        with col2:
            st.metric("Beam Length", f"{length:.1f} m")
            st.metric("Cross-sectional Area", f"{b * d / 1000:.1f} cm²")
            st.metric("L/D Ratio", f"{(length * 1000 / results['d_effective']):.1f}")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Bottom Steel**")
            st.metric("Area of Steel", f"{results['ast_bottom']:.0f} mm²")
            st.metric("Steel Percentage", f"{results['pt_bottom']:.2f}%")
            
        with col2:
            st.markdown("**Top Steel**")
            st.metric("Area of Steel", f"{results['ast_top']:.0f} mm²")  
            st.metric("Steel Percentage", f"{results['pt_top']:.2f}%")
        
        # Steel adequacy check
        if results['steel_check'] == "OK":
            st.success(f"✅ Steel percentage OK ({results['pt_min']:.2f}% ≤ {results['pt_total']:.2f}% ≤ {results['pt_max']:.1f}%)")
        else:
            st.error(f"❌ Steel percentage not within limits ({results['pt_min']:.2f}% to {results['pt_max']:.1f}%)")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Moment Capacity**")
            st.metric("Applied Moment", f"{results['max_moment']:.1f} kNm")
            st.metric("Moment of Resistance", f"{results['Mr_actual']:.1f} kNm")
            if results['moment_check'] == "OK":
                st.success("✅ Moment capacity adequate")
            else:
                st.error("❌ Moment capacity insufficient")
                
        with col2:
            st.markdown("**Shear Capacity**")
            st.metric("Applied Shear", f"{results['max_shear']:.1f} kN")
            st.metric("Shear Resistance", f"{results['Vc']:.1f} kN")
            if results['shear_check'] == "OK":
                st.success("✅ Shear capacity adequate")
            else:
                st.warning("⚠️ Needs shear reinforcement")
        
        # Deflection check
        st.markdown("**Deflection Check**")
        if results['deflection_check'] == "OK":
            st.success(f"✅ Deflection OK (L/d = {results['span_depth_actual']:.1f} ≤ {results['span_depth_allowed']:.1f})")
        else:
            st.error(f"❌ Deflection excessive (L/d = {results['span_depth_actual']:.1f} > {results['span_depth_allowed']:.1f})")
    
    with tab4:
        st.markdown("**Design Summary**")
        
        summary_data = {
            "Parameter": ["Section Type", "Total Steel %", "Moment Check", "Shear Check", "Deflection Check"],
            "Value": [results['section_type'], f"{results['pt_total']:.2f}%", 
                     results['moment_check'], results['shear_check'], results['deflection_check']],
            "Status": ["ℹ️", "ℹ️", 
                      "✅" if results['moment_check'] == "OK" else "❌",
                      "✅" if results['shear_check'] == "OK" else "⚠️",
                      "✅" if results['deflection_check'] == "OK" else "❌"]
        }
        
        st.table(summary_data)
        
        # Recommendations
        st.markdown("**Recommendations:**")
        if results['steel_check'] != "OK":
            st.warning("• Adjust reinforcement to meet minimum/maximum steel requirements")
        if results['moment_check'] != "OK":
            st.warning("• Increase tension reinforcement or beam depth")
        if results['shear_check'] != "OK":
            st.warning("• Reduce stirrup spacing or increase stirrup diameter")
        if results['deflection_check'] != "OK":
            st.warning("• Increase beam depth or reduce span")

def generate_rectangular_beam_dxf(b, d, dia_bottom, n_bottom, dia_top, n_top, 
                                 stirrup_dia, stirrup_spacing, beam_num, scale, results):
    """
    Generate DXF drawing for rectangular beam based on BEAMRECT.LSP logic
    """
    # Create DXF document
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Extract scale factor
    scale_factor = int(scale.split(':')[1])
    
    # Drawing parameters
    dim_text_height = 3 * scale_factor
    
    # Beam corner points (bottom-left origin)
    pt1 = (0, 0)  # Bottom left
    pt2 = (b, 0)  # Bottom right  
    pt3 = (b, d)  # Top right
    pt4 = (0, d)  # Top left
    
    # Draw beam outline
    msp.add_lwpolyline([pt1, pt2, pt3, pt4, pt1])
    
    # Calculate reinforcement positions
    cover = 25  # Standard cover
    d_eff = results['d_effective']
    
    # Bottom reinforcement positions
    dda_sb = cover + stirrup_dia + dia_bottom/2
    pt_bottom_start = (dda_sb, dda_sb)
    
    if n_bottom > 1:
        spacing_bottom = (b - 2 * dda_sb) / (n_bottom - 1)
    else:
        spacing_bottom = 0
    
    # Top reinforcement positions  
    dda_st = cover + stirrup_dia + dia_top/2
    pt_top_start = (dda_st, d - dda_st)
    
    if n_top > 1:
        spacing_top = (b - 2 * dda_st) / (n_top - 1)
    else:
        spacing_top = 0
    
    # Draw bottom bars
    for i in range(n_bottom):
        x_pos = pt_bottom_start[0] + i * spacing_bottom
        center = (x_pos, pt_bottom_start[1])
        msp.add_circle(center, dia_bottom/2, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Draw top bars
    for i in range(n_top):
        x_pos = pt_top_start[0] + i * spacing_top
        center = (x_pos, pt_top_start[1])
        msp.add_circle(center, dia_top/2, dxfattribs={'layer': 'REINFORCEMENT'})
    
    # Draw stirrup outline (simplified)
    stirrup_clear = cover
    stirrup_pts = [
        (stirrup_clear, stirrup_clear),
        (b - stirrup_clear, stirrup_clear),
        (b - stirrup_clear, d - stirrup_clear),
        (stirrup_clear, d - stirrup_clear),
        (stirrup_clear, stirrup_clear)
    ]
    msp.add_lwpolyline(stirrup_pts, dxfattribs={'layer': 'STIRRUPS'})
    
    # Add dimensions
    # Width dimension
    dim_y_width = -1.2 * dim_text_height
    msp.add_linear_dim(
        base=(b/2, dim_y_width),
        p1=pt1,
        p2=(b, 0),
        dimstyle="EZDXF"
    ).render()
    
    # Height dimension
    dim_x_height = -1.2 * dim_text_height  
    msp.add_linear_dim(
        base=(dim_x_height, d/2),
        p1=pt1,
        p2=(0, d),
        angle=90,
        dimstyle="EZDXF"
    ).render()
    
    # Add reinforcement details
    text_y_pos = d + 0.5 * dim_text_height
    text_height = 0.1 * d
    
    # Bottom steel note
    bottom_note = f"{n_bottom}NOS.{dia_bottom}MM DIA.TOR BARS"
    msp.add_text(bottom_note, 
                dxfattribs={'height': text_height, 'insert': (b + 25, text_y_pos)})
    
    # Top steel note
    top_note = f"{n_top}NOS.{dia_top}MM DIA.TOR BARS" 
    text_y_pos += 1.5 * text_height
    msp.add_text(top_note,
                dxfattribs={'height': text_height, 'insert': (b + 25, text_y_pos)})
    
    # Stirrup note
    stirrup_note = f"{stirrup_dia}MM DIA.TWO LEGGED STIRRUPS @{stirrup_spacing}MM C/C."
    text_y_pos += 1.5 * text_height
    msp.add_text(stirrup_note,
                dxfattribs={'height': text_height, 'insert': (b + 25, text_y_pos)})
    
    # Beam identification
    beam_title = f"BEAM NO.B-{beam_num}"
    title_y_pos = -4 * dim_text_height
    title_height = 0.125 * d
    msp.add_text(beam_title,
                dxfattribs={'height': title_height, 'insert': (0, title_y_pos)})
    
    # Add leader lines for reinforcement
    # Bottom bar leader
    leader_start = (pt_bottom_start[0] + dia_bottom/4, pt_bottom_start[1])
    leader_end = (b + 20, text_y_pos - 4 * text_height)
    msp.add_line(leader_start, leader_end, dxfattribs={'layer': 'LEADERS'})
    
    # Top bar leader
    leader_start = (pt_top_start[0] + dia_top/4, pt_top_start[1])
    leader_end = (b + 20, text_y_pos - 2.5 * text_height)
    msp.add_line(leader_start, leader_end, dxfattribs={'layer': 'LEADERS'})
    
    # Set zoom to fit drawing
    # This would be handled by the CAD software when opening
    
    # Save DXF to bytes
    with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tmp_file:
        doc.saveas(tmp_file.name)
        with open(tmp_file.name, 'rb') as f:
            dxf_content = f.read()
        import os
        os.unlink(tmp_file.name)
    
    return dxf_content

if __name__ == "__main__":
    page_rectangular_beam()
