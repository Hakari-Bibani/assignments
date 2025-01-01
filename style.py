styles = """
/* Moving title animation */
@keyframes moveTitle {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.moving-title {
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 2rem;
}

.moving-title h1 {
    display: inline-block;
    animation: moveTitle 15s linear infinite;
    font-size: 3.5rem;
    color: #2E86C1;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

/* Flip card styles */
.flip-card {
    background-color: transparent;
    width: 100%;
    height: 200px;
    perspective: 1000px;
    margin-bottom: 1rem;
    cursor: pointer;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
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
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.flip-card-front {
    background: linear-gradient(45deg, #2E86C1, #3498DB);
    color: white;
}

.flip-card-back {
    background: linear-gradient(45deg, #2ECC71, #27AE60);
    color: white;
    transform: rotateY(180deg);
}

.flip-card h2 {
    margin: 0;
    font-size: 1.5rem;
}

.flip-card p {
    margin: 0;
    font-size: 1rem;
}
"""
