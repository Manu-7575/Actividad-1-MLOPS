# Actividad-1-MLOPS
# Actividad 1: Fundamentos, versionamiento y seguimiento (MLOps)

## 👥 Integrantes del Grupo
* Emmanuel Marin
* Jose Figueroa
* Juan Rodriguez

---

## 📌 Descripción del Proyecto
Este repositorio contiene el desarrollo de la **Actividad 1** de MLOps. El objetivo es implementar un pipeline de Machine Learning reproducible y robusto utilizando herramientas estándar de la industria:
* **Poetry**: Gestión y control estricto de dependencias y entornos virtuales.
* **Prefect**: Orquestación y control de flujos de trabajo (*flows* y *tasks*).
* **MLflow**: Seguimiento de experimentos, registro de parámetros, métricas y artefactos.
* **Pytest**: Pruebas unitarias para validar la integridad de los datos y los componentes.

---

## 🗂️ Estructura del Repositorio
* `configs/`: Contiene los archivos de configuración (`config.yaml`).
* `data/`: Almacena el dataset sintético utilizado para el entrenamiento (`churn_sintetico.csv`).
* `flows/`: Flujos principales de orquestación con Prefect (`experimento_flow.py`, `prueba_flow.py`).
* `scripts/`: Scripts utilitarios para la generación y carga de datos (`generate_data.py`, `load_data.py`).
* `tests/`: Pruebas unitarias automatizadas con Pytest (`test_data.py`, etc.).
* `pyproject.toml` / `poetry.lock`: Definición y versiones bloqueadas del entorno.

---

## 🚀 Guía de Instalación y Ejecución (Clonación Limpia)

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Manu-7575/Actividad-1-MLOPS.git](https://github.com/Manu-7575/Actividad-1-MLOPS.git)
cd Actividad-1-MLOPS