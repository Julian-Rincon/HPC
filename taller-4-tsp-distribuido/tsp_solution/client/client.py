import itertools
import requests
import concurrent.futures
import time
import sys

# Configuración
API_URL = "http://localhost:5000/calculate_distance"
# Si se ejecuta dentro de Docker o en otra máquina, ajustar la URL.
# Para Docker Swarm local expuesto en puerto 5000, localhost está bien.

# Definición de ciudades (Ejemplo)
CITIES = [
    {"name": "A", "x": 0, "y": 0},
    {"name": "B", "x": 10, "y": 0},
    {"name": "C", "x": 10, "y": 10},
    {"name": "D", "x": 0, "y": 10},
    {"name": "E", "x": 5, "y": 5}
]

def calculate_route_distance(route):
    """Envía una ruta a la API para calcular su distancia."""
    payload = {"cities": route}
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()['total_distance']
        else:
            print(f"Error en API: {response.status_code} - {response.text}")
            return float('inf')
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return float('inf')

def solve_tsp_brute_force(cities):
    """Encuentra la ruta más corta probando todas las permutaciones."""
    shortest_distance = float('inf')
    best_route = None
    
    # Generar todas las permutaciones
    # Fijamos la primera ciudad para reducir el espacio de búsqueda (opcional en TSP simétrico, 
    # pero el enunciado pide fuerza bruta sobre permutaciones).
    # Si el enunciado pide TODAS las permutaciones sin fijar inicio, usamos itertools.permutations(cities)
    # Asumiremos permutaciones completas para cumplir estrictamente "all permutations".
    permutations = list(itertools.permutations(cities))
    
    print(f"Evaluando {len(permutations)} rutas posibles...")
    
    start_time = time.time()
    
    # Ejecución paralela para aprovechar el cluster
    # Ajustar max_workers según la capacidad de la máquina cliente
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Mapeamos cada permutación a la función de cálculo
        future_to_route = {executor.submit(calculate_route_distance, route): route for route in permutations}
        
        for future in concurrent.futures.as_completed(future_to_route):
            route = future_to_route[future]
            try:
                distance = future.result()
                if distance < shortest_distance:
                    shortest_distance = distance
                    best_route = route
            except Exception as exc:
                print(f'La ruta generó una excepción: {exc}')

    end_time = time.time()
    duration = end_time - start_time
    
    return best_route, shortest_distance, duration

if __name__ == "__main__":
    print("Iniciando cliente TSP...")
    print(f"Ciudades: {[c['name'] for c in CITIES]}")
    
    try:
        best_route, distance, duration = solve_tsp_brute_force(CITIES)
        
        if best_route:
            route_names = [city['name'] for city in best_route]
            print("\nResultados:")
            print(f"Mejor ruta encontrada: {' -> '.join(route_names)}")
            print(f"Distancia total: {distance:.2f}")
            print(f"Tiempo de ejecución: {duration:.4f} segundos")
        else:
            print("No se encontró una ruta válida.")
            
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
