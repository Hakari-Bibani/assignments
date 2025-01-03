import streamlit as st

def apply_style():
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes slideInFromLeft {
            0% {
                transform: translateX(-100%);
                opacity: 0;
            }
            100% {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .animated-title h1 {
            color: #FF0000;
            font-size: 4rem;
            text-align: center;
            animation: slideInFromLeft 1.5s ease-out;
            margin-bottom: 2rem;
        }
        
        /* Flip Card Styles */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 180px;
            perspective: 1000px;
            margin: 20px auto;
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
            font-size: 1.2rem;
            border-radius: 10px;
        }

        .flip-card-front {
            background: linear-gradient(45deg, #6c5ce7, #a8a4e6);
            color: white;
        }

        .flip-card-back {
            background: linear-gradient(45deg, #a8a4e6, #6c5ce7);
            color: white;
            transform: rotateY(180deg);
        }
        
        /* Custom headers */
        h2 {
            color: #333;
            text-align: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def get_flip_card_html(title, content, link):
    return f"""
    <div class="flip-card" onclick="window.location.href='{link}'">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <h3>{title}</h3>
            </div>
            <div class="flip-card-back">
                <p>{content}</p>
            </div>
        </div>
    </div>
    """
