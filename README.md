# Luntan 论坛项目

这是一个基于 FastAPI (后端) 和 Vue 3 (前端) 的论坛系统，专为 CentOS Stream 9 服务器部署设计。

## 🚀 部署流程概览

本项目旨在直接部署到 Linux 服务器。请按照以下步骤操作：

1.  **推送代码**: 将本代码推送到您的 GitHub 仓库。
2.  **服务器拉取**: 登录您的 Linux 服务器，拉取代码。
3.  **执行部署**: 按照详细文档安装依赖并启动服务。

## 📄 详细部署文档

请阅读 **[DEPLOY.md](DEPLOY.md)** 获取完整的服务器部署指令。

该文档包含：
*   系统依赖安装 (Python, Node.js, Nginx)
*   后端服务配置 (Systemd)
*   前端构建与 Nginx 反向代理设置

## 📂 项目结构

*   `backend/`: Python FastAPI 源码
*   `frontend/`: Vue 3 源码
*   `DEPLOY.md`: **核心部署指南**
