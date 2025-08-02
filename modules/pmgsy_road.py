import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_pmgsy_road():
    st.title("🛤️ PMGSY Road Designer")
    st.markdown("Design rural roads as per PMGSY (Pradhan Mantri Gram Sadak Yojana) specifications")

    with st.form("pmgsy_road_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 PMGSY Road Category")
            road_category = st.selectbox("Road Category", 
                                       ["Through Route", "Major Rural Link", "Minor Rural Link", "Village Road"],
                                       index=1, help="PMGSY road classification")
            
            # Set default widths based on category
            width_defaults = {
                "Through Route": 5.5,
                "Major Rural Link": 4.75,
                "Minor Rural Link": 4.0,
                "Village Road": 3.75
            }
            
            carriageway_width = st.number_input("Carriageway Width (m)", 
                                              min_value=3.0, max_value=7.0, 
                                              value=width_defaults[road_category], step=0.25,
                                              help="As per PMGSY specifications")
            
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=0.5, max_value=1.5, value=1.0, step=0.25,
                                           help="Earthen shoulder width")
            
            st.markdown("**Terrain Type**")
            terrain = st.selectbox("Terrain", ["Plain", "Rolling", "Hilly", "Steep"], index=0,
                                 help="Terrain classification affects design standards")

        with col2:
            st.subheader("🛤️ Pavement Design")
            traffic_category = st.selectbox("Traffic Category", ["T1", "T2", "T3", "T4"], index=1,
                                          help="PMGSY traffic categories")
            
            # Traffic loads
            traffic_loads = {
                "T1": "< 10 CVPD",
                "T2": "10-20 CVPD", 
                "T3": "20-50 CVPD",
                "T4": "> 50 CVPD"
            }
            st.info(f"Traffic Load: {traffic_loads[traffic_category]}")
            
            # Pavement structure based on traffic
            pavement_structures = {
                "T1": {"surface": 20, "base": 100, "subbase": 150},
                "T2": {"surface": 25, "base": 125, "subbase": 150},
                "T3": {"surface": 30, "base": 150, "subbase": 200},
                "T4": {"surface": 40, "base": 175, "subbase": 225}
            }
            
            structure = pavement_structures[traffic_category]
            
            surface_thickness = st.number_input("Surface Course (mm)", min_value=15, max_value=50, 
                                              value=structure["surface"], step=5,
                                              help="SDBC/Bituminous surface")
            base_thickness = st.number_input("Base Course (mm)", min_value=75, max_value=200, 
                                           value=structure["base"], step=25,
                                           help="WBM/Granular base")
            subbase_thickness = st.number_input("Sub-base (mm)", min_value=100, max_value=250, 
                                              value=structure["subbase"], step=25,
                                              help="Granular sub-base")

        with col3:
            st.subheader("🌊 Drainage & Specifications")
            cross_fall = st.number_input("Cross Fall (%)", min_value=2.0, max_value=4.0, value=2.5, step=0.5,
                                       help="Cross-fall for surface drainage")
            
            side_drain_required = st.checkbox("Side Drains", value=True, help="Roadside drainage")
            if side_drain_required:
                drain_depth = st.number_input("Drain Depth (mm)", min_value=300, max_value=600, value=450, step=50)
                drain_width = st.number_input("Drain Width (mm)", min_value=300, max_value=600, value=450, step=50)
            
            st.markdown("**Construction Standards**")
            construction_season = st.selectbox("Construction Season", ["Dry Season", "Post-Monsoon"], index=0,
                                             help="Preferred construction period")
            
            quality_control = st.selectbox("Quality Control Level", ["Standard", "Enhanced"], index=0,
                                         help="Level of quality control measures")
            
            st.markdown("**Environmental Features**")
            tree_avenue = st.checkbox("Tree Avenue", value=True, help="Roadside tree plantation")
            milestone_required = st.checkbox("Milestones", value=True, help="Distance markers")

        submitted = st.form_submit_button("🔄 Design PMGSY Road", type="primary")

    if submitted:
        with st.spinner("🔄 Designing PMGSY road..."):
            try:
                # Calculate PMGSY specific parameters
                formation_width = carriageway_width + 2 * shoulder_width
                total_pavement = surface_thickness + base_thickness + subbase_thickness
                
                # Create DXF drawing
                doc = create_pmgsy_road_dxf(
                    road_category, carriageway_width, shoulder_width, cross_fall,
                    surface_thickness, base_thickness, subbase_thickness,
                    side_drain_required, drain_depth if side_drain_required else 0,
                    drain_width if side_drain_required else 0, traffic_category
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ PMGSY road design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 PMGSY Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Road Classification**")
                            st.write(f"• Category: {road_category}")
                            st.write(f"• Traffic Category: {traffic_category}")
                            st.write(f"• Traffic Load: {traffic_loads[traffic_category]}")
                            st.write(f"• Terrain: {terrain}")
                            
                            st.markdown("**Geometric Standards**")
                            st.write(f"• Carriageway: {carriageway_width} m")
                            st.write(f"• Shoulders: {shoulder_width} m (each side)")
                            st.write(f"• Formation Width: {formation_width} m")
                            st.write(f"• Cross Fall: {cross_fall}%")
                            
                        with summary_col2:
                            st.markdown("**Pavement Structure**")
                            st.write(f"• Surface Course: {surface_thickness} mm")
                            st.write(f"• Base Course: {base_thickness} mm") 
                            st.write(f"• Sub-base: {subbase_thickness} mm")
                            st.write(f"• **Total Thickness: {total_pavement} mm**")
                            
                            # Check compliance with PMGSY standards
                            min_widths = {
                                "Through Route": 5.5,
                                "Major Rural Link": 4.75,
                                "Minor Rural Link": 4.0,
                                "Village Road": 3.75
                            }
                            
                            if carriageway_width >= min_widths[road_category]:
                                st.success(f"✅ Width compliant (min: {min_widths[road_category]}m)")
                            else:
                                st.error(f"❌ Increase width (min: {min_widths[road_category]}m)")

                    # PMGSY specifications
                    with st.expander("📋 PMGSY Technical Specifications", expanded=True):
                        spec_col1, spec_col2 = st.columns(2)
                        
                        with spec_col1:
                            st.markdown("**Design Standards**")
                            
                            # Design speed based on terrain and category
                            design_speeds = {
                                "Plain": {"Through Route": 80, "Major Rural Link": 65, "Minor Rural Link": 50, "Village Road": 40},
                                "Rolling": {"Through Route": 65, "Major Rural Link": 50, "Minor Rural Link": 40, "Village Road": 35},
                                "Hilly": {"Through Route": 50, "Major Rural Link": 40, "Minor Rural Link": 30, "Village Road": 25},
                                "Steep": {"Through Route": 40, "Major Rural Link": 30, "Minor Rural Link": 25, "Village Road": 20}
                            }
                            
                            design_speed = design_speeds[terrain][road_category]
                            st.write(f"• Design Speed: {design_speed} kmph")
                            
                            # Gradient limits
                            gradient_limits = {
                                "Plain": 4, "Rolling": 6, "Hilly": 8, "Steep": 10
                            }
                            st.write(f"• Max Gradient: {gradient_limits[terrain]}%")
                            
                            # Minimum curve radius
                            min_radius = design_speed ** 2 / (127 * 0.15)  # Simplified formula
                            st.write(f"• Min Curve Radius: {min_radius:.0f} m")
                            
                        with spec_col2:
                            st.markdown("**Material Specifications**")
                            
                            # Material types based on traffic category
                            surface_materials = {
                                "T1": "SDBC (20mm)",
                                "T2": "SDBC (25mm)",
                                "T3": "BC (30mm)",
                                "T4": "BC (40mm)"
                            }
                            
                            st.write(f"• Surface: {surface_materials[traffic_category]}")
                            st.write(f"• Base: WBM Grade-II")
                            st.write(f"• Sub-base: GSB")
                            st.write(f"• Shoulders: Granular/Earth")
                            
                            # Quality requirements
                            st.write(f"• CBR: Min 15% (Subgrade)")
                            st.write(f"• Compaction: 98% MDD")

                    # Construction and cost details
                    with st.expander("🏗️ Construction & Cost Estimation", expanded=True):
                        const_col1, const_col2 = st.columns(2)
                        
                        with const_col1:
                            st.markdown("**Construction Requirements**")
                            
                            st.write(f"• Construction Season: {construction_season}")
                            st.write(f"• Quality Control: {quality_control}")
                            
                            # Construction duration estimate
                            const_rate = {"Plain": 2.0, "Rolling": 1.5, "Hilly": 1.0, "Steep": 0.8}
                            rate = const_rate[terrain]
                            st.write(f"• Construction Rate: ~{rate} km/month")
                            
                            # Special requirements
                            if terrain in ["Hilly", "Steep"]:
                                st.write("• Retaining walls may be required")
                                st.write("• Bioengineering for slope protection")
                            
                            if side_drain_required:
                                st.write("• Side drains with stone pitching")
                            
                        with const_col2:
                            st.markdown("**Quantity Estimates (per km)**")
                            
                            # Calculate material quantities
                            pavement_area = carriageway_width * 1000  # m² per km
                            
                            surface_volume = pavement_area * surface_thickness / 1000  # m³
                            base_volume = pavement_area * base_thickness / 1000
                            subbase_volume = pavement_area * subbase_thickness / 1000
                            
                            st.write(f"• Surface Course: {surface_volume:.0f} m³")
                            st.write(f"• Base Course: {base_volume:.0f} m³")
                            st.write(f"• Sub-base: {subbase_volume:.0f} m³")
                            
                            # Earthwork estimate
                            avg_fill_height = 0.5  # Assumed average
                            earthwork = formation_width * 1000 * avg_fill_height
                            st.write(f"• Earthwork: ~{earthwork:.0f} m³")
                            
                            # Drainage
                            if side_drain_required:
                                drain_excavation = 2 * (drain_width * drain_depth / 1e6) * 1000
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
                        file_name=f"pmgsy_road_{road_category.replace(' ', '_')}_{traffic_category}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_pmgsy_report(
                        road_category, traffic_category, carriageway_width, formation_width,
                        terrain, design_speed, surface_thickness, base_thickness, subbase_thickness,
                        surface_volume, base_volume, subbase_volume
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"pmgsy_road_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_pmgsy_road_dxf(road_category, carriageway_width, shoulder_width, cross_fall,
                         surface_thickness, base_thickness, subbase_thickness,
                         side_drain_required, drain_depth, drain_width, traffic_category):
    """Create DXF drawing for PMGSY road"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Scale for drawing
    scale = 50  # 1:50 scale for cross-section
    
    def scale_dim(value_m):
        return value_m * 1000 / scale
    
    def scale_height(value_mm):
        return value_mm / scale
    
    # Road geometry
    formation_width = carriageway_width + 2 * shoulder_width
    carriageway_half = scale_dim(carriageway_width / 2)
    shoulder_width_scaled = scale_dim(shoulder_width)
    
    # Center line and datum
    center_x = 0
    center_y = 0
    
    # Road surface with cross-fall
    cross_fall_drop = scale_dim(carriageway_width / 2 * cross_fall / 100)
    
    # Surface profile points
    surface_points = [
        (-carriageway_half - shoulder_width_scaled, center_y - scale_dim(shoulder_width * 0.03)),  # 3% shoulder slope
        (-carriageway_half, center_y),
        (0, center_y + cross_fall_drop),  # Crown at center
        (carriageway_half, center_y),
        (carriageway_half + shoulder_width_scaled, center_y - scale_dim(shoulder_width * 0.03))
    ]
    
    # Draw road surface
    msp.add_lwpolyline(surface_points, dxfattribs={'color': 1, 'lineweight': 70})
    
    # Pavement layers
    total_pavement = surface_thickness + base_thickness + subbase_thickness
    
    # Surface course
    surface_level = center_y - scale_height(surface_thickness)
    msp.add_line((-carriageway_half, surface_level), (carriageway_half, surface_level),
                dxfattribs={'color': 2, 'linetype': 'DASHED'})
    
    # Base course
    base_level = center_y - scale_height(surface_thickness + base_thickness)
    msp.add_line((-carriageway_half, base_level), (carriageway_half, base_level),
                dxfattribs={'color': 3, 'linetype': 'DASHED'})
    
    # Sub-base level (formation level)
    formation_level = center_y - scale_height(total_pavement)
    msp.add_line((-carriageway_half, formation_level), (carriageway_half, formation_level),
                dxfattribs={'color': 4, 'linetype': 'DASHED'})
    
    # Formation (full width)
    formation_points = [
        (-scale_dim(formation_width/2), formation_level),
        (scale_dim(formation_width/2), formation_level)
    ]
    msp.add_line(formation_points[0], formation_points[1], dxfattribs={'color': 5, 'lineweight': 35})
    
    # Shoulders
    shoulder_bottom = center_y - scale_height(100)  # 100mm shoulder thickness
    
    # Left shoulder
    msp.add_lwpolyline([
        (-carriageway_half - shoulder_width_scaled, center_y - scale_dim(shoulder_width * 0.03)),
        (-carriageway_half, center_y),
        (-carriageway_half, shoulder_bottom),
        (-carriageway_half - shoulder_width_scaled, shoulder_bottom - scale_dim(shoulder_width * 0.03)),
        (-carriageway_half - shoulder_width_scaled, center_y - scale_dim(shoulder_width * 0.03))
    ], dxfattribs={'color': 6})
    
    # Right shoulder
    msp.add_lwpolyline([
        (carriageway_half, center_y),
        (carriageway_half + shoulder_width_scaled, center_y - scale_dim(shoulder_width * 0.03)),
        (carriageway_half + shoulder_width_scaled, shoulder_bottom - scale_dim(shoulder_width * 0.03)),
        (carriageway_half, shoulder_bottom),
        (carriageway_half, center_y)
    ], dxfattribs={'color': 6})
    
    # Side drains
    if side_drain_required:
        drain_offset = scale_dim(formation_width/2 + 0.5)  # 0.5m from formation edge
        drain_depth_scaled = scale_height(drain_depth)
        drain_width_scaled = scale_height(drain_width)
        
        # Ground level
        ground_level = formation_level - scale_dim(0.2)  # 200mm below formation
        
        # Left drain
        left_drain_points = [
            (-drain_offset - drain_width_scaled/2, ground_level),
            (-drain_offset - drain_width_scaled/4, ground_level - drain_depth_scaled),
            (-drain_offset + drain_width_scaled/4, ground_level - drain_depth_scaled),
            (-drain_offset + drain_width_scaled/2, ground_level)
        ]
        msp.add_lwpolyline(left_drain_points, dxfattribs={'color': 4})
        
        # Right drain
        right_drain_points = [
            (drain_offset - drain_width_scaled/2, ground_level),
            (drain_offset - drain_width_scaled/4, ground_level - drain_depth_scaled),
            (drain_offset + drain_width_scaled/4, ground_level - drain_depth_scaled),
            (drain_offset + drain_width_scaled/2, ground_level)
        ]
        msp.add_lwpolyline(right_drain_points, dxfattribs={'color': 4})
    
    # Add dimensions
    add_dimensions(msp, [
        ((-carriageway_half - shoulder_width_scaled, center_y + scale_dim(1)),
         (carriageway_half + shoulder_width_scaled, center_y + scale_dim(1)),
         (0, center_y + scale_dim(1.5)), f"{formation_width:.2f}m FORMATION"),
        ((-carriageway_half, center_y + scale_dim(0.5)),
         (carriageway_half, center_y + scale_dim(0.5)),
         (0, center_y + scale_dim(1)), f"{carriageway_width:.2f}m CARRIAGEWAY"),
        ((carriageway_half + shoulder_width_scaled + scale_dim(0.5), center_y),
         (carriageway_half + shoulder_width_scaled + scale_dim(0.5), formation_level),
         (carriageway_half + shoulder_width_scaled + scale_dim(1), center_y - scale_height(total_pavement/2)),
         f"{total_pavement}mm PAVEMENT")
    ])
    
    # Title and specifications
    title_y = center_y + scale_dim(3)
    msp.add_text(
        f"PMGSY ROAD CROSS SECTION\n{road_category.upper()} - TRAFFIC {traffic_category}\nSCALE 1:{scale}",
        dxfattribs={'height': scale_dim(0.4), 'style': 'STANDARD'}
    ).set_placement((-scale_dim(formation_width/2), title_y))
    
    # Technical specifications
    spec_x = scale_dim(formation_width/2 + 2)
    spec_y = center_y + scale_dim(1)
    
    spec_text = f"""PMGSY SPECIFICATIONS:

ROAD CATEGORY: {road_category}
TRAFFIC CATEGORY: {traffic_category}
CARRIAGEWAY: {carriageway_width:.2f}m
FORMATION: {formation_width:.2f}m

PAVEMENT STRUCTURE:
SURFACE: {surface_thickness}mm
BASE: {base_thickness}mm (WBM-II)
SUB-BASE: {subbase_thickness}mm (GSB)

CROSS FALL: {cross_fall}%
SHOULDER SLOPE: 3%

STANDARDS:
- PMGSY Technical Specifications
- IRC:SP:20 (Rural Roads Manual)
- IRC:37 (Flexible Pavement Design)"""
    
    msp.add_text(spec_text, dxfattribs={'height': scale_dim(0.25), 'style': 'STANDARD'}
                ).set_placement((spec_x, spec_y))
    
    # Center line
    msp.add_line((0, center_y + scale_dim(0.5)), (0, formation_level - scale_dim(0.5)),
                dxfattribs={'color': 7, 'linetype': 'CENTER'})
    
    # PMGSY logo placeholder
    logo_x = -scale_dim(formation_width/2)
    logo_y = formation_level - scale_dim(2)
    
    msp.add_text("PMGSY", dxfattribs={'height': scale_dim(0.6), 'style': 'STANDARD'}
                ).set_placement((logo_x, logo_y))
    
    return doc

def generate_pmgsy_report(road_category, traffic_category, carriageway_width, formation_width,
                         terrain, design_speed, surface_thickness, base_thickness, subbase_thickness,
                         surface_volume, base_volume, subbase_volume):
    """Generate PMGSY road design report"""
    
    total_pavement = surface_thickness + base_thickness + subbase_thickness
    
    report = f"""
PMGSY ROAD DESIGN REPORT
========================

PROJECT CLASSIFICATION:
- Road Category: {road_category}
- Traffic Category: {traffic_category}
- Terrain Type: {terrain}
- Design Speed: {design_speed} kmph

GEOMETRIC DESIGN:
- Carriageway Width: {carriageway_width:.2f} m
- Formation Width: {formation_width:.2f} m
- Cross Fall: 2.5%
- Shoulder Slope: 3.0%

PAVEMENT DESIGN:
- Surface Course: {surface_thickness} mm
- Base Course: {base_thickness} mm (WBM Grade-II)
- Sub-base Course: {subbase_thickness} mm (GSB)
- Total Pavement Thickness: {total_pavement} mm

DESIGN STANDARDS:
- PMGSY Technical Specifications
- IRC:SP:20 (Rural Roads Manual)
- IRC:37 (Guidelines for Design of Flexible Pavements)
- IRC:15 (Standard Specifications and Code of Practice)

MATERIAL SPECIFICATIONS:
- Surface Course: SDBC/BC as per IRC:111
- Base Course: Water Bound Macadam as per IRC:113
- Sub-base: Granular Sub-base as per IRC:113
- Subgrade: CBR minimum 15%

QUALITY CONTROL REQUIREMENTS:
- Material testing as per IRC specifications
- Compaction: 98% of Maximum Dry Density
- Surface regularity: ±10mm from design level
- Geometric accuracy as per drawings

MATERIAL QUANTITIES (per km):
- Surface Course: {surface_volume:.0f} m³
- Base Course: {base_volume:.0f} m³  
- Sub-base Course: {subbase_volume:.0f} m³
- Earthwork: Variable based on terrain
- Side drain excavation: As required

CONSTRUCTION METHODOLOGY:
- Season: Dry season preferred
- Layer-wise construction with proper curing
- Quality control at each stage
- Traffic management during construction

DRAINAGE PROVISIONS:
- Cross drainage structures at water crossings
- Side drains for surface water disposal
- Adequate camber and cross-fall
- Proper outlets for collected water

ENVIRONMENTAL CONSIDERATIONS:
- Tree plantation along road corridor
- Erosion control measures
- Proper disposal of construction waste
- Noise and dust control during construction

MAINTENANCE REQUIREMENTS:
- Regular inspection and preventive maintenance
- Pothole filling and crack sealing
- Drainage system cleaning
- Shoulder and verge maintenance
- Periodic overlay as required

SPECIAL FEATURES FOR RURAL ROADS:
- Cattle crossings at regular intervals
- Bus stops at village connections
- Milestone and sign boards
- Speed control measures in village areas

COMPLIANCE CERTIFICATION:
This design complies with PMGSY technical specifications
and relevant IRC standards for rural road construction.

Generated by RajLisp Structural Design Suite
Standards: PMGSY & IRC (Indian Roads Congress)
Date: Current Date
"""
    return report
