def apply_custom_style():
    return """
        <style>
        @keyframes title-animation {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(0); }
        }
        
        .main-title {
            color: red;
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            animation: title-animation 1.5s ease-out;
        }
        
        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding: 20px;
        }
        
        .section-title {
            width: 100%;
            color: #2c3e50;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-left: 20px;
        }
        
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            transition: background-color 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #45a049;
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 15px;
            margin: 10px;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        </style>
    """
