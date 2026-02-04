import warnings
from datetime import datetime
from typing import List

import pandas as pd

warnings.filterwarnings('ignore')


class CDEReporter:
    """Generador de reportes ejecutivos para CDE."""

    def __init__(self, df: pd.DataFrame, analyzer: CDEAnalyzer):
        self.df = df
        self.analyzer = analyzer

    def generate_executive_report(self, app_columns: List[str], output_path: str):
        """Genera reporte ejecutivo completo."""
        report = []
        report.append("=" * 80)
        report.append("REPORTE EJECUTIVO - ANÁLISIS DE USO DE REDES SOCIALES CDE".center(80))
        report.append("=" * 80)
        report.append(f"\nFecha del Análisis: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"Dataset: CDE.xlsx")
        report.append(f"Registros Analizados: {len(self.df)}")

        # Ranking de apps
        report.append("\n" + "─" * 80)
        report.append("RANKING DE APPS MÁS UTILIZADAS")
        report.append("─" * 80)
        avg_usage = self.df[app_columns].mean().sort_values(ascending=False)
        medals = ["🥇", "🥈", "🥉", "  ", "  ", "  ", "  "]
        for rank, (app, hours) in enumerate(avg_usage.items(), 1):
            medal = medals[rank - 1] if rank <= len(medals) else "  "
            report.append(f"{medal} #{rank}. {app}: {hours:.2f} horas/día")

        # Análisis por estatus
        if 'Estatus' in self.df.columns:
            report.append("\n" + "─" * 80)
            report.append("ANÁLISIS POR ESTATUS ACADÉMICO")
            report.append("─" * 80)
            status_totals = {}
            for status in self.df['Estatus'].unique():
                if pd.notna(status):
                    subset = self.df[self.df['Estatus'] == status]
                    total = subset[app_columns].sum(axis=1).mean()
                    status_totals[status] = total

            for status, total in sorted(status_totals.items(), key=lambda x: x[1], reverse=True):
                count = len(self.df[self.df['Estatus'] == status])
                report.append(f"• {status}: {total:.2f} hrs/día (n={count})")

            if len(status_totals) >= 2:
                values = list(status_totals.values())
                diff = abs(values[0] - values[1])
                pct_diff = (diff / min(values)) * 100
                report.append(f"\n💡 Diferencia: {diff:.2f} hrs ({pct_diff:.1f}%)")

        # App líder por OS
        if 'Sistema_Operativo' in self.df.columns:
            report.append("\n" + "─" * 80)
            report.append("APP LÍDER POR SISTEMA OPERATIVO")
            report.append("─" * 80)
            os_leaders = self.analyzer.find_top_app_by_os(app_columns)
            for _, row in os_leaders.iterrows():
                report.append(f"\n{row['Sistema_Operativo']}: {row['App_Lider']} ({row['Horas_Promedio']}h)")

        report.append("\n" + "=" * 80)

        report_text = "\n".join(report)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n✓ Reporte ejecutivo guardado: {output_path}")
        print("\n" + report_text)
