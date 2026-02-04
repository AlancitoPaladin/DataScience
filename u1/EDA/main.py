"""
Análisis Exploratorio de Datos - Dataset CDE.xlsx
==================================================

Script optimizado con detección automática de ruta del archivo.

INSTRUCCIONES DE USO:
1. Coloca el archivo CDE.xlsx en el mismo directorio que este script
2. O actualiza la variable FILE_PATH en la sección de configuración
3. Ejecuta: python main.py

Autor: Senior Data Scientist & Python Developer
"""

import warnings
from pathlib import Path

from CDEAnalyzer import CDEAnalyzer
from CDEDataCleaner import CDEDataCleaner
from CDEReporter import CDEReporter
from CDEVisualizer import CDEVisualizer

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN - AJUSTA ESTA SECCIÓN SEGÚN TU ENTORNO
# ============================================================================

# Opción 1: Ruta relativa (archivo en el mismo directorio que el script)
# FILE_PATH = "CDE.xlsx"

# Opción 2: Ruta absoluta (descomenta y ajusta si es necesario)
# FILE_PATH = "/Users/tuusuario/Desktop/CDE.xlsx"

# Opción 3: En subdirectorio (descomenta si tu archivo está en una carpeta)
FILE_PATH = "datasets/CDE.xlsx"

# Directorio de salida para resultados
OUTPUT_DIR = "outputs"


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def find_file_automatically():
    """
    Intenta encontrar el archivo CDE.xlsx automáticamente.

    Returns:
        str: Ruta al archivo si se encuentra, None si no
    """
    possible_locations = [
        "CDE.xlsx",
        "datasets/CDE.xlsx",
        "../CDE.xlsx",
        "../datasets/CDE.xlsx",
        "data/CDE.xlsx",
    ]

    # También buscar en el directorio actual y subdirectorios
    current_dir = Path.cwd()

    # Buscar en ubicaciones predefinidas
    for location in possible_locations:
        if Path(location).exists():
            print(f"✓ Archivo encontrado en: {location}")
            return location

    # Buscar recursivamente en el directorio actual
    for file_path in current_dir.rglob("CDE.xlsx"):
        print(f"✓ Archivo encontrado en: {file_path}")
        return str(file_path)

    return None


def validate_file_path(file_path: str) -> bool:
    """
    Valida que el archivo existe y es accesible.

    Args:
        file_path: Ruta al archivo

    Returns:
        bool: True si el archivo existe
    """
    path = Path(file_path)

    if not path.exists():
        print(f"\n ERROR: No se encontró el archivo en '{file_path}'")
        print(f"\n📍 Directorio actual: {Path.cwd()}")
        print(f"\n Soluciones:")
        print(f"   1. Coloca el archivo 'CDE.xlsx' en: {Path.cwd()}")
        print(f"   2. O actualiza la variable FILE_PATH en el script con la ruta correcta")
        print(f"   3. Ejemplo: FILE_PATH = '/ruta/completa/al/archivo/CDE.xlsx'")
        return False

    if not path.is_file():
        print(f"\n ERROR: '{file_path}' no es un archivo válido")
        return False

    if path.suffix.lower() not in ['.xlsx', '.xls']:
        print(f"\n  ADVERTENCIA: El archivo no tiene extensión .xlsx")
        print(f"   Extensión detectada: {path.suffix}")

    return True


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal - Ejecuta el análisis EDA completo."""
    print("\n" + "=" * 80)
    print(" ANÁLISIS EXPLORATORIO DE DATOS - DATASET CDE.xlsx")
    print("=" * 80)

    # 1. Validar/encontrar archivo
    print("\n FASE 1: CARGA Y LIMPIEZA")

    file_to_use = FILE_PATH

    # Si el archivo configurado no existe, intentar encontrarlo
    if not Path(file_to_use).exists():
        print(f"  Archivo no encontrado en: {file_to_use}")
        print(f" Buscando archivo automáticamente...")
        found_file = find_file_automatically()

        if found_file:
            file_to_use = found_file
        else:
            print(f"\n No se pudo encontrar el archivo CDE.xlsx")
            print(f"\n SOLUCIÓN:")
            print(f"   1. Coloca el archivo 'CDE.xlsx' en: {Path.cwd()}")
            print(f"   2. O crea una carpeta 'datasets' y ponlo ahí")
            print(f"   3. O actualiza FILE_PATH en el script con la ruta correcta")
            return False

    # Validar que el archivo existe y es válido
    if not validate_file_path(file_to_use):
        return False

    # Crear directorio de salida
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 2. Cargar y limpiar
        cleaner = CDEDataCleaner(file_to_use)
        df = cleaner.load_and_clean()
        app_columns = cleaner.get_app_columns()

        # 3. Análisis estadístico
        print("\n FASE 2: ANÁLISIS ESTADÍSTICO")
        print("─" * 80)
        analyzer = CDEAnalyzer(df)
        stats = analyzer.generate_comprehensive_stats(app_columns)
        print("\n Estadísticas Descriptivas:")
        print(stats.to_string())

        # 4. Visualizaciones
        print("\n FASE 3: GENERACIÓN DE VISUALIZACIONES")
        print("─" * 80)
        visualizer = CDEVisualizer(df)

        visualizer.plot_boxplots(app_columns, f"{output_dir}/01_boxplots_outliers.png")
        corr = analyzer.calculate_correlations(app_columns)
        visualizer.plot_correlation_heatmap(corr, f"{output_dir}/02_correlation_matrix.png")
        visualizer.plot_status_comparison(app_columns, f"{output_dir}/03_comparison_status.png")
        visualizer.plot_ranking(app_columns, f"{output_dir}/04_app_ranking.png")
        visualizer.plot_os_comparison(app_columns, f"{output_dir}/05_comparison_os.png")

        # 5. Reporte
        print("\n FASE 4: GENERACIÓN DE REPORTE EJECUTIVO")
        print("─" * 80)
        reporter = CDEReporter(df, analyzer)
        reporter.generate_executive_report(app_columns, f"{output_dir}/reporte_ejecutivo.txt")

        # 6. Exportar datos
        df.to_csv(f"{output_dir}/datos_limpios.csv", index=False, encoding='utf-8')
        stats.to_csv(f"{output_dir}/estadisticas_descriptivas.csv", encoding='utf-8')

        print("\n" + "=" * 80)
        print(" ANÁLISIS COMPLETO FINALIZADO CON ÉXITO")
        print("=" * 80)
        print(f"\n Archivos generados en: {output_dir.absolute()}/")

        return True

    except Exception as e:
        print(f"\n ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
