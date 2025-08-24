import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions

def page_staircase():
    st.title("🪜 Staircase Designer")
    st.markdown("Design reinforced concrete staircases with detailed reinforcement layout")

    with st.form("staircase_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Staircase Geometry")
            flight_length = st.number_input("Flight Length (mm)", min_value=2000, max_value=6000, value=3500, step=250,
                                          help="Horizontal length of stair flight")
            flight_height = st.number_input("Flight Height (mm)", min_value=1500, max_value=4000, value=2700, step=150,
                                          help="Total vertical rise")
            
            slab_thickness = st.number_input("Slab Thickness (mm)", min_value=125, max_value=250, value=150, step=25,
                                           help="Thickness of stair slab")
            
            st.markdown("**Step Details**")
            riser_height = st.number_input("Riser Height (mm)", min_value=150, max_value=200, value=175, step=5,
                                         help="Height of each step")
            tread_width = st.number_input("Tread Width (mm)", min_value=250, max_value=350, value=300, step=25,
                                        help="Width of each step")
            
            # Calculate number of steps
            num_risers = int(flight_height / riser_height)
            num_treads = num_risers - 1
            
            st.info(f"Calculated: {num_risers} risers, {num_treads} treads")

        with col2:
            st.subheader("🔩 Main Reinforcement")
            main_bar_dia = st.selectbox("Main Bar Diameter (mm)", [10, 12, 16, 20], index=2,
                                      help="Diameter of main reinforcement")
            main_bar_spacing = st.number_input("Main Bar Spacing (mm)", min_value=100, max_value=200, value=150, step=25,
                                             help="Spacing of main bars")
            
            dist_bar_dia = st.selectbox("Distribution Bar Diameter (mm)", [8, 10, 12], index=1,
                                      help="Diameter of distribution bars")
            dist_bar_spacing = st.number_input("Distribution Spacing (mm)", min_value=150, max_value=300, value=200, step=25,
                                             help="Spacing of distribution bars")
            
            st.markdown("**Additional Reinforcement**")
            step_bar_dia = st.selectbox("Step Bar Diameter (mm)", [8, 10, 12], index=0,
                                      help="Additional bars at step corners")
            
            beam_width = st.number_input("Supporting Beam Width (mm)", min_value=200, max_value=400, value=300, step=25,
                                       help="Width of supporting beam if any")

        with col3:
            st.subheader("🏗️ Materials & Loading")
            concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30"], index=1)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500"], index=1)
            clear_cover = st.number_input("Clear Cover (mm)", min_value=15, max_value=30, value=20, step=5,
                                        help="Clear cover to reinforcement")
            
            st.markdown("**Loading**")
            live_load = st.number_input("Live Load (kN/m²)", min_value=3, max_value=8, value=4, step=1,
                                      help="Live load on staircase")
            floor_finish = st.number_input("Floor Finish (kN/m²)", min_value=0.5, max_value=2, value=1, step=0.5,
                                         help="Weight of floor finish")
            
            st.markdown("**Support Conditions**")
            support_type = st.radio("Support Type", ["Simply Supported", "One End Fixed", "Both Ends Fixed"], 
                                   help="Support conditions for analysis")

        submitted = st.form_submit_button("🔄 Design Staircase", type="primary")

    if submitted:
        with st.spinner("🔄 Designing staircase..."):
            try:
                # Calculate design parameters
                effective_span = flight_length
                inclined_length = np.sqrt(flight_length**2 + flight_height**2)
                
                # Load calculations
                self_weight = 25 * slab_thickness / 1000  # kN/m²
                step_weight = 25 * riser_height / 2 / 1000  # kN/m² (triangular load)
                total_dead_load = self_weight + step_weight + floor_finish
                total_load = total_dead_load + live_load
                
                # Convert to load per unit length on inclined slab
                load_per_meter = total_load * 1.0  # Assuming 1m width
                
                # Moment calculation based on support conditions
                if support_type == "Simply Supported":
                    design_moment = load_per_meter * (effective_span/1000)**2 / 8
                elif support_type == "One End Fixed":
                    design_moment = load_per_meter * (effective_span/1000)**2 / 12
                else:  # Both Ends Fixed
                    design_moment = load_per_meter * (effective_span/1000)**2 / 24
                
                design_shear = load_per_meter * (effective_span/1000) / 2

                # Create DXF drawing
                doc = create_staircase_dxf(
                    flight_length, flight_height, slab_thickness, riser_height, tread_width,
                    main_bar_dia, main_bar_spacing, dist_bar_dia, dist_bar_spacing,
                    step_bar_dia, clear_cover, num_risers, num_treads
                )

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Staircase design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Staircase Geometry**")
                            st.write(f"• Flight Length: {flight_length} mm")
                            st.write(f"• Flight Height: {flight_height} mm")
                            st.write(f"• Inclined Length: {inclined_length:.0f} mm")
                            st.write(f"• Slab Thickness: {slab_thickness} mm")
                            st.write(f"• Number of Risers: {num_risers}")
                            st.write(f"• Number of Treads: {num_treads}")
                            
                            # Check step proportions
                            step_formula = 2 * riser_height + tread_width
                            st.write(f"• Step Formula (2R+T): {step_formula} mm")
                            if 550 <= step_formula <= 700:
                                st.success("✅ Step proportions OK")
                            else:
                                st.warning("⚠️ Check step proportions")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement Details**")
                            st.write(f"• Main Bars: ⌀{main_bar_dia}mm @ {main_bar_spacing}mm c/c")
                            st.write(f"• Distribution: ⌀{dist_bar_dia}mm @ {dist_bar_spacing}mm c/c")
                            st.write(f"• Step Bars: ⌀{step_bar_dia}mm")
                            
                            # Calculate steel areas
                            main_steel_per_meter = (1000 / main_bar_spacing) * np.pi * (main_bar_dia/2)**2
                            dist_steel_per_meter = (1000 / dist_bar_spacing) * np.pi * (dist_bar_dia/2)**2
                            
                            st.write(f"• Main Steel: {main_steel_per_meter:.0f} mm²/m")
                            st.write(f"• Dist Steel: {dist_steel_per_meter:.0f} mm²/m")

                    # Load analysis
                    with st.expander("📊 Load Analysis", expanded=True):
                        load_col1, load_col2 = st.columns(2)
                        
                        with load_col1:
                            st.markdown("**Load Components**")
                            st.write(f"• Self Weight: {self_weight:.2f} kN/m²")
                            st.write(f"• Step Weight: {step_weight:.2f} kN/m²")
                            st.write(f"• Floor Finish: {floor_finish:.2f} kN/m²")
                            st.write(f"• Live Load: {live_load:.2f} kN/m²")
                            st.write(f"• **Total Load: {total_load:.2f} kN/m²**")
                            
                        with load_col2:
                            st.markdown("**Design Forces**")
                            st.write(f"• Load per meter: {load_per_meter:.2f} kN/m")
                            st.write(f"• Design Moment: {design_moment:.2f} kNm/m")
                            st.write(f"• Design Shear: {design_shear:.1f} kN/m")
                            st.write(f"• Support Type: {support_type}")

                    # Design verification
                    with st.expander("🔍 Design Verification", expanded=True):
                        verify_col1, verify_col2 = st.columns(2)
                        
                        with verify_col1:
                            st.markdown("**Reinforcement Check**")
                            effective_depth = slab_thickness - clear_cover - main_bar_dia/2
                            
                            # Minimum reinforcement check
                            min_steel = 0.12 * slab_thickness * 1000 / 100  # 0.12% of gross area
                            provided_steel = main_steel_per_meter + dist_steel_per_meter
                            
                            st.write(f"• Effective Depth: {effective_depth:.0f} mm")
                            st.write(f"• Min Steel Required: {min_steel:.0f} mm²/m")
                            st.write(f"• Provided Steel: {provided_steel:.0f} mm²/m")
                            
                            if provided_steel >= min_steel:
                                st.success("✅ Minimum steel satisfied")
                            else:
                                st.error("❌ Increase reinforcement")
                        
                        with verify_col2:
                            st.markdown("**Geometric Checks**")
                            
                            # Span to effective depth ratio
                            span_depth_ratio = flight_length / effective_depth
                            limiting_ratio = 26 if support_type == "Simply Supported" else 32
                            
                            st.write(f"• Span/Depth Ratio: {span_depth_ratio:.1f}")
                            st.write(f"• Limiting Ratio: {limiting_ratio}")
                            
                            if span_depth_ratio <= limiting_ratio:
                                st.success("✅ Deflection control OK")
                            else:
                                st.warning("⚠️ Check deflection")
                            
                            # Angle of inclination
                            angle = np.degrees(np.arctan(flight_height / flight_length))
                            st.write(f"• Angle of Inclination: {angle:.1f}°")
                            
                            if angle <= 40:
                                st.success("✅ Angle within limits")
                            else:
                                st.warning("⚠️ Steep staircase")

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
                        file_name=f"staircase_{flight_length}x{flight_height}_{num_risers}R.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_staircase_report(
                        flight_length, flight_height, slab_thickness, riser_height, tread_width,
                        num_risers, num_treads, concrete_grade, steel_grade,
                        main_bar_dia, main_bar_spacing, total_load, design_moment, support_type
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name="staircase_design_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_staircase_dxf(flight_length, flight_height, slab_thickness, riser_height, tread_width,
                        main_bar_dia, main_bar_spacing, dist_bar_dia, dist_bar_spacing,
                        step_bar_dia, clear_cover, num_risers, num_treads):
    """Create DXF drawing for staircase"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    # Section view of staircase
    # Draw the inclined slab
    slab_top_points = []
    slab_bottom_points = []
    
    current_x = 0
    current_y = 0
    
    # Create step profile
    for i in range(num_treads):
        # Top of step
        slab_top_points.append((current_x, current_y + slab_thickness))
        slab_top_points.append((current_x + tread_width, current_y + slab_thickness))
        
        # Bottom follows inclined slab
        slab_bottom_points.append((current_x, current_y))
        slab_bottom_points.append((current_x + tread_width, current_y))
        
        # Move to next step
        current_x += tread_width
        current_y += riser_height
    
    # Final riser
    slab_top_points.append((current_x, current_y + slab_thickness))
    slab_bottom_points.append((current_x, current_y))
    
    # Draw step outlines
    for i in range(num_treads):
        step_x = i * tread_width
        step_y = i * riser_height
        
        # Step outline
        step_points = [
            (step_x, step_y),
            (step_x + tread_width, step_y),
            (step_x + tread_width, step_y + riser_height),
            (step_x + tread_width, step_y + riser_height + slab_thickness),
            (step_x, step_y + slab_thickness),
            (step_x, step_y)
        ]
        msp.add_lwpolyline(step_points)
    
    # Draw reinforcement
    # Main reinforcement (parallel to inclined slab)
    num_main_bars = int(flight_length / main_bar_spacing) + 1
    
    for i in range(num_main_bars):
        x_pos = i * main_bar_spacing
        if x_pos <= flight_length:
            # Calculate y position on inclined slab
            y_start = (x_pos / flight_length) * flight_height + clear_cover + main_bar_dia/2
            y_end = y_start + slab_thickness - 2*clear_cover - main_bar_dia
            
            msp.add_line((x_pos, y_start), (x_pos, y_end))
    
    # Distribution bars (perpendicular to main bars)
    inclined_length = np.sqrt(flight_length**2 + flight_height**2)
    num_dist_bars = int(inclined_length / dist_bar_spacing) + 1
    
    angle = np.arctan(flight_height / flight_length)
    
    for i in range(num_dist_bars):
        dist_along_incline = i * dist_bar_spacing
        
        # Position along the inclined slab
        x_center = (dist_along_incline * np.cos(angle))
        y_center = (dist_along_incline * np.sin(angle)) + slab_thickness/2
        
        if x_center <= flight_length:
            # Draw short line representing distribution bar
            bar_length = 200  # Visual representation
            msp.add_line(
                (x_center - bar_length/2, y_center),
                (x_center + bar_length/2, y_center),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Plan view (offset below)
    plan_y_offset = -flight_height - 1000
    
    # Staircase plan
    plan_width = 1000  # Assumed width for plan
    
    # Overall plan outline
    msp.add_lwpolyline([
        (0, plan_y_offset),
        (flight_length, plan_y_offset),
        (flight_length, plan_y_offset + plan_width),
        (0, plan_y_offset + plan_width),
        (0, plan_y_offset)
    ])
    
    # Step divisions in plan
    for i in range(1, num_treads):
        x_pos = i * tread_width
        msp.add_line(
            (x_pos, plan_y_offset),
            (x_pos, plan_y_offset + plan_width),
            dxfattribs={'linetype': 'DASHED'}
        )
    
    # Reinforcement in plan
    # Main bars
    for i in range(0, int(plan_width / main_bar_spacing) + 1):
        y_pos = plan_y_offset + i * main_bar_spacing
        if y_pos <= plan_y_offset + plan_width:
            msp.add_line((0, y_pos), (flight_length, y_pos))
    
    # Distribution bars
    for i in range(0, int(flight_length / dist_bar_spacing) + 1):
        x_pos = i * dist_bar_spacing
        if x_pos <= flight_length:
            msp.add_line(
                (x_pos, plan_y_offset),
                (x_pos, plan_y_offset + plan_width),
                dxfattribs={'linetype': 'DASHED'}
            )
    
    # Add dimensions
    add_dimensions(msp, [
        ((0, -200), (flight_length, -200), (flight_length/2, -300), f"{flight_length}"),
        ((-200, 0), (-200, flight_height), (-300, flight_height/2), f"{flight_height}"),
        ((0, -100), (tread_width, -100), (tread_width/2, -150), f"{tread_width} TYP"),
        ((flight_length + 100, 0), (flight_length + 100, riser_height), (flight_length + 150, riser_height/2), f"{riser_height} TYP"),
        ((0, plan_y_offset - 100), (flight_length, plan_y_offset - 100), (flight_length/2, plan_y_offset - 150), f"{flight_length}"),
        ((-100, plan_y_offset), (-100, plan_y_offset + plan_width), (-150, plan_y_offset + plan_width/2), f"{plan_width}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"STAIRCASE SECTION\n{num_risers} RISERS x {riser_height}mm\n{num_treads} TREADS x {tread_width}mm\nSLAB THICKNESS: {slab_thickness}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, flight_height + 200))
    
    msp.add_text(
        f"REINFORCEMENT:\nMAIN: ⌀{main_bar_dia}mm @ {main_bar_spacing}mm C/C\nDIST: ⌀{dist_bar_dia}mm @ {dist_bar_spacing}mm C/C\nSTEP: ⌀{step_bar_dia}mm AT CORNERS",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((flight_length + 200, flight_height/2))
    
    msp.add_text(
        "STAIRCASE PLAN",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, plan_y_offset + plan_width + 100))
    
    return doc

def generate_staircase_report(flight_length, flight_height, slab_thickness, riser_height, tread_width,
                             num_risers, num_treads, concrete_grade, steel_grade,
                             main_bar_dia, main_bar_spacing, total_load, design_moment, support_type):
    """Generate staircase design report"""
    
    inclined_length = np.sqrt(flight_length**2 + flight_height**2)
    angle = np.degrees(np.arctan(flight_height / flight_length))
    main_steel_per_meter = (1000 / main_bar_spacing) * np.pi * (main_bar_dia/2)**2
    
    report = f"""
STAIRCASE DESIGN REPORT
=======================

GEOMETRY:
- Flight Length: {flight_length} mm
- Flight Height: {flight_height} mm
- Inclined Length: {inclined_length:.0f} mm
- Angle of Inclination: {angle:.1f}°
- Slab Thickness: {slab_thickness} mm

STEP DETAILS:
- Number of Risers: {num_risers}
- Number of Treads: {num_treads}
- Riser Height: {riser_height} mm
- Tread Width: {tread_width} mm
- Step Formula (2R+T): {2*riser_height + tread_width} mm

MATERIALS:
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

LOADING:
- Total Load: {total_load:.2f} kN/m²
- Design Moment: {design_moment:.2f} kNm/m
- Support Condition: {support_type}

REINFORCEMENT:
- Main Bars: ⌀{main_bar_dia}mm @ {main_bar_spacing}mm c/c
- Main Steel Area: {main_steel_per_meter:.0f} mm²/m

DESIGN VERIFICATION:
- Step proportions: {'OK' if 550 <= (2*riser_height + tread_width) <= 700 else 'CHECK'}
- Minimum steel: {'Satisfied' if main_steel_per_meter >= 0.12*slab_thickness*10 else 'CHECK'}
- Angle of inclination: {'OK' if angle <= 40 else 'STEEP'}

DESIGN NOTES:
1. Design based on IS 456:2000
2. Staircase treated as inclined slab
3. Step loads considered as triangular distribution
4. Deflection limits as per span/effective depth ratio
5. Minimum reinforcement 0.12% of gross area

CONSTRUCTION REQUIREMENTS:
1. Proper formwork for steps and slab
2. Adequate curing of concrete
3. Non-slip surface treatment required
4. Handrail attachment points to be provided
5. Proper drainage if external staircase

SAFETY CONSIDERATIONS:
1. Riser height should be uniform
2. Tread width should be uniform
3. Adequate lighting for safety
4. Non-slip finish essential
5. Handrails as per building code

Generated by RajLisp Structural Design Suite
"""
    return report
