# Rcodes Island (码德岛) - 个人博客系统

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Vue 3](https://img.shields.io/badge/frontend-Vue%203-4FC08D.svg)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![Docker](https://img.shields.io/badge/deploy-Docker-2496ED.svg)

**Rcodes Island (码德岛)** 是一个现代化的全栈个人博客系统，其名称与设计灵感来源于游戏《明日方舟》中的组织“罗德岛 (Rhodes Island)”。

本项目采用了独特的**终端风格 UI**，结合了 Vue 3 的响应式体验与 FastAPI 的高性能后端，并完全容器化以便于部署。

![RCODES ISLAND Homepage](docs/homepage.png)

## ✨ 功能特性

### 🎨 UI/UX 设计
- **明日方舟主题**: 定制的“码德岛”终端美学，包含扫描线效果、等宽字体和沉浸式视觉体验。
- **响应式布局**: 基于 Tailwind CSS 构建，完美适配桌面端与移动端。
- **交互体验**: 流畅的过渡动画、悬停特效以及内置的音乐播放器挂件。

### 📝 内容管理
- **Markdown 编辑器**: 支持实时预览的双栏 Markdown 编辑体验，所见即所得。
- **图片上传**: 支持直接在编辑器中拖拽上传图片，自动生成 Markdown 链接。
- **标签系统**: 通过标签组织内容，侧边栏提供“热门标签”云以便快速筛选。
- **搜索与排序**: 实时搜索功能，支持按日期、浏览量或点赞数排序。

### ⚙️ 核心功能
- **用户系统**: 基于 JWT 的身份验证，管理员可进行发布、编辑和删除操作。
- **互动功能**: 访客评论系统和点赞功能。
- **数据统计**: 基础的文章浏览量计数和“正在流行”文章追踪。
- **分页加载**: 服务端分页，确保大数据量下的性能。

## 🛠 技术栈

### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **样式**: Tailwind CSS + @tailwindcss/typography
- **图标库**: Lucide Icons
- **HTTP 客户端**: Axios
- **Markdown 解析**: marked

### 后端 (Backend)
- **框架**: FastAPI (Python 3.9+)
- **数据库**: MySQL 5.7
- **ORM**: SQLAlchemy
- **认证**: OAuth2 with Password (JWT)
- **服务器**: Uvicorn

### 基础设施 (Infrastructure)
- **容器化**: Docker & Docker Compose
- **Web 服务器**: Nginx (反向代理)

## 🚀 快速开始

### 前置要求
- 本地已安装 Docker 和 Docker Compose。
- 已安装 Git。

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Acselerator/Rcodes-Island-Blog.git
   cd Rcodes-Island-Blog
   ```

2. **环境配置**
   在根目录创建 `.env` 文件（可选，开发环境已有默认值）：
   ```env
   MYSQL_ROOT_PASSWORD=rootpassword
   MYSQL_DATABASE=blog_db
   MYSQL_USER=bloguser
   MYSQL_PASSWORD=blogpassword
   DATABASE_URL=mysql+pymysql://bloguser:blogpassword@db/blog_db
   ```

3. **使用 Docker Compose 启动**
   ```bash
   docker-compose up -d --build
   ```

4. **访问应用**
   - 前端页面: `http://localhost`
   - 后端 API 文档: `http://localhost:8000/docs`

## 📂 项目结构

```
Rcodes-Island-Blog/
├── backend/                 # FastAPI 后端
│   ├── app/                 # 应用逻辑 (models, schemas, routes)
│   ├── uploads/             # 静态文件上传目录
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── components/      # Vue 组件 (PostList, Editor 等)
│   │   ├── App.vue          # 主布局与路由逻辑
│   │   └── main.js          # 入口文件
│   ├── Dockerfile
│   └── nginx.conf           # Nginx 配置
├── db/                      # 数据库初始化脚本
├── docker-compose.yml       # Docker 编排文件
└── README.md                # 项目文档
```

## 📦 部署指南

### 快速部署命令
```bash
# 在服务器上执行
docker-compose pull
docker-compose up -d
```

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---
*Designed & Developed by [Acselerator](https://github.com/Acselerator)*
