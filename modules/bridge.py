import streamlit as st
import pandas as pd
import ezdxf
import math
import numpy as np
import tempfile
import os
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi

def page_bridge():
    st.title("🌉 Bridge Designer")
    st.markdown("Comprehensive bridge design with multi-span analysis, pier design, and abutments")
    
    # Create tabs for different aspects of bridge design
    tab1, tab2, tab3, tab4 = st.tabs(["📐 Bridge Geometry", "🏗️ Structural Elements", "📊 Analysis", "📄 Drawing"])
    
    with tab1:
        bridge_geometry_section()
    
    with tab2:
        structural_elements_section()
        
    with tab3:
        analysis_section()
        
    with tab4:
        drawing_generation_section()

def bridge_geometry_section():
    st.subheader("🔧 Bridge Geometry Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Basic Parameters**")
        scale1 = st.number_input("Drawing Scale 1", min_value=1, max_value=1000, value=186, step=1)
        scale2 = st.number_input("Drawing Scale 2", min_value=1, max_value=1000, value=100, step=1)
        skew = st.number_input("Skew Angle (degrees)", min_value=0.0, max_value=45.0, value=0.0, step=0.5)
        
        st.markdown("**Bridge Layout**")
        nspan = st.number_input("Number of Spans", min_value=1, max_value=10, value=4, step=1)
        span1 = st.number_input("Span Length (m)", min_value=5.0, max_value=50.0, value=10.8, step=0.1)
        lbridge = st.number_input("Total Bridge Length (m)", min_value=10.0, max_value=500.0, value=43.2, step=0.1)
    
    with col2:
        st.markdown("**Vertical Alignment**")
        datum = st.number_input("Datum Level", min_value=0.0, max_value=200.0, value=100.0, step=0.1)
        toprl = st.number_input("Top RL of Bridge", min_value=datum, max_value=200.0, value=110.98, step=0.01)
        rtl = st.number_input("Road Top Level", min_value=datum, max_value=200.0, value=110.98, step=0.01)
        sofl = st.number_input("Soffit Level", min_value=datum, max_value=toprl, value=110.0, step=0.01)
        
        st.markdown("**Carriageway**")
        ccbr = st.number_input("Clear Carriageway Width (m)", min_value=3.0, max_value=20.0, value=11.1, step=0.1)
        kerbw = st.number_input("Kerb Width (m)", min_value=0.1, max_value=1.0, value=0.23, step=0.01)
        kerbd = st.number_input("Kerb Depth (m)", min_value=0.1, max_value=0.5, value=0.23, step=0.01)
    
    with col3:
        st.markdown("**Slab Details**")
        slbthc = st.number_input("Slab Thickness Centre (m)", min_value=0.3, max_value=2.0, value=0.9, step=0.05)
        slbthe = st.number_input("Slab Thickness Edge (m)", min_value=0.3, max_value=2.0, value=0.75, step=0.05)
        slbtht = st.number_input("Slab Thickness Tip (m)", min_value=0.3, max_value=2.0, value=0.75, step=0.05)
        wcth = st.number_input("Wearing Course Thickness (m)", min_value=0.05, max_value=0.2, value=0.08, step=0.01)
        
        st.markdown("**Approach Slabs**")
        laslab = st.number_input("Length of Approach Slab (m)", min_value=1.0, max_value=10.0, value=3.5, step=0.1)
        apwth = st.number_input("Width of Approach Slab (m)", min_value=5.0, max_value=20.0, value=12.0, step=0.1)
        apthk = st.number_input("Thickness of Approach Slab (m)", min_value=0.2, max_value=1.0, value=0.38, step=0.01)
    
    # Store parameters in session state for use in other tabs
    bridge_params = {
        'scale1': scale1, 'scale2': scale2, 'skew': skew, 'nspan': int(nspan),
        'span1': span1, 'lbridge': lbridge, 'datum': datum, 'toprl': toprl,
        'rtl': rtl, 'sofl': sofl, 'ccbr': ccbr, 'kerbw': kerbw, 'kerbd': kerbd,
        'slbthc': slbthc, 'slbthe': slbthe, 'slbtht': slbtht, 'wcth': wcth,
        'laslab': laslab, 'apwth': apwth, 'apthk': apthk
    }
    st.session_state.bridge_params = bridge_params

def structural_elements_section():
    st.subheader("🏗️ Structural Elements")
    
    if 'bridge_params' not in st.session_state:
        st.warning("Please configure bridge geometry first!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Pier Design**")
        capt = st.number_input("Pier Cap Top RL", min_value=100.0, max_value=120.0, value=110.0, step=0.1)
        capb = st.number_input("Pier Cap Bottom RL", min_value=100.0, max_value=120.0, value=109.4, step=0.1)
        capw = st.number_input("Cap Width (m)", min_value=0.8, max_value=3.0, value=1.2, step=0.1)
        piertw = st.number_input("Pier Top Width (m)", min_value=0.5, max_value=2.0, value=1.2, step=0.1)
        battr = st.number_input("Pier Batter", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
        pierst = st.number_input("Straight Length of Pier (m)", min_value=5.0, max_value=20.0, value=12.0, step=0.5)
        
        st.markdown("**Foundation**")
        futrl = st.number_input("Founding RL", min_value=90.0, max_value=110.0, value=100.0, step=0.1)
        futd = st.number_input("Depth of Footing (m)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
        futw = st.number_input("Width of Footing (m)", min_value=2.0, max_value=8.0, value=4.5, step=0.1)
        futl = st.number_input("Length of Footing (m)", min_value=5.0, max_value=20.0, value=12.0, step=0.5)
    
    with col2:
        st.markdown("**Abutment Design**")
        abtlen = st.number_input("Abutment Length (m)", min_value=8.0, max_value=20.0, value=12.0, step=0.5)
        dwth = st.number_input("Dirt Wall Thickness (m)", min_value=0.2, max_value=0.6, value=0.3, step=0.05)
        alcw = st.number_input("Abutment Cap Width (m)", min_value=0.5, max_value=2.0, value=0.75, step=0.05)
        alcd = st.number_input("Abutment Cap Depth (m)", min_value=0.8, max_value=2.0, value=1.2, step=0.1)
        
        # Abutment levels and batters
        alfl = st.number_input("Abutment Left Footing Level", min_value=95.0, max_value=105.0, value=100.0, step=0.1)
        alfb = st.number_input("Abutment Front Batter", min_value=5.0, max_value=15.0, value=10.0, step=0.5)
        altb = st.number_input("Abutment Toe Batter", min_value=3.0, max_value=10.0, value=10.0, step=0.5)
        albb = st.number_input("Abutment Back Batter", min_value=2.0, max_value=8.0, value=3.0, step=0.5)
        alfo = st.number_input("Front Offset to Footing (m)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
        alfd = st.number_input("Abutment Footing Depth (m)", min_value=0.8, max_value=2.0, value=1.0, step=0.1)
    
    # Store structural parameters
    structural_params = {
        'capt': capt, 'capb': capb, 'capw': capw, 'piertw': piertw,
        'battr': battr, 'pierst': pierst, 'futrl': futrl, 'futd': futd,
        'futw': futw, 'futl': futl, 'abtlen': abtlen, 'dwth': dwth,
        'alcw': alcw, 'alcd': alcd, 'alfl': alfl, 'alfb': alfb,
        'altb': altb, 'albb': albb, 'alfo': alfo, 'alfd': alfd
    }
    st.session_state.structural_params = structural_params

def analysis_section():
    st.subheader("📊 Bridge Analysis")
    
    if 'bridge_params' not in st.session_state or 'structural_params' not in st.session_state:
        st.warning("Please configure bridge geometry and structural elements first!")
        return
    
    params = {**st.session_state.bridge_params, **st.session_state.structural_params}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📏 Geometric Analysis**")
        
        # Calculate bridge geometry
        total_span_length = params['nspan'] * params['span1']
        sc = params['scale1'] / params['scale2']
        skew_rad = params['skew'] * pi / 180
        
        st.metric("Total Span Length", f"{total_span_length:.1f} m")
        st.metric("Scale Factor", f"{sc:.2f}")
        st.metric("Skew (radians)", f"{skew_rad:.3f}")
        
        # Pier calculations
        pier_count = max(0, params['nspan'] - 1)
        st.metric("Number of Piers", pier_count)
        
        if pier_count > 0:
            pier_height = params['capb'] - params['futrl'] - params['futd']
            pier_bottom_width = pier_height / params['battr'] + params['piertw']
            st.metric("Pier Height", f"{pier_height:.1f} m")
            st.metric("Pier Bottom Width", f"{pier_bottom_width:.2f} m")
    
    with col2:
        st.markdown("**🏗️ Structural Analysis**")
        
        # Deck slab analysis
        total_deck_area = params['lbridge'] * (params['ccbr'] + 2 * params['kerbw'])
        deck_volume = (total_deck_area * params['slbthc'])  # Simplified average thickness
        deck_weight = deck_volume * 25  # kN (assuming concrete density 25 kN/m³)
        
        st.metric("Deck Area", f"{total_deck_area:.1f} m²")
        st.metric("Deck Volume", f"{deck_volume:.1f} m³")
        st.metric("Deck Self Weight", f"{deck_weight:.0f} kN")
        
        # Live load calculations (simplified)
        live_load_area = total_deck_area
        live_load = live_load_area * 8  # kN (assuming 8 kN/m² live load)
        st.metric("Live Load", f"{live_load:.0f} kN")
        
        # Total load on substructure
        if pier_count > 0:
            load_per_pier = (deck_weight + live_load) / pier_count
            st.metric("Load per Pier", f"{load_per_pier:.0f} kN")

def drawing_generation_section():
    st.subheader("📄 Drawing Generation")
    
    if 'bridge_params' not in st.session_state or 'structural_params' not in st.session_state:
        st.warning("Please configure bridge geometry and structural elements first!")
        return
    
    params = {**st.session_state.bridge_params, **st.session_state.structural_params}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Drawing Options**")
        
        drawing_types = st.multiselect(
            "Select drawings to generate:",
            ["General Arrangement - Elevation", "General Arrangement - Plan", "Pier Details", "Abutment Details", 
             "Foundation Plan", "Cross Section", "Longitudinal Section"],
            default=["General Arrangement - Elevation", "General Arrangement - Plan"]
        )
        
        include_dimensions = st.checkbox("Include dimensions", value=True)
        include_annotations = st.checkbox("Include annotations", value=True)
        include_title_block = st.checkbox("Include title block", value=True)
        
        drawing_scale = st.selectbox("Drawing Scale", ["1:100", "1:200", "1:500"], index=1)
        paper_size = st.selectbox("Paper Size", ["A1", "A2", "A3", "A4"], index=0)
    
    with col2:
        st.markdown("**Preview**")
        st.info(f"Bridge Length: {params['lbridge']:.1f} m")
        st.info(f"Number of Spans: {params['nspan']}")
        st.info(f"Span Length: {params['span1']:.1f} m")
        
        if params['skew'] > 0:
            st.warning(f"Skew Bridge: {params['skew']:.1f}°")
    
    # Generate DXF button
    if st.button("🎨 Generate Bridge Drawings", type="primary", use_container_width=True):
        with st.spinner("Generating bridge drawings..."):
            try:
                dxf_content = generate_bridge_dxf(params, drawing_types, include_dimensions, include_annotations)
                
                # Create download
                st.download_button(
                    label="📥 Download DXF File",
                    data=dxf_content,
                    file_name=f"bridge_design_{params['nspan']}span_{params['span1']:.1f}m.dxf",
                    mime="application/dxf",
                    use_container_width=True
                )
                
                st.success("✅ Bridge drawings generated successfully!")
                
                # Show drawing summary
                with st.expander("📋 Drawing Summary"):
                    st.write("**Generated Drawings:**")
                    for drawing in drawing_types:
                        st.write(f"• {drawing}")
                    
                    st.write("**Bridge Parameters:**")
                    st.write(f"• Total Length: {params['lbridge']:.1f} m")
                    st.write(f"• Number of Spans: {params['nspan']}")
                    st.write(f"• Carriageway Width: {params['ccbr']:.1f} m")
                    if params['skew'] > 0:
                        st.write(f"• Skew Angle: {params['skew']:.1f}°")
                
            except Exception as e:
                st.error(f"❌ Error generating drawings: {str(e)}")
                st.error("Please check your input parameters and try again.")

def generate_bridge_dxf(params, drawing_types, include_dimensions, include_annotations):
    """Generate comprehensive bridge DXF drawing based on the original bridge_gad_app logic"""
    
    # Create DXF document
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Setup drawing parameters
    scale1 = params['scale1']
    scale2 = params['scale2']
    sc = scale1 / scale2
    skew_rad = params['skew'] * pi / 180
    
    # Helper functions (from original bridge_gad_app.py)
    def vpos(a):
        return params['datum'] + 1000.0 * (a - params['datum'])
    
    def hpos(a):
        return 0 + 1000.0 * (a - 0)
    
    def h2pos(a):
        return 0 + sc * 1000.0 * (a - 0)
    
    def v2pos(a):
        return params['datum'] + sc * 1000.0 * (a - params['datum'])
    
    # Generate different drawing types
    if "General Arrangement - Elevation" in drawing_types:
        draw_bridge_elevation(msp, params, hpos, vpos, include_dimensions)
    
    if "General Arrangement - Plan" in drawing_types:
        draw_bridge_plan(msp, params, hpos, vpos, include_dimensions)
    
    if "Pier Details" in drawing_types:
        draw_pier_details(msp, params, h2pos, v2pos, include_dimensions)
    
    if "Foundation Plan" in drawing_types:
        draw_foundation_plan(msp, params, hpos, vpos, include_dimensions)
    
    # Add title block if requested
    if include_annotations:
        add_title_block(msp, params)
    
    # Save to memory buffer
    with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tmp_file:
        doc.saveas(tmp_file.name)
        with open(tmp_file.name, 'rb') as f:
            dxf_content = f.read()
        os.unlink(tmp_file.name)
    
    return dxf_content

def draw_bridge_elevation(msp, params, hpos, vpos, include_dimensions):
    """Draw bridge elevation view"""
    
    # Draw superstructure spans
    for i in range(params['nspan']):
        span_start = i * params['span1']
        span_end = (i + 1) * params['span1']
        
        # Deck slab outline
        x1 = hpos(span_start)
        x2 = hpos(span_end)
        y1 = vpos(params['rtl'])
        y2 = vpos(params['sofl'])
        
        # Draw span rectangle
        msp.add_lwpolyline([
            (x1 + 25, y1), (x2 - 25, y1),
            (x2 - 25, y2), (x1 + 25, y2), (x1 + 25, y1)
        ])
    
    # Draw piers (if any)
    if params['nspan'] > 1:
        draw_piers_elevation(msp, params, hpos, vpos)
    
    # Draw approach slabs
    draw_approach_slabs(msp, params, hpos, vpos)
    
    # Add dimensions if requested
    if include_dimensions:
        add_span_dimensions(msp, params, hpos, vpos)

def draw_piers_elevation(msp, params, hpos, vpos):
    """Draw piers in elevation"""
    
    for i in range(1, params['nspan']):
        pier_location = i * params['span1']
        
        # Pier cap
        cap_x1 = hpos(pier_location - params['capw']/2)
        cap_x2 = hpos(pier_location + params['capw']/2)
        cap_y1 = vpos(params['capt'])
        cap_y2 = vpos(params['capb'])
        
        msp.add_lwpolyline([
            (cap_x1, cap_y1), (cap_x2, cap_y1),
            (cap_x2, cap_y2), (cap_x1, cap_y2), (cap_x1, cap_y1)
        ])
        
        # Pier shaft (simplified)
        pier_height = params['capb'] - params['futrl'] - params['futd']
        pier_bottom_width = pier_height / params['battr'] + params['piertw']
        
        shaft_x1 = hpos(pier_location - params['piertw']/2)
        shaft_x2 = hpos(pier_location + params['piertw']/2)
        shaft_x3 = hpos(pier_location - pier_bottom_width/2)
        shaft_x4 = hpos(pier_location + pier_bottom_width/2)
        
        shaft_y1 = vpos(params['capb'])
        shaft_y2 = vpos(params['futrl'] + params['futd'])
        
        # Pier outline (trapezoidal)
        msp.add_lwpolyline([
            (shaft_x1, shaft_y1), (shaft_x2, shaft_y1),
            (shaft_x4, shaft_y2), (shaft_x3, shaft_y2), (shaft_x1, shaft_y1)
        ])

def draw_bridge_plan(msp, params, hpos, vpos):
    """Draw bridge plan view"""
    
    # Deck outline in plan
    bridge_width = params['ccbr'] + 2 * params['kerbw']
    
    x1 = hpos(-params['laslab'])
    x2 = hpos(params['lbridge'] + params['laslab'])
    y1 = vpos(params['datum'] - 30 - bridge_width/2)
    y2 = vpos(params['datum'] - 30 + bridge_width/2)
    
    # Main deck outline
    msp.add_lwpolyline([
        (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
    ])
    
    # Draw piers in plan
    if params['nspan'] > 1:
        draw_piers_plan(msp, params, hpos, vpos)

def draw_piers_plan(msp, params, hpos, vpos):
    """Draw piers in plan view"""
    
    for i in range(1, params['nspan']):
        pier_location = i * params['span1']
        
        # Footing outline
        x1 = hpos(pier_location - params['futw']/2)
        x2 = hpos(pier_location + params['futw']/2)
        y1 = vpos(params['datum'] - 30 - params['futl']/2)
        y2 = vpos(params['datum'] - 30 + params['futl']/2)
        
        msp.add_lwpolyline([
            (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
        ])
        
        # Pier shaft in plan
        px1 = hpos(pier_location - params['piertw']/2)
        px2 = hpos(pier_location + params['piertw']/2)
        py1 = vpos(params['datum'] - 30 - params['pierst']/2)
        py2 = vpos(params['datum'] - 30 + params['pierst']/2)
        
        msp.add_lwpolyline([
            (px1, py1), (px2, py1), (px2, py2), (px1, py2), (px1, py1)
        ])

def draw_pier_details(msp, params, h2pos, v2pos, include_dimensions):
    """Draw detailed pier cross-section"""
    
    # Offset for side view
    offset_x = 2 * params['span1'] * params['nspan'] * params['scale1']
    offset_y = 2 * params['span1'] * params['nspan'] * params['scale1']
    
    # Pier cross-section details
    pier_x = h2pos(params['span1']) + offset_x
    pier_y_top = v2pos(params['capt']) + offset_y
    pier_y_bottom = v2pos(params['futrl']) + offset_y
    
    # Cap details
    cap_width = params['capw'] * params['scale1'] * params['scale2'] / params['scale1']
    cap_x1 = pier_x - cap_width/2
    cap_x2 = pier_x + cap_width/2
    cap_y1 = v2pos(params['capt']) + offset_y
    cap_y2 = v2pos(params['capb']) + offset_y
    
    msp.add_lwpolyline([
        (cap_x1, cap_y1), (cap_x2, cap_y1),
        (cap_x2, cap_y2), (cap_x1, cap_y2), (cap_x1, cap_y1)
    ])

def draw_foundation_plan(msp, params, hpos, vpos):
    """Draw foundation plan details"""
    
    # Foundation layout
    for i in range(1, params['nspan']):
        pier_location = i * params['span1']
        
        # Detailed footing
        x1 = hpos(pier_location - params['futw']/2)
        x2 = hpos(pier_location + params['futw']/2)
        y1 = vpos(params['datum'] - 50 - params['futl']/2)
        y2 = vpos(params['datum'] - 50 + params['futl']/2)
        
        msp.add_lwpolyline([
            (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
        ])
        
        # Add reinforcement pattern (simplified)
        # Longitudinal bars
        for j in range(5):
            bar_y = y1 + j * (y2 - y1) / 4
            msp.add_line((x1, bar_y), (x2, bar_y))
        
        # Transverse bars
        for k in range(8):
            bar_x = x1 + k * (x2 - x1) / 7
            msp.add_line((bar_x, y1), (bar_x, y2))

def draw_approach_slabs(msp, params, hpos, vpos):
    """Draw approach slabs"""
    
    # Left approach slab
    x1_left = hpos(-params['laslab'])
    x2_left = hpos(0)
    y1_left = vpos(params['rtl'])
    y2_left = vpos(params['rtl'] - params['apthk'])
    
    msp.add_lwpolyline([
        (x1_left, y1_left), (x2_left, y1_left),
        (x2_left, y2_left), (x1_left, y2_left), (x1_left, y1_left)
    ])
    
    # Right approach slab
    x1_right = hpos(params['lbridge'])
    x2_right = hpos(params['lbridge'] + params['laslab'])
    
    msp.add_lwpolyline([
        (x1_right, y1_left), (x2_right, y1_left),
        (x2_right, y2_left), (x1_right, y2_left), (x1_right, y1_left)
    ])

def add_span_dimensions(msp, params, hpos, vpos):
    """Add span dimensions to the drawing"""
    
    # Span dimensions
    for i in range(params['nspan']):
        span_start = i * params['span1']
        span_end = (i + 1) * params['span1']
        
        dim_y = vpos(params['rtl'] + 2)
        
        # Add dimension line
        msp.add_line((hpos(span_start), dim_y), (hpos(span_end), dim_y))
        
        # Add dimension text
        dim_x = hpos((span_start + span_end) / 2)
        msp.add_text(f"{params['span1']:.1f}m", 
                    dxfattribs={'height': 200, 'insert': (dim_x, dim_y + 300)})

def add_title_block(msp, params):
    """Add title block with project information"""
    
    # Title block position (bottom right)
    title_x = 15000
    title_y = -8000
    
    # Title block outline
    msp.add_lwpolyline([
        (title_x, title_y), (title_x + 5000, title_y),
        (title_x + 5000, title_y + 2000), (title_x, title_y + 2000), (title_x, title_y)
    ])
    
    # Title text
    msp.add_text("BRIDGE GENERAL ARRANGEMENT", 
                dxfattribs={'height': 300, 'insert': (title_x + 100, title_y + 1600)})
    
    # Bridge details
    msp.add_text(f"Length: {params['lbridge']:.1f}m, Spans: {params['nspan']}", 
                dxfattribs={'height': 200, 'insert': (title_x + 100, title_y + 1200)})
    
    msp.add_text(f"Carriageway: {params['ccbr']:.1f}m", 
                dxfattribs={'height': 200, 'insert': (title_x + 100, title_y + 900)})
    
    if params['skew'] > 0:
        msp.add_text(f"Skew: {params['skew']:.1f}°", 
                    dxfattribs={'height': 200, 'insert': (title_x + 100, title_y + 600)})
    
    # Date and scale
    msp.add_text("Scale: 1:200", 
                dxfattribs={'height': 150, 'insert': (title_x + 100, title_y + 300)})

# Additional utility functions from the original bridge_gad_app.py can be added here
# This includes the comprehensive Excel reading, cross-section generation, etc.

if __name__ == "__main__":
    page_bridge()
