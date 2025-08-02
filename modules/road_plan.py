import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_road_plan():
    st.title("🗺️ Road Plan Designer")
    st.markdown("Design road plan layout with horizontal alignment, curves, and intersections")

    with st.form("road_plan_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Road Alignment")
            total_length = st.number_input("Total Length (m)", min_value=500, max_value=20000, value=2000, step=100,
                                         help="Total length of road alignment")
            road_width = st.number_input("Carriageway Width (m)", min_value=3.5, max_value=15, value=7.0, step=0.5,
                                       help="Width of carriageway")
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=1.0, max_value=3.0, value=1.5, step=0.5,
                                           help="Width of road shoulder")
            
            st.markdown("**Horizontal Curves**")
            num_curves = st.slider("Number of Curves", min_value=0, max_value=5, value=2, step=1,
                                 help="Number of horizontal curves in alignment")
            
            if num_curves > 0:
                curve_radius = st.number_input("Curve Radius (m)", min_value=30, max_value=1000, value=150, step=25,
                                             help="Radius of horizontal curves")

        with col2:
            st.subheader("🛤️ Design Parameters")
            design_speed = st.selectbox("Design Speed (kmph)", [30, 50, 60, 80, 100, 120], index=2,
                                      help="Design speed for geometric design")
            super_elevation = st.number_input("Super-elevation (%)", min_value=2.5, max_value=7.0, value=4.0, step=0.5,
                                            help="Banking of road at curves")
            
            st.markdown("**Right of Way**")
            row_width = st.number_input("ROW Width (m)", min_value=15, max_value=60, value=30, step=5,
                                      help="Total right of way width")
            
            st.markdown("**Intersections**")
            num_intersections = st.slider("Number of Intersections", min_value=0, max_value=3, value=1, step=1,
                                        help="Number of road intersections")
            
            if num_intersections > 0:
                intersection_type = st.selectbox("Intersection Type", ["T-Junction", "Cross Junction", "Roundabout"], 
                                               index=0, help="Type of intersection")

        with col3:
            st.subheader("🏗️ Infrastructure")
            median_width = st.number_input("Median Width (m)", min_value=0, max_value=5, value=0, step=0.5,
                                         help="Width of central median (0 for no median)")
            
            st.markdown("**Utilities**")
            service_road = st.checkbox("Service Road", value=False, help="Include service road")
            if service_road:
                service_width = st.number_input("Service Road Width (m)", min_value=3.0, max_value=6.0, value=4.0, step=0.5)
            
            st.markdown("**Drainage**")
            side_drain = st.checkbox("Side Drains", value=True, help="Include roadside drainage")
            if side_drain:
                drain_type = st.selectbox("Drain Type", ["Open Drain", "Covered Drain", "Pipe Drain"], index=0)
            
            st.markdown("**Environment**")
            tree_plantation = st.checkbox("Tree Plantation", value=True, help="Include tree plantation areas")
            noise_barrier = st.checkbox("Noise Barrier", value=False, help="Include noise barriers if required")

        submitted = st.form_submit_button("🔄 Generate Road Plan", type="primary")

    if submitted:
        with st.spinner("🔄 Generating road plan layout..."):
            try:
                # Create DXF drawing
                doc = create_road_plan_dxf(
                    total_length, road_width, shoulder_width, row_width,
                    num_curves, curve_radius if num_curves > 0 else 0,
                    num_intersections, intersection_type if num_intersections > 0 else "",
                    median_width, service_road, service_width if service_road else 0,
                    design_speed, super_elevation
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Road plan layout generated successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Road Geometry**")
                            st.write(f"• Total Length: {total_length} m")
                            st.write(f"• Carriageway Width: {road_width} m")
                            st.write(f"• Shoulder Width: {shoulder_width} m each side")
                            
                            formation_width = road_width + 2 * shoulder_width + median_width
                            st.write(f"• Formation Width: {formation_width} m")
                            st.write(f"• Right of Way: {row_width} m")
                            
                            if num_curves > 0:
                                st.write(f"• Number of Curves: {num_curves}")
                                st.write(f"• Curve Radius: {curve_radius} m")
                            
                        with summary_col2:
                            st.markdown("**Design Standards**")
                            st.write(f"• Design Speed: {design_speed} kmph")
                            
                            # Check minimum radius for design speed
                            min_radius_required = {30: 30, 50: 60, 60: 95, 80: 180, 100: 280, 120: 410}
                            min_req = min_radius_required.get(design_speed, 100)
                            
                            if num_curves > 0:
                                if curve_radius >= min_req:
                                    st.success(f"✅ Curve radius OK (min: {min_req}m)")
                                else:
                                    st.error(f"❌ Increase radius (min: {min_req}m)")
                            
                            st.write(f"• Super-elevation: {super_elevation}%")
                            
                            if median_width > 0:
                                st.write(f"• Median Width: {median_width} m")

                    # Infrastructure details
                    with st.expander("🏗️ Infrastructure & Utilities", expanded=True):
                        infra_col1, infra_col2 = st.columns(2)
                        
                        with infra_col1:
                            st.markdown("**Road Infrastructure**")
                            
                            if num_intersections > 0:
                                st.write(f"• Intersections: {num_intersections} ({intersection_type})")
                            
                            if service_road:
                                st.write(f"• Service Road: {service_width} m width")
                            
                            if side_drain:
                                st.write(f"• Drainage: {drain_type}")
                            
                        with infra_col2:
                            st.markdown("**Environmental Features**")
                            
                            if tree_plantation:
                                st.write("• Tree plantation areas provided")
                            
                            if noise_barrier:
                                st.write("• Noise barriers included")
                            
                            # Calculate area requirements
                            total_area = row_width * total_length / 10000  # hectares
                            st.write(f"• Total Land Area: {total_area:.2f} hectares")

                    # Design calculations
                    with st.expander("🧮 Design Calculations", expanded=True):
                        calc_col1, calc_col2 = st.columns(2)
                        
                        with calc_col1:
                            st.markdown("**Geometric Calculations**")
                            
                            if num_curves > 0:
                                # Curve calculations
                                curve_length = (np.pi * curve_radius * 90) / 180  # Assuming 90° curves
                                transition_length = design_speed**2 / (2.5 * curve_radius)  # Simplified
                                
                                st.write(f"• Curve Length: {curve_length:.0f} m (per curve)")
                                st.write(f"• Transition Length: {transition_length:.0f} m")
                                
                                total_curve_length = num_curves * curve_length
                                straight_length = total_length - total_curve_length
                                
                                st.write(f"• Total Curve Length: {total_curve_length:.0f} m")
                                st.write(f"• Straight Length: {straight_length:.0f} m")
                            
                            # Sight distance
                            sight_distances = {30: 30, 50: 60, 60: 85, 80: 120, 100: 160, 120: 200}
                            required_sight = sight_distances.get(design_speed, 85)
                            st.write(f"• Required Sight Distance: {required_sight} m")
                        
                        with calc_col2:
                            st.markdown("**Area & Volume Calculations**")
                            
                            # Pavement area
                            pavement_area = road_width * total_length
                            shoulder_area = 2 * shoulder_width * total_length
                            
                            st.write(f"• Pavement Area: {pavement_area:.0f} m²")
                            st.write(f"• Shoulder Area: {shoulder_area:.0f} m²")
                            
                            if service_road:
                                service_area = 2 * service_width * total_length  # Both sides
                                st.write(f"• Service Road Area: {service_area:.0f} m²")
                            
                            # ROW utilization
                            utilized_width = formation_width + (2 * service_width if service_road else 0)
                            row_utilization = (utilized_width / row_width) * 100
                            
                            st.write(f"• ROW Utilization: {row_utilization:.1f}%")

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
                        file_name=f"road_plan_{total_length}m_{design_speed}kmph.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_road_plan_report(
                        total_length, road_width, shoulder_width, row_width,
                        design_speed, num_curves, curve_radius if num_curves > 0 else 0,
                        num_intersections, pavement_area + shoulder_area
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"road_plan_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_road_plan_dxf(total_length, road_width, shoulder_width, row_width,
                        num_curves, curve_radius, num_intersections, intersection_type,
                        median_width, service_road, service_width, design_speed, super_elevation):
    """Create DXF drawing for road plan"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Scale for drawing (1:1000 typical for road plans)
    scale = 1000
    length_scaled = total_length * 1000 / scale  # Convert to mm then scale
    width_scaled = row_width * 1000 / scale
    
    # Road centerline (main alignment)
    if num_curves == 0:
        # Straight road
        msp.add_line((0, 0), (length_scaled, 0), dxfattribs={'color': 1, 'lineweight': 50})
    else:
        # Road with curves - simplified as a serpentine pattern
        points = []
        segment_length = length_scaled / (num_curves + 1)
        
        for i in range(num_curves + 2):
            x = i * segment_length
            if i % 2 == 0:
                y = 0
            else:
                y = (curve_radius * 1000 / scale) / 4  # Simplified curve representation
            points.append((x, y))
        
        msp.add_spline(points, dxfattribs={'color': 1, 'lineweight': 50})
    
    # Road edges
    road_half_width = (road_width * 1000 / scale) / 2
    
    # Left edge
    left_edge_points = []
    right_edge_points = []
    
    if num_curves == 0:
        left_edge_points = [(0, -road_half_width), (length_scaled, -road_half_width)]
        right_edge_points = [(0, road_half_width), (length_scaled, road_half_width)]
    else:
        # Simplified curve edges
        segment_length = length_scaled / (num_curves + 1)
        for i in range(num_curves + 2):
            x = i * segment_length
            if i % 2 == 0:
                y_center = 0
            else:
                y_center = (curve_radius * 1000 / scale) / 4
            
            left_edge_points.append((x, y_center - road_half_width))
            right_edge_points.append((x, y_center + road_half_width))
    
    msp.add_spline(left_edge_points, dxfattribs={'color': 2})
    msp.add_spline(right_edge_points, dxfattribs={'color': 2})
    
    # Shoulders
    shoulder_width_scaled = shoulder_width * 1000 / scale
    
    # Left shoulder
    left_shoulder_points = [(x, y - shoulder_width_scaled) for x, y in left_edge_points]
    msp.add_spline(left_shoulder_points, dxfattribs={'color': 3, 'linetype': 'DASHED'})
    
    # Right shoulder
    right_shoulder_points = [(x, y + shoulder_width_scaled) for x, y in right_edge_points]
    msp.add_spline(right_shoulder_points, dxfattribs={'color': 3, 'linetype': 'DASHED'})
    
    # Right of Way boundary
    row_half_width = (row_width * 1000 / scale) / 2
    msp.add_line((0, -row_half_width), (length_scaled, -row_half_width), 
                dxfattribs={'color': 4, 'linetype': 'DASHDOT'})
    msp.add_line((0, row_half_width), (length_scaled, row_half_width), 
                dxfattribs={'color': 4, 'linetype': 'DASHDOT'})
    
    # Median (if provided)
    if median_width > 0:
        median_half_width = (median_width * 1000 / scale) / 2
        median_left = [(x, y + median_half_width) for x, y in [(0, 0), (length_scaled, 0)]]
        median_right = [(x, y - median_half_width) for x, y in [(0, 0), (length_scaled, 0)]]
        
        msp.add_line(median_left[0], median_left[1], dxfattribs={'color': 5})
        msp.add_line(median_right[0], median_right[1], dxfattribs={'color': 5})
    
    # Intersections
    if num_intersections > 0:
        intersection_spacing = length_scaled / (num_intersections + 1)
        
        for i in range(num_intersections):
            x_pos = (i + 1) * intersection_spacing
            
            if intersection_type == "T-Junction":
                # Simple T-junction
                junction_length = 200 / scale * 1000
                msp.add_line((x_pos, road_half_width), 
                           (x_pos, road_half_width + junction_length),
                           dxfattribs={'color': 6, 'lineweight': 30})
                
            elif intersection_type == "Cross Junction":
                # Cross junction
                junction_length = 200 / scale * 1000
                msp.add_line((x_pos, -road_half_width - junction_length), 
                           (x_pos, road_half_width + junction_length),
                           dxfattribs={'color': 6, 'lineweight': 30})
                
            elif intersection_type == "Roundabout":
                # Simple roundabout
                roundabout_radius = 50 / scale * 1000
                msp.add_circle((x_pos, 0), roundabout_radius, 
                             dxfattribs={'color': 6, 'lineweight': 30})
    
    # Service roads
    if service_road:
        service_offset = (road_half_width + shoulder_width_scaled + 
                         service_width * 1000 / scale / 2 + 100 / scale * 1000)
        
        # Left service road
        msp.add_line((0, -service_offset), (length_scaled, -service_offset),
                    dxfattribs={'color': 7, 'linetype': 'DASHED'})
        
        # Right service road
        msp.add_line((0, service_offset), (length_scaled, service_offset),
                    dxfattribs={'color': 7, 'linetype': 'DASHED'})
    
    # Chainage markers every 100m
    chainage_interval = 100 * 1000 / scale
    num_chainages = int(length_scaled / chainage_interval) + 1
    
    for i in range(num_chainages):
        x_pos = i * chainage_interval
        if x_pos <= length_scaled:
            # Chainage line across road
            msp.add_line((x_pos, -road_half_width), (x_pos, road_half_width),
                        dxfattribs={'color': 8, 'linetype': 'CENTER'})
            
            # Chainage text
            msp.add_text(f"{i * 100}m",
                        dxfattribs={'height': 100 / scale * 1000, 'style': 'STANDARD'}
                        ).set_placement((x_pos, road_half_width + 200 / scale * 1000))
    
    # North arrow
    north_arrow_size = 500 / scale * 1000
    north_x = length_scaled - 1000 / scale * 1000
    north_y = row_half_width - 500 / scale * 1000
    
    # North arrow triangle
    msp.add_lwpolyline([
        (north_x, north_y),
        (north_x - north_arrow_size/2, north_y - north_arrow_size),
        (north_x + north_arrow_size/2, north_y - north_arrow_size),
        (north_x, north_y)
    ], dxfattribs={'color': 1})
    
    msp.add_text("N", dxfattribs={'height': 200 / scale * 1000, 'style': 'STANDARD'}
                ).set_placement((north_x - 100 / scale * 1000, north_y + 100 / scale * 1000))
    
    # Title block
    title_x = 0
    title_y = row_half_width + 1000 / scale * 1000
    
    msp.add_text(
        f"ROAD PLAN\nLENGTH: {total_length}m, WIDTH: {road_width}m\nDESIGN SPEED: {design_speed} KMPH\nSCALE 1:{scale}",
        dxfattribs={'height': 300 / scale * 1000, 'style': 'STANDARD'}
    ).set_placement((title_x, title_y))
    
    # Legend
    legend_x = length_scaled - 3000 / scale * 1000
    legend_y = -row_half_width - 1000 / scale * 1000
    
    legend_text = f"""LEGEND:
ROAD CENTERLINE
ROAD EDGES
SHOULDERS
ROW BOUNDARY
CHAINAGES
{'INTERSECTIONS' if num_intersections > 0 else ''}
{'SERVICE ROADS' if service_road else ''}"""
    
    msp.add_text(legend_text,
                dxfattribs={'height': 150 / scale * 1000, 'style': 'STANDARD'}
                ).set_placement((legend_x, legend_y))
    
    return doc

def generate_road_plan_report(total_length, road_width, shoulder_width, row_width,
                            design_speed, num_curves, curve_radius, num_intersections, total_area):
    """Generate road plan design report"""
    
    formation_width = road_width + 2 * shoulder_width
    
    report = f"""
ROAD PLAN DESIGN REPORT
=======================

PROJECT DETAILS:
- Total Length: {total_length} m
- Carriageway Width: {road_width} m
- Shoulder Width: {shoulder_width} m (each side)
- Formation Width: {formation_width} m
- Right of Way Width: {row_width} m
- Design Speed: {design_speed} kmph

HORIZONTAL ALIGNMENT:
- Number of Curves: {num_curves}
- Curve Radius: {curve_radius} m
- Minimum Radius Required: {30 if design_speed <= 30 else 60 if design_speed <= 50 else 95 if design_speed <= 60 else 180 if design_speed <= 80 else 280 if design_speed <= 100 else 410} m
- Radius Adequacy: {'Adequate' if curve_radius >= (30 if design_speed <= 30 else 60 if design_speed <= 50 else 95 if design_speed <= 60 else 180 if design_speed <= 80 else 280 if design_speed <= 100 else 410) else 'Inadequate'}

INTERSECTIONS:
- Number of Intersections: {num_intersections}
- Sight Distance Required: {30 if design_speed <= 30 else 60 if design_speed <= 50 else 85 if design_speed <= 60 else 120 if design_speed <= 80 else 160 if design_speed <= 100 else 200} m

AREA CALCULATIONS:
- Total Pavement Area: {total_area:.0f} m²
- Total Land Area: {(row_width * total_length)/10000:.2f} hectares
- ROW Utilization: {(formation_width/row_width)*100:.1f}%

DESIGN STANDARDS:
- IRC:73-1980 (Geometric Design Standards for Rural Roads)
- IRC:86-1983 (Geometric Design Standards for Urban Roads)
- IRC:SP:84-2019 (Manual of Specifications and Standards)

GEOMETRIC FEATURES:
- Horizontal Curves: Provided with adequate radius
- Super-elevation: As per design speed requirements
- Transition Curves: To be provided as per IRC standards
- Sight Distance: Clear sight distance maintained

INFRASTRUCTURE REQUIREMENTS:
- Road Signs and Markings as per IRC:35
- Guard Rails at necessary locations
- Lighting for urban sections
- Drainage structures as required

ENVIRONMENTAL CONSIDERATIONS:
- Tree plantation in available ROW area
- Noise barriers if required near sensitive areas
- Proper drainage to prevent water logging
- Soil erosion control measures

CONSTRUCTION RECOMMENDATIONS:
1. Detailed soil investigation at regular intervals
2. Quality control of construction materials
3. Proper compaction of each layer
4. Traffic management during construction
5. Safety measures for workers and public

MAINTENANCE REQUIREMENTS:
- Regular inspection of pavement condition
- Maintenance of drainage systems
- Upkeep of road furniture and signage
- Vegetation control in ROW
- Periodic resurfacing as required

Generated by RajLisp Structural Design Suite
Design Standards: IRC (Indian Roads Congress)
"""
    return report
