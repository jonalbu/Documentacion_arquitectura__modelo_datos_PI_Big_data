"""
EA1: Ingestion de Datos desde un API

Descripcion:
Este script realiza la extraccion de datos desde una API REST publica,
crea y almacena la informacion en una base de datos SQLite analitica,
genera una muestra representativa en formato Excel utilizando Pandas,
y produce un reporte de auditoria (.txt) verificando la integridad de los datos.
"""

import os
import sys
import sqlite3
import datetime
import requests
import pandas as pd

# Configuracion de rutas relativas al proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
DB_DIR = os.path.join(SRC_DIR, "db")
XLSX_DIR = os.path.join(SRC_DIR, "xlsx")
AUDIT_DIR = os.path.join(SRC_DIR, "static", "auditoria")

DB_PATH = os.path.join(DB_DIR, "ingestion.db")
XLSX_PATH = os.path.join(XLSX_DIR, "ingestion.xlsx")
AUDIT_PATH = os.path.join(AUDIT_DIR, "ingestion.txt")

# URL del API a consultar (JSONPlaceholder - Endpoint publico confiable)
API_URL = "https://jsonplaceholder.typicode.com/posts"


def ensure_directories():
    """Crea los directorios requeridos si no existen."""
    for folder in [DB_DIR, XLSX_DIR, AUDIT_DIR]:
        os.makedirs(folder, exist_ok=True)
    print("[OK] Directorios verificados.")


def fetch_data_from_api(url: str):
    """
    Realiza la peticion GET al API REST y retorna la lista de registros en formato JSON.
    """
    print(f"[INFO] Consultando API en: {url} ...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"[OK] Se extrajeron exitosamente {len(data)} registros desde el API.")
        return data
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Error critico al conectar con el API: {error}", file=sys.stderr)
        raise


def store_data_in_sqlite(data: list, db_path: str):
    """
    Crea la base de datos SQLite, define el esquema de la tabla e inserta los datos extraidos.
    """
    print(f"[INFO] Conectando a la base de datos SQLite en: {db_path} ...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creacion de la tabla con esquema analitico
    create_table_query = """
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)

    # Insercion o reemplazo de registros
    insert_query = """
    INSERT OR REPLACE INTO posts (id, userId, title, body)
    VALUES (?, ?, ?, ?);
    """

    records_to_insert = [
        (item.get("id"), item.get("userId"), item.get("title"), item.get("body"))
        for item in data
    ]

    cursor.executemany(insert_query, records_to_insert)
    conn.commit()
    print(f"[OK] {len(records_to_insert)} registros almacenados en la tabla 'posts'.")

    # Lectura de verificacion mediante Pandas
    df = pd.read_sql_query("SELECT * FROM posts", conn)
    conn.close()
    return df


def generate_excel_sample(df: pd.DataFrame, output_path: str, sample_size: int = 20):
    """
    Genera un archivo Excel (.xlsx) con una muestra representativa de los registros usando Pandas.
    """
    print(f"[INFO] Generando muestra representativa en Excel...")
    
    # Tomar muestra (o todos si el total es menor que el tamano de muestra)
    if len(df) > sample_size:
        sample_df = df.head(sample_size).copy()
    else:
        sample_df = df.copy()

    # Guardar en archivo Excel
    sample_df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"[OK] Archivo de muestra generado exitosamente en: {output_path} ({len(sample_df)} filas)")


def generate_audit_report(api_data: list, db_df: pd.DataFrame, output_path: str):
    """
    Compara los datos extraidos del API vs los almacenados en la base de datos SQLite,
    generando un informe de auditoria en formato .txt.
    """
    print(f"[INFO] Generando informe de auditoria de integridad...")
    execution_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api_count = len(api_data)
    db_count = len(db_df)

    # Validaciones de integridad
    count_match = (api_count == db_count)
    
    # Validacion de IDs extraidos vs IDs en BD
    api_ids = set(item.get("id") for item in api_data)
    db_ids = set(db_df["id"].tolist())
    missing_ids = api_ids - db_ids
    extra_ids = db_ids - api_ids
    ids_match = (len(missing_ids) == 0 and len(extra_ids) == 0)

    # Verificacion de valores nulos en columnas clave
    null_counts = db_df[["id", "userId", "title", "body"]].isnull().sum().to_dict()
    has_nulls = any(val > 0 for val in null_counts.values())

    status = "EXITOSO (100% Integridad)" if (count_match and ids_match and not has_nulls) else "CON DISCREPANCIAS"

    report_content = f"""================================================================================
                    REPORTE DE AUDITORIA DE INGESTA DE DATOS
================================================================================
Asignatura : Arquitectura Big Data
Actividad  : EA1. Ingestion de Datos desde un API
Fecha/Hora : {execution_time}
Origen API : {API_URL}
Destino BD : {DB_PATH}
================================================================================

1. RESUMEN DE CONTEO DE REGISTROS:
--------------------------------------------------------------------------------
- Registros extraidos desde el API       : {api_count}
- Registros almacenados en SQLite        : {db_count}
- Coincidencia de conteos                : {"SI" if count_match else "NO"}

2. VERIFICACION DE INTEGRIDAD DE CLAVES (IDs):
--------------------------------------------------------------------------------
- Total IDs unicos en API               : {len(api_ids)}
- Total IDs unicos en SQLite            : {len(db_ids)}
- IDs faltantes en BD                   : {len(missing_ids)} {list(missing_ids) if missing_ids else "[]"}
- IDs sobrantes en BD                   : {len(extra_ids)} {list(extra_ids) if extra_ids else "[]"}
- Integridad de IDs verificada           : {"SI" if ids_match else "NO"}

3. AUDITORIA DE VALORES NULOS EN CAMPOS CLAVE:
--------------------------------------------------------------------------------
- Nulos en 'id'                         : {null_counts.get('id', 0)}
- Nulos en 'userId'                     : {null_counts.get('userId', 0)}
- Nulos en 'title'                      : {null_counts.get('title', 0)}
- Nulos en 'body'                       : {null_counts.get('body', 0)}
- Datos completos sin nulos             : {"SI" if not has_nulls else "NO"}

4. MUESTRA DE VALIDACION DE CONTENIDO:
--------------------------------------------------------------------------------
- Primer registro (API ID: {api_data[0].get('id')}):
  * Titulo API : {api_data[0].get('title')[:50]}...
  * Titulo BD  : {db_df.iloc[0]['title'][:50]}...
  * Coincidencia: {"SI" if api_data[0].get('title') == db_df.iloc[0]['title'] else "NO"}

================================================================================
ESTADO FINAL DE LA AUDITORIA: {status}
================================================================================
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"[OK] Reporte de auditoria guardado en: {output_path}")
    print(f"[ESTADO] {status}")


def main():
    print("=" * 60)
    print("   INICIO DEL PROCESO DE INGESTA DE DATOS (EA1 - BIG DATA)")
    print("=" * 60)

    # 1. Asegurar directorios
    ensure_directories()

    # 2. Extraccion de API
    api_data = fetch_data_from_api(API_URL)

    # 3. Almacenamiento en SQLite
    db_df = store_data_in_sqlite(api_data, DB_PATH)

    # 4. Generacion de archivo Excel de muestra
    generate_excel_sample(db_df, XLSX_PATH, sample_size=20)

    # 5. Generacion de archivo de auditoria
    generate_audit_report(api_data, db_df, AUDIT_PATH)

    print("=" * 60)
    print("   PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
