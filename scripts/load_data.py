from pathlib import Path
import pandas as pd
import yaml


def load_data():
  # Cargar configuración desde configs/config.yaml
  config_path = Path(__file__).parent.parent / "configs" / "config.yaml"
  with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

  ruta_relativa = config["datos"]["ruta"]
  base_dir = Path(__file__).parent.parent
  csv_path = (base_dir / ruta_relativa).resolve()

  print(f"Cargando dataset desde: {csv_path}")

  # Leer el CSV
  df = pd.read_csv(csv_path)
  print(f"¡Dataset cargado con éxito! Dimensiones: {df.shape}")

  return df


if __name__ == "__main__":
  load_data()