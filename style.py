def load_css():
    return st.markdown("""
        <style>
        /* Animated title */
        .animated-title {
            text-align: center;
            animation: moveTitle 2s infinite alternate;
        }
        
        .animated-title h1 {
            color: red;
            font-size: 4rem;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        @keyframes moveTitle {
            from {transform: translateY(0px);}
            to {transform: translateY(10px);}
        }
        
        /* Flip Cards */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 200px;
            perspective: 1000px;
            margin: 20px 0;
        }
        
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
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
            flex-direction: column;
            padding: 20px;
            border-radius: 10px;
        }
        
        .flip-card-front {
            background-color: #2e7d32;
            color: white;
        }
        
        .flip-card-back {
            background-color: #1565c0;
            color: white;
            transform: rotateY(180deg);
        }
        </style>
    """, unsafe_allow_html=True)
