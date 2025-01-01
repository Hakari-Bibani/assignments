styles = """
<style>
/* Moving title animation */
@keyframes moveTitle {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.title-container {
    overflow: hidden;
    width: 100%;
    margin: 20px 0;
}

.moving-title {
    color: red;
    font-size: 3.5em;
    animation: moveTitle 10s linear infinite;
    white-space: nowrap;
    display: inline-block;
}

/* Flip card styles */
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
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.flip-card-front {
    background-color: #2196F3;
    color: white;
}

.flip-card-back {
    background-color: #4CAF50;
    color: white;
    transform: rotateY(180deg);
}

button {
    padding: 10px 20px;
    margin-top: 10px;
    background-color: #ffffff;
    color: #4CAF50;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #e0e0e0;
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}
</style>
"""
