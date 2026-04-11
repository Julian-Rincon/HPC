# Taller 4: TSP Distribuido con Docker Swarm

Solución cliente-servidor para el problema del viajante, desplegable como servicio replicado con Docker Swarm.

## Contenido

- `tsp_solution/server/app.py`: API Flask para calcular distancias
- `tsp_solution/server/Dockerfile`: imagen del servicio
- `tsp_solution/client/client.py`: cliente que prueba rutas por fuerza bruta
- `tsp_solution/tests/`: pruebas unitarias

## Requisitos

- Docker Desktop con Swarm habilitado
- Python 3.9+
- `pip`

## Instalación

### Dependencias del cliente

```bash
python -m pip install -r taller-4-tsp-distribuido/tsp_solution/client/requirements.txt
```

### Construcción del servidor

```bash
docker build -t travel-calculator:1.0 ./taller-4-tsp-distribuido/tsp_solution/server
```

## Despliegue

```bash
docker swarm init
docker service create --name calculator --replicas 4 -p 5000:5000 travel-calculator:1.0
```

## Ejecución del cliente

```bash
python taller-4-tsp-distribuido/tsp_solution/client/client.py
```

## Pruebas

```bash
python -m unittest discover -s taller-4-tsp-distribuido/tsp_solution/tests
```

## Resumen

- El servidor expone `POST /calculate_distance`.
- El cliente genera permutaciones y distribuye peticiones concurrentes.
- Docker Swarm permite balancear la carga entre varias réplicas.
