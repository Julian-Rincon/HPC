# Solución TSP Distribuida con Docker Swarm

Este proyecto implementa una solución distribuida para el Problema del Viajante (TSP) utilizando una API Flask containerizada y un cliente Python que realiza búsquedas de fuerza bruta.

## Requisitos
- Docker Desktop (con Swarm habilitado o listo para iniciar)
- Python 3.x

## Instrucciones de Despliegue

### 1. Inicializar Docker Swarm
Si no has iniciado Swarm aún:
```powershell
docker swarm init
```

### 2. Construir la Imagen del Servidor
Navega a la carpeta `tsp_solution` y construye la imagen:
```powershell
cd "c:\Users\jrinc\Desktop\HPC 2\Taller 4\tsp_solution"
docker build -t travel-calculator:1.0 ./server
```

### 3. Crear el Servicio en Swarm
Despliega el servicio con 4 réplicas (puedes ajustar el número):
```powershell
docker service create --name calculator --replicas 4 -p 5000:5000 travel-calculator:1.0
```

Verifica que el servicio esté corriendo:
```powershell
docker service ls
docker service ps calculator
```

### 4. Ejecutar el Cliente
Instala las dependencias del cliente y ejecútalo:

```powershell
pip install -r ./client/requirements.txt
python ./client/client.py
```

El cliente generará permutaciones de las ciudades definidas en `client.py`, enviará peticiones al servicio balanceado por Swarm, y mostrará la mejor ruta.

### 5. Limpieza
Para detener y eliminar el servicio:
```powershell
docker service rm calculator
```
