import streamlit as st
import numpy as np
import ezdxf
import tempfile
from utils.dxf_utils import create_dxf_header, add_dimensions
from utils.calculations import calculate_beam_moment, calculate_shear_reinforcement

def page_lintel():
    st.title("🔗 Lintel Designer")
    st.markdown("Design reinforced concrete lintels for doors and windows")

    with st.form("lintel_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📐 Lintel Dimensions")
            span = st.number_input("Clear Span (mm)", min_value=600, max_value=6000, value=1200, step=100,
                                 help="Clear span between supports")
            width = st.number_input("Width (mm)", min_value=150, max_value=500, value=230, step=10,
                                  help="Width of lintel (usually wall thickness)")
            depth = st.number_input("Depth (mm)", min_value=150, max_value=600, value=230, step=10,
                                  help="Overall depth of lintel")
            bearing_length = st.number_input("Bearing Length (mm)", min_value=150, max_value=500, value=200, step=25,
                                           help="Bearing length at each support")

        with col2:
            st.subheader("🔩 Reinforcement")
            main_bar_dia = st.selectbox("Main Bar Diameter (mm)", [10, 12, 16, 20, 25], index=2,
                                      help="Diameter of main tension reinforcement")
            num_main_bars = st.slider("Number of Main Bars", min_value=2, max_value=6, value=3, step=1,
                                    help="Number of main bars at bottom")
            top_bar_dia = st.selectbox("Top Bar Diameter (mm)", [8, 10, 12, 16], index=1,
                                     help="Diameter of compression bars")
            num_top_bars = st.slider("Number of Top Bars", min_value=2, max_value=4, value=2, step=1,
                                   help="Number of hanger bars at top")
            stirrup_dia = st.selectbox("Stirrup Diameter (mm)", [6, 8, 10], index=1,
                                     help="Diameter of stirrups")
            stirrup_spacing = st.number_input("Stirrup Spacing (mm)", min_value=75, max_value=300, value=150, step=25,
                                            help="Center to center spacing of stirrups")

        with col3:
            st.subheader("🏗️ Loading & Materials")
            concrete_grade = st.selectbox("Concrete Grade", ["M20", "M25", "M30"], index=1)
            steel_grade = st.selectbox("Steel Grade", ["Fe415", "Fe500"], index=1)
            clear_cover = st.number_input("Clear Cover (mm)", min_value=15, max_value=40, value=25, step=5,
                                        help="Clear cover to reinforcement")
            
            st.markdown("**Loading**")
            wall_load = st.number_input("Wall Load (kN/m)", min_value=0, max_value=50, value=10, step=1,
                                      help="Load from wall above lintel")
            floor_load = st.number_input("Floor Load (kN/m)", min_value=0, max_value=30, value=5, step=1,
                                       help="Load from floor/slab above")
            live_load = st.number_input("Live Load (kN/m)", min_value=0, max_value=20, value=3, step=1,
                                      help="Live load transmitted to lintel")

        submitted = st.form_submit_button("🔄 Design Lintel", type="primary")

    if submitted:
        with st.spinner("🔄 Designing lintel..."):
            try:
                # Calculate design parameters
                total_load = wall_load + floor_load + live_load
                design_moment = total_load * (span/1000)**2 / 8  # kNm for simply supported beam
                design_shear = total_load * (span/1000) / 2  # kN
                
                # Perform design calculations
                results = calculate_beam_moment(depth, width, concrete_grade, steel_grade, 
                                              main_bar_dia, num_main_bars, design_moment)
                
                shear_results = calculate_shear_reinforcement(depth, width, concrete_grade, 
                                                            stirrup_dia, stirrup_spacing, design_shear)

                # Create DXF drawing
                doc = create_lintel_dxf(span, width, depth, bearing_length, main_bar_dia, 
                                      num_main_bars, top_bar_dia, num_top_bars, 
                                      stirrup_dia, stirrup_spacing, clear_cover)

                # Display results
                col_results, col_download = st.columns([2, 1])

                with col_results:
                    st.success("✅ Lintel design completed successfully!")
                    
                    # Design summary
                    with st.expander("📋 Design Summary", expanded=True):
                        summary_col1, summary_col2 = st.columns(2)
                        
                        with summary_col1:
                            st.markdown("**Lintel Dimensions**")
                            st.write(f"• Clear Span: {span} mm")
                            st.write(f"• Width: {width} mm")
                            st.write(f"• Depth: {depth} mm")
                            st.write(f"• Effective Depth: {depth - clear_cover - stirrup_dia - main_bar_dia/2:.0f} mm")
                            st.write(f"• Bearing Length: {bearing_length} mm each end")
                            
                        with summary_col2:
                            st.markdown("**Reinforcement Details**")
                            st.write(f"• Main Bars: {num_main_bars}-⌀{main_bar_dia}mm")
                            
                            main_steel_area = num_main_bars * np.pi * (main_bar_dia/2)**2
                            st.write(f"• Main Steel Area: {main_steel_area:.0f} mm²")
                            
                            steel_percentage = (main_steel_area / (width * depth)) * 100
                            st.write(f"• Steel %: {steel_percentage:.2f}%")
                            
                            st.write(f"• Top Bars: {num_top_bars}-⌀{top_bar_dia}mm")
                            st.write(f"• Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm c/c")

                    # Loading and analysis
                    with st.expander("📊 Load Analysis", expanded=True):
                        load_col1, load_col2 = st.columns(2)
                        
                        with load_col1:
                            st.markdown("**Applied Loads**")
                            st.write(f"• Wall Load: {wall_load} kN/m")
                            st.write(f"• Floor Load: {floor_load} kN/m")
                            st.write(f"• Live Load: {live_load} kN/m")
                            st.write(f"• **Total Load: {total_load} kN/m**")
                            
                        with load_col2:
                            st.markdown("**Design Forces**")
                            st.write(f"• Design Moment: {design_moment:.2f} kNm")
                            st.write(f"• Design Shear: {design_shear:.1f} kN")
                            
                            # Self weight check
                            self_weight = 25 * width * depth * 1e-6  # kN/m
                            st.write(f"• Self Weight: {self_weight:.1f} kN/m")
                            total_with_self = total_load + self_weight
                            st.write(f"• Total with Self Weight: {total_with_self:.1f} kN/m")

                    # Design verification
                    if results and shear_results:
                        with st.expander("🔍 Design Verification", expanded=True):
                            verify_col1, verify_col2 = st.columns(2)
                            
                            with verify_col1:
                                st.markdown("**Moment Capacity**")
                                moment_capacity = results.get('moment_capacity', 0)
                                moment_ratio = design_moment / moment_capacity if moment_capacity > 0 else 1
                                
                                st.write(f"• Moment Capacity: {moment_capacity:.2f} kNm")
                                st.write(f"• Applied Moment: {design_moment:.2f} kNm")
                                
                                if moment_ratio <= 1.0:
                                    st.success(f"✅ Moment OK - Ratio: {moment_ratio:.2f}")
                                else:
                                    st.error(f"❌ Moment Inadequate - Ratio: {moment_ratio:.2f}")
                            
                            with verify_col2:
                                st.markdown("**Shear Capacity**")
                                shear_capacity = shear_results.get('shear_capacity', 0)
                                shear_ratio = design_shear / shear_capacity if shear_capacity > 0 else 1
                                
                                st.write(f"• Shear Capacity: {shear_capacity:.1f} kN")
                                st.write(f"• Applied Shear: {design_shear:.1f} kN")
                                
                                if shear_ratio <= 1.0:
                                    st.success(f"✅ Shear OK - Ratio: {shear_ratio:.2f}")
                                else:
                                    st.error(f"❌ Shear Inadequate - Ratio: {shear_ratio:.2f}")

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
                        file_name=f"lintel_{span}x{width}x{depth}.dxf",
                        mime="application/dxf"
                    )
                    
                    # Generate report
                    report = generate_lintel_report(
                        span, width, depth, bearing_length, concrete_grade, steel_grade,
                        main_bar_dia, num_main_bars, total_load, design_moment, design_shear, results
                    )
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"lintel_design_report.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")

def create_lintel_dxf(span, width, depth, bearing_length, main_bar_dia, num_main_bars, 
                     top_bar_dia, num_top_bars, stirrup_dia, stirrup_spacing, clear_cover):
    """Create DXF drawing for lintel"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Drawing setup
    doc.header['$INSUNITS'] = 4  # Millimeters
    
    total_length = span + 2 * bearing_length
    
    # Elevation view
    lintel_outline = [
        (0, 0),
        (total_length, 0),
        (total_length, depth),
        (0, depth),
        (0, 0)
    ]
    msp.add_lwpolyline(lintel_outline)
    
    # Support bearings
    msp.add_lwpolyline([
        (0, -50),
        (bearing_length, -50),
        (bearing_length, 0),
        (0, 0),
        (0, -50)
    ], dxfattribs={'linetype': 'DASHED'})
    
    msp.add_lwpolyline([
        (total_length - bearing_length, -50),
        (total_length, -50),
        (total_length, 0),
        (total_length - bearing_length, 0),
        (total_length - bearing_length, -50)
    ], dxfattribs={'linetype': 'DASHED'})
    
    # Main reinforcement
    effective_depth = depth - clear_cover - stirrup_dia - main_bar_dia/2
    main_y = clear_cover + stirrup_dia + main_bar_dia/2
    
    for i in range(num_main_bars):
        spacing = (width - 2*clear_cover - 2*stirrup_dia - num_main_bars*main_bar_dia) / (num_main_bars - 1) if num_main_bars > 1 else 0
        x_offset = clear_cover + stirrup_dia + main_bar_dia/2 + i * (spacing + main_bar_dia)
        
        # Main bar representation (extend into bearings)
        msp.add_line(
            (bearing_length/2, main_y),
            (total_length - bearing_length/2, main_y)
        )
    
    # Top bars
    top_y = depth - clear_cover - stirrup_dia - top_bar_dia/2
    for i in range(num_top_bars):
        msp.add_line(
            (bearing_length, top_y),
            (total_length - bearing_length, top_y),
            dxfattribs={'linetype': 'DASHED'}
        )
    
    # Stirrups
    num_stirrups = int(span / stirrup_spacing) + 1
    for i in range(num_stirrups):
        x_pos = bearing_length + i * stirrup_spacing
        if x_pos <= total_length - bearing_length:
            msp.add_lwpolyline([
                (x_pos, clear_cover + stirrup_dia/2),
                (x_pos, depth - clear_cover - stirrup_dia/2)
            ], dxfattribs={'linetype': 'DASHED'})
    
    # Cross-section view (offset below)
    section_y_offset = -depth - 200
    
    # Lintel cross-section
    msp.add_lwpolyline([
        (0, section_y_offset),
        (width, section_y_offset),
        (width, section_y_offset + depth),
        (0, section_y_offset + depth),
        (0, section_y_offset)
    ])
    
    # Reinforcement in cross-section
    bar_spacing = (width - 2*clear_cover - 2*stirrup_dia - num_main_bars*main_bar_dia) / (num_main_bars - 1) if num_main_bars > 1 else 0
    
    for i in range(num_main_bars):
        x_pos = clear_cover + stirrup_dia + main_bar_dia/2 + i * (bar_spacing + main_bar_dia)
        msp.add_circle(center=(x_pos, section_y_offset + main_y), radius=main_bar_dia/2)
    
    for i in range(num_top_bars):
        top_spacing = (width - 2*clear_cover - 2*stirrup_dia - num_top_bars*top_bar_dia) / (num_top_bars - 1) if num_top_bars > 1 else 0
        x_pos = clear_cover + stirrup_dia + top_bar_dia/2 + i * (top_spacing + top_bar_dia)
        msp.add_circle(center=(x_pos, section_y_offset + top_y), radius=top_bar_dia/2)
    
    # Stirrup outline
    stirrup_outline = [
        (clear_cover + stirrup_dia/2, section_y_offset + clear_cover + stirrup_dia/2),
        (width - clear_cover - stirrup_dia/2, section_y_offset + clear_cover + stirrup_dia/2),
        (width - clear_cover - stirrup_dia/2, section_y_offset + depth - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, section_y_offset + depth - clear_cover - stirrup_dia/2),
        (clear_cover + stirrup_dia/2, section_y_offset + clear_cover + stirrup_dia/2)
    ]
    msp.add_lwpolyline(stirrup_outline, dxfattribs={'linetype': 'DASHED'})
    
    # Add dimensions
    add_dimensions(msp, [
        ((0, -100), (total_length, -100), (total_length/2, -150), f"{total_length}"),
        ((bearing_length, -75), (total_length - bearing_length, -75), (total_length/2, -125), f"{span} CLEAR"),
        ((-100, 0), (-100, depth), (-150, depth/2), f"{depth}"),
        ((-50, section_y_offset), (-50, section_y_offset + depth), (-100, section_y_offset + depth/2), f"{depth}"),
        ((0, section_y_offset - 50), (width, section_y_offset - 50), (width/2, section_y_offset - 100), f"{width}")
    ])
    
    # Add text annotations
    msp.add_text(
        f"LINTEL BEAM\n{span}mm CLEAR SPAN\n{width}mm x {depth}mm",
        dxfattribs={'height': 50, 'style': 'STANDARD'}
    ).set_placement((0, depth + 100))
    
    msp.add_text(
        f"REINFORCEMENT:\nMAIN: {num_main_bars}-⌀{main_bar_dia}mm\nTOP: {num_top_bars}-⌀{top_bar_dia}mm\nSTIRRUPS: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm C/C",
        dxfattribs={'height': 30, 'style': 'STANDARD'}
    ).set_placement((total_length + 100, depth/2))
    
    return doc

def generate_lintel_report(span, width, depth, bearing_length, concrete_grade, steel_grade,
                          main_bar_dia, num_main_bars, total_load, design_moment, design_shear, results):
    """Generate lintel design report"""
    
    main_steel_area = num_main_bars * np.pi * (main_bar_dia/2)**2
    steel_percentage = (main_steel_area / (width * depth)) * 100
    
    report = f"""
LINTEL BEAM DESIGN REPORT
=========================

GEOMETRY:
- Clear Span: {span} mm
- Width: {width} mm
- Depth: {depth} mm
- Bearing Length: {bearing_length} mm each end
- Total Length: {span + 2*bearing_length} mm

MATERIALS:
- Concrete Grade: {concrete_grade}
- Steel Grade: {steel_grade}

LOADING:
- Total Applied Load: {total_load} kN/m
- Design Moment: {design_moment:.2f} kNm
- Design Shear: {design_shear:.1f} kN

REINFORCEMENT:
- Main Bars: {num_main_bars} - ⌀{main_bar_dia}mm
- Main Steel Area: {main_steel_area:.0f} mm²
- Steel Percentage: {steel_percentage:.2f}%

DESIGN VERIFICATION:
- Moment Capacity: {results.get('moment_capacity', 0):.2f} kNm
- Applied/Capacity Ratio: {design_moment/results.get('moment_capacity', 1):.2f}
- Design Status: {'SAFE' if design_moment <= results.get('moment_capacity', 0) else 'REVIEW REQUIRED'}

DESIGN NOTES:
1. Design based on IS 456:2000
2. Simply supported beam analysis
3. Adequate bearing length provided
4. Minimum reinforcement requirements satisfied
5. Deflection check may be required for spans > 6m

CONSTRUCTION NOTES:
1. Provide adequate curing for concrete
2. Maintain specified cover to reinforcement
3. Ensure proper anchorage at supports
4. Check for any openings or services

Generated by RajLisp Structural Design Suite
"""
    return report
