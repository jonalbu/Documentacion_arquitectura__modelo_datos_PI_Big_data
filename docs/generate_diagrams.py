import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Diagrama de arquitectura generado en: {output_path}")


def create_er_diagram(output_path: str):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(7, 8.5, "MODELO DE DATOS ENTIDAD - RELACIÓN (DATA MODEL ER)", 
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0d47a1")

    # Central Table: ENRICHED_PLAYERS
    rect_main = patches.FancyBboxPatch((4.5, 2.2), 5.0, 5.2, boxstyle="round,pad=0.2", 
                                      ec="#0d47a1", fc="#e3f2fd", lw=2.2)
    ax.add_patch(rect_main)
    ax.text(7.0, 7.0, "TABLA PRINCIPAL: enriched_players", ha="center", va="center", 
            fontsize=11, fontweight="bold", color="#0d47a1")
    
    fields_main = [
        "PK  sofifa_id (INTEGER)",
        "    short_name / long_name (TEXT)",
        "    age, height_cm, weight_kg (INTEGER)",
        "    overall, potential (INTEGER)",
        "    value_eur, wage_eur (REAL)",
        "FK  nationality (TEXT)",
        "FK  club (TEXT)",
        "    pace, shooting, passing... (REAL)",
        "    bmi, potential_growth (REAL)",
        "    overall_normalized (REAL)",
        "    wage_tier, market_value_tier (TEXT)",
        "    is_intercontinental (INTEGER)",
        "    star_rating_index (REAL)"
    ]
    for idx, f in enumerate(fields_main):
        ax.text(4.8, 6.4 - (idx * 0.32), f, fontsize=8, color="#01579b", 
                fontweight="bold" if "PK" in f or "FK" in f else "normal")

    # Peripheral Tables
    # 1. Countries (JSON / HTML)
    r1 = patches.FancyBboxPatch((0.5, 5.0), 3.4, 2.4, boxstyle="round,pad=0.2", ec="#2e7d32", fc="#e8f5e9", lw=1.5)
    ax.add_patch(r1)
    ax.text(2.2, 7.1, "countries_info (JSON/HTML)", ha="center", va="center", fontsize=9, fontweight="bold", color="#1b5e20")
    ax.text(0.7, 6.5, "PK nationality (TEXT)\n   continent (TEXT)\n   fifa_confederation (TEXT)\n   fifa_ranking_tier (TEXT)\n   world_cup_titles (INT)\n   continental_trophies (INT)", fontsize=7.5, color="#1b5e20")

    # 2. Club Leagues (CSV)
    r2 = patches.FancyBboxPatch((10.1, 5.0), 3.4, 2.4, boxstyle="round,pad=0.2", ec="#ef6c00", fc="#fff3e0", lw=1.5)
    ax.add_patch(r2)
    ax.text(11.8, 7.1, "club_leagues (CSV)", ha="center", va="center", fontsize=9, fontweight="bold", color="#e65100")
    ax.text(10.3, 6.5, "PK club (TEXT)\n   league_name (TEXT)\n   league_country (TEXT)\n   league_tier (INT)\n   is_top_5_european_league (INT)", fontsize=7.5, color="#bf360c")

    # 3. Stadiums (XML)
    r3 = patches.FancyBboxPatch((10.1, 1.8), 3.4, 2.4, boxstyle="round,pad=0.2", ec="#6a1b9a", fc="#f3e5f5", lw=1.5)
    ax.add_patch(r3)
    ax.text(11.8, 3.9, "stadiums_info (XML)", ha="center", va="center", fontsize=9, fontweight="bold", color="#4a148c")
    ax.text(10.3, 3.3, "PK club (TEXT)\n   stadium_name (TEXT)\n   stadium_capacity (INT)\n   main_sponsor (TEXT)\n   sponsor_tier (TEXT)", fontsize=7.5, color="#4a148c")

    # 4. Contracts (TXT)
    r4 = patches.FancyBboxPatch((0.5, 1.8), 3.4, 2.4, boxstyle="round,pad=0.2", ec="#c2185b", fc="#fce4ec", lw=1.5)
    ax.add_patch(r4)
    ax.text(2.2, 3.9, "player_contracts (TXT)", ha="center", va="center", fontsize=9, fontweight="bold", color="#880e4f")
    ax.text(0.7, 3.3, "PK sofifa_id (INT)\n   contract_tier (TEXT)\n   rep_stars (INT)", fontsize=7.5, color="#880e4f")

    # Relationship connectors
    rel_style = dict(arrowstyle="<->", lw=1.8, color="#0d47a1")
    ax.annotate("", xy=(3.9, 6.2), xytext=(4.5, 6.2), arrowprops=rel_style)
    ax.text(4.2, 6.4, "1:N", fontsize=8, fontweight="bold", color="#0d47a1", ha="center")

    ax.annotate("", xy=(9.5, 6.2), xytext=(10.1, 6.2), arrowprops=rel_style)
    ax.text(9.8, 6.4, "N:1", fontsize=8, fontweight="bold", color="#0d47a1", ha="center")

    ax.annotate("", xy=(9.5, 3.0), xytext=(10.1, 3.0), arrowprops=rel_style)
    ax.text(9.8, 3.2, "N:1", fontsize=8, fontweight="bold", color="#0d47a1", ha="center")

    ax.annotate("", xy=(3.9, 3.0), xytext=(4.5, 3.0), arrowprops=rel_style)
    ax.text(4.2, 3.2, "1:1", fontsize=8, fontweight="bold", color="#0d47a1", ha="center")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Diagrama ER generado en: {output_path}")


if __name__ == "__main__":
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    os.makedirs(docs_dir, exist_ok=True)
    create_architecture_diagram(os.path.join(docs_dir, "diagrama_arquitectura.png"))
    create_er_diagram(os.path.join(docs_dir, "diagrama_modelo_er.png"))
