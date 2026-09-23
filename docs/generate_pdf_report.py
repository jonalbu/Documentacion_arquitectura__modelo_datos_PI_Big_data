import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado para encabezados y pies de pagina."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Omitir portada
        if self._pageNumber > 1:
            self.drawString(54, 750, "IU Digital de Antioquia | Arquitectura Big Data - Documento de Arquitectura y Modelo de Datos")
            self.setStrokeColor(colors.HexColor("#cccccc"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            self.line(54, 45, 558, 45)
            self.drawString(54, 32, "EA4. Proyecto Integrador - Ciclo de Vida de los Datos")
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(558, 32, page_text)
        self.restoreState()


def build_pdf_document(output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#0d47a1")
    c_secondary = colors.HexColor("#1565c0")
    c_dark = colors.HexColor("#212121")

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=c_primary, alignment=1, spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=c_secondary, alignment=1, spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=c_primary, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_secondary, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=c_dark, spaceAfter=6, alignment=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=c_dark, leftIndent=12, spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=11,
        textColor=colors.HexColor("#455a64"), alignment=1, spaceBefore=2, spaceAfter=6
    )

    tbl_header_style = ParagraphStyle(
        'TblHdr', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white, alignment=1
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=9.5,
        textColor=c_dark
    )

    story = []

    # =========================================================================
    # PORTADA
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("INSTITUCIÓN UNIVERSITARIA DIGITAL DE ANTIOQUIA", ParagraphStyle('Univ', fontName='Helvetica-Bold', fontSize=12, leading=15, alignment=1, textColor=colors.HexColor("#475569"))))
    story.append(Paragraph("FACULTAD DE INGENIERÍA | INGENIERÍA DE SOFTWARE", ParagraphStyle('Fac', fontName='Helvetica', fontSize=9.5, leading=13, alignment=1, textColor=colors.HexColor("#64748b"))))
    story.append(Spacer(1, 20))
    
    story.append(HRFlowable(width="85%", thickness=2.5, color=c_primary, spaceAfter=20, spaceBefore=5))
    story.append(Paragraph("DOCUMENTO DE ARQUITECTURA DE BIG DATA Y MODELO DE DATOS", title_style))
    story.append(Paragraph("Actividad Evaluativa 4 (EA4) - Proyecto Integrador", subtitle_style))
    story.append(HRFlowable(width="85%", thickness=1, color=c_secondary, spaceAfter=30, spaceBefore=5))

    meta_data = [
        [Paragraph("<b>Asignatura:</b>", tbl_cell_style), Paragraph("Arquitectura Big Data (7° Semestre)", tbl_cell_style)],
        [Paragraph("<b>Docente Asesor:</b>", tbl_cell_style), Paragraph("Facultad de Ingeniería - IU Digital de Antioquia", tbl_cell_style)],
        [Paragraph("<b>Pipeline Implementado:</b>", tbl_cell_style), Paragraph("Ingestión API (EA1) ➔ Limpieza (EA2) ➔ Enriquecimiento Multiformato (EA3) ➔ Arquitectura (EA4)", tbl_cell_style)],
        [Paragraph("<b>Dataset Base:</b>", tbl_cell_style), Paragraph("FIFA 20 Complete Player Dataset (18,278 registros) + 6 Fuentes Multiformato", tbl_cell_style)],
        [Paragraph("<b>Entorno de Ejecución:</b>", tbl_cell_style), Paragraph("Simulación Cloud (SQLite Data Lakehouse) + GitHub Actions CI/CD Automatizado", tbl_cell_style)],
        [Paragraph("<b>Fecha:</b>", tbl_cell_style), Paragraph("Septiembre 2026", tbl_cell_style)]
    ]
    t_meta = Table(meta_data, colWidths=[140, 340])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # =========================================================================
    # 1. INTRODUCCIÓN Y VISIÓN GLOBAL
    # =========================================================================
    story.append(Paragraph("1. Introducción y Descripción Global de la Arquitectura", h1_style))
    story.append(Paragraph(
        "El presente documento técnico detalla la arquitectura de software y datos diseñada e implementada para el "
        "<b>Proyecto Integrador de Big Data</b> en la Institución Universitaria Digital de Antioquia. El sistema cubre de "
        "forma exhaustiva el ciclo de vida integral del dato, abarcando las cuatro etapas metodológicas establecidas:", body_style
    ))
    
    phases = [
        "<b>Fase 1 (EA1 - Ingestión):</b> Conexión automatizada vía HTTP a servicios web y APIs REST públicas, extrayendo datos semiestructurados (JSON) y persistiendo su estado crudo en una base de datos relacional analítica.",
        "<b>Fase 2 (EA2 - Preprocesamiento y Limpieza):</b> Depuración masiva de inconsistencias, eliminación de duplicados, imputación estadística de valores nulos (mediana e imputaciones por dominio), corrección de tipos e ingeniería de variables biométricas.",
        "<b>Fase 3 (EA3 - Enriquecimiento Multiformato):</b> Integración sinérgica de datos complementarios provenientes de <b>6 formatos heterogéneos</b> (JSON, CSV, XML, HTML, TXT y XLSX) mediante operaciones relacionales de cruce (LEFT JOIN) preservando la integridad referencial al 100%.",
        "<b>Fase 4 (EA4 - Modelo de Datos y Automatización CI/CD):</b> Consolidación del esquema dimensional analítico en SQLite, generación de evidencias ejecutivas y orquestación desatendida mediante GitHub Actions."
    ]
    for p in phases:
        story.append(Paragraph(f"• {p}", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "La solución adopta el patrón de <b>Arquitectura Medallion (Data Lakehouse)</b>, dividiendo el flujo en capas de madurez: "
        "<b>Bronze (Datos Crudos / Ingestión)</b>, <b>Silver (Datos Depurados / Limpieza)</b> y <b>Gold (Datos Enriquecidos / Analítica y Modelado)</b>, "
        "garantizando trazabilidad, reproducibilidad y gobernanza en todo momento.", body_style
    ))

    # =========================================================================
    # 2. DIAGRAMAS DE ARQUITECTURA Y FLUJO DE DATOS
    # =========================================================================
    story.append(Paragraph("2. Diagrama de Arquitectura y Flujo de Procesamiento", h1_style))
    story.append(Paragraph(
        "El diagrama a continuación ilustra la interacción entre las fuentes heterogéneas, los scripts de procesamiento en Python, "
        "la persistencia escalonada en SQLite y el pipeline de automatización continua CI/CD en GitHub Actions:", body_style
    ))
    
    diag_arq_path = os.path.join(os.path.dirname(__file__), "diagrama_arquitectura.png")
    if os.path.exists(diag_arq_path):
        story.append(Image(diag_arq_path, width=470, height=240))
        story.append(Paragraph("<i>Figura 1: Arquitectura Medallion End-to-End y Pipeline CI/CD en GitHub Actions.</i>", callout_style))

    # =========================================================================
    # 3. MODELO DE DATOS Y DIAGRAMA ENTIDAD-RELACIÓN (ER)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Modelo de Datos y Diagrama Entidad - Relación (ER)", h1_style))
    story.append(Paragraph(
        "El modelo de datos se estructura bajo un enfoque analítico optimizado para consultas de alto rendimiento y modelos de Machine Learning. "
        "La entidad central <code>enriched_players</code> combina los atributos intrínsecos de los jugadores con las dimensiones externas integradas:", body_style
    ))

    diag_er_path = os.path.join(os.path.dirname(__file__), "diagrama_modelo_er.png")
    if os.path.exists(diag_er_path):
        story.append(Image(diag_er_path, width=470, height=240))
        story.append(Paragraph("<i>Figura 2: Diagrama Entidad-Relación (ER) del Modelo de Datos Enriquecido.</i>", callout_style))

    story.append(Paragraph("Diccionario de Datos y Estructura de Tablas:", h2_style))
    
    dict_data = [
        [Paragraph("Tabla / Entidad", tbl_header_style), Paragraph("Formato", tbl_header_style), Paragraph("Clave (PK / FK)", tbl_header_style), Paragraph("Atributos Relevantes", tbl_header_style)],
        [Paragraph("<b>enriched_players</b><br/>(Tabla Maestra Gold)", tbl_cell_style), Paragraph("SQLite DB", tbl_cell_style), Paragraph("PK: sofifa_id<br/>FK: nationality, club", tbl_cell_style), Paragraph("sofifa_id, short_name, overall, potential, value_eur, wage_eur, bmi, potential_growth, star_rating_index (44 cols)", tbl_cell_style)],
        [Paragraph("<b>countries_info</b>", tbl_cell_style), Paragraph("JSON (.json)", tbl_cell_style), Paragraph("PK: nationality", tbl_cell_style), Paragraph("continent, fifa_confederation, country_iso3, fifa_ranking_tier", tbl_cell_style)],
        [Paragraph("<b>club_leagues</b>", tbl_cell_style), Paragraph("CSV (.csv)", tbl_cell_style), Paragraph("PK: club", tbl_cell_style), Paragraph("league_name, league_country, league_tier, is_top_5_european_league", tbl_cell_style)],
        [Paragraph("<b>stadiums_info</b>", tbl_cell_style), Paragraph("XML (.xml)", tbl_cell_style), Paragraph("PK: club", tbl_cell_style), Paragraph("stadium_name, stadium_capacity", tbl_cell_style)],
        [Paragraph("<b>national_trophies</b>", tbl_cell_style), Paragraph("HTML (.html)", tbl_cell_style), Paragraph("PK: nationality", tbl_cell_style), Paragraph("world_cup_titles, continental_trophies", tbl_cell_style)],
        [Paragraph("<b>player_contracts</b>", tbl_cell_style), Paragraph("TXT (.txt)", tbl_cell_style), Paragraph("PK: sofifa_id", tbl_cell_style), Paragraph("contract_tier, rep_stars", tbl_cell_style)],
        [Paragraph("<b>sponsorship_tiers</b>", tbl_cell_style), Paragraph("XLSX (.xlsx)", tbl_cell_style), Paragraph("PK: club", tbl_cell_style), Paragraph("main_sponsor, sponsor_tier", tbl_cell_style)]
    ]
    t_dict = Table(dict_data, colWidths=[110, 60, 95, 215])
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_dict)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Justificación del Modelo:</b>", h2_style))
    story.append(Paragraph(
        "Se adoptó un modelo híbrido relacional/desnormalizado tipo <i>Estrella (Star Schema)</i>. Esta estructura permite "
        "entrenar algoritmos de agrupamiento (Clustering), clasificación y regresión sin incurrir en penalizaciones computacionales "
        "por múltiples uniones en tiempo de ejecución, optimizando los tiempos de procesamiento en Big Data.", body_style
    ))

    # =========================================================================
    # 4. JUSTIFICACIÓN DE HERRAMIENTAS Y TECNOLOGÍAS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Justificación de Herramientas y Tecnologías", h1_style))
    
    tools = [
        ("SQLite3 (Motor de Persistencia Analítica)", 
         "Actúa como emulador local de alta eficiencia de un Data Lakehouse / Data Warehouse en la nube. Proporciona almacenamiento "
         "ligero, embebido, sin requerir despliegue de infraestructura pesada en etapas de desarrollo, ofreciendo compatibilidad SQL estándar y transacciones ACID."),
        ("Pandas y NumPy (Capa de Preprocesamiento y ETL)", 
         "Librerías líderes en el ecosistema de Python para manipulación vectorial en memoria. Permiten transformaciones matriciales, "
         "tratamiento masivo de valores nulos, normalizaciones Min-Max y cálculos vectorizados (como el BMI e índices compuestos) con alta velocidad."),
        ("PySpark / Ecosistema Distribuido (Simulación de Escalabilidad)", 
         "Para cargas de trabajo que superan la memoria RAM de un nodo (escala de Terabytes), el pipeline está concebido para interoperar "
         "con PySpark mediante DataFrames distribuidos (Resilient Distributed Datasets / Catalyst Optimizer) en clusters de procesamiento."),
        ("GitHub Actions (Orquestación CI/CD y Calidad de Datos)", 
         "Plataforma de automatización de flujos de trabajo en la nube. Permite ejecutar de forma desatendida el pipeline ante cada cambio en el código, "
         "validar aserciones de integridad de datos mediante pruebas automáticas y publicar artefactos de evidencia (bases de datos, hojas Excel y reportes TXT).")
    ]
    for title, desc in tools:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", body_style))

    # =========================================================================
    # 5. SIMULACIÓN CLOUD VS NUBE REAL
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Simulación del Entorno Cloud vs Nube Real", h1_style))
    story.append(Paragraph(
        "El proyecto fue diseñado bajo el principio de <i>Portabilidad Cloud-Native</i>. La siguiente tabla presenta el mapeo directo de cada componente "
        "local simulado hacia los servicios administrados de los tres proveedores líderes de nube (AWS, GCP y Azure):", body_style
    ))

    cloud_map = [
        [Paragraph("Fase / Componente", tbl_header_style), Paragraph("Simulación Local", tbl_header_style), Paragraph("AWS", tbl_header_style), Paragraph("GCP", tbl_header_style), Paragraph("Microsoft Azure", tbl_header_style)],
        [Paragraph("<b>Almacenamiento Crudo (Bronze)</b>", tbl_cell_style), Paragraph("players_20.csv / SQLite", tbl_cell_style), Paragraph("Amazon S3 (Raw Bucket)", tbl_cell_style), Paragraph("Google Cloud Storage (GCS)", tbl_cell_style), Paragraph("Azure Blob / ADLS Gen2", tbl_cell_style)],
        [Paragraph("<b>Motor de Procesamiento (Silver)</b>", tbl_cell_style), Paragraph("Python / Pandas", tbl_cell_style), Paragraph("AWS Glue / EMR Spark", tbl_cell_style), Paragraph("Dataproc / Dataflow", tbl_cell_style), Paragraph("Azure Synapse Spark Pool", tbl_cell_style)],
        [Paragraph("<b>Capa Analítica (Gold)</b>", tbl_cell_style), Paragraph("SQLite (ingestion.db)", tbl_cell_style), Paragraph("Amazon Athena / Redshift", tbl_cell_style), Paragraph("Google BigQuery", tbl_cell_style), Paragraph("Azure Synapse Analytics", tbl_cell_style)],
        [Paragraph("<b>Orquestación y CI/CD</b>", tbl_cell_style), Paragraph("GitHub Actions", tbl_cell_style), Paragraph("AWS Step Functions / MWAA", tbl_cell_style), Paragraph("Cloud Composer (Airflow)", tbl_cell_style), Paragraph("Azure Data Factory (ADF)", tbl_cell_style)]
    ]
    t_cloud = Table(cloud_map, colWidths=[90, 85, 100, 100, 105])
    t_cloud.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_cloud)

    # =========================================================================
    # 6. FLUJO DE AUTOMATIZACIÓN Y TRAZABILIDAD
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Flujo de Datos y Automatización en GitHub Actions", h1_style))
    story.append(Paragraph(
        "El flujo de trabajo automatizado (configurado en <code>.github/workflows/bigdata.yml</code>) asegura la reproducibilidad técnica completa. "
        "En cada ejecución se siguen las siguientes fases:", body_style
    ))
    
    ci_steps = [
        "<b>1. Aprovisionamiento:</b> Instancia virtual Ubuntu Latest con Python 3.11 y caché de dependencias.",
        "<b>2. Instalación de Dependencias:</b> Instalación determinística desde <code>requirements.txt</code>.",
        "<b>3. Ejecución del Pipeline:</b> Invocación secuencial de la ingesta, preprocesamiento y enriquecimiento multiformato.",
        "<b>4. Pruebas de Aserción e Integridad:</b> Validación formal de la existencia no vacía de <code>ingestion.db</code>, <code>enriched_data.xlsx</code> y <code>enriched_report.txt</code>.",
        "<b>5. Auditoría en Logs:</b> Despliegue en tiempo real del informe de auditoría con las tasas de coincidencia del 100%.",
        "<b>6. Publicación de Artefactos:</b> Empaquetado y almacenamiento de las evidencias (retención de 30 días) accesibles para revisión docente."
    ]
    for cs in ci_steps:
        story.append(Paragraph(f"• {cs}", bullet_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # 7. CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    story.append(Paragraph("7. Conclusiones y Recomendaciones", h1_style))
    
    story.append(Paragraph("<b>Principales Beneficios de la Arquitectura:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Integridad y Calidad Garantizada:</b> Reducción del 100% de valores nulos en variables clave y cero pérdida de registros en las operaciones de cruce multiformato.<br/>"
        "• <b>Modularidad y Mantenibilidad:</b> Separación clara de responsabilidades en scripts independientes para ingesta, limpieza y enriquecimiento.<br/>"
        "• <b>Automatización Continua:</b> Eliminación de tareas operativas manuales gracias a GitHub Actions.", body_style
    ))

    story.append(Paragraph("<b>Recomendaciones para Implementación en Producción:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Adopción de Almacenamiento Formato Parquet / Delta Lake:</b> Migrar el formato de almacenamiento de SQLite a Apache Parquet con compresión Snappy para optimizar lecturas columnares en Big Data.<br/>"
        "• <b>Implementación de Data Governance:</b> Incorporar herramientas de catálogo de datos como Apache Atlas o Google Dataplex para trazabilidad de linaje.<br/>"
        "• <b>Monitoreo y Alertas en Tiempo Real:</b> Integrar alertas automáticas vía Slack o correo ante caídas en las tasas de match o fallos en las fuentes externas.", body_style
    ))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=10, spaceBefore=5))
    story.append(Paragraph("<b>Fin del Documento Técnico de Arquitectura</b> | Institución Universitaria Digital de Antioquia", ParagraphStyle('End', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor("#666666"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Documento PDF compilado en: {output_pdf_path}")


if __name__ == "__main__":
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    os.makedirs(docs_dir, exist_ok=True)
    pdf_target = os.path.join(docs_dir, "arquitectura_modelo.pdf")
    build_pdf_document(pdf_target)
