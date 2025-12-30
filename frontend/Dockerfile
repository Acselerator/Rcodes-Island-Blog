# Build stage
FROM node:18-alpine as build-stage
WORKDIR /app
COPY package*.json ./
# 使用 --unsafe-perm 确保 npm 以 root 权限执行脚本，避免权限降级
RUN npm install --unsafe-perm
COPY . .
# 恢复使用 npm run build，因为 --unsafe-perm 应该解决了权限问题
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
# 复制自定义 Nginx 配置（如果有的话，这里我们先用默认的，稍后可能需要处理路由 fallback）
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
