# 华为云部署指南 (Huawei Cloud Deployment Guide)

本指南将帮助你将个人博客系统部署到华为云服务器 (ECS) 上。

## 1. 准备工作 (Prerequisites)

### 1.1 购买/准备华为云 ECS
- **操作系统**: 推荐使用 Ubuntu 20.04/22.04 LTS 或 CentOS 7/8。
- **配置**: 至少 2vCPU, 4GB RAM (因为我们要运行 MySQL, Python 后端, Vue 前端构建等)。
- **安全组 (Security Group)**: 确保入方向规则允许以下端口：
    - **22** (SSH 远程连接)
    - **80** (HTTP Web 访问)
    - **443** (HTTPS, 如果后续配置 SSL)

### 1.2 连接服务器
使用 SSH 工具 (如 PuTTY, Xshell, 或 VS Code Remote - SSH) 连接到你的服务器。

```bash
ssh root@your_server_ip
```

### 1.3 安装 Docker 和 Docker Compose
在服务器上执行以下命令安装 Docker 环境。

**Ubuntu:**
```bash
# 更新软件包
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose (如果 Docker 版本较新，可能已内置 docker compose 命令，否则需单独安装)
# 验证安装
docker --version
docker compose version
```

**CentOS:**
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

## 2. 上传项目文件 (Upload Project)

你需要将本地的项目代码上传到服务器。可以使用 `scp` 命令或 SFTP 工具 (如 FileZilla)。

**需要上传的文件/文件夹:**
- `backend/`
- `frontend/`
- `db/`
- `docker-compose.yml`
- `.env` (包含敏感密码，请确保安全)

**使用 SCP 示例 (在本地终端执行):**
```bash
# 假设你的项目在 d:\CODES\my-personal-blog
# 将整个目录上传到服务器的 /opt/my-blog 目录
scp -r d:\CODES\my-personal-blog root@your_server_ip:/opt/my-blog
```

## 3. 部署运行 (Deploy & Run)

### 3.1 进入项目目录
```bash
cd /opt/my-blog
```

### 3.2 检查环境变量
确保 `.env` 文件存在且内容正确。
```bash
cat .env
```
*注意: 生产环境建议修改 `.env` 中的密码为更复杂的强密码。*

### 3.3 启动服务
使用 Docker Compose 构建并启动所有服务。

```bash
docker compose up -d --build
```
- `-d`: 后台运行
- `--build`: 强制重新构建镜像 (确保代码更新生效)

### 3.4 查看状态
```bash
docker compose ps
```
你应该能看到 `frontend`, `backend`, `blog_db` 三个容器都处于 `Up` 状态。

## 4. 验证访问 (Verification)

打开浏览器，访问你的服务器公网 IP：
`http://your_server_ip`

你应该能看到你的博客首页。

## 5. 常见问题排查 (Troubleshooting)

- **无法访问网页**:
    - 检查华为云控制台的安全组规则，确认 **80 端口** 是否已放行。
    - 检查防火墙: `sudo ufw status` (Ubuntu) 或 `systemctl status firewalld` (CentOS)。

- **数据库连接失败**:
    - 查看后端日志: `docker compose logs backend`
    - 确认 `.env` 中的 `DATABASE_URL` 格式正确，且密码与 `MYSQL_PASSWORD` 一致。

- **查看所有日志**:
    - `docker compose logs -f` (实时查看日志)

## 6. 后续优化建议

- **配置域名**: 在华为云购买域名并解析到你的服务器 IP。
- **启用 HTTPS**: 修改 `frontend/nginx.conf` 配置 SSL 证书 (可以使用 Let's Encrypt 免费证书)。
- **数据备份**: 定期备份 `db_data` 卷或导出 SQL 文件。
