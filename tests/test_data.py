from pathlib import Path
import pandas as pd


def test_dataset_sintetico_existe():
  base_dir = Path(__file__).parent.parent
  csv_path = (base_dir / "data/churn_sintetico.csv").resolve()
  assert csv_path.exists(), (
      "El archivo de datos sintéticos no fue encontrado."
  )


def test_cargar_datos_columnas():
  base_dir = Path(__file__).parent.parent
  csv_path = (base_dir / "data/churn_sintetico.csv").resolve()
  df = pd.read_csv(csv_path)

  # Verificar que el DataFrame no esté vacío
  assert not df.empty, "El dataset cargado está vacío."

  # Verificar columnas obligatorias del modelo de Churn
  columnas_esperadas = ["CreditScore", "Geography", "Gender", "Age", "Exited"]
  for col in columnas_esperadas:
    assert col in df.columns, (
        f"La columna obligatoria '{col}' no se encuentra en el dataset."
    )