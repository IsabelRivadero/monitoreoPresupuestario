# Sistema Inteligente de Monitoreo Presupuestario y Auditoria Gubernamental

Este repositorio contiene la solucion analitica desarrollada para el Trabajo Practico Integrador Final de la materia Laboratorio de Datos (Tecnicatura Universitaria en Ciencia de Datos e IA - UGR).

El proyecto aborda la gestion de datos publicos y la priorizacion de auditorias gubernamentales sobre el Sistema de Contrataciones Electronicas (COMPR.AR) y la Ejecucion Presupuestaria de Gastos. Integra un pipeline de Gobernanza de Datos, higienizacion tributaria (Golden Record), un algoritmo no supervisado de deteccion de anomalias (Isolation Forest) y una matriz sintetica denominada Audit Risk Score (ARS).

---

## Estructura del Repositorio

app.py                  - Aplicacion web interactiva en Streamlit para auditores
lab_de_datostp3.ipynb   - Notebook con ETL, limpieza de CUIT, modelado y exportacion
requirements.txt        - Librerias de Python requeridas
.gitignore              - Exclusion de archivos pesados de datos y entornos
README.md               - Documentacion del proyecto

---

## Guia de Instalacion y Ejecucion

### 1. Clonar el repositorio
git clone https://github.com/IsabelRivadero/monitoreoPresupuestario.git
cd monitoreoPresupuestario

### 2. Crear y activar un entorno virtual
En Linux / macOS:
python3 -m venv datalab
source datalab/bin/activate

En Windows:
python -m venv datalab
datalab\Scripts\activate

### 3. Instalar las dependencias
pip install -r requirements.txt

### 4. Generar el Data Mart Analitico (auditoria_datamart.parquet)
La interfaz visual requiere del repositorio de datos precalculado por la canalizacion. Para generarlo:
1. Asegurate de disponer de la carpeta de datos originales (/data/) con los archivos transaccionales.
2. Abre y ejecuta todas las celdas del cuaderno Jupyter:
   jupyter notebook lab_de_datostp3.ipynb
3. La ultima celda exportara automaticamente el archivo auditoria_datamart.parquet en la carpeta data/.

### 5. Levantar el Tablero Interactivo de Streamlit
Una vez generado el Data Mart, inicia la aplicacion web con el siguiente comando:

streamlit run app.py

La plataforma se abrira de forma automatica en tu navegador predeterminado en la direccion:
http://localhost:8501

---

## Funcionalidades del Tablero de Auditoria

- Filtrado Dinamico de Riesgo: Ajuste del umbral minimo de Audit Risk Score (ARS) mediante deslizador interactivo.
- Filtro por Unidad Ejecutora / Ministerio: Vista focalizada por organismo comprador.
- Indicadores Clave de Gestion (KPIs): Visualizacion del monto expuesto evaluado, total de procesos en alerta y cantidad de CUITs unificados.
- Matriz de Riesgo y Ranking Top 10: Graficos de dispersion logaritmica y barras jerarquicas con deteccion de anomalias por Machine Learning.
- Inspeccion de Casos (Human-in-the-Loop): Tabla interactiva con el desglose de puntajes para control humano.

---

## Flujo de Trabajo para Subir Cambios Futuros

Para registrar y sincronizar actualizaciones en GitHub:

git status
git add .
git commit -m "Docs: actualizacion de documentacion README.md"
git push