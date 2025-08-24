import streamlit as st
import os
import sys

# Optional Sentry error tracking
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk
        sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.0)
    except Exception:
        pass

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all page modules (best-effort; not required for native multipage)
try:
    from modules import (
        circular_column, rectangular_column, rect_column_footing, 
        circular_column_footing, sunshade, lintel, t_beam, l_beam,
        staircase, road_lsection, road_plan, road_cross_section,
        pmgsy_road
    )
except ImportError:
    # Native pages don't need these imports at top-level
    pass

def main():
    st.set_page_config(
        page_title="🏗️ RajLisp - Structural Design Suite",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    show_home_page()


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
        - **Circular Column** - Round column design with reinforcement (see sidebar pages)
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
    st.info("💡 Select a page from the sidebar navigation to begin.")

if __name__ == "__main__":
    main()
