## 部署注意事项

### 1. 服务器环境准备
由于后端服务对内存要求较高，低配服务器（2G内存）**必须**开启 Swap 虚拟内存，否则会报线程错误：
```bash
# 开启 2G Swap
dd if=/dev/zero of=/swapfile bs=1M count=2048
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile