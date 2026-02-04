═══════════════════════════════════════════════════════════════════════════════
    🚀 GUÍA DE INICIO RÁPIDO - ANÁLISIS EDA DE REDES SOCIALES
═══════════════════════════════════════════════════════════════════════════════

📦 PASO 1: INSTALAR DEPENDENCIAS
────────────────────────────────────────────────────────────────────────────────

En tu terminal, ejecuta:

    pip install pandas numpy matplotlib seaborn openpyxl --break-system-packages

O usa el archivo requirements.txt:

    pip install -r requirements.txt --break-system-packages


📁 PASO 2: ORGANIZAR TUS ARCHIVOS
────────────────────────────────────────────────────────────────────────────────

Estructura de carpetas recomendada:

    mi_proyecto/
    ├── CDE.xlsx - Hoja 1.csv              ← Tu archivo de datos
    ├── eda_social_media_analysis.py       ← Script principal
    ├── config.py                          ← Configuración
    ├── ejemplo_uso.py                     ← Ejemplos de uso
    ├── utilidades.py                      ← Utilidades extras
    ├── requirements.txt                   ← Dependencias
    └── README.md                          ← Documentación


⚙️ PASO 3: CONFIGURAR (config.py)
────────────────────────────────────────────────────────────────────────────────

Abre config.py y ajusta estos valores según tus columnas:

    FILE_PATH = "CDE.xlsx - Hoja 1.csv"
    STATUS_COL = "Estatus"                 # ← Cambia según tu archivo
    OS_COL = "Sistema_Operativo"           # ← Cambia según tu archivo

💡 TIP: Si no conoces los nombres exactos de tus columnas, ejecuta:

    python utilidades.py

    Esto te mostrará todas las columnas detectadas automáticamente.


▶️ PASO 4: EJECUTAR EL ANÁLISIS
────────────────────────────────────────────────────────────────────────────────

Opción A - Análisis Completo (Recomendado):
────────────────────────────────────────────

    python eda_social_media_analysis.py

Esto generará:
✓ Limpieza automática de datos
✓ Análisis estadístico completo
✓ 4 visualizaciones profesionales
✓ Reporte ejecutivo en texto


Opción B - Análisis Rápido (Diagnóstico):
──────────────────────────────────────────

    python utilidades.py

Esto mostrará:
✓ Diagnóstico del archivo
✓ Detección automática de columnas
✓ Resumen rápido de estadísticas
✓ Insights principales


Opción C - Ejemplos Personalizados:
────────────────────────────────────

    python ejemplo_uso.py

Incluye 4 ejemplos diferentes:
1. Análisis completo automático
2. Análisis paso a paso
3. Análisis personalizado
4. Solo visualizaciones


📊 PASO 5: REVISAR RESULTADOS
────────────────────────────────────────────────────────────────────────────────

Los resultados se guardan en: outputs/

    outputs/
    ├── 01_boxplots_outliers.png          ← Detección de outliers
    ├── 02_correlation_matrix.png         ← Matriz de correlación
    ├── 03_comparison_by_status.png       ← Comparación por estatus
    ├── 04_app_ranking.png                ← Ranking de apps
    └── reporte_ejecutivo.txt             ← Resumen ejecutivo


🎯 USO AVANZADO EN PYTHON
────────────────────────────────────────────────────────────────────────────────

En tu propio script:

    from eda_social_media_analysis import EDAOrchestrator

    # Crear instancia
    eda = EDAOrchestrator("tu_archivo.csv")

    # Ejecutar análisis completo
    eda.run_complete_eda(
        app_columns=None,              # Detección automática
        status_col="Estatus",
        os_col="Sistema_Operativo"
    )


Uso modular:

    from eda_social_media_analysis import DataCleaner, StatisticalAnalyzer, Visualizer

    # 1. Limpiar datos
    cleaner = DataCleaner(df)
    df_clean = cleaner.clean_numeric_columns(app_columns)

    # 2. Analizar
    analyzer = StatisticalAnalyzer(df_clean)
    stats = analyzer.compute_descriptive_stats(app_columns)

    # 3. Visualizar
    viz = Visualizer(df_clean)
    fig = viz.plot_boxplots(app_columns)


🔧 SOLUCIÓN DE PROBLEMAS COMUNES
────────────────────────────────────────────────────────────────────────────────

Problema: "FileNotFoundError"
Solución: Verifica que el archivo esté en la misma carpeta y que el nombre
          en config.py sea EXACTAMENTE igual al nombre del archivo.


Problema: "ModuleNotFoundError: No module named 'pandas'"
Solución: pip install pandas numpy matplotlib seaborn openpyxl --break-system-packages


Problema: "UnicodeDecodeError"
Solución: En config.py, cambia FILE_ENCODING = "latin-1"


Problema: Las columnas no se detectan
Solución: En config.py, especifica manualmente:
          APP_COLUMNS = ["Instagram", "Facebook", "TikTok"]


Problema: "KeyError" o error de columna no encontrada
Solución: 1. Ejecuta python utilidades.py para ver las columnas disponibles
          2. Ajusta STATUS_COL y OS_COL en config.py con los nombres exactos


📚 DOCUMENTACIÓN COMPLETA
────────────────────────────────────────────────────────────────────────────────

Para más detalles, consulta:
→ README.md              - Documentación completa
→ ejemplo_uso.py         - 4 ejemplos de uso diferentes
→ eda_social_media_analysis.py - Código principal con docstrings


💡 TIPS PROFESIONALES
────────────────────────────────────────────────────────────────────────────────

1. SIEMPRE ejecuta primero utilidades.py para diagnosticar tu archivo
2. Revisa el reporte_ejecutivo.txt para insights accionables
3. Los gráficos están en alta resolución (300 DPI) listos para presentaciones
4. Puedes modificar el estilo de gráficos en config.py (PLOT_STYLE)
5. El código maneja automáticamente fechas en campos numéricos


🎨 PERSONALIZACIÓN
────────────────────────────────────────────────────────────────────────────────

Cambiar estilo de gráficos (config.py):
    PLOT_STYLE = "darkgrid"          # darkgrid, whitegrid, white, dark, ticks
    COLOR_PALETTE = "viridis"        # viridis, coolwarm, Set2, muted

Cambiar factor de outliers (config.py):
    OUTLIER_FACTOR = 1.5             # Más bajo = más sensible a outliers

Cambiar resolución de imágenes (config.py):
    PLOT_DPI = 600                   # Mayor DPI = mejor calidad


📞 AYUDA ADICIONAL
────────────────────────────────────────────────────────────────────────────────

Si tienes problemas:
1. Verifica que todos los pasos anteriores estén completos
2. Revisa los mensajes de error cuidadosamente
3. Ejecuta python utilidades.py para diagnosticar
4. Lee el README.md para documentación detallada


# DataScience
