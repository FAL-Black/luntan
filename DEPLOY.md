# CentOS Stream 9 部署指南

本指南介绍如何在 CentOS Stream 9 服务器上部署该论坛应用。

## 1. 环境准备

首先，更新系统并安装必要的软件包：

```bash
sudo dnf update -y
sudo dnf install -y git python3-pip python3-devel nginx
```

### 安装 Node.js (使用 NodeSource 源)

```bash
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo dnf install -y nodejs
```

## 2. 克隆代码

假设您已经将代码上传到了 GitHub 或 Gitee 等平台。

```bash
cd /var/www
# 将下面的 URL 替换为您的 GitHub 仓库地址
sudo git clone https://github.com/your-username/your-repo.git luntan
cd luntan
sudo chown -R $USER:$USER .
```

## 3. 后端部署 (FastAPI)

建议使用 Python 虚拟环境：

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 配置 Systemd 服务

创建服务文件 `/etc/systemd/system/luntan-backend.service`:

```ini
[Unit]
Description=Luntan FastAPI Backend
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/luntan/backend
Environment="PATH=/var/www/luntan/backend/venv/bin"
# 设置数据库环境变量 (请替换为您设置的密码)
Environment="DB_USER=luntan_user"
Environment="DB_PASSWORD=password123"
Environment="DB_HOST=localhost"
Environment="DB_NAME=luntan"
ExecStart=/var/www/luntan/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start luntan-backend
sudo systemctl enable luntan-backend
```

## 4. 前端部署 (Vue3)

构建静态文件：

```bash
cd ../frontend
npm install
npm run build
```

构建完成后，生成的静态文件位于 `frontend/dist` 目录。

## 5. Nginx 配置

编辑 `/etc/nginx/conf.d/luntan.conf`:

> **注意**：复制时请务必小心，不要把代码块标记（如 ```nginx）也复制进去了。文件内容应以 `server {` 开头。

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或 IP

    # 前端静态文件
    location / {
        root /var/www/luntan/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Swagger 文档代理 (可选)
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**注意**：如果 `/etc/nginx/nginx.conf` 中已有默认的 `server` 块，可能需要将其注释掉以免端口冲突。

重启 Nginx：
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 6. 防火墙设置

如果开启了 firewalld，需要允许 HTTP 流量：

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

## 7. 常见问题排查 (Troubleshooting)

### Nginx 启动失败

如果 `systemctl restart nginx` 失败，请尝试以下步骤：

1.  **检查配置文件语法**：
    ```bash
    sudo nginx -t
    ```
    这会直接告诉你配置文件哪一行写错了。

2.  **SELinux 权限问题 (CentOS 特有)**：
    CentOS 默认开启 SELinux，这通常是导致 Nginx 无法启动或访问文件的原因。

    *   **允许 Nginx 网络连接 (解决 502 Bad Gateway)**:
        ```bash
        sudo setsebool -P httpd_can_network_connect 1
        ```
    *   **允许 Nginx 读取前端文件 (解决 403 Forbidden)**:
        ```bash
        sudo chcon -R -t httpd_sys_content_t /var/www/luntan/frontend/dist
        ```

3.  **端口冲突**：
    检查 80 端口是否被占用：
    ```bash
    sudo ss -tuln | grep :80
    ```
