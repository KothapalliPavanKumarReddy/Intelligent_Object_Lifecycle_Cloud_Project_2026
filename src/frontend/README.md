# Frontend Architecture

While early project scaffolding originally considered a basic Streamlit script, the final platform was implemented as a production-grade, responsive **FastAPI + Jinja2 + Chart.js** web interface located in [`web/`](../../web/):

- **Templates:** [`web/templates/`](../../web/templates/)
  - `dashboard.html`: Live KPI overview, tier breakdown charts, and recent activity log.
  - `analyze.html`: Drag-and-drop satellite imagery upload, real-time contrast stretching preview, CLIP inference output, and tier assignment.
  - `archive.html`: Interactive catalog browser with search, category filters, and live AWS S3 bucket exploration/upload panel.
  - `analytics.html`: Statistical histograms and interactive AWS cloud storage cost optimization calculators.
  - `architecture.html`: Side-by-side technical comparison of the local prototype vs. proposed AWS cloud deployment.
- **Styling & Assets:** [`web/static/css/style.css`](../../web/static/css/style.css) and [`web/static/js/app.js`](../../web/static/js/app.js) — Custom aerospace dark-mode design system with responsive Chart.js visualizers.
