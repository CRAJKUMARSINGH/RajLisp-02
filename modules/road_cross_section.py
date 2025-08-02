import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_road_cross_section():
    st.title("✂️ Road Cross Section Designer")
    st.markdown("Design typical road cross-sections with pavement layers, drainage, and utilities")

    with st.form("road_cross_section_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Road Geometry")
            carriageway_width = st.number_input("Carriageway Width (m)", min_value=3.5, max_value=15, value=7.0, step=0.5,
                                              help="Width of main carriageway")
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=1.0, max_value=3.0, value=1.5, step=0.5,
                                           help="Width of road shoulder each side")
            median_width = st.number_input("Median Width (m)", min_value=0, max_value=5, value=0, step=0.5,
                                         help="Central median width (0 for no median)")
            
            st.markdown("**Cross-fall & Camber**")
            camber = st.number_input("Camber (%)", min_value=1.5, max_value=4.0, value=2.5, step=0.5,
                                   help="Cross-fall for drainage")
            shoulder_slope = st.number_input("Shoulder Slope (%)", min_value=2.0, max_value=5.0, value=3.0, step=0.5,
                                           help="Slope of shoulder for drainage")

        with col2:
            st.subheader("🛤️ Pavement Structure")
            surface_course = st.number_input("Surface Course (mm)", min_value=20, max_value=100, value=40, step=10,
                                           help="Bituminous concrete surface")
            binder_course = st.number_input("Binder Course (mm)", min_value=0, max_value=80, value=30, step=10,
                                          help="Dense bituminous macadam")
            base_course = st.number_input("Base Course (mm)", min_value=100, max_value=300, value=150, step=25,
                                        help="Water bound macadam base")
            subbase_course = st.number_input("Sub-base Course (mm)", min_value=150, max_value=400, value=200, step=25,
                                           help="Granular sub-base")
            
            st.markdown("**Shoulder Construction**")
            shoulder_type = st.selectbox("Shoulder Type", ["Bituminous", "Concrete", "Granular", "Earth"], index=2,
                                       help="Type of shoulder surface")
            shoulder_thickness = st.number_input("Shoulder Thickness (mm)", min_value=75, max_value=200, value=100, step=25,
                                               help="Thickness of shoulder pavement")

        with col3:
            st.subheader("💧 Drainage & Utilities")
            side_drain = st.checkbox("Side Drains", value=True, help="Include roadside drainage")
            if side_drain:
                drain_depth = st.number_input("Drain Depth (mm)", min_value=300, max_value=1000, value=600, step=100)
                drain_width = st.number_input("Drain Top Width (mm)", min_value=300, max_value=800, value=500, step=100)
                drain_side_slope = st.number_input("Drain Side Slope (H:V)", min_value=1.0, max_value=3.0, value=1.5, step=0.5)
            
            st.markdown("**Embankment/Cut**")
            embankment_height = st.number_input("Embankment Height (m)", min_value=0, max_value=10, value=1.5, step=0.5,
                                              help="Height above natural ground (0 for at grade)")
            side_slope = st.number_input("Embankment Side Slope (H:V)", min_value=1.5, max_value=3.0, value=2.0, step=0.5,
                                       help="Side slope of embankment")
            
            st.markdown("**Utilities**")
            utility_corridor = st.checkbox("Utility Corridor", value=False, help="Include utility corridor")
            if utility_corridor:
                utility_width = st.number_input("Utility Width (m)", min_value=2, max_value=5, value=3, step=1)

        submitted = st.form_submit_button("🔄 Generate Cross Section", type="primary")

    if submitted:
        with st.spinner("🔄 Generating road cross section..."):
            try:
                # Calculate total widths
                total_carriageway = carriageway_width + median_width
                formation_width = total_carriageway + 2 * shoulder_width
                
                # Create DXF drawing
                doc = create_road_cross_section_dxf(
                    carriageway_width, shoulder_width, median_width, camber, shoulder_slope,
                    surface_course, binder_course, base_course, subbase_course,
                    shoulder_type, shoulder_thickness, side_drain, drain_depth if side_drain else 0,
                    drain_width if side_drain else 0, drain_side_slope if side_drain else 0,
                    embankment_height, side_slope, utility_corridor, utility_width if utility_corridor else 0
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Road cross section generated successfully!")
                    
                    # Design summary
                    with st.expander("📋 Cross Section Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Road Geometry**")
                            st.write(f"• Carriageway Width: {carriageway_width} m")
                            st.write(f"• Shoulder Width: {shoulder_width} m (each side)")
                            if median_width > 0:
                                st.write(f"• Median Width: {median_width} m")
                            st.write(f"• Formation Width: {formation_width} m")
                            st.write(f"• Camber: {camber}%")
                            st.write(f"• Shoulder Slope: {shoulder_slope}%")
                            
                        with summary_col2:
                            st.markdown("**Pavement Layers**")
                            st.write(f"• Surface Course: {surface_course} mm")
                            if binder_course > 0:
                                st.write(f"• Binder Course: {binder_course} mm")
                            st.write(f"• Base Course: {base_course} mm")
                            st.write(f"• Sub-base: {subbase_course} mm")
                            
                            total_pavement = surface_course + binder_course + base_course + subbase_course
                            st.write(f"• **Total Thickness: {total_pavement} mm**")
                            
                            st.write(f"• Shoulder: {shoulder_thickness} mm ({shoulder_type})")

                    # Drainage and earthwork
                    with st.expander("💧 Drainage & Earthwork", expanded=True):
                        drain_col1, drain_col2 = st.columns(2)
                        
                        with drain_col1:
                            st.markdown("**Drainage Details**")
                            if side_drain:
                                st.write(f"• Side Drain Depth: {drain_depth} mm")
                                st.write(f"• Drain Top Width: {drain_width} mm")
                                st.write(f"• Side Slope: {drain_side_slope}:1 (H:V)")
                                
                                # Calculate drain area
                                bottom_width = drain_width - 2 * drain_depth / drain_side_slope
                                if bottom_width > 0:
                                    drain_area = (drain_width + bottom_width) * drain_depth / 2 / 1e6  # m²
                                    st.write(f"• Drain Area: {drain_area:.3f} m²")
                                else:
                                    st.warning("⚠️ Drain geometry needs adjustment")
                            else:
                                st.write("• No side drains provided")
                            
                            # Camber adequacy
                            min_camber = 1.5 if surface_course >= 40 else 2.0
                            if camber >= min_camber:
                                st.success(f"✅ Camber adequate (min: {min_camber}%)")
                            else:
                                st.warning(f"⚠️ Increase camber (min: {min_camber}%)")
                        
                        with drain_col2:
                            st.markdown("**Earthwork Details**")
                            if embankment_height > 0:
                                st.write(f"• Embankment Height: {embankment_height} m")
                                st.write(f"• Side Slope: {side_slope}:1 (H:V)")
                                
                                # Calculate embankment top width
                                embankment_top = formation_width + 2 * 0.5  # 0.5m margin each side
                                embankment_bottom = embankment_top + 2 * side_slope * embankment_height
                                
                                st.write(f"• Embankment Top: {embankment_top:.1f} m")
                                st.write(f"• Embankment Bottom: {embankment_bottom:.1f} m")
                                
                                # Embankment area per meter length
                                embankment_area = (embankment_top + embankment_bottom) * embankment_height / 2
                                st.write(f"• Embankment Area: {embankment_area:.2f} m²/m")
                            else:
                                st.write("• Road at natural ground level")

                    # Material quantities
                    with st.expander("🧮 Material Quantities (per km)", expanded=True):
                        qty_col1, qty_col2 = st.columns(2)
                        
                        with qty_col1:
                            st.markdown("**Pavement Materials**")
                            
                            # Calculate volumes per km
                            pavement_area = carriageway_width  # m² per m length
                            
                            surface_volume = pavement_area * surface_course / 1000 * 1000  # m³ per km
                            binder_volume = pavement_area * binder_course / 1000 * 1000 if binder_course > 0 else 0
                            base_volume = pavement_area * base_course / 1000 * 1000
                            subbase_volume = pavement_area * subbase_course / 1000 * 1000
                            
                            st.write(f"• Surface Course: {surface_volume:.0f} m³")
                            if binder_volume > 0:
                                st.write(f"• Binder Course: {binder_volume:.0f} m³")
                            st.write(f"• Base Course: {base_volume:.0f} m³")
                            st.write(f"• Sub-base: {subbase_volume:.0f} m³")
                            
                            total_pavement_volume = surface_volume + binder_volume + base_volume + subbase_volume
                            st.write(f"• **Total Pavement: {total_pavement_volume:.0f} m³**")
                        
                        with qty_col2:
                            st.markdown("**Shoulder & Other Materials**")
                            
                            shoulder_area = 2 * shoulder_width  # Both sides
                            shoulder_volume = shoulder_area * shoulder_thickness / 1000 * 1000  # m³ per km
                            
                            st.write(f"• Shoulder Material: {shoulder_volume:.0f} m³")
                            
                            if embankment_height > 0:
                                embankment_volume = embankment_area * 1000  # m³ per km
                                st.write(f"• Embankment Fill: {embankment_volume:.0f} m³")
                            
                            # Drainage excavation
                            if side_drain:
                                drain_excavation = 2 * drain_area * 1000  # Both sides, per km
                                st.write(f"• Drain Excavation: {drain_excavation:.0f} m³")

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
                        file_name=f"road_cross_section_{carriageway_width}m_{total_pavement}mm.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_road_cross_section_report(
                        carriageway_width, shoulder_width, median_width, formation_width,
                        surface_course, base_course, subbase_course, total_pavement,
                        embankment_height, side_slope, total_pavement_volume
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"road_cross_section_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_road_cross_section_dxf(carriageway_width, shoulder_width, median_width, camber, shoulder_slope,
                                 surface_course, binder_course, base_course, subbase_course,
                                 shoulder_type, shoulder_thickness, side_drain, drain_depth,
                                 drain_width, drain_side_slope, embankment_height, side_slope,
                                 utility_corridor, utility_width):
    """Create DXF drawing for road cross section"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Scale factor for drawing
    scale = 100  # 1:100 scale
    
    # Convert dimensions to scaled mm
    def scale_dim(value_m):
        return value_m * 1000 / scale
    
    def scale_height(value_mm):
        return value_mm / scale
    
    # Calculate road geometry
    total_carriageway = carriageway_width + median_width
    formation_width = total_carriageway + 2 * shoulder_width
    
    # Road centerline
    center_x = 0
    center_y = 0
    
    # Ground level (datum)
    ground_level = center_y - scale_height(surface_course + binder_course + base_course + subbase_course) - scale_dim(embankment_height)
    
    # Draw road surface with camber
    carriageway_half = scale_dim(carriageway_width / 2)
    median_half = scale_dim(median_width / 2)
    shoulder_width_scaled = scale_dim(shoulder_width)
    
    # Surface profile points (including camber)
    camber_drop = scale_dim(carriageway_width / 2 * camber / 100)  # Maximum camber drop
    
    surface_points = []
    
    # Left side
    left_shoulder_end = center_x - carriageway_half - median_half - shoulder_width_scaled
    left_carriageway_start = center_x - carriageway_half - median_half
    
    # Right side  
    right_carriageway_end = center_x + carriageway_half + median_half
    right_shoulder_end = center_x + carriageway_half + median_half + shoulder_width_scaled
    
    # Create surface profile with camber
    if median_width > 0:
        # Divided carriageway
        surface_points = [
            (left_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100)),
            (left_carriageway_start, center_y),
            (center_x - median_half, center_y - camber_drop),
            (center_x + median_half, center_y - camber_drop),
            (right_carriageway_end, center_y),
            (right_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100))
        ]
    else:
        # Single carriageway
        surface_points = [
            (left_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100)),
            (left_carriageway_start, center_y),
            (center_x, center_y + camber_drop),
            (right_carriageway_end, center_y),
            (right_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100))
        ]
    
    # Draw road surface
    msp.add_lwpolyline(surface_points, dxfattribs={'color': 1, 'lineweight': 50})
    
    # Draw pavement layers
    layer_depths = [surface_course, binder_course, base_course, subbase_course]
    layer_names = ['Surface', 'Binder', 'Base', 'Sub-base']
    layer_colors = [2, 3, 4, 5]
    
    cumulative_depth = 0
    for i, (depth, name, color) in enumerate(zip(layer_depths, layer_names, layer_colors)):
        if depth > 0:
            cumulative_depth += depth
            layer_y = center_y - scale_height(cumulative_depth)
            
            # Layer under carriageway
            layer_points = [
                (left_carriageway_start, layer_y),
                (right_carriageway_end, layer_y)
            ]
            msp.add_line(layer_points[0], layer_points[1], dxfattribs={'color': color, 'linetype': 'DASHED'})
    
    # Draw shoulders
    shoulder_depth = scale_height(shoulder_thickness)
    left_shoulder_bottom = center_y - shoulder_depth
    right_shoulder_bottom = center_y - shoulder_depth
    
    # Left shoulder
    msp.add_lwpolyline([
        (left_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100)),
        (left_carriageway_start, center_y),
        (left_carriageway_start, left_shoulder_bottom),
        (left_shoulder_end, left_shoulder_bottom - scale_dim(shoulder_width * shoulder_slope / 100)),
        (left_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100))
    ], dxfattribs={'color': 6})
    
    # Right shoulder
    msp.add_lwpolyline([
        (right_carriageway_end, center_y),
        (right_shoulder_end, center_y - scale_dim(shoulder_width * shoulder_slope / 100)),
        (right_shoulder_end, right_shoulder_bottom - scale_dim(shoulder_width * shoulder_slope / 100)),
        (right_carriageway_end, right_shoulder_bottom),
        (right_carriageway_end, center_y)
    ], dxfattribs={'color': 6})
    
    # Draw median if present
    if median_width > 0:
        median_points = [
            (center_x - median_half, center_y - camber_drop),
            (center_x + median_half, center_y - camber_drop),
            (center_x + median_half, center_y - camber_drop - scale_height(200)),  # 200mm median depth
            (center_x - median_half, center_y - camber_drop - scale_height(200)),
            (center_x - median_half, center_y - camber_drop)
        ]
        msp.add_lwpolyline(median_points, dxfattribs={'color': 5})
    
    # Draw embankment if present
    if embankment_height > 0:
        embankment_top_width = scale_dim(formation_width + 1.0)  # 0.5m margin each side
        embankment_bottom_width = embankment_top_width + 2 * scale_dim(side_slope * embankment_height)
        embankment_height_scaled = scale_dim(embankment_height)
        
        formation_level = center_y - scale_height(surface_course + binder_course + base_course + subbase_course)
        
        embankment_points = [
            (-embankment_bottom_width/2, ground_level),
            (-embankment_top_width/2, formation_level),
            (embankment_top_width/2, formation_level),
            (embankment_bottom_width/2, ground_level),
            (-embankment_bottom_width/2, ground_level)
        ]
        msp.add_lwpolyline(embankment_points, dxfattribs={'color': 8, 'linetype': 'DASHED'})
    
    # Draw side drains if present
    if side_drain:
        drain_depth_scaled = scale_height(drain_depth)
        drain_width_scaled = scale_height(drain_width)
        
        # Calculate drain position
        drain_offset = scale_dim(formation_width/2 + 1.0)  # 1m from formation edge
        drain_invert_level = ground_level - drain_depth_scaled
        
        # Left drain
        drain_bottom_width = drain_width_scaled - 2 * drain_depth_scaled / drain_side_slope
        if drain_bottom_width > 0:
            left_drain_points = [
                (-drain_offset - drain_width_scaled/2, ground_level),
                (-drain_offset - drain_bottom_width/2, drain_invert_level),
                (-drain_offset + drain_bottom_width/2, drain_invert_level),
                (-drain_offset + drain_width_scaled/2, ground_level)
            ]
            msp.add_lwpolyline(left_drain_points, dxfattribs={'color': 4})
        
        # Right drain
        if drain_bottom_width > 0:
            right_drain_points = [
                (drain_offset - drain_width_scaled/2, ground_level),
                (drain_offset - drain_bottom_width/2, drain_invert_level),
                (drain_offset + drain_bottom_width/2, drain_invert_level),
                (drain_offset + drain_width_scaled/2, ground_level)
            ]
            msp.add_lwpolyline(right_drain_points, dxfattribs={'color': 4})
    
    # Add dimensions
    add_dimensions(msp, [
        ((-carriageway_half - median_half - shoulder_width_scaled, center_y + scale_dim(2)),
         (carriageway_half + median_half + shoulder_width_scaled, center_y + scale_dim(2)),
         (0, center_y + scale_dim(3)), f"{formation_width:.1f}m FORMATION"),
        ((-carriageway_half - median_half, center_y + scale_dim(1.5)),
         (carriageway_half + median_half, center_y + scale_dim(1.5)),
         (0, center_y + scale_dim(2.5)), f"{total_carriageway:.1f}m CARRIAGEWAY"),
        ((carriageway_half + median_half + shoulder_width_scaled + scale_dim(1), center_y),
         (carriageway_half + median_half + shoulder_width_scaled + scale_dim(1), center_y - scale_height(surface_course + binder_course + base_course + subbase_course)),
         (carriageway_half + median_half + shoulder_width_scaled + scale_dim(1.5), center_y - scale_height((surface_course + binder_course + base_course + subbase_course)/2)),
         f"{surface_course + binder_course + base_course + subbase_course}mm PAVEMENT")
    ])
    
    # Add text annotations
    title_y = center_y + scale_dim(5)
    msp.add_text(
        f"ROAD CROSS SECTION\nCARRIAGEWAY: {carriageway_width}m, FORMATION: {formation_width:.1f}m\nSCALE 1:{scale}",
        dxfattribs={'height': scale_dim(0.5), 'style': 'STANDARD'}
    ).set_placement((-scale_dim(formation_width/2), title_y))
    
    # Layer details
    details_x = scale_dim(formation_width/2 + 3)
    details_y = center_y
    
    layer_text = f"""PAVEMENT LAYERS:
SURFACE: {surface_course}mm
{'BINDER: ' + str(binder_course) + 'mm' if binder_course > 0 else ''}
BASE: {base_course}mm
SUB-BASE: {subbase_course}mm
TOTAL: {surface_course + binder_course + base_course + subbase_course}mm

SHOULDERS: {shoulder_thickness}mm {shoulder_type}
CAMBER: {camber}%
SHOULDER SLOPE: {shoulder_slope}%"""
    
    msp.add_text(layer_text, dxfattribs={'height': scale_dim(0.3), 'style': 'STANDARD'}
                ).set_placement((details_x, details_y))
    
    # Centerline
    msp.add_line((center_x, center_y + scale_dim(1)), (center_x, ground_level - scale_dim(1)),
                dxfattribs={'color': 7, 'linetype': 'CENTER'})
    
    return doc

def generate_road_cross_section_report(carriageway_width, shoulder_width, median_width, formation_width,
                                     surface_course, base_course, subbase_course, total_pavement,
                                     embankment_height, side_slope, total_pavement_volume):
    """Generate road cross section report"""
    
    report = f"""
ROAD CROSS SECTION DESIGN REPORT
=================================

GEOMETRIC DESIGN:
- Carriageway Width: {carriageway_width} m
- Shoulder Width: {shoulder_width} m (each side)
- Median Width: {median_width} m
- Formation Width: {formation_width:.1f} m
- Total Right of Way: {formation_width + 4:.1f} m (minimum)

PAVEMENT STRUCTURE:
- Surface Course: {surface_course} mm (Bituminous Concrete)
- Base Course: {base_course} mm (Water Bound Macadam)
- Sub-base Course: {subbase_course} mm (Granular Sub-base)
- Total Pavement Thickness: {total_pavement} mm

CROSS-DRAINAGE:
- Camber provided for surface drainage
- Shoulder slope for water disposal
- Side drains for collection and disposal
- Cross-drainage structures at regular intervals

EMBANKMENT DETAILS:
- Embankment Height: {embankment_height} m
- Side Slope: {side_slope}:1 (H:V)
- Foundation: Natural ground or prepared subgrade
- Compaction: 95% of maximum dry density

MATERIAL SPECIFICATIONS:
- Surface Course: As per IRC:111
- Base Course: As per IRC:113
- Sub-base: As per IRC:113
- Embankment: Selected soil as per IRC:36

CONSTRUCTION STANDARDS:
- IRC:SP:84 - Manual of Specifications and Standards
- IRC:37 - Guidelines for Design of Flexible Pavements
- IRC:15 - Standard Specifications and Code of Practice

DRAINAGE DESIGN:
- Surface water disposal through camber and cross-fall
- Subsurface drainage if required
- Adequate capacity of side drains
- Regular maintenance of drainage system

QUALITY CONTROL:
- Material testing as per relevant IRC codes
- Compaction control for each layer
- Surface regularity and texture requirements
- Geometric accuracy during construction

MAINTENANCE REQUIREMENTS:
- Regular inspection and maintenance
- Crack sealing and patch repairs
- Overlay when surface deteriorates
- Drainage system cleaning and repair

ENVIRONMENTAL CONSIDERATIONS:
- Noise control measures if required
- Air quality considerations
- Proper disposal of construction waste
- Erosion control during construction

Generated by RajLisp Structural Design Suite
Standards: IRC (Indian Roads Congress)
"""
    return report
