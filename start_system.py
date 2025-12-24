import os

os.system("uvicorn backend.mcp_server:app --port 8001 &")
os.system("uvicorn external_mcp.mock_calendar_mcp:app --port 8002 &")
os.system("uvicorn ui_server:app --port 9000 &")
