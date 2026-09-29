import os
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def save_fig_clean(fig, output_path, dpi=300):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    with open(output_path, "wb") as f:
        f.write(buf.getvalue())


def create_architecture_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Title
    ax.text(7, 8.5, "ARQUITECTURA DE DATOS BIG DATA - MEDALLION & CI/CD", 
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1a237e")

    # Colors
    c_source = "#e8eaf6"
    c_bronze = "#ffe0b2"
    c_silver = "#e0f2f1"
    c_gold = "#fff9c4"
    c_output = "#f3e5f5"
    c_cicd = "#eceff1"

    # 1. Sources Box
    rect_sources = patches.FancyBboxPatch((0.5, 1.5), 2.5, 6.2, boxstyle="round,pad=0.2", 
                                         ec="#3949ab", fc=c_source, lw=1.8)
    ax.add_patch(rect_sources)
    ax.text(1.75, 7.3, "FUENTES HETEROGÉNEAS\n(MULTIFORMATO)", ha="center", va="center", 
            fontsize=10, fontweight="bold", color="#1a237e")
    
    sources = [
        "• REST API (JSON)",
        "• players_20.csv",
        "• countries_info.json",
        "• club_leagues.csv",
        "• stadiums_info.xml",
        "• national_trophies.html",
        "• player_contracts.txt",
        "• sponsorship.xlsx"
    ]
    for i, s in enumerate(sources):
        ax.text(0.7, 6.3 - (i * 0.6), s, fontsize=8.5, color="#283593")

    # 2. Bronze / Ingestion Box
    rect_bronze = patches.FancyBboxPatch((3.5, 4.8), 2.6, 2.9, boxstyle="round,pad=0.2", 
                                        ec="#e65100", fc=c_bronze, lw=1.8)
    ax.add_patch(rect_bronze)
    ax.text(4.8, 7.3, "CAPA BRONZE (RAW)\nIngestión Base", ha="center", va="center", 
            fontsize=10, fontweight="bold", color="#e65100")
    ax.text(4.8, 6.3, "• ingestion.py\n• SQLite: raw_players\n• Validación de conexión\n• 18,278 registros", 
            ha="center", va="center", fontsize=8.5, color="#bf360c")

    # 3. Silver / Cleaning Box
    rect_silver = patches.FancyBboxPatch((6.6, 4.8), 2.6, 2.9, boxstyle="round,pad=0.2", 
                                        ec="#004d40", fc=c_silver, lw=1.8)
    ax.add_patch(rect_silver)
    ax.text(7.9, 7.3, "CAPA SILVER (CLEAN)\nLimpieza y Preproceso", ha="center", va="center", 
            fontsize=10, fontweight="bold", color="#004d40")
    ax.text(7.9, 6.3, "• cleaning.py\n• SQLite: cleaned_players\n• Imputación de nulos\n• BMI, Normalización", 
            ha="center", va="center", fontsize=8.5, color="#004d40")

    # 4. Gold / Enrichment Box
    rect_gold = patches.FancyBboxPatch((9.7, 4.8), 2.6, 2.9, boxstyle="round,pad=0.2", 
                                      ec="#f57f17", fc=c_gold, lw=1.8)
    ax.add_patch(rect_gold)
    ax.text(11.0, 7.3, "CAPA GOLD (ENRICHED)\nEnriquecimiento y Joins", ha="center", va="center", 
            fontsize=10, fontweight="bold", color="#f57f17")
    ax.text(11.0, 6.3, "• enrichement.py\n• SQLite: enriched_players\n• Joins 6 formatos\n• 44 columnas analíticas", 
            ha="center", va="center", fontsize=8.5, color="#e65100")

    # 5. Output Evidences Box
    rect_output = patches.FancyBboxPatch((5.0, 0.6), 7.3, 1.8, boxstyle="round,pad=0.2", 
                                         ec="#4a148c", fc=c_output, lw=1.8)
    ax.add_patch(rect_output)
    ax.text(8.65, 2.0, "EVIDENCIAS Y ARTEFACTOS ANALÍTICOS GENERADOS", ha="center", va="center", 
            fontsize=10, fontweight="bold", color="#4a148c")
    ax.text(8.65, 1.2, "• SQLite: ingestion.db   |   • Excel: enriched_data.xlsx   |   • Auditoría: enriched_report.txt (100% Match)", 
            ha="center", va="center", fontsize=8.5, color="#4a148c")

    # 6. CI/CD Box
    rect_cicd = patches.FancyBboxPatch((3.5, 2.8), 8.8, 1.6, boxstyle="round,pad=0.2", 
                                      ec="#37474f", fc=c_cicd, lw=1.8)
    ax.add_patch(rect_cicd)
    ax.text(7.9, 4.0, "AUTOMATIZACIÓN CI/CD - GITHUB ACTIONS WORKFLOW (bigdata.yml)", 
            ha="center", va="center", fontsize=10, fontweight="bold", color="#263238")
    ax.text(7.9, 3.2, "Disparador (Push / Dispatch)  -->  Setup Python 3.11  -->  Ejecución Pipeline  -->  Asserts de Integridad  -->  Upload Artifacts", 
            ha="center", va="center", fontsize=8, color="#37474f")

    # Arrows
    arrow_style = dict(arrowstyle="->", lw=2, color="#1a237e")
    ax.annotate("", xy=(3.5, 6.25), xytext=(3.0, 6.25), arrowprops=arrow_style)
    ax.annotate("", xy=(6.6, 6.25), xytext=(6.1, 6.25), arrowprops=arrow_style)
    ax.annotate("", xy=(9.7, 6.25), xytext=(9.2, 6.25), arrowprops=arrow_style)
    ax.annotate("", xy=(8.65, 2.4), xytext=(8.65, 2.8), arrowprops=arrow_style)

    plt.tight_layout()
    save_fig_clean(fig, output_path, dpi=300)
    print(f"[OK] Diagrama de arquitectura generado en: {output_path}")


def draw_table_card(ax, x, y, width, height, header_title, header_bg, body_bg, fields, pk_list=None, fk_list=None):
    """Dibuja una tarjeta de tabla de base de datos con encabezado diferenciado y lista de campos sin solapamiento."""
    header_h = 0.65
    body_h = height - header_h
    pk_list = pk_list or []
    fk_list = fk_list or []

    # Fondo del cuerpo de la tabla
    rect_body = patches.Rectangle((x, y), width, body_h, facecolor=body_bg, edgecolor=header_bg, linewidth=1.5)
    ax.add_patch(rect_body)

    # Encabezado
    rect_head = patches.Rectangle((x, y + body_h), width, header_h, facecolor=header_bg, edgecolor=header_bg, linewidth=1.5)
    ax.add_patch(rect_head)

    # Texto del encabezado
    ax.text(x + width / 2.0, y + body_h + (header_h / 2.0), header_title,
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="white")

    # Campos de la tabla (con espaciado vertical distribuido)
    line_spacing = (body_h - 0.3) / max(len(fields), 1)
    for idx, (col_name, col_type) in enumerate(fields):
        field_y = (y + body_h - 0.25) - (idx * line_spacing)
        
        prefix = ""
        font_wt = "normal"
        txt_color = "#212121"
        
        if col_name in pk_list:
            prefix = "[PK] "
            font_wt = "bold"
            txt_color = "#b71c1c"
        elif col_name in fk_list:
            prefix = "[FK] "
            font_wt = "bold"
            txt_color = "#0d47a1"

        ax.text(x + 0.2, field_y, f"{prefix}{col_name}", ha="left", va="center", fontsize=8, fontweight=font_wt, color=txt_color)
        ax.text(x + width - 0.2, field_y, col_type, ha="right", va="center", fontsize=7.5, color="#555555", style="italic")


def create_er_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    ax.text(7.5, 9.0, "MODELO DE DATOS ENTIDAD - RELACIÓN (DATA MODEL ER)", 
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0d47a1")

    # 1. TABLA CENTRAL: enriched_players
    main_fields = [
        ("sofifa_id", "INTEGER"),
        ("short_name", "TEXT"),
        ("long_name", "TEXT"),
        ("age", "INTEGER"),
        ("height_cm / weight_kg", "INTEGER"),
        ("nationality", "TEXT"),
        ("club", "TEXT"),
        ("overall / potential", "INTEGER"),
        ("value_eur / wage_eur", "REAL"),
        ("bmi / potential_growth", "REAL"),
        ("overall_normalized", "REAL"),
        ("wage_tier / market_tier", "TEXT"),
        ("is_intercontinental", "INTEGER"),
        ("star_rating_index", "REAL")
    ]
    draw_table_card(
        ax, x=4.8, y=1.2, width=5.4, height=6.8,
        header_title="enriched_players (Tabla Maestra Gold)",
        header_bg="#0d47a1", body_bg="#f0f7ff",
        fields=main_fields,
        pk_list=["sofifa_id"],
        fk_list=["nationality", "club"]
    )

    # 2. TABLA: countries_info (JSON / HTML)
    countries_fields = [
        ("nationality", "TEXT"),
        ("continent", "TEXT"),
        ("fifa_confederation", "TEXT"),
        ("country_iso3", "TEXT"),
        ("fifa_ranking_tier", "TEXT"),
        ("world_cup_titles", "INTEGER"),
        ("continental_trophies", "INTEGER")
    ]
    draw_table_card(
        ax, x=0.5, y=5.0, width=3.7, height=3.0,
        header_title="countries_info (JSON / HTML)",
        header_bg="#1b5e20", body_bg="#f1f8e9",
        fields=countries_fields,
        pk_list=["nationality"]
    )

    # 3. TABLA: club_leagues (CSV)
    leagues_fields = [
        ("club", "TEXT"),
        ("league_name", "TEXT"),
        ("league_country", "TEXT"),
        ("league_tier", "INTEGER"),
        ("is_top_5_european_league", "INTEGER")
    ]
    draw_table_card(
        ax, x=10.8, y=5.2, width=3.7, height=2.8,
        header_title="club_leagues (CSV)",
        header_bg="#e65100", body_bg="#fff8e1",
        fields=leagues_fields,
        pk_list=["club"]
    )

    # 4. TABLA: player_contracts (TXT)
    contracts_fields = [
        ("sofifa_id", "INTEGER"),
        ("contract_tier", "TEXT"),
        ("rep_stars", "INTEGER")
    ]
    draw_table_card(
        ax, x=0.5, y=1.5, width=3.7, height=2.2,
        header_title="player_contracts (TXT)",
        header_bg="#880e4f", body_bg="#fce4ec",
        fields=contracts_fields,
        pk_list=["sofifa_id"]
    )

    # 5. TABLA: stadiums_info (XML / XLSX)
    stadiums_fields = [
        ("club", "TEXT"),
        ("stadium_name", "TEXT"),
        ("stadium_capacity", "INTEGER"),
        ("main_sponsor", "TEXT"),
        ("sponsor_tier", "TEXT")
    ]
    draw_table_card(
        ax, x=10.8, y=1.5, width=3.7, height=2.6,
        header_title="stadiums_sponsors (XML / XLSX)",
        header_bg="#4a148c", body_bg="#f3e5f5",
        fields=stadiums_fields,
        pk_list=["club"]
    )

    # Connectors / Relationships
    arrow_style = dict(arrowstyle="<->", lw=1.8, color="#0d47a1")

    # countries_info <-> enriched_players (1:N)
    ax.annotate("", xy=(4.2, 6.5), xytext=(4.8, 6.5), arrowprops=arrow_style)
    ax.text(4.5, 6.75, "1 : N", fontsize=8.5, fontweight="bold", color="#0d47a1", ha="center")

    # club_leagues <-> enriched_players (N:1)
    ax.annotate("", xy=(10.2, 6.5), xytext=(10.8, 6.5), arrowprops=arrow_style)
    ax.text(10.5, 6.75, "N : 1", fontsize=8.5, fontweight="bold", color="#0d47a1", ha="center")

    # player_contracts <-> enriched_players (1:1)
    ax.annotate("", xy=(4.2, 2.6), xytext=(4.8, 2.6), arrowprops=arrow_style)
    ax.text(4.5, 2.85, "1 : 1", fontsize=8.5, fontweight="bold", color="#0d47a1", ha="center")

    # stadiums_sponsors <-> enriched_players (N:1)
    ax.annotate("", xy=(10.2, 2.8), xytext=(10.8, 2.8), arrowprops=arrow_style)
    ax.text(10.5, 3.05, "N : 1", fontsize=8.5, fontweight="bold", color="#0d47a1", ha="center")

    plt.tight_layout()
    save_fig_clean(fig, output_path, dpi=300)
    print(f"[OK] Diagrama ER generado exitosamente sin solapamientos en: {output_path}")


if __name__ == "__main__":
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    os.makedirs(docs_dir, exist_ok=True)
    create_architecture_diagram(os.path.join(docs_dir, "diagrama_arquitectura.png"))
    create_er_diagram(os.path.join(docs_dir, "diagrama_modelo_er.png"))
    # Clean test file
    test_path = os.path.join(docs_dir, "test_fig.png")
    if os.path.exists(test_path):
        os.remove(test_path)
