import warnings
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings('ignore')


class CDEVisualizer:
    """Generador de visualizaciones profesionales para CDE."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10

    def plot_boxplots(self, app_columns: List[str], output_path: str):
        """Genera boxplots para detectar outliers."""
        n_apps = len(app_columns)
        n_cols = 3
        n_rows = (n_apps + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 5 * n_rows))
        axes = axes.flatten()

        for idx, col in enumerate(app_columns):
            ax = axes[idx]
            data = self.df[col].dropna()
            sns.boxplot(y=data, ax=ax, color='skyblue', width=0.5)
            ax.set_title(f'{col}', fontsize=12, fontweight='bold')
            ax.set_ylabel('Horas/Día', fontsize=10)
            ax.grid(True, alpha=0.3)

            median = data.median()
            mean = data.mean()
            ax.axhline(median, color='red', linestyle='--', linewidth=1.5,
                       label=f'Mediana: {median:.2f}h')
            ax.axhline(mean, color='green', linestyle='--', linewidth=1.5,
                       label=f'Media: {mean:.2f}h')
            ax.legend(fontsize=9, loc='upper right')

        for idx in range(n_apps, len(axes)):
            axes[idx].set_visible(False)

        plt.suptitle('📊 Análisis de Distribución - Detección de Outliers',
                     fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Guardado: {output_path}")

    def plot_correlation_heatmap(self, corr_matrix: pd.DataFrame, output_path: str):
        """Genera heatmap de correlación."""
        fig, ax = plt.subplots(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                    vmin=-1, vmax=1, ax=ax)
        ax.set_title('🔗 Matriz de Correlación - Uso de Redes Sociales',
                     fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Guardado: {output_path}")

    def plot_status_comparison(self, app_columns: List[str], output_path: str):
        """Genera comparación por estatus Regular vs No Regular."""
        if 'Estatus' not in self.df.columns:
            return
        data_list = []
        for app in app_columns:
            for status in self.df['Estatus'].unique():
                if pd.notna(status):
                    subset = self.df[self.df['Estatus'] == status][app]
                    data_list.append({'App': app, 'Estatus': status, 'Horas': subset.mean()})

        plot_df = pd.DataFrame(data_list)
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(data=plot_df, x='App', y='Horas', hue='Estatus', ax=ax, palette='Set2')
        ax.set_title('👥 Comparación de Uso: Regular vs No Regular',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Red Social / App', fontsize=12)
        ax.set_ylabel('Horas Promedio / Día', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, fontsize=9)

        plt.legend(title='Estatus Académico', fontsize=11)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Guardado: {output_path}")

    def plot_ranking(self, app_columns: List[str], output_path: str):
        """Genera ranking de apps más usadas."""
        avg_usage = self.df[app_columns].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = sns.color_palette("viridis", len(avg_usage))
        bars = ax.barh(range(len(avg_usage)), avg_usage.values, color=colors)
        ax.set_yticks(range(len(avg_usage)))
        ax.set_yticklabels(avg_usage.index, fontsize=11)
        ax.set_xlabel('Horas Promedio / Día', fontsize=12, fontweight='bold')
        ax.set_title('🏆 Ranking de Apps Más Utilizadas',
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')

        for i, (bar, val) in enumerate(zip(bars, avg_usage.values)):
            ax.text(val + 0.1, i, f'{val:.2f}h', va='center', fontsize=10, fontweight='bold')

        medals = ['🥇', '🥈', '🥉']
        for i, medal in enumerate(medals):
            if i < len(avg_usage):
                ax.text(-0.5, i, medal, fontsize=16, va='center')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Guardado: {output_path}")

    def plot_os_comparison(self, app_columns: List[str], output_path: str):
        """Genera comparación por sistema operativo."""
        if 'Sistema_Operativo' not in self.df.columns:
            return
        data_list = []
        for os in self.df['Sistema_Operativo'].unique():
            if pd.notna(os):
                subset = self.df[self.df['Sistema_Operativo'] == os]
                for app in app_columns:
                    data_list.append({'Sistema': os, 'App': app, 'Horas': subset[app].mean()})

        plot_df = pd.DataFrame(data_list)
        top_apps = self.df[app_columns].mean().sort_values(ascending=False).head(5).index
        plot_df = plot_df[plot_df['App'].isin(top_apps)]

        fig, ax = plt.subplots(figsize=(12, 7))
        sns.barplot(data=plot_df, x='App', y='Horas', hue='Sistema', ax=ax, palette='muted')
        ax.set_title('💻 Uso por Sistema Operativo (Top 5 Apps)',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Red Social / App', fontsize=12)
        ax.set_ylabel('Horas Promedio / Día', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, fontsize=9)

        plt.legend(title='Sistema Operativo', fontsize=11)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Guardado: {output_path}")
