/* Moving title animation */
@keyframes moveTitle {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.moving-title {
    color: red;
    font-size: 3.5em;
    font-weight: bold;
    white-space: nowrap;
    animation: moveTitle 15s linear infinite;
    margin-bottom: 40px;
}

/* Flip Card Styles */
.flip-card {
    background-color: transparent;
    width: 300px;
    height: 200px;
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
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.flip-card-front {
    background: linear-gradient(45deg, #2193b0, #6dd5ed);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
}

.flip-card-back {
    background: linear-gradient(45deg, #834d9b, #d04ed6);
    color: white;
    transform: rotateY(180deg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.tab-button {
    background-color: white;
    color: #834d9b;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    margin-top: 15px;
    transition: all 0.3s ease;
}

.tab-button:hover {
    background-color: #834d9b;
    color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
    .flip-card {
        width: 250px;
        height: 180px;
    }
    .moving-title {
        font-size: 2.5em;
    }
}
