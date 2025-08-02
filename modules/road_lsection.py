import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_road_lsection():
    st.title("🛣️ Road Longitudinal Section Designer")
    st.markdown("Design road longitudinal sections with gradients, curves, and drainage details")

    with st.form("road_lsection_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Road Geometry")
            road_length = st.number_input("Road Length (m)", min_value=100, max_value=10000, value=1000, step=100,
                                        help="Total length of road section")
            road_width = st.number_input("Road Width (m)", min_value=3.5, max_value=15, value=7.0, step=0.5,
                                       help="Total carriageway width")
            
            st.markdown("**Gradients**")
            start_level = st.number_input("Start Level (m)", min_value=0, max_value=500, value=100, step=1,
                                        help="Starting elevation/level")
            end_level = st.number_input("End Level (m)", min_value=0, max_value=500, value=105, step=1,
                                      help="Ending elevation/level")
            
            # Calculate gradient
            gradient = ((end_level - start_level) / road_length) * 100
            st.info(f"Calculated Gradient: {gradient:.2f}%")

        with col2:
            st.subheader("🛤️ Pavement Layers")
            surface_thickness = st.number_input("Surface Course (mm)", min_value=20, max_value=100, value=40, step=10,
                                              help="Bituminous surface course thickness")
            base_thickness = st.number_input("Base Course (mm)", min_value=100, max_value=300, value=150, step=25,
                                           help="Granular base course thickness")
            subbase_thickness = st.number_input("Sub-base (mm)", min_value=150, max_value=400, value=200, step=25,
                                              help="Granular sub-base thickness")
            
            st.markdown("**Shoulder Details**")
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=1.0, max_value=3.0, value=1.5, step=0.5,
                                           help="Width of road shoulder")
            shoulder_type = st.selectbox("Shoulder Type", ["Paved", "Granular", "Earth"], index=1,
                                       help="Type of shoulder construction")

        with col3:
            st.subheader("💧 Drainage & Utilities")
            camber = st.number_input("Camber (%)", min_value=1.5, max_value=4.0, value=2.5, step=0.5,
                                   help="Cross-fall for drainage")
            
            side_drain_depth = st.number_input("Side Drain Depth (mm)", min_value=300, max_value=1000, value=600, step=100,
                                             help="Depth of roadside drainage")
            side_drain_width = st.number_input("Side Drain Width (mm)", min_value=300, max_value=800, value=500, step=100,
                                             help="Top width of side drain")
            
            st.markdown("**Design Standards**")
            design_speed = st.selectbox("Design Speed (kmph)", [30, 50, 60, 80, 100, 120], index=2,
                                      help="Design speed for geometric design")
            terrain_type = st.selectbox("Terrain", ["Plain", "Rolling", "Hilly", "Steep"], index=0,
                                      help="Terrain classification")

        submitted = st.form_submit_button("🔄 Generate L-Section", type="primary")

    if submitted:
        with st.spinner("🔄 Generating road longitudinal section..."):
            try:
                # Create DXF drawing
                doc = create_road_lsection_dxf(
                    road_length, road_width, start_level, end_level,
                    surface_thickness, base_thickness, subbase_thickness,
                    shoulder_width, side_drain_depth, side_drain_width, camber
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Road longitudinal section generated successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Road Geometry**")
                            st.write(f"• Length: {road_length} m")
                            st.write(f"• Width: {road_width} m")
                            st.write(f"• Start Level: {start_level} m")
                            st.write(f"• End Level: {end_level} m")
                            st.write(f"• Gradient: {gradient:.2f}%")
                            
                            # Check gradient limits
                            if terrain_type == "Plain" and abs(gradient) <= 3:
                                st.success("✅ Gradient within limits for plain terrain")
                            elif terrain_type == "Rolling" and abs(gradient) <= 6:
                                st.success("✅ Gradient within limits for rolling terrain")
                            elif terrain_type == "Hilly" and abs(gradient) <= 8:
                                st.success("✅ Gradient within limits for hilly terrain")
                            else:
                                st.warning("⚠️ Check gradient limits for terrain type")
                            
                        with summary_col2:
                            st.markdown("**Pavement Structure**")
                            st.write(f"• Surface Course: {surface_thickness} mm")
                            st.write(f"• Base Course: {base_thickness} mm")
                            st.write(f"• Sub-base: {subbase_thickness} mm")
                            
                            total_pavement = surface_thickness + base_thickness + subbase_thickness
                            st.write(f"• **Total Thickness: {total_pavement} mm**")
                            
                            st.write(f"• Shoulder: {shoulder_width} m ({shoulder_type})")
                            st.write(f"• Camber: {camber}%")

                    # Drainage and geometric details
                    with st.expander("💧 Drainage & Geometric Details", expanded=True):
                        drain_col1, drain_col2 = st.columns(2)
                        
                        with drain_col1:
                            st.markdown("**Drainage Details**")
                            st.write(f"• Side Drain Depth: {side_drain_depth} mm")
                            st.write(f"• Side Drain Width: {side_drain_width} mm")
                            
                            # Calculate drain capacity (simplified)
                            drain_area = (side_drain_depth * side_drain_width) / 1e6  # m²
                            st.write(f"• Drain Cross-section: {drain_area:.3f} m²")
                            
                            # Camber check
                            min_camber = 1.5 if surface_thickness >= 40 else 2.0
                            if camber >= min_camber:
                                st.success(f"✅ Camber adequate (min: {min_camber}%)")
                            else:
                                st.warning(f"⚠️ Increase camber (min: {min_camber}%)")
                        
                        with drain_col2:
                            st.markdown("**Geometric Standards**")
                            st.write(f"• Design Speed: {design_speed} kmph")
                            st.write(f"• Terrain Type: {terrain_type}")
                            
                            # Minimum curve radius for design speed
                            min_radius = {30: 30, 50: 60, 60: 95, 80: 180, 100: 280, 120: 410}
                            st.write(f"• Min Curve Radius: {min_radius.get(design_speed, 100)} m")
                            
                            # Sight distance
                            sight_distance = {30: 30, 50: 60, 60: 85, 80: 120, 100: 160, 120: 200}
                            st.write(f"• Stopping Sight Distance: {sight_distance.get(design_speed, 85)} m")

                    # Design calculations
                    with st.expander("🧮 Design Calculations", expanded=True):
                        calc_col1, calc_col2 = st.columns(2)
                        
                        with calc_col1:
                            st.markdown("**Earthwork Quantities**")
                            
                            # Simplified earthwork calculation
                            avg_height = abs(end_level - start_level) / 2
                            formation_width = road_width + 2 * shoulder_width + 1.0  # Including side drains
                            
                            cut_fill_area = avg_height * formation_width
                            total_earthwork = cut_fill_area * road_length
                            
                            st.write(f"• Formation Width: {formation_width} m")
                            st.write(f"• Avg Cut/Fill Height: {avg_height:.2f} m")
                            st.write(f"• Estimated Earthwork: {total_earthwork:.0f} m³")
                        
                        with calc_col2:
                            st.markdown("**Material Quantities**")
                            
                            # Calculate material quantities
                            pavement_area = road_width * road_length
                            
                            surface_volume = (pavement_area * surface_thickness) / 1000  # m³
                            base_volume = (pavement_area * base_thickness) / 1000  # m³
                            subbase_volume = (pavement_area * subbase_thickness) / 1000  # m³
                            
                            st.write(f"• Surface Course: {surface_volume:.0f} m³")
                            st.write(f"• Base Course: {base_volume:.0f} m³")
                            st.write(f"• Sub-base: {subbase_volume:.0f} m³")
                            
                            total_material = surface_volume + base_volume + subbase_volume
                            st.write(f"• **Total Material: {total_material:.0f} m³**")

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
                        file_name=f"road_lsection_{road_length}m_{design_speed}kmph.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_road_lsection_report(
                        road_length, road_width, start_level, end_level, gradient,
                        surface_thickness, base_thickness, subbase_thickness,
                        design_speed, terrain_type, total_earthwork, total_material
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"road_lsection_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_road_lsection_dxf(road_length, road_width, start_level, end_level,
                           surface_thickness, base_thickness, subbase_thickness,
                           shoulder_width, side_drain_depth, side_drain_width, camber):
    """Create DXF drawing for road longitudinal section"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Convert to drawing units (mm)
    length_mm = road_length * 1000
    start_level_mm = start_level * 1000
    end_level_mm = end_level * 1000
    
    # Scale for drawing
    scale_factor = 0.1 if road_length > 2000 else 0.2
    
    # Ground profile
    ground_start = (0, start_level_mm * scale_factor)
    ground_end = (length_mm * scale_factor, end_level_mm * scale_factor)
    msp.add_line(ground_start, ground_end, dxfattribs={'color': 3})  # Green for ground
    
    # Formation level (road surface)
    formation_offset = (surface_thickness + base_thickness + subbase_thickness)
    formation_start = (0, (start_level_mm - formation_offset) * scale_factor)
    formation_end = (length_mm * scale_factor, (end_level_mm - formation_offset) * scale_factor)
    msp.add_line(formation_start, formation_end, dxfattribs={'color': 1})  # Red for formation
    
    # Pavement layers
    # Sub-base
    subbase_start = (0, (start_level_mm - subbase_thickness) * scale_factor)
    subbase_end = (length_mm * scale_factor, (end_level_mm - subbase_thickness) * scale_factor)
    msp.add_line(subbase_start, subbase_end, dxfattribs={'linetype': 'DASHED'})
    
    # Base course
    base_start = (0, (start_level_mm - surface_thickness - base_thickness) * scale_factor)
    base_end = (length_mm * scale_factor, (end_level_mm - surface_thickness - base_thickness) * scale_factor)
    msp.add_line(base_start, base_end, dxfattribs={'linetype': 'DASHED'})
    
    # Road surface
    surface_start = (0, start_level_mm * scale_factor)
    surface_end = (length_mm * scale_factor, end_level_mm * scale_factor)
    msp.add_line(surface_start, surface_end, dxfattribs={'color': 2, 'lineweight': 35})  # Yellow, thick line
    
    # Side drains
    drain_depth_mm = side_drain_depth
    drain_offset = (road_width/2 + shoulder_width) * 1000 * scale_factor
    
    # Left side drain
    left_drain_bottom = (0, (start_level_mm - drain_depth_mm) * scale_factor)
    left_drain_end = (length_mm * scale_factor, (end_level_mm - drain_depth_mm) * scale_factor)
    msp.add_line(left_drain_bottom, left_drain_end, dxfattribs={'color': 4, 'linetype': 'DASHED'})
    
    # Chainage marks every 100m
    num_chainages = int(road_length / 100) + 1
    for i in range(num_chainages):
        chainage_x = i * 100 * 1000 * scale_factor
        chainage_y_ground = start_level_mm + (end_level_mm - start_level_mm) * (i * 100 / road_length)
        chainage_y = chainage_y_ground * scale_factor
        
        # Chainage line
        msp.add_line(
            (chainage_x, chainage_y - 50 * scale_factor),
            (chainage_x, chainage_y + 50 * scale_factor),
            dxfattribs={'color': 7}
        )
        
        # Chainage text
        msp.add_text(
            f"{i * 100}m",
            dxfattribs={'height': 100 * scale_factor, 'style': 'STANDARD'}
        ).set_placement((chainage_x, chainage_y + 100 * scale_factor))
    
    # Level annotations
    msp.add_text(
        f"START LEVEL: {start_level}m",
        dxfattribs={'height': 150 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((0, start_level_mm * scale_factor + 200 * scale_factor))
    
    msp.add_text(
        f"END LEVEL: {end_level}m",
        dxfattribs={'height': 150 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((length_mm * scale_factor - 500 * scale_factor, end_level_mm * scale_factor + 200 * scale_factor))
    
    # Gradient text
    gradient = ((end_level - start_level) / road_length) * 100
    msp.add_text(
        f"GRADIENT: {gradient:.2f}%",
        dxfattribs={'height': 200 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((length_mm * scale_factor / 2, (start_level_mm + end_level_mm) / 2 * scale_factor + 300 * scale_factor))
    
    # Title and legend
    title_y = max(start_level_mm, end_level_mm) * scale_factor + 500 * scale_factor
    msp.add_text(
        f"ROAD LONGITUDINAL SECTION\nLENGTH: {road_length}m, WIDTH: {road_width}m",
        dxfattribs={'height': 300 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((0, title_y))
    
    # Legend
    legend_x = length_mm * scale_factor + 500 * scale_factor
    legend_y = start_level_mm * scale_factor
    
    legend_text = f"""PAVEMENT DETAILS:
SURFACE: {surface_thickness}mm
BASE: {base_thickness}mm
SUB-BASE: {subbase_thickness}mm
TOTAL: {surface_thickness + base_thickness + subbase_thickness}mm

SHOULDER: {shoulder_width}m
SIDE DRAIN: {side_drain_depth}mm DEEP"""
    
    msp.add_text(
        legend_text,
        dxfattribs={'height': 150 * scale_factor, 'style': 'STANDARD'}
    ).set_placement((legend_x, legend_y))
    
    return doc

def generate_road_lsection_report(road_length, road_width, start_level, end_level, gradient,
                                surface_thickness, base_thickness, subbase_thickness,
                                design_speed, terrain_type, total_earthwork, total_material):
    """Generate road longitudinal section report"""
    
    report = f"""
ROAD LONGITUDINAL SECTION DESIGN REPORT
=======================================

PROJECT DETAILS:
- Road Length: {road_length} m
- Road Width: {road_width} m
- Design Speed: {design_speed} kmph
- Terrain Type: {terrain_type}

VERTICAL ALIGNMENT:
- Start Level: {start_level} m
- End Level: {end_level} m
- Gradient: {gradient:.2f}%
- Level Difference: {abs(end_level - start_level):.2f} m

PAVEMENT STRUCTURE:
- Surface Course: {surface_thickness} mm (Bituminous)
- Base Course: {base_thickness} mm (Granular)
- Sub-base Course: {subbase_thickness} mm (Granular)
- Total Pavement Thickness: {surface_thickness + base_thickness + subbase_thickness} mm

GEOMETRIC STANDARDS:
- Design Speed: {design_speed} kmph
- Maximum Gradient: {'3% (Plain)' if terrain_type == 'Plain' else '6% (Rolling)' if terrain_type == 'Rolling' else '8% (Hilly)'}
- Gradient Provided: {gradient:.2f}%
- Gradient Status: {'Within Limits' if abs(gradient) <= (3 if terrain_type == 'Plain' else 6 if terrain_type == 'Rolling' else 8) else 'Exceeds Limits'}

ESTIMATED QUANTITIES:
- Earthwork: {total_earthwork:.0f} m³
- Pavement Materials: {total_material:.0f} m³
- Surface Course: {(road_width * road_length * surface_thickness)/1000:.0f} m³
- Base Course: {(road_width * road_length * base_thickness)/1000:.0f} m³
- Sub-base Course: {(road_width * road_length * subbase_thickness)/1000:.0f} m³

DESIGN STANDARDS REFERENCE:
- IRC:73-1980 (Geometric Design Standards)
- IRC:37-2018 (Guidelines for Design of Flexible Pavements)
- IRC:SP:84-2019 (Manual of Specifications & Standards)

DRAINAGE CONSIDERATIONS:
- Cross drainage structures at natural water crossings
- Side drains for surface water disposal
- Adequate camber for surface drainage
- Subsurface drainage if required

CONSTRUCTION NOTES:
1. Proper compaction of each layer as per specifications
2. Quality control of materials as per IRC standards
3. Adequate curing of bituminous layers
4. Provision of road marking and signage
5. Environmental clearances if required

RECOMMENDATIONS:
1. Detailed soil investigation for foundation design
2. Traffic survey for pavement design confirmation
3. Environmental impact assessment if required
4. Detailed drainage design for cross drainage
5. Safety audit after construction completion

Generated by RajLisp Structural Design Suite
Design Date: Current Date
Standards: IRC (Indian Roads Congress)
"""
    return report
