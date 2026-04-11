import unittest
import json
import sys
import os

# Agregar el directorio padre al path para importar el servidor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import app

class TestTSPServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calculate_distance_basic(self):
        # Triángulo rectángulo 3-4-5
        cities = [
            {"name": "A", "x": 0, "y": 0},
            {"name": "B", "x": 3, "y": 0}, # Distancia 3
            {"name": "C", "x": 3, "y": 4}  # Distancia 4
        ]
        # Ruta A->B->C. Distancia total = 3 + 4 = 7
        response = self.app.post('/calculate_distance', 
                                 data=json.dumps({'cities': cities}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_distance'], 7.0)

    def test_calculate_distance_empty(self):
        response = self.app.post('/calculate_distance', 
                                 data=json.dumps({'cities': []}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['total_distance'], 0.0)

    def test_calculate_distance_single_city(self):
        cities = [{"name": "A", "x": 0, "y": 0}]
        response = self.app.post('/calculate_distance', 
                                 data=json.dumps({'cities': cities}),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['total_distance'], 0.0)

    def test_invalid_input(self):
        response = self.app.post('/calculate_distance', 
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
