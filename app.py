import streamlit as st

def get_animated_title():
    return '''
    <style>
        @keyframes slide {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .sliding-text {
            color: red;
            font-size: 3em;
            font-weight: bold;
            white-space: nowrap;
            animation: slide 15s linear infinite;
            position: relative;
            overflow: hidden;
        }
    </style>
    <div style="overflow: hidden;">
        <div class="sliding-text">Welcome to ImpactHub</div>
    </div>
    '''

def apply_styles():
    st.markdown('''
        <style>
            .flip-card {
                background-color: transparent;
                width: 300px;
                height: 200px;
                perspective: 1000px;
                margin: 20px;
            }
            
            .flip-card-inner {
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.8s;
                transform-style: preserve-3d;
                cursor: pointer;
            }
            
            .flip-card:hover .flip-card-inner {
                transform: rotateY(180deg);
            }
            
            .flip-card-front, .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
            }
            
            .flip-card-front {
                background-color: #2c3e50;
                color: white;
            }
            
            .flip-card-back {
                background-color: #3498db;
                color: white;
                transform: rotateY(180deg);
                padding: 20px;
            }
            
            .stButton button {
                width: 100%;
                margin-top: 10px;
            }
        </style>
    ''', unsafe_allow_html=True)
