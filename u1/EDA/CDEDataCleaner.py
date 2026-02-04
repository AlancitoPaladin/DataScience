import pandas as pd
import warnings
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class CDEDataCleaner:
    """Limpiador especializado para el dataset CDE.xlsx"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.cleaning_log = []

    def load_and_clean(self) -> pd.DataFrame:
        """Carga y limpia el dataset completo."""
        print("\n" + "=" * 80)
        print("🧹 INICIANDO LIMPIEZA ESPECIALIZADA DEL DATASET CDE")
        print("=" * 80)

        # 1. Cargar datos
        try:
            self.df = pd.read_excel(self.file_path, sheet_name=0)
            self.cleaning_log.append(f"✓ Archivo cargado: {self.df.shape[0]} filas × {self.df.shape[1]} columnas")
        except Exception as e:
            raise Exception(f"Error al cargar el archivo: {e}")

        # 2-8. Proceso de limpieza
        self.df = self._remove_empty_columns()
        self.df = self._remove_empty_rows()
        self.df = self._standardize_column_names()
        self.df = self._standardize_categorical_values()
        self.df = self._clean_app_columns()
        self.df = self._clean_age_column()
        self._generate_cleaning_report()

        return self.df

    def _remove_empty_columns(self) -> pd.DataFrame:
        """Elimina columnas completamente vacías."""
        cols_before = len(self.df.columns)
        unnamed_cols = [col for col in self.df.columns if 'Unnamed' in str(col)]
        self.df = self.df.drop(columns=unnamed_cols)
        cols_after = len(self.df.columns)
        removed = cols_before - cols_after
        if removed > 0:
            self.cleaning_log.append(f"✓ Eliminadas {removed} columnas vacías")
        return self.df

    def _remove_empty_rows(self) -> pd.DataFrame:
        """Elimina filas completamente vacías."""
        rows_before = len(self.df)
        important_cols = ['Edad', 'Genero (F/M/O)', 'Regular(Si/No)']
        self.df = self.df.dropna(subset=important_cols, how='all')
        rows_after = len(self.df)
        removed = rows_before - rows_after
        if removed > 0:
            self.cleaning_log.append(f"✓ Eliminadas {removed} filas vacías")
        return self.df

    def _standardize_column_names(self) -> pd.DataFrame:
        """Estandariza nombres de columnas."""
        rename_map = {
            'Genero (F/M/O)': 'Genero',
            'Foraneo(Si/No)': 'Foraneo',
            'Regular(Si/No)': 'Estatus',
            'Sist. Operatvo': 'Sistema_Operativo',
            'X': 'Twitter_X'
        }
        self.df = self.df.rename(columns=rename_map)
        self.cleaning_log.append(f"✓ Nombres de columnas estandarizados")
        return self.df

    def _standardize_categorical_values(self) -> pd.DataFrame:
        """Estandariza valores categóricos."""
        for col in ['Foraneo', 'Estatus']:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.upper().str.strip()
                self.df[col] = self.df[col].replace({'SI': 'Si', 'NO': 'No'})
                self.cleaning_log.append(f"✓ Estandarizado: {col}")

        if 'Sistema_Operativo' in self.df.columns:
            self.df['Sistema_Operativo'] = self.df['Sistema_Operativo'].astype(str).str.strip()
            self.df['Sistema_Operativo'] = self.df['Sistema_Operativo'].replace({'IOS': 'iOS'})
            self.cleaning_log.append(f"✓ Estandarizado: Sistema_Operativo")

        if 'Genero' in self.df.columns:
            self.df['Genero'] = self.df['Genero'].astype(str).str.upper().str.strip()
            self.cleaning_log.append(f"✓ Estandarizado: Genero")

        return self.df

    def _clean_app_columns(self) -> pd.DataFrame:
        """Limpia columnas de apps - CRÍTICO."""
        app_columns = ['Facebook', 'Instagram', 'TikTok', 'Youtube',
                       'Twitter_X', 'Spotify', 'WhatsApp']

        for col in app_columns:
            if col not in self.df.columns:
                continue

            problemas_detectados = 0

            def clean_value(val):
                nonlocal problemas_detectados
                if isinstance(val, (int, float)):
                    return float(val) if not pd.isna(val) else np.nan
                if isinstance(val, datetime):
                    problemas_detectados += 1
                    return np.nan
                if isinstance(val, str):
                    val = val.strip()
                    if val.startswith('.'):
                        val = '0' + val
                    try:
                        return float(val)
                    except ValueError:
                        problemas_detectados += 1
                        return np.nan
                return np.nan

            self.df[col] = self.df[col].apply(clean_value)

            if self.df[col].notna().sum() > 0:
                median_val = self.df[col].median()
                nulls_before = self.df[col].isnull().sum()
                self.df[col] = self.df[col].fillna(median_val)
                self.cleaning_log.append(
                    f"✓ {col}: {problemas_detectados} valores anómalos detectados, "
                    f"{nulls_before} imputados con mediana ({median_val:.2f})"
                )

            self.df[col] = self.df[col].astype(float)

        return self.df

    def _clean_age_column(self) -> pd.DataFrame:
        """Limpia la columna de edad."""
        if 'Edad' in self.df.columns:
            self.df['Edad'] = pd.to_numeric(self.df['Edad'], errors='coerce')
            if self.df['Edad'].isnull().any():
                median_age = self.df['Edad'].median()
                self.df['Edad'] = self.df['Edad'].fillna(median_age)
            self.df['Edad'] = self.df['Edad'].astype(int)
            self.cleaning_log.append(f"✓ Edad limpiada y convertida a entero")
        return self.df

    def _generate_cleaning_report(self):
        """Genera y muestra el reporte de limpieza."""
        print("\n📋 REPORTE DE LIMPIEZA:")
        print("─" * 80)
        for log in self.cleaning_log:
            print(f"   {log}")
        print(f"\n✅ RESULTADO FINAL:")
        print(f"   • Registros válidos: {len(self.df)}")
        print(f"   • Columnas útiles: {len(self.df.columns)}")
        print(f"   • Columnas: {list(self.df.columns)}")

    def get_app_columns(self) -> List[str]:
        """Retorna lista de columnas de apps."""
        return ['Facebook', 'Instagram', 'TikTok', 'Youtube',
                'Twitter_X', 'Spotify', 'WhatsApp']

    def get_cleaned_data(self) -> pd.DataFrame:
        """Retorna el DataFrame limpio."""
        return self.df
