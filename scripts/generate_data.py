from pathlib import Path
import numpy as np
import pandas as pd


def generate_synthetic_data():
  # Definir ruta de salida (en ../data/churn_sintetico.csv)
  base_dir = Path(__file__).parent.parent
  output_path = (base_dir / "../data/churn_sintetico.csv").resolve()

  # Si el archivo ya existe, no lo sobrescribe
  if output_path.exists():
    print(f"El archivo ya existe en: {output_path}. No se sobrescribirá.")
    return

  # Crear carpeta data si no existe
  output_path.parent.mkdir(parents=True, exist_ok=True)

  # Generar datos sintéticos con semilla fija
  np.random.seed(42)
  n_samples = 1000

  data = {
      "RowNumber": range(1, n_samples + 1),
      "CustomerID": np.random.randint(15000000, 16000000, size=n_samples),
      "Surname": [f"User_{i}" for i in range(n_samples)],
      "CreditScore": np.random.randint(350, 850, size=n_samples),
      "Geography": np.random.choice(
          ["France", "Spain", "Germany"], size=n_samples
      ),
      "Gender": np.random.choice(["Female", "Male"], size=n_samples),
      "Age": np.random.randint(18, 70, size=n_samples),
      "Tenure": np.random.randint(0, 10, size=n_samples),
      "Balance": np.random.uniform(0, 150000, size=n_samples),
      "NumOfProducts": np.random.randint(1, 4, size=n_samples),
      "HasCrCard": np.random.choice([0, 1], size=n_samples),
      "IsActiveMember": np.random.choice([0, 1], size=n_samples),
      "EstimatedSalary": np.random.uniform(10000, 200000, size=n_samples),
      "Exited": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]),
      "Complain": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]),
  }

  df = pd.DataFrame(data)
  df.to_csv(output_path, index=False)
  print(f"¡Dataset sintético generado con éxito en: {output_path}!")


if __name__ == "__main__":
  generate_synthetic_data()