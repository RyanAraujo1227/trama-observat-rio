# TRAMA — Observatório de IA e Mercado de Trabalho

Aplicação Flask pronta para publicação no Render.

## Rodar localmente
```bash
pip install -r requirements.txt
python app.py
```

## Publicar no Render
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

O arquivo `render.yaml` já contém essa configuração.
