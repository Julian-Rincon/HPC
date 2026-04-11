import unittest
import sys
import os
from unittest.mock import patch

# Agregar el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client.client import solve_tsp_brute_force

class TestTSPClient(unittest.TestCase):
    
    @patch('client.client.calculate_route_distance')
    def test_solve_tsp_brute_force(self, mock_calculate):
        # Mockear la respuesta de la API para evitar llamadas reales
        # Simulamos 3 ciudades: A, B, C
        # Permutaciones: ABC, ACB, BAC, BCA, CAB, CBA
        
        cities = [
            {"name": "A", "x": 0, "y": 0},
            {"name": "B", "x": 1, "y": 0},
            {"name": "C", "x": 2, "y": 0}
        ]
        
        # Definir distancias para cada ruta (tupla de nombres como clave simplificada)
        # La ruta real es una lista de dicts, pero el mock recibirá eso.
        # Haremos que el mock devuelva valores basados en el orden.
        
        def side_effect(route):
            names = "".join([c['name'] for c in route])
            if names == "ABC": return 2.0 # 0->1->2 (Distancia 1+1=2)
            if names == "CBA": return 2.0
            return 10.0 # Otras rutas son más largas para probar la lógica
            
        mock_calculate.side_effect = side_effect
        
        best_route, distance, duration = solve_tsp_brute_force(cities)
        
        best_route_names = "".join([c['name'] for c in best_route])
        
        # Debería encontrar ABC o CBA (ambas tienen distancia 2.0)
        self.assertIn(best_route_names, ["ABC", "CBA"])
        self.assertEqual(distance, 2.0)

if __name__ == '__main__':
    unittest.main()
