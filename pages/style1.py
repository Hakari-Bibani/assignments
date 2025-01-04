import streamlit as st
from streamlit_folium import st_folium

def style_output(output):
    if output:
        st.markdown(f"""
        <div style='font-family: monospace; padding: 10px; 
                    background-color: #f8f9fa; border-left: 3px solid #2196F3;'>
        {output}
        </div>
        """, unsafe_allow_html=True)

def display_error(error):
    st.markdown(f"""
    <div style='color: red; font-family: monospace; padding: 10px; 
                background-color: #f8f9fa; border-left: 3px solid red;'>
    {error}
    </div>
    """, unsafe_allow_html=True)

def display_map_and_distances():
    if st.session_state.map_obj:
        st_folium(st.session_state.map_obj, width=800, height=500)
        if st.session_state.distances:
            st.markdown("### 📏 Distance Report")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Points 1-2", f"{st.session_state.distances['Distance 1-2']} km")
            with col2:
                st.metric("Points 2-3", f"{st.session_state.distances['Distance 2-3']} km")
            with col3:
                st.metric("Points 1-3", f"{st.session_state.distances['Distance 1-3']} km")
