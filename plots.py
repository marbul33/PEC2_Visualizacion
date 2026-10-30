import io
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ==============================================================================
# PLANTILLA HTML EDITORIAL
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
        <span>PEC 2 · Visualización de Datos — <strong>Marius Bulat Simon</strong></span>
        <span>Datos abiertos: <a href="datos_small_multiple.csv">CSV 1</a> · <a href="datos_slope_chart.csv">CSV 2</a> · <a href="datos_connected_scatterplot.csv">CSV 3</a></span>
    </footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)


HEADERS = {"User-Agent": "PEC2-VisualizacionDatos/1.0 (fetch script)"}


# ==============================================================================
# 1. TÉCNICA GRUPO I: SMALL MULTIPLE
# ==============================================================================
OWID_URL = (
    "https://ourworldindata.org/grapher/share-electricity-renewables.csv"
    "?v=1&csvType=full&useColumnShortNames=false"
)

paises_sm = [
    "Dinamarca",
    "Suecia",
    "Portugal",
    "España",
    "Alemania",
    "Países Bajos",
    "Italia",
    "Francia",
    "Polonia",
]

# Mapa
mapa_paises_owid = {
    "Dinamarca": "Denmark",
    "Suecia": "Sweden",
    "Portugal": "Portugal",
    "España": "Spain",
    "Alemania": "Germany",
    "Países Bajos": "Netherlands",
    "Italia": "Italy",
    "Francia": "France",
    "Polonia": "Poland",
}

years_sm = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

resp_owid = requests.get(OWID_URL, headers=HEADERS, timeout=60)
resp_owid.raise_for_status()
df_owid_raw = pd.read_csv(io.StringIO(resp_owid.text))


cols_fijas = {"Entity", "Code", "Year"}
col_valor_owid = [c for c in df_owid_raw.columns if c not in cols_fijas][0]
df_owid_raw = df_owid_raw.rename(columns={col_valor_owid: "Renovable_pct"})

df_owid_raw = df_owid_raw[df_owid_raw["Entity"].isin(mapa_paises_owid.values())]
df_owid_raw = df_owid_raw[df_owid_raw["Year"].isin(years_sm)]

mapa_inverso = {v: k for k, v in mapa_paises_owid.items()}
df_owid_raw["Pais"] = df_owid_raw["Entity"].map(mapa_inverso)

rows_sm = (
    df_owid_raw[["Pais", "Year", "Renovable_pct"]]
    .rename(columns={"Year": "Anio"})
    .sort_values(["Pais", "Anio"])
)
rows_sm.to_csv("datos_small_multiple.csv", index=False)


data_sm = {}
for pais in paises_sm:
    serie = rows_sm[rows_sm["Pais"] == pais].set_index("Anio")["Renovable_pct"]
    data_sm[pais] = [round(float(serie.get(y, float("nan"))), 1) for y in years_sm]

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
# 2. TÉCNICA GRUPO II: SLOPE CHART
# ==============================================================================
EUROSTAT_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/lfsa_ehomp/"
    "?format=SDMX-CSV&compressed=false"
)

mapa_paises_eurostat = {
    "Países Bajos": "NL",
    "Irlanda": "IE",
    "Finlandia": "FI",
    "Suecia": "SE",
    "Alemania": "DE",
    "Francia": "FR",
    "España": "ES",
    "Italia": "IT",
}

resp_eurostat = requests.get(EUROSTAT_URL, headers=HEADERS, timeout=120)
resp_eurostat.raise_for_status()
df_eurostat_raw = pd.read_csv(io.StringIO(resp_eurostat.text))
df_eurostat_raw.columns = [c.strip().lower() for c in df_eurostat_raw.columns]

# Filtramos la serie de interés: total empleo, 15-74 años, empleados, % del total.
# NOTA: la dimensión "frequenc" distingue trabajo habitual (USU), a veces (SMT)
# y nunca (NVR). El enunciado pide "habitualmente o a veces", así que sumamos
# USU + SMT por país y año. Revisar estos códigos contra la documentación del
# dataset si Eurostat los hubiera cambiado, ya que no se pudo verificar por
# ejecución en este entorno (sin acceso de red a ec.europa.eu).
filtro_base = (
    (df_eurostat_raw["sex"] == "T")
    & (df_eurostat_raw["age"] == "Y15-74")
    & (df_eurostat_raw["wstatus"] == "EMP")
    & (df_eurostat_raw["unit"] == "PC")
    & (df_eurostat_raw["geo"].isin(mapa_paises_eurostat.values()))
    & (df_eurostat_raw["time_period"].isin([2019, 2024]))
)
df_eurostat_f = df_eurostat_raw[filtro_base].copy()
if "frequenc" in df_eurostat_f.columns:
    df_eurostat_f = df_eurostat_f[df_eurostat_f["frequenc"].isin(["USU", "SMT"])]

df_eurostat_f = df_eurostat_f.rename(
    columns={"time_period": "Anio", "obs_value": "valor"}
)
tabla_wfh = df_eurostat_f.groupby(["geo", "Anio"])["valor"].sum().reset_index()

mapa_inverso_eurostat = {v: k for k, v in mapa_paises_eurostat.items()}
tabla_wfh["Pais"] = tabla_wfh["geo"].map(mapa_inverso_eurostat)

filas_slope = []
for pais in mapa_paises_eurostat:
    sub = tabla_wfh[tabla_wfh["Pais"] == pais].set_index("Anio")["valor"]
    y2019 = round(float(sub.get(2019, float("nan"))), 1)
    y2024 = round(float(sub.get(2024, float("nan"))), 1)
    diff = y2024 - y2019
    if diff >= 25:
        grupo = f"Salto estructural (+{diff:.1f} pp)".replace(".", ",")
    elif diff >= 15:
        grupo = "Consolidación alta"
    elif diff >= 12:
        grupo = "Crecimiento medio"
    else:
        grupo = f"Rezago relativo (+{diff:.1f} pp)".replace(".", ",")
    filas_slope.append({"Pais": pais, "y2019": y2019, "y2024": y2024, "Grupo": grupo})

df_slope = pd.DataFrame(filas_slope)
df_slope.to_csv("datos_slope_chart.csv", index=False)

fig_sc = go.Figure()

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

# Offsets calculados para evitar colisiones de etiquetas en 2019 y 2024
y_offset_2019 = {
    "Finlandia": 1.5,
    "Países Bajos": -1.8,
    "Irlanda": 2.5,
    "Francia": 1,
    "Suecia": -0.8,
    "Alemania": -2.2,
    "España": -3.8,
    "Italia": -5.2,
}

y_offset_2024 = {
    "Finlandia": 1.4,
    "Irlanda": -1.4,
    "Alemania": 1.0,
    "Francia": -1.0,
    "España": 0.8,
    "Italia": -0.8,
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
        y=row["y2024"] + y_offset_2024.get(pais, 0),
        text=f"{peso_txt}{pais}: {row['y2024']}% (+{diff:.1f} pp){cierre_txt}",
        xanchor="left",
        showarrow=False,
        font=dict(size=12, color=color_txt),
    )

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
        "<span style='font-size:14px;color:#475569'>Porcentaje de ocupados que trabajan habitualmente o a veces desde casa (Eurostat, lfsa_ehomp). El ángulo refleja el salto estructural.</span>",
        x=0.0,
        y=0.97,
    ),
    height=680,
    margin=dict(t=95, b=40, l=180, r=220),
    xaxis=dict(range=[-0.35, 1.4], visible=False),
    yaxis=dict(range=[-3, 62], visible=False),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI, Roboto, sans-serif"),
)

guardar_html_editorial(fig_sc, "slope-chart.html", "Slope Chart", "sc")


# ==============================================================================
# 3. TÉCNICA GRUPO III: CONNECTED SCATTERPLOT
# ==============================================================================
def descargar_indicador_wb(indicador, pais_iso2="ES", year_ini=2007, year_fin=2024):
    url = (
        f"https://api.worldbank.org/v2/country/{pais_iso2}/indicator/{indicador}"
        f"?format=json&date={year_ini}:{year_fin}&per_page=1000"
    )
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    payload = r.json()
    registros = payload[1] if len(payload) > 1 and payload[1] else []
    df = pd.DataFrame(
        [{"Anio": int(reg["date"]), "valor": reg["value"]} for reg in registros]
    )
    return df.dropna(subset=["valor"]).sort_values("Anio")


df_paro = descargar_indicador_wb("SL.UEM.TOTL.ZS")
df_inflacion = descargar_indicador_wb("FP.CPI.TOTL.ZG")

df_cs = pd.merge(
    df_paro.rename(columns={"valor": "Paro"}),
    df_inflacion.rename(columns={"valor": "Inflacion"}),
    on="Anio",
    how="inner",
).sort_values("Anio")

df_cs["Paro"] = df_cs["Paro"].round(1)
df_cs["Inflacion"] = df_cs["Inflacion"].round(1)


def etiquetar_etapa(anio):
    if anio <= 2013:
        return "1. Crisis Financiera y Deuda (2007–2013)"
    elif anio <= 2019:
        return "2. Recuperación y Desinflación (2014–2019)"
    else:
        return "3. Pandemia y Shock Inflacionario (2020–2024)"


df_cs["Etapa"] = df_cs["Anio"].apply(etiquetar_etapa)
df_cs = df_cs[(df_cs["Anio"] >= 2007) & (df_cs["Anio"] <= 2024)].reset_index(drop=True)
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
    annotation_position="top left",
    annotation_font=dict(size=11, color="#64748b"),
)

segmentos_def = [
    (
        "1. Crisis Financiera y Deuda (2007–2013)",
        "#dc2626",
        "1. Gran Recesión (2007–2013)",
    ),
    (
        "2. Recuperación y Desinflación (2014–2019)",
        "#0284c7",
        "2. Recuperación (2014–2019)",
    ),
    (
        "3. Pandemia y Shock Inflacionario (2020–2024)",
        "#7c3aed",
        "3. Shock Pandemia y Energía (2020–2024)",
    ),
]


etapas_orden = [e[0] for e in segmentos_def]
for i, (etapa, color_seg, nombre_seg) in enumerate(segmentos_def):
    sub_df = df_cs[df_cs["Etapa"] == etapa].copy()
    if i > 0:
        anterior = df_cs[df_cs["Etapa"] == etapas_orden[i - 1]]
        if not anterior.empty:
            sub_df = pd.concat([anterior.iloc[[-1]], sub_df]).reset_index(drop=True)

    anios_a_etiquetar = set(sub_df["Anio"]) & {
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
    }

    fig_cs.add_trace(
        go.Scatter(
            x=sub_df["Paro"],
            y=sub_df["Inflacion"],
            mode="lines+markers+text",
            line=dict(color=color_seg, width=3.2, shape="spline", smoothing=0.35),
            marker=dict(symbol="arrow", size=12, angleref="previous", color=color_seg),
            text=[str(a) if a in anios_a_etiquetar else "" for a in sub_df["Anio"]],
            textposition="top center",
            textfont=dict(size=11.5, color=color_seg),
            name=nombre_seg,
            customdata=sub_df["Anio"],
            hovertemplate="<b>Año %{customdata}</b><br>Desempleo: %{x:.1f}%<br>Inflación (IPC): %{y:.1f}%<extra></extra>",
        )
    )

max_paro_row = df_cs.loc[df_cs["Paro"].idxmax()]
max_inflacion_row = df_cs.loc[df_cs["Inflacion"].idxmax()]
ultimo_row = df_cs.iloc[-1]

fig_cs.add_annotation(
    x=max_paro_row["Paro"],
    y=max_paro_row["Inflacion"],
    text=f"<b>{int(max_paro_row['Anio'])}: Máximo histórico de paro ({max_paro_row['Paro']}%)</b><br>Desplazamiento horizontal tras estallar la burbuja",
    showarrow=True,
    arrowhead=2,
    ax=-90,
    ay=-65,
    bgcolor="#fef2f2",
    bordercolor="#fca5a5",
    borderpad=5,
    font=dict(size=11),
)
fig_cs.add_annotation(
    x=max_inflacion_row["Paro"],
    y=max_inflacion_row["Inflacion"],
    text=f"<b>{int(max_inflacion_row['Anio'])}: Pico inflacionario ({max_inflacion_row['Inflacion']}%)</b><br>Shock energético mientras el paro sigue bajando",
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
    x=ultimo_row["Paro"],
    y=ultimo_row["Inflacion"],
    text=f"<b>{int(ultimo_row['Anio'])}: Aterrizaje suave</b><br>({ultimo_row['Paro']}% paro | {ultimo_row['Inflacion']}% IPC)",
    showarrow=True,
    arrowhead=2,
    ax=45,
    ay=-42,
    bgcolor="#f8fafc",
    bordercolor="#cbd5e1",
    borderpad=5,
    font=dict(size=11),
)

fig_cs.update_layout(
    title=dict(
        text="<b>Los tres ciclos de la Curva de Phillips en España (2007–2024)</b><br>"
        "<span style='font-size:14px;color:#475569'>Trayectoria conjunta de la Tasa de Desempleo (eje X) y la Inflación IPC (eje Y). Fuente: World Bank (SL.UEM.TOTL.ZS, FP.CPI.TOTL.ZG). Las flechas indican el avance temporal.</span>",
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
# 4. PORTADA INDEX.HTML
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
print(f"Fuente 1 (OWID): {OWID_URL}")
print(f"Fuente 2 (Eurostat lfsa_ehomp): {EUROSTAT_URL}")
print("Fuente 3 (World Bank): SL.UEM.TOTL.ZS y FP.CPI.TOTL.ZG, country=ES")
