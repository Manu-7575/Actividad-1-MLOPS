from pathlib import Path
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import yaml
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


@task(name="Cargar Datos")
def cargar_datos_task(config):
  ruta_relativa = config["datos"]["ruta"]
  base_dir = Path(__file__).parent.parent
  csv_path = (base_dir / ruta_relativa).resolve()

  df = pd.read_csv(csv_path)
  print(f"Dataset cargado correctamente. Filas: {df.shape[0]}")
  return df


@task(name="Entrenar y Registrar Modelo")
def entrenar_modelo_task(df, config):
  # 1. Preparación de datos (excluyendo identificadores)
  cols_a_ignorar = [
      "RowNumber",
      "CustomerID",
      "Surname",
      "Exited",
  ]
  features = [col for col in df.columns if col not in cols_a_ignorar]

  X = df[features]
  X = pd.get_dummies(X, drop_first=True)
  y = df["Exited"]
  
  test_size = config["division"]["test_size"]
  random_state = config["division"]["random_state"]

  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=test_size, random_state=random_state, stratify=y
  )

  # 2. Configurar el modelo desde config.yaml
  tipo_modelo = config["modelo"]["tipo"]
  if tipo_modelo == "gradient_boosting":
    model = GradientBoostingClassifier(
        random_state=random_state, **config["modelo"].get("parametros", {})
    )
  else:
    model = LogisticRegression(
        random_state=random_state, **config["modelo"].get("parametros", {})
    )

  # 3. MLflow Tracking
  mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
  mlflow.set_experiment(config["mlflow"]["experimento"])

  with mlflow.start_run(run_name=config["mlflow"]["nombre_run"]) as run:
    # Registrar parámetros
    mlflow.log_param("test_size", test_size)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("tipo_modelo", tipo_modelo)
    umbral = config["metricas"]["umbral"]
    mlflow.log_param("umbral", umbral)

    # Entrenar
    model.fit(X_train, y_train)

    # Predicciones y métricas
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= umbral).astype(int)

    auc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    # Registrar métricas en MLflow
    mlflow.log_metric("AUC", auc)
    mlflow.log_metric("Accuracy", acc)
    mlflow.log_metric("Precision", prec)
    mlflow.log_metric("Recall", rec)
    mlflow.log_metric("F1", f1)

    # Registrar modelo
    mlflow.sklearn.log_model(model, "modelo_churn")

    run_id = run.info.run_id
    print(f"Entrenamiento finalizado. Run ID de MLflow: {run_id}")

  return run_id, df.shape[0], auc, tipo_modelo


@task(name="Generar Resumen Prefect")
def resumen_artifact_task(run_id, n_filas, auc, tipo_modelo):
  markdown_report = f"""# Resumen del Experimento MLOps
  - **Modelo utilizado:** `{tipo_modelo}`
  - **Número de filas procesadas:** `{n_filas}`
  - **Métrica AUC obtenida:** `{auc:.4f}`
  - **MLflow Run ID:** `{run_id}`
  """
  create_markdown_artifact(
      key="resumen-experimento-churn",
      markdown=markdown_report,
      description="Reporte de ejecución del flujo de Churn",
  )
  print("Artefacto de Markdown creado exitosamente en Prefect.")


@flow(name="experimento-churn-flow")
def experimento_flow():
  # Cargar configuración
  config_path = Path(__file__).parent.parent / "configs" / "config.yaml"
  with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

  # Ejecutar tareas en orden
  df = cargar_datos_task(config)
  run_id, n_filas, auc, tipo_modelo = entrenar_modelo_task(df, config)
  resumen_artifact_task(run_id, n_filas, auc, tipo_modelo)


if __name__ == "__main__":
  experimento_flow()