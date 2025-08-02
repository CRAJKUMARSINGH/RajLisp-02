import streamlit as st
import os
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all page modules
try:
    from modules import (
        circular_column, rectangular_column, rect_column_footing, 
        circular_column_footing, sunshade, lintel, t_beam, l_beam,
        staircase, road_lsection, road_plan, road_cross_section,
        pmgsy_road, bridge
    )
except ImportError as e:
    st.error(f"Error importing modules: {str(e)}")
    st.error("Please make sure all module files exist in the modules/ directory.")
    st.stop()

def main():
    st.set_page_config(
        page_title="🏗️ RajLisp - Structural Design Suite",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for engineering theme
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .module-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1e3c72;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="main-header"><h2>🏗️ RajLisp Suite</h2><p>Structural Design & CAD</p></div>', unsafe_allow_html=True)
        
        st.markdown("### 📋 Navigation")
        
        # Group modules by category
        structural_modules = [
            "🏠 Home",
            "🔘 Circular Column", 
            "⬜ Rectangular Column",
            "🔘🦶 Circular Column + Footing",
            "⬜🦶 Rectangular Column + Footing"
        ]
        
        beam_modules = [
            "🌞 Sunshade",
            "🔗 Lintel", 
            "📐 T-Beam",
            "📏 L-Beam"
        ]
        
        misc_modules = [
            "🪜 Staircase",
            "🌉 Bridge"
        ]
        
        road_modules = [
            "🛣️ Road L-Section",
            "🗺️ Road Plan", 
            "✂️ Road Cross Section",
            "🛤️ PMGSY Road"
        ]
        
        # Create expandable sections
        with st.expander("🏗️ Structural Elements", expanded=True):
            page = st.radio("", structural_modules, key="structural")
            
        with st.expander("📏 Beams & Elements", expanded=False):
            beam_page = st.radio("", beam_modules, key="beams")
            if beam_page != beam_modules[0]:  # If not default selection
                page = beam_page
                
        with st.expander("🏘️ Other Structures", expanded=False):
            misc_page = st.radio("", misc_modules, key="misc")
            if misc_page != misc_modules[0]:  # If not default selection
                page = misc_page
                
        with st.expander("🛣️ Road Design", expanded=False):
            road_page = st.radio("", road_modules, key="roads")
            if road_page != road_modules[0]:  # If not default selection
                page = road_page

        # About section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **RajLisp Structural Design Suite**
        
        Professional CAD tools for:
        - Structural Design
        - Road Engineering  
        - Bridge Design
        - DXF Generation
        
        *Modernized from RajLisp*
        """)

    # Page routing with enhanced UI
    if page == "🏠 Home" or not 'page' in locals():
        show_home_page()
    elif page == "🔘 Circular Column":
        circular_column.page_circular_column()
    elif page == "⬜ Rectangular Column":
        rectangular_column.page_rectangular_column()
    elif page == "🔘🦶 Circular Column + Footing":
        circular_column_footing.page_circular_column_footing()
    elif page == "⬜🦶 Rectangular Column + Footing":
        rect_column_footing.page_rect_column_footing()
    elif page == "🌞 Sunshade":
        sunshade.page_sunshade()
    elif page == "🔗 Lintel":
        lintel.page_lintel()
    elif page == "📐 T-Beam":
        t_beam.page_t_beam()
    elif page == "📏 L-Beam":
        l_beam.page_l_beam()
    elif page == "🪜 Staircase":
        staircase.page_staircase()

    elif page == "🛣️ Road L-Section":
        road_lsection.page_road_lsection()
    elif page == "🗺️ Road Plan":
        road_plan.page_road_plan()
    elif page == "✂️ Road Cross Section":
        road_cross_section.page_road_cross_section()
    elif page == "🛤️ PMGSY Road":
        pmgsy_road.page_pmgsy_road()

def show_home_page():
    st.markdown('<div class="main-header"><h1>🏗️ RajLisp Structural Design Suite</h1><p>Professional CAD Tools for Civil Engineers</p></div>', unsafe_allow_html=True)
    
    # Stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>14</h3><p>Design Modules</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>DXF</h3><p>CAD Export</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>IS</h3><p>Code Compliant</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Real-time</h3><p>Calculations</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Module categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("🏗️ Structural Elements")
        st.markdown("""
        - **Circular Column** - Round column design with reinforcement
        - **Rectangular Column** - Rectangular column design 
        - **Column with Footing** - Combined column-footing design
        - **Sunshade** - Cantilever sunshade design
        - **Lintel** - Door/window lintel design
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("📏 Beam Design")  
        st.markdown("""
        - **T-Beam** - T-shaped beam design
        - **L-Beam** - L-shaped beam design
        - **Advanced reinforcement** - Detailed bar placement
        - **Load calculations** - Moment and shear analysis
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("🛣️ Road Engineering")
        st.markdown("""
        - **Road L-Section** - Longitudinal section design
        - **Road Plan** - Plan view layout  
        - **Road Cross Section** - Cross-sectional design
        - **PMGSY Road** - Rural road design standards
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="module-card">', unsafe_allow_html=True)
        st.subheader("🏘️ Other Structures")
        st.markdown("""
        - **Staircase** - Stair design and detailing
        - **Bridge** - Bridge structural design
        - **Advanced features** - Load analysis & optimization
        - **Professional reports** - Detailed documentation
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Features highlight
    st.subheader("✨ Key Features")
    
    feature_cols = st.columns(3)
    
    with feature_cols[0]:
        st.markdown("""
        **🎯 Professional Design**
        - IS Code compliant designs
        - Structural calculations
        - Load analysis
        - Safety factor validation
        """)
        
    with feature_cols[1]:
        st.markdown("""
        **📐 CAD Integration**  
        - DXF file generation
        - AutoCAD compatible
        - Detailed drawings
        - Dimensioning & notes
        """)
        
    with feature_cols[2]:
        st.markdown("""
        **🖥️ Modern Interface**
        - Responsive design
        - Real-time preview
        - Input validation
        - Professional reports
        """)

    st.markdown("---")
    st.info("💡 **Getting Started:** Select a design module from the sidebar to begin creating your structural drawings!")

if __name__ == "__main__":
    main()
