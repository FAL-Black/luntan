# 论坛项目 (Luntan)

这是一个基于 FastAPI (后端) 和 Vue 3 (前端) 的论坛项目。

## 目录结构

- `backend/`: Python FastAPI 后端代码
- `frontend/`: Vue 3 前端代码
- `DEPLOY.md`: CentOS Stream 9 部署指南

## 快速开始 (本地开发)

### 1. 启动后端

请打开一个终端窗口：

```bash
cd backend
# 建议创建虚拟环境 (可选)
# python -m venv venv
# .\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务器
uvicorn main:app --reload
```
后端服务将在 `http://localhost:8000` 启动。

### 2. 启动前端

请打开另一个终端窗口：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```
前端页面将在 `http://localhost:5173` 启动。

## 部署

关于如何在 CentOS Stream 9 云服务器上部署，请参考 [DEPLOY.md](DEPLOY.md)。
