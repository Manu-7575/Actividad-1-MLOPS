from mlflow import log_metric, set_experiment
from prefect import flow, task


@task
def sumar_numeros():
  # Suma números del 1 al 5 como indica la prueba de la actividad
  total = sum(range(1, 6))
  return total


@flow(name="prueba-flow")
def prueba_flow():
  set_experiment("prueba-validacion")

  # Registrar métrica de prueba en MLflow
  resultado = sumar_numeros()
  log_metric("suma_total", resultado)
  print(f"¡Flujo de prueba ejecutado con éxito! Resultado: {resultado}")


if __name__ == "__main__":
  prueba_flow()