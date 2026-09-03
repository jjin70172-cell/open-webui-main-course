@echo off
REM Open WebUI local start script (backend + built frontend on port 8081)
cd /d "%~dp0"
set WEBUI_SECRET_KEY=fiAfZXcyPp_UzSq9YIPcmAB8tdcRUqE7Tqx_GwWAsN1vhhxQ9xKya_tYTXdf0a6e
set WEBUI_JWT_SECRET_KEY=MA3qkZJRFtl5TaQ_xj0YLffXS4Q9GVAaJl3yYEGVVtlYz3nZ8Y_DVHSVrtZmYei9
set FRONTEND_BUILD_DIR=%CD%\build
set RAG_EMBEDDING_ENGINE=ollama
.venv\Scripts\open-webui.exe serve --host 0.0.0.0 --port 8081
