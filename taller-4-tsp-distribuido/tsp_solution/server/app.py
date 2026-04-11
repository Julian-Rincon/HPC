import math
from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_euclidean_distance(p1, p2):
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    data = request.get_json()
    
    if not data or 'cities' not in data:
        return jsonify({'error': 'Invalid input, "cities" list is required'}), 400
    
    cities = data['cities']
    if len(cities) < 2:
        return jsonify({'total_distance': 0.0})
    
    total_distance = 0.0
    for i in range(len(cities) - 1):
        total_distance += calculate_euclidean_distance(cities[i], cities[i+1])
        
    return jsonify({'total_distance': total_distance})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
