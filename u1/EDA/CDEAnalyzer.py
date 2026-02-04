import warnings
from typing import Dict, List

import pandas as pd

warnings.filterwarnings('ignore')


class CDEAnalyzer:
    """Analizador estadístico especializado para CDE."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_comprehensive_stats(self, app_columns: List[str]) -> pd.DataFrame:
        """Genera estadísticas descriptivas completas."""
        stats = {}
        for col in app_columns:
            if col not in self.df.columns:
                continue
            stats[col] = {
                'Media': self.df[col].mean(),
                'Mediana': self.df[col].median(),
                'Desv_Est': self.df[col].std(),
                'Min': self.df[col].min(),
                'Max': self.df[col].max(),
                'Q1': self.df[col].quantile(0.25),
                'Q3': self.df[col].quantile(0.75),
                'Skewness': self.df[col].skew(),
                'Kurtosis': self.df[col].kurtosis(),
                'CV_%': (self.df[col].std() / self.df[col].mean() * 100) if self.df[col].mean() > 0 else 0
            }
        return pd.DataFrame(stats).T.round(3)

    def compare_by_status(self, app_columns: List[str]) -> Dict:
        """Compara uso entre Regular vs No Regular."""
        if 'Estatus' not in self.df.columns:
            return {}
        comparison = {}
        for app in app_columns:
            if app not in self.df.columns:
                continue
            grouped = self.df.groupby('Estatus')[app].agg(['mean', 'median', 'count'])
            comparison[app] = grouped
        return comparison

    def find_top_app_by_os(self, app_columns: List[str]) -> pd.DataFrame:
        """Encuentra app líder por sistema operativo."""
        if 'Sistema_Operativo' not in self.df.columns:
            return pd.DataFrame()
        results = []
        for os in self.df['Sistema_Operativo'].unique():
            if pd.isna(os):
                continue
            subset = self.df[self.df['Sistema_Operativo'] == os]
            avg_usage = subset[app_columns].mean()
            top_app = avg_usage.idxmax()
            top_value = avg_usage.max()
            results.append({
                'Sistema_Operativo': os,
                'App_Lider': top_app,
                'Horas_Promedio': round(top_value, 2),
                'Usuarios': len(subset)
            })
        return pd.DataFrame(results)

    def calculate_correlations(self, app_columns: List[str]) -> pd.DataFrame:
        """Calcula matriz de correlación."""
        return self.df[app_columns].corr()
