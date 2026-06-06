# High Performance Computing

**Four parallel computing workshops benchmarking sequential vs. parallel execution across CPU-bound, image processing, video processing, and distributed computing problems.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Swarm-2496ED.svg)](https://docs.docker.com/engine/swarm/)
[![Flask](https://img.shields.io/badge/API-Flask-black.svg)](https://flask.palletsprojects.com/)

---

## Overview

Each workshop implements the same problem twice — sequential and parallel — and measures speedup, CPU utilization, and execution time. The final workshop scales the solution to a distributed architecture using Docker Swarm with a Flask API backend and Python client.

---

## Repository Structure

```text
HPC/
├── taller-1-tsp-fuerza-bruta/       # TSP brute force: sequential vs parallel
├── taller-2-deteccion-bordes-sobel/ # Sobel edge detection: sequential vs parallel
├── taller-3-procesamiento-video/    # Video grayscale: sequential vs parallel
└── taller-4-tsp-distribuido/        # Distributed TSP with Docker Swarm + Flask API
```

---

## Workshops

### 1. TSP Brute Force

`taller-1-tsp-fuerza-bruta/`

Sequential and parallel implementations of the Travelling Salesman Problem using brute force enumeration. Benchmark comparison measures execution time reduction from multiprocessing.

- `tsp_bruteforce.py` — sequential + parallel implementations
- `HPC_Tsp.pdf` — benchmark report

### 2. Sobel Edge Detection

`taller-2-deteccion-bordes-sobel/`

Sobel convolution filter applied to images in sequential and parallel modes on CPU. Results compare frame processing times and visual output quality.

- `CPU-Secuencial.py` — sequential Sobel
- `CPU-Paralelo.py` — parallel Sobel
- `Comparador Secuencial vs Paralelo.py` — benchmark runner
- `Resultados/` — generated output images and timing evidence

### 3. Video Grayscale Processing

`taller-3-procesamiento-video/`

Frame-by-frame grayscale conversion on a video file, comparing sequential processing against parallel workers. Measures total conversion time and frames-per-second throughput.

- `video_processor_Secuencial.py` — sequential version
- `video_processor_Paralelo.py` — parallel version
- `comparacion_resultados.py` — result comparison and visualization

### 4. Distributed TSP with Docker Swarm

`taller-4-tsp-distribuido/`

TSP brute force distributed across a Docker Swarm cluster. A Flask REST API receives route evaluation requests from a Python client and dispatches work across worker nodes. Demonstrates horizontal scaling and load distribution.

- Flask API deployable as a Docker service
- Python client for route evaluation
- Source in `tsp_solution/`

---

## Requirements

- Python 3.9+
- Docker Desktop with Swarm mode enabled (Workshop 4 only)
- Per-workshop dependencies listed in each folder's `README.md`

```bash
pip install -r requirements.txt
```

---

## Quick Start

```bash
git clone git@github.com:Julian-Rincon/HPC.git
cd HPC
```

Navigate to the workshop folder and follow its `README.md`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Parallelism | `multiprocessing`, `concurrent.futures` |
| Distributed | Docker Swarm, Docker Compose |
| API | Flask |
| Visualization | Matplotlib, OpenCV |

---

## Authors

- **Julian Rincon** — [github.com/Julian-Rincon](https://github.com/Julian-Rincon)
- **Paula Caballero** — [github.com/Pauc09](https://github.com/Pauc09)

*Universidad Sergio Arboleda — High Performance Computing*
