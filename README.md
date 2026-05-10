# 🍺 Chelasabe

> Tu guía personal de cerveza artesanal — conectando principiantes con el conocimiento colectivo de catadores expertos.

---

## ¿Qué es Chelasabe?

Chelasabe es una web app que ayuda a personas que se están iniciando en la cerveza artesanal a descubrir qué estilos probablemente les van a gustar, basándose en:

- Sus preferencias de cervezas comerciales que ya conocen
- Su perfil general de sabores, aromas y atributos

El sistema cruza esa información con los perfiles de catadores avanzados registrados en la app, y genera una recomendación personalizada de estilos artesanales.

---

## Estructura del proyecto

```
chelasabe/
├── app.py           # App principal de Streamlit (UI + routing)
├── data.py          # Catálogos: cervezas comerciales, estilos, notas
├── db.py            # Capa SQLite (init, guardar, leer usuarios)
├── matching.py      # Motor de recomendación (similitud coseno)
├── requirements.txt
├── README.md
└── chelasabe.db     # Se crea automáticamente al correr la app
```

---

## Instalación y uso local

### 1. Clonar / descargar el proyecto

```bash
# Si usas git
git clone <tu-repo>
cd chelasabe

# O simplemente coloca los archivos en una carpeta
cd chelasabe
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Correr la app

```bash
streamlit run app.py
```

La app abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## Cómo usar la app

### Flujo "Avanzado" → Uno para todos

1. Llega un usuario con experiencia en artesanal
2. Selecciona **"Registrar mi perfil avanzado"**
3. Completa el cuestionario (comerciales + preferencias + estilos artesanales)
4. Su perfil se guarda en `chelasabe.db`

### Flujo "Principiante" → Todos para uno

1. Llega un usuario nuevo en artesanal
2. Selecciona **"Quiero descubrir mi estilo"**
3. Completa el cuestionario parcial (comerciales + preferencias generales)
4. El sistema:
   - Vectoriza su perfil con las mismas dimensiones que los avanzados
   - Calcula similitud coseno contra todos los avanzados registrados
   - Selecciona los top-5 más similares
   - Pondera sus ratings de estilos artesanales por score de similitud
   - Presenta el ranking de estilos recomendados

---

## Motor de recomendación

### Vectorización

Cada usuario se representa como un vector de **37 dimensiones**:

| Dimensiones | Descripción |
|-------------|-------------|
| 8           | Ratings de cervezas comerciales (normalizados 0–1) |
| 4           | Preferencias ordinales: color, ABV, amargor, cuerpo |
| 12          | One-hot: notas de aroma seleccionadas |
| 13          | One-hot: notas de sabor seleccionadas |

### Similitud

Se usa **similitud coseno** entre el vector del principiante y el de cada avanzado.

### Recomendación ponderada

Para cada estilo artesanal:

```
score(estilo) = Σ(sim_i × rating_i) / Σ(sim_i)
```

Solo se consideran ratings de estilos que el avanzado haya probado (rating > 0).

---

## Deployment en Streamlit Community Cloud (gratis)

1. Sube el proyecto a un repositorio de GitHub (puede ser privado)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repo y el archivo `app.py`
5. Deploy ✅

> **Nota:** En Streamlit Cloud, el archivo `chelasabe.db` se resetea en cada redeploy. Para persistencia real en producción, considera migrar `db.py` a **Supabase** (PostgreSQL gratuito) o **PlanetScale**.

---

## Roadmap sugerido

- [ ] Panel de administración: ver usuarios avanzados registrados
- [ ] Exportar perfil de recomendación como PDF o imagen
- [ ] Modo "Taproom": mostrar descripción detallada de cada estilo recomendado para pedir con más confianza
- [ ] Añadir campo de "cervezas artesanales que ya probé" para avanzados
- [ ] Migrar BD a Supabase para persistencia en producción
- [ ] Visualización de similitud: scatter plot de catadores en 2D (PCA/UMAP)
- [ ] Sistema de feedback: el principiante regresa y califica si la recomendación fue acertada
