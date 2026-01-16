# Luntan 论坛项目

这是一个基于 FastAPI (后端) 和 Vue 3 (前端) 的论坛系统，专为 CentOS Stream 9 服务器部署设计。

## 🔄 日常开发与更新流程

### 1. 本地开发与推送 (Windows)

当你修改了代码后：

```powershell
# 1. 提交更改
git add .
git commit -m "描述你的修改"

# 2. 推送到 Gitee
git push gitee main
```

### 2. 服务器更新 (Linux)

登录服务器，运行更新脚本（首次需要赋予执行权限）：

```bash
# 首次运行前赋予权限
chmod +x /var/www/luntan/update_server.sh

# 以后每次更新只需运行：
/var/www/luntan/update_server.sh
```

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
