from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Configuración de la página Streamlit
st.set_page_config(
    page_title='Sistema de Auditoría e Inteligencia Presupuestaria',
    page_icon='🔍',
    layout='wide',
)


# Carga optimizada de datos con Cache de Streamlit
@st.cache_data
def load_data():
  # Búsqueda en rutas relativas y absolutas posibles
  possible_paths = [
      Path('../data/auditoria_datamart.parquet'),
      Path('data/auditoria_datamart.parquet'),
      Path('auditoria_datamart.parquet'),
      Path.cwd().parent / 'data' / 'auditoria_datamart.parquet',
  ]

  for path in possible_paths:
    if path.exists():
      return pd.read_parquet(path)

  # Si no lo encuentra en ninguna ruta, muestra advertencia clara en la app
  st.error(
      '⚠️ **No se encontró el archivo Data Mart (`auditoria_datamart.parquet`).**\n\n'
      'Por favor, ejecuta la última celda de exportación en tu notebook '
      '(`laboratorio_de_datostp3.ipynb`) para generar el archivo de datos.'
  )
  st.stop()


df = load_data()

# ------------------------------------------------------------------------------
# CABECERA Y TITULO
# ------------------------------------------------------------------------------
st.title('🔍 Sistema Inteligente de Monitoreo y Auditoría Gubernamental')
st.caption(
    'Herramienta de Apoyo a la Decisión basada en Machine Learning No'
    ' Supervisado (Isolation Forest) y Gobernanza de Datos'
)
st.markdown('---')

# ------------------------------------------------------------------------------
# FILTROS DE BARRA LATERAL (SIDEBAR)
# ------------------------------------------------------------------------------
st.sidebar.header('⚙️ Filtros de Control de Riesgo')

ars_minimo = st.sidebar.slider(
    'Umbral de Riesgo Mínimo (ARS)',
    min_value=0,
    max_value=100,
    value=70,
    step=5,
    help='Filtra transacciones por su Audit Risk Score.',
)

organismos_disponibles = ['Todos'] + sorted(
    df['Unidad_Ejecutora'].dropna().unique().tolist()
    if 'Unidad_Ejecutora' in df.columns
    else df['Organismo'].dropna().unique().tolist()
)

organismo_sel = st.sidebar.selectbox(
    'Filtrar por Organismo / Unidad Ejecutora', organismos_disponibles
)

# Aplicar filtros
col_org = 'Unidad_Ejecutora' if 'Unidad_Ejecutora' in df.columns else 'Organismo'
col_monto = [c for c in df.columns if 'monto' in c.lower()][0]

df_filtrado = df[df['Audit_Risk_Score'] >= ars_minimo].copy()

if organismo_sel != 'Todos':
  df_filtrado = df_filtrado[df_filtrado[col_org] == organismo_sel]

# ------------------------------------------------------------------------------
# PANEL DE TARJETAS DE MÉTRICAS (KPIs)
# ------------------------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
  st.metric(
      'Monto Filtrado Evaluado',
      f'${df_filtrado[col_monto].sum()/1e9:,.2f} B',
      help='Monto acumulado de las contrataciones seleccionadas.',
  )

with kpi2:
  st.metric(
      'Casos en Alerta de Riesgo',
      f'{len(df_filtrado):,}',
      delta=f'{len(df_filtrado)/len(df)*100:.1f}% del total',
      delta_color='inverse',
  )

with kpi3:
  st.metric('CUITs Unificados Únicos', f'{df_filtrado["CUIT_Limpio"].nunique():,}')

with kpi4:
  max_ars = (
      df_filtrado['Audit_Risk_Score'].max() if len(df_filtrado) > 0 else 0
  )
  st.metric('ARS Máximo Registrado', f'{max_ars:.1f} / 100')

st.markdown('---')

# ------------------------------------------------------------------------------
# GRÁFICOS INTERACTIVOS
# ------------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
  st.subheader('📈 Matriz de Riesgo: Monto vs. ARS')
  fig, ax = plt.subplots(figsize=(8, 4))
  sns.set_theme(style='whitegrid')

  sns.scatterplot(
      data=df_filtrado,
      x='log_monto',
      y='Audit_Risk_Score',
      hue='Estado_Modelo',
      palette={
          'Anomalía ML (Alerta)': '#d9534f',
          'Operación Normal': '#2b5c8f',
      },
      alpha=0.7,
      ax=ax,
  )
  ax.set_xlabel('Log10 (Monto Adjudicado)')
  ax.set_ylabel('Audit Risk Score (ARS)')
  st.pyplot(fig)

with col_right:
  st.subheader('🏆 Top 10 Adjudicaciones Prioritarias')
  top10 = df_filtrado.sort_values(by='Audit_Risk_Score', ascending=False).head(
      10
  )

  if len(top10) > 0:
    top10['label'] = top10['CUIT_Limpio'] + ' | ' + top10[col_org].str[:15]
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=top10, x='Audit_Risk_Score', y='label', palette='Reds_r')
    ax2.set_xlabel('Score de Riesgo')
    ax2.set_ylabel('')
    st.pyplot(fig2)
  else:
    st.info('No hay contrataciones que superen el umbral seleccionado.')

st.markdown('---')

# ------------------------------------------------------------------------------
# TABLA DE DETALLE PARA AUDITORÍA HUMANA
# ------------------------------------------------------------------------------
st.subheader('📋 Listado Priorizado para Inspección Humana (Human-in-the-Loop)')

cols_tabla = [
    'CUIT_Limpio',
    col_org,
    col_monto,
    'score_anomalia_ml',
    'score_concentracion',
    'Audit_Risk_Score',
]
cols_existentes = [c for c in cols_tabla if c in df_filtrado.columns]

df_tabla = (
    df_filtrado[cols_existentes]
    .sort_values(by='Audit_Risk_Score', ascending=False)
    .head(50)
)

st.dataframe(
    df_tabla.style.format({
        col_monto: '${:,.2f}',
        'score_anomalia_ml': '{:.1f}',
        'score_concentracion': '{:.1f}',
        'Audit_Risk_Score': '{:.1f}',
    }),
    use_container_width=True,
)