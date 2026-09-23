"""
EA4: Orquestador Maestro del Pipeline de Big Data
Asignatura: Arquitectura Big Data
Institucion: IU Digital de Antioquia

Descripcion:
Este script ejecuta de manera secuencial e integrada todas las fases del ciclo de vida de los datos:
1. Fase 1 (EA1): Ingestion desde API / Ingestion de datos base.
2. Fase 2 (EA2): Preprocesamiento, limpieza e imputacion analitica.
3. Fase 3 (EA3): Enriquecimiento multiformato (JSON, CSV, XML, HTML, TXT, XLSX).
4. Fase 4 (EA4): Verificacion integral del Data Lake / Data Warehouse analitico.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")


def run_stage(script_name: str, stage_label: str):
    script_path = os.path.join(SRC_DIR, script_name)
    print("\n" + "=" * 75)
    print(f"   EJECUTANDO: {stage_label} ({script_name})")
    print("=" * 75)
    
    result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR, capture_output=False)
    if result.returncode != 0:
        print(f"[ERROR] La etapa {stage_label} fallo con codigo de salida {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)
    print(f"[EXITO] Etapa '{stage_label}' completada exitosamente.")


def main():
    print("=" * 80)
    print("      ORQUESTADOR END-TO-END DEL PROYECTO INTEGRADOR BIG DATA (EA1 - EA4)")
    print("=" * 80)

    # 1. Ingestion
    run_stage("ingestion.py", "FASE 1: Ingestion de Datos desde API")

    # 2. Limpieza
    run_stage("cleaning.py", "FASE 2: Preprocesamiento y Limpieza de Datos")

    # 3. Enriquecimiento Multiformato
    run_stage("enrichement.py", "FASE 3: Enriquecimiento e Integracion Multiformato")

    print("\n" + "=" * 80)
    print("      TODAS LAS FASES DEL PIPELINE SE HAN EJECUTADO CON EXITO (100%)")
    print("=" * 80)


if __name__ == "__main__":
    main()
