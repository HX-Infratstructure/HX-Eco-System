# HX Eco-System — Architecture Orientation

## Control and infrastructure
- HX-1: Samba AD / DNS / Kerberos / NTP
- HX-5: CentCom / DeepSeek Harness / dev-test
- HX-6: OmniRoute
- HX-7: NGINX, dev/test UI rendering only
- HX-15: FastMCP shared/custom MCP development host

## Inference
- HX-2: Qwen-X
- HX-3: Coder-X
- HX-4: Meta-X + shared embedding/reranking
- HX-5: Ornith

## State / retrieval
- HX-9: PostgreSQL + Redis + assigned MCP servers
- HX-10: Qdrant + Web UI + MCP

## Knowledge / RAG
- HX-16: Docling + Granite-Docling 258M + MCP
- HX-17: Crawl4AI + MCP
- HX-11: LightRAG + MCP
- HX-13: Mem0

## Agent / workflow / UI
- HX-12: Deep Agents by LangChain
- HX-14: n8n + MCP
- HX-8: Open WebUI

## Direction
Base-build first, integration later. Small reversible functional tests are allowed during base build to prove an application works end-to-end against one already-proven dependency. They are not permanent integration architecture unless explicitly approved.
