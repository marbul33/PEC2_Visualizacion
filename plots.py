import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ==============================================================================
# PLANTILLA HTML EDITORIAL (ESTILO THE ECONOMIST / OUR WORLD IN DATA)
# ==============================================================================
def guardar_html_editorial(fig, filename, titulo_pestana, url_activa):
    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={"displayModeBar": False, "responsive": True},
    )

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo_pestana} | PEC 2 Visualización de Datos</title>
    <style>
        :root {{ --bg: #f8fafc; --card: #ffffff; --text: #0f172a; --muted: #475569; --accent: #0284c7; --border: #e2e8f0; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; padding-bottom: 40px; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
        .brand {{ font-weight: 700; font-size: 0.95rem; color: var(--text); text-decoration: none; }}
        nav {{ display: flex; gap: 10px; }}
        nav a {{ text-decoration: none; font-size: 0.85rem; font-weight: 600; color: var(--muted); padding: 6px 14px; border-radius: 6px; transition: all 0.15s; }}
        nav a:hover {{ background: #f1f5f9; color: var(--text); }}
        nav a.active {{ background: var(--text); color: #fff; }}
        main {{ max-width: 1120px; margin: 28px auto; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 28px 32px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03); }}
        footer {{ max-width: 1120px; margin: 12px auto 0; padding: 0 8px; font-size: 0.8rem; color: var(--muted); display: flex; justify-content: space-between; }}
        footer a {{ color: var(--accent); text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <a class="brand" href="index.html">PEC 2 · Técnicas de Visualización de Datos</a>
        <nav>
            <a href="index.html" class="{"active" if url_activa == "index" else ""}">Inicio y URLs</a>
            <a href="small-multiple.html" class="{"active" if url_activa == "sm" else ""}">1. Small Multiple</a>
            <a href="slope-chart.html" class="{"active" if url_activa == "sc" else ""}">2. Slope Chart</a>
            <a href="connected-scatterplot.html" class="{"active" if url_activa == "cs" else ""}">3. Connected Scatterplot</a>
        </nav>
    </header>
    <main>
        {plot_html}
    </main>
    <footer>
        <span>Diseño optimizado para evaluación de carga cognitiva y percepción visual (PEC 2)</span>
        <span>Datos abiertos descargables en el repositorio: <a href="datos_small_multiple.csv">CSV 1</a> · <a href="datos_slope_chart.csv">CSV 2</a> · <a href="datos_connected_scatterplot.csv">CSV 3</a></span>
    </footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)


# ==============================================================================
# 1. TÉCNICA GRUPO I: SMALL MULTIPLE (Energía Renovable en la UE 2000-2024)
# ==============================================================================
years_sm = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
data_sm = {
    "Dinamarca": [16.7, 27.1, 28.9, 48.3, 60.5, 81.6, 88.4],
    "Suecia": [55.4, 46.1, 55.6, 59.8, 57.1, 68.5, 71.2],
    "Portugal": [30.5, 24.5, 32.9, 45.2, 55.5, 59.6, 68.1],
    "España": [15.6, 18.2, 23.7, 33.5, 38.6, 44.0, 56.8],
    "Alemania": [6.6, 9.5, 15.1, 23.5, 29.8, 44.9, 57.5],
    "Países Bajos": [3.9, 6.7, 8.9, 12.1, 12.5, 26.5, 51.4],
    "Italia": [18.8, 17.9, 21.8, 31.0, 37.4, 41.7, 45.2],
    "Francia": [15.1, 13.5, 14.4, 16.5, 19.6, 24.8, 27.9],
    "Polonia": [1.7, 2.1, 4.4, 10.7, 13.8, 16.3, 29.1],
}

# Guardar CSV limpio
rows_sm = [
    {"Pais": p, "Anio": y, "Renovable_pct": v}
    for p, vals in data_sm.items()
    for y, v in zip(years_sm, vals)
]
pd.DataFrame(rows_sm).to_csv("datos_small_multiple.csv", index=False)

paises_sm = list(data_sm.keys())
fig_sm = make_subplots(
    rows=3,
    cols=3,
    shared_xaxes=True,
    shared_yaxes=True,
    subplot_titles=[
        f"<b>{p}</b> ({data_sm[p][0]}% → {data_sm[p][-1]}%)" for p in paises_sm
    ],
    vertical_spacing=0.11,
    horizontal_spacing=0.06,
)

# Color jerárquico: Azul intenso para los de mayor aceleración, gris azulado para el resto
colores_sm = {
    "Dinamarca": "#0284c7",
    "España": "#0284c7",
    "Alemania": "#0284c7",
    "Países Bajos": "#0284c7",
    "Suecia": "#334155",
    "Portugal": "#334155",
    "Italia": "#64748b",
    "Francia": "#dc2626",
    "Polonia": "#d97706",
}

for idx, pais_foco in enumerate(paises_sm):
    r, c = (idx // 3) + 1, (idx % 3) + 1

    # 1) Líneas de fondo (los otros 8 países en gris claro para dar contexto visual inmediato)
    for pais_bg, vals_bg in data_sm.items():
        if pais_bg != pais_foco:
            fig_sm.add_trace(
                go.Scatter(
                    x=years_sm,
                    y=vals_bg,
                    mode="lines",
                    line=dict(color="#e2e8f0", width=1.4),
                    hoverinfo="skip",
                    showlegend=False,
                ),
                row=r,
                col=c,
            )

    # 2) Serie protagonista del panel con área sombreada suave y etiquetas en extremos
    vals_foco = data_sm[pais_foco]
    color_f = colores_sm[pais_foco]
    fig_sm.add_trace(
        go.Scatter(
            x=years_sm,
            y=vals_foco,
            mode="lines+markers+text",
            line=dict(color=color_f, width=3.2),
            marker=dict(size=[7, 0, 0, 0, 0, 0, 8], color=color_f),
            fill="tozeroy",
            fillcolor="rgba(2, 132, 199, 0.08)"
            if color_f == "#0284c7"
            else "rgba(100, 116, 139, 0.06)",
            text=[f"{vals_foco[0]}%", "", "", "", "", "", f"<b>{vals_foco[-1]}%</b>"],
            textposition=[
                "top right",
                "top center",
                "top center",
                "top center",
                "top center",
                "top center",
                "top left",
            ],
            textfont=dict(size=11, color=color_f),
            name=pais_foco,
            hovertemplate=f"<b>{pais_foco}</b> (%{{x}}): %{{y:.1f}}%<extra></extra>",
            showlegend=False,
        ),
        row=r,
        col=c,
    )

fig_sm.update_layout(
    title=dict(
        text="<b>La transformación asimétrica de la electricidad verde en Europa (2000–2024)</b><br>"
        "<span style='font-size:14px;color:#475569'>Cuota de generación eléctrica renovable (%). Cada panel resalta un país frente a los otros ocho en gris de fondo.</span>",
        x=0.0,
        y=0.98,
    ),
    height=720,
    margin=dict(t=95, b=50, l=45, r=25),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI, Roboto, sans-serif", color="#0f172a"),
)
fig_sm.update_xaxes(
    range=[1998.5, 2025.8],
    tickvals=[2000, 2012, 2024],
    showgrid=False,
    linecolor="#cbd5e1",
)
fig_sm.update_yaxes(range=[0, 100], ticksuffix="%", gridcolor="#f1f5f9", zeroline=False)

guardar_html_editorial(fig_sm, "small-multiple.html", "Small Multiple", "sm")


# ==============================================================================
# 2. TÉCNICA GRUPO II: SLOPE CHART (Teletrabajo en Europa: 2019 vs 2024)
# ==============================================================================
df_slope = pd.DataFrame(
    [
        {
            "Pais": "Países Bajos",
            "y2019": 14.1,
            "y2024": 52.3,
            "Grupo": "Salto estructural (+38,2 pp)",
        },
        {
            "Pais": "Irlanda",
            "y2019": 7.0,
            "y2024": 37.8,
            "Grupo": "Salto estructural (+30,8 pp)",
        },
        {
            "Pais": "Finlandia",
            "y2019": 14.5,
            "y2024": 39.2,
            "Grupo": "Consolidación alta",
        },
        {"Pais": "Suecia", "y2019": 5.9, "y2024": 34.1, "Grupo": "Consolidación alta"},
        {"Pais": "Alemania", "y2019": 5.2, "y2024": 23.6, "Grupo": "Crecimiento medio"},
        {"Pais": "Francia", "y2019": 7.0, "y2024": 21.8, "Grupo": "Crecimiento medio"},
        {
            "Pais": "España",
            "y2019": 4.8,
            "y2024": 15.1,
            "Grupo": "Rezago relativo (+10,3 pp)",
        },
        {
            "Pais": "Italia",
            "y2019": 3.6,
            "y2024": 12.2,
            "Grupo": "Rezago relativo (+8,6 pp)",
        },
    ]
)
df_slope.to_csv("datos_slope_chart.csv", index=False)

fig_sc = go.Figure()

# Líneas verticales de los dos estados temporales (2019 y 2024)
for x_pos, label_anio in [
    (0, "<b>2019</b> (Pre-pandemia)"),
    (1, "<b>2024</b> (Nuevo equilibrio)"),
]:
    fig_sc.add_shape(
        type="line",
        x0=x_pos,
        x1=x_pos,
        y0=0,
        y1=56,
        line=dict(color="#cbd5e1", width=2),
    )
    fig_sc.add_annotation(
        x=x_pos,
        y=58.5,
        text=label_anio,
        showarrow=False,
        font=dict(size=14, color="#0f172a"),
    )

# Pequeños ajustes de posición Y en etiquetas izquierdas/derechas para evitar solapamiento (overplotting)
y_offset_2019 = {
    "Países Bajos": -0.8,
    "Finlandia": 0.8,
    "Irlanda": 0.6,
    "Francia": -0.6,
    "Suecia": 0.3,
    "Alemania": -0.4,
    "España": 0.2,
    "Italia": -0.3,
}

for _, row in df_slope.iterrows():
    pais = row["Pais"]
    es_lider = pais in ["Países Bajos", "Irlanda"]
    es_rezagado = pais in ["España", "Italia"]

    color_linea = "#0284c7" if es_lider else ("#e11d48" if es_rezagado else "#94a3b8")
    grosor = 3.8 if (es_lider or es_rezagado) else 1.8
    opacidad = 1.0 if (es_lider or es_rezagado) else 0.65
    diff = row["y2024"] - row["y2019"]

    fig_sc.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[row["y2019"], row["y2024"]],
            mode="lines+markers",
            line=dict(color=color_linea, width=grosor),
            marker=dict(size=9, color=color_linea),
            opacity=opacidad,
            name=pais,
            hovertemplate=f"<b>{pais}</b><br>2019: {row['y2019']}% → 2024: {row['y2024']}% (<b>+{diff:.1f} pp</b>)<extra></extra>",
            showlegend=False,
        )
    )

    # Etiquetas directas a la izquierda (2019) y a la derecha (2024)
    peso_txt = "<b>" if (es_lider or es_rezagado) else ""
    cierre_txt = "</b>" if (es_lider or es_rezagado) else ""
    color_txt = "#0f172a" if (es_lider or es_rezagado) else "#64748b"

    fig_sc.add_annotation(
        x=-0.03,
        y=row["y2019"] + y_offset_2019.get(pais, 0),
        text=f"{peso_txt}{pais}: {row['y2019']}%{cierre_txt}",
        xanchor="right",
        showarrow=False,
        font=dict(size=12, color=color_txt),
    )
    fig_sc.add_annotation(
        x=1.03,
        y=row["y2024"],
        text=f"{peso_txt}{pais}: {row['y2024']}% (+{diff:.1f} pp){cierre_txt}",
        xanchor="left",
        showarrow=False,
        font=dict(size=12, color=color_txt),
    )

# Anotación explicativa central
fig_sc.add_annotation(
    x=0.5,
    y=43,
    text="<b>Brecha norte-sur:</b><br>Irlanda y Suecia superan a Francia<br>mientras España e Italia quedan por debajo del 16%",
    showarrow=True,
    arrowhead=2,
    ax=-50,
    ay=-35,
    bgcolor="#f8fafc",
    bordercolor="#cbd5e1",
    borderwidth=1,
    borderpad=6,
    font=dict(size=11.5, color="#334155"),
)

fig_sc.update_layout(
    title=dict(
        text="<b>El teletrabajo divide Europa en dos velocidades tras la pandemia (2019 vs. 2024)</b><br>"
        "<span style='font-size:14px;color:#475569'>Porcentaje de ocupados que trabajan habitualmente o a veces desde casa (Eurostat). El ángulo refleja el salto estructural.</span>",
        x=0.0,
        y=0.97,
    ),
    height=680,
    margin=dict(t=95, b=40, l=180, r=220),
    xaxis=dict(range=[-0.35, 1.4], visible=False),
    yaxis=dict(range=[0, 62], visible=False),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI, Roboto, sans-serif"),
)

guardar_html_editorial(fig_sc, "slope-chart.html", "Slope Chart", "sc")


# ==============================================================================
# 3. TÉCNICA GRUPO III: CONNECTED SCATTERPLOT (Curva de Phillips España 2007-2024)
# ==============================================================================
df_cs = pd.DataFrame(
    [
        {
            "Anio": 2007,
            "Paro": 8.2,
            "Inflacion": 2.8,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2008,
            "Paro": 11.3,
            "Inflacion": 4.1,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2009,
            "Paro": 17.9,
            "Inflacion": -0.3,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2010,
            "Paro": 19.9,
            "Inflacion": 1.8,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2011,
            "Paro": 21.4,
            "Inflacion": 3.2,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2012,
            "Paro": 24.8,
            "Inflacion": 2.4,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2013,
            "Paro": 26.1,
            "Inflacion": 1.4,
            "Etapa": "1. Crisis Financiera y Deuda (2007–2013)",
        },
        {
            "Anio": 2014,
            "Paro": 24.4,
            "Inflacion": -0.2,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2015,
            "Paro": 22.1,
            "Inflacion": -0.5,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2016,
            "Paro": 19.6,
            "Inflacion": -0.2,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2017,
            "Paro": 17.2,
            "Inflacion": 2.0,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2018,
            "Paro": 15.3,
            "Inflacion": 1.7,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2019,
            "Paro": 14.1,
            "Inflacion": 0.7,
            "Etapa": "2. Recuperación y Desinflación (2014–2019)",
        },
        {
            "Anio": 2020,
            "Paro": 15.5,
            "Inflacion": -0.3,
            "Etapa": "3. Pandemia y Shock Inflacionario (2020–2024)",
        },
        {
            "Anio": 2021,
            "Paro": 14.8,
            "Inflacion": 3.1,
            "Etapa": "3. Pandemia y Shock Inflacionario (2020–2024)",
        },
        {
            "Anio": 2022,
            "Paro": 12.9,
            "Inflacion": 8.4,
            "Etapa": "3. Pandemia y Shock Inflacionario (2020–2024)",
        },
        {
            "Anio": 2023,
            "Paro": 12.2,
            "Inflacion": 3.5,
            "Etapa": "3. Pandemia y Shock Inflacionario (2020–2024)",
        },
        {
            "Anio": 2024,
            "Paro": 11.4,
            "Inflacion": 2.8,
            "Etapa": "3. Pandemia y Shock Inflacionario (2020–2024)",
        },
    ]
)
df_cs.to_csv("datos_connected_scatterplot.csv", index=False)

fig_cs = go.Figure()

# Línea de referencia de inflación 0% y objetivo BCE 2%
fig_cs.add_hline(y=0, line_dash="solid", line_color="#cbd5e1", line_width=1.5)
fig_cs.add_hline(
    y=2.0,
    line_dash="dot",
    line_color="#94a3b8",
    line_width=1.5,
    annotation_text="Objetivo BCE (2%)",
    annotation_position="bottom right",
    annotation_font=dict(size=11, color="#64748b"),
)

# Trazado por etapas con flechas direccionales para guiar la lectura cronológica
segmentos = [
    (df_cs.iloc[0:7], "#dc2626", "1. Gran Recesión (2007–2013)"),
    (df_cs.iloc[6:13], "#0284c7", "2. Recuperación (2014–2019)"),
    (df_cs.iloc[12:18], "#7c3aed", "3. Shock Pandemia y Energía (2020–2024)"),
]

for sub_df, color_seg, nombre_seg in segmentos:
    fig_cs.add_trace(
        go.Scatter(
            x=sub_df["Paro"],
            y=sub_df["Inflacion"],
            mode="lines+markers+text",
            line=dict(color=color_seg, width=3.2, shape="spline", smoothing=0.35),
            marker=dict(symbol="arrow", size=12, angleref="previous", color=color_seg),
            text=[
                str(a)
                if a
                in [
                    2007,
                    2008,
                    2009,
                    2011,
                    2013,
                    2015,
                    2017,
                    2019,
                    2020,
                    2021,
                    2022,
                    2024,
                ]
                else ""
                for a in sub_df["Anio"]
            ],
            textposition="top center",
            textfont=dict(size=11.5, color=color_seg),
            name=nombre_seg,
            customdata=sub_df["Anio"],
            hovertemplate="<b>Año %{customdata}</b><br>Desempleo: %{x:.1f}%<br>Inflación (IPC): %{y:.1f}%<extra></extra>",
        )
    )

# Anotaciones de los 3 hitos macroeconómicos clave
fig_cs.add_annotation(
    x=26.1,
    y=1.4,
    text="<b>2013: Máximo histórico de paro (26,1%)</b><br>Desplazamiento horizontal tras estallar la burbuja",
    showarrow=True,
    arrowhead=2,
    ax=-110,
    ay=-40,
    bgcolor="#fef2f2",
    bordercolor="#fca5a5",
    borderpad=5,
    font=dict(size=11),
)
fig_cs.add_annotation(
    x=12.9,
    y=8.4,
    text="<b>2022: Pico inflacionario (8,4%)</b><br>Shock energético mientras el paro sigue bajando",
    showarrow=True,
    arrowhead=2,
    ax=115,
    ay=10,
    bgcolor="#f5f3ff",
    bordercolor="#c4b5fd",
    borderpad=5,
    font=dict(size=11),
)
fig_cs.add_annotation(
    x=11.4,
    y=2.8,
    text="<b>2024: Aterrizaje suave</b><br>(11,4% paro | 2,8% IPC)",
    showarrow=True,
    arrowhead=2,
    ax=-90,
    ay=28,
    bgcolor="#f8fafc",
    bordercolor="#cbd5e1",
    borderpad=5,
    font=dict(size=11),
)

fig_cs.update_layout(
    title=dict(
        text="<b>Los tres ciclos de la Curva de Phillips en España (2007–2024)</b><br>"
        "<span style='font-size:14px;color:#475569'>Trayectoria conjunta de la Tasa de Desempleo (eje X) y la Inflación IPC (eje Y). Las flechas indican el avance temporal.</span>",
        x=0.0,
        y=0.97,
    ),
    height=680,
    margin=dict(t=95, b=65, l=65, r=40),
    xaxis=dict(
        title="<b>Tasa de Desempleo (% de la población activa)</b>",
        ticksuffix="%",
        range=[6.5, 28],
        gridcolor="#f1f5f9",
    ),
    yaxis=dict(
        title="<b>Inflación anual IPC (%)</b>",
        ticksuffix="%",
        range=[-1.5, 9.8],
        gridcolor="#f1f5f9",
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1.0),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI, Roboto, sans-serif", color="#0f172a"),
)

guardar_html_editorial(
    fig_cs, "connected-scatterplot.html", "Connected Scatterplot", "cs"
)


# ==============================================================================
# 4. PORTADA INDEX.HTML (PARA MOSTRAR EN LOS PRIMEROS 30 SEGUNDOS DEL VÍDEO)
# ==============================================================================
index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PEC 2 · Visualización de Datos</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; max-width: 960px; margin: 48px auto; padding: 0 24px; }
        .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
        h1 { font-size: 1.75rem; margin-bottom: 8px; }
        p.sub { color: #475569; margin-bottom: 24px; }
        .links { display: grid; gap: 16px; margin-top: 20px; }
        .link-box { display: flex; justify-content: space-between; align-items: center; padding: 18px 22px; border: 1px solid #cbd5e1; border-radius: 8px; text-decoration: none; color: #0f172a; transition: all 0.15s; }
        .link-box:hover { border-color: #0284c7; background: #f0f9ff; }
        .badge { background: #0284c7; color: #fff; padding: 4px 10px; border-radius: 99px; font-size: 0.78rem; font-weight: 600; }
        code { background: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; color: #0369a1; }
    </style>
</head>
<body>
    <div class="card">
        <h1>PEC 2 — Descubriendo técnicas de visualización</h1>
        <p class="sub">Repositorio público de visualizaciones interactivas con datos abiertos (Acceso directo sin registro)</p>
        <div class="links">
            <a class="link-box" href="small-multiple.html">
                <div>
                    <strong>Técnica Grupo I (Básicas y populares): Small Multiple</strong><br>
                    <small>Transición hacia la electricidad renovable en 9 economías europeas (2000–2024)</small>
                </div>
                <span class="badge">Abrir Visualización →</span>
            </a>
            <a class="link-box" href="slope-chart.html">
                <div>
                    <strong>Técnica Grupo II (Habituales y específicas): Slope Chart</strong><br>
                    <small>Evolución estructural del teletrabajo en la Unión Europea (2019 vs. 2024)</small>
                </div>
                <span class="badge">Abrir Visualización →</span>
            </a>
            <a class="link-box" href="connected-scatterplot.html">
                <div>
                    <strong>Técnica Grupo III (Menos habituales): Connected Scatterplot</strong><br>
                    <small>Dinámica bivariante de Desempleo e Inflación en España — Curva de Phillips (2007–2024)</small>
                </div>
                <span class="badge">Abrir Visualización →</span>
            </a>
        </div>
    </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("¡Listo! Se han generado index.html, los 3 gráficos HTML y los 3 archivos CSV.")
