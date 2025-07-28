# Talk 技术博客论坛系统

## 项目简介
Talk 是一个基于 Flask + MySQL + Vue3 + Tailwind CSS 的高科技感技术博客论坛，支持积分/经验体系、社交、群组、富文本、WebSocket 实时聊天等。

## 功能特性
- 用户系统：注册、登录、JWT鉴权、RBAC权限、个人信息、封禁
- 内容管理：发帖、评论、富文本（Markdown）、点赞、帖子/评论管理
- 积分与经验体系：发帖/评论/被赞自动加分，积分消费，经验与等级系统，积分明细
- 积分商城：虚拟商品兑换、下载、兑换记录
- 群组功能：创建/搜索/加入群组、成员管理、角色分级
- 私信系统：WebSocket 实时私信、群聊、离线消息
- 响应式科技感UI：深色主题、粒子动效、玻璃拟态卡片、渐变边框
- 管理员后台：帖子/评论/用户/积分管理

## 一键本地部署

### 1. 启动后端与数据库
```bash
cd deploy
# 一键启动后端+MySQL
# 首次启动后，访问前端页面，填写数据库信息完成初始化
# 后端端口5000，数据库3306
# 如需Nginx反代，需自行启动Nginx

docker-compose up --build
```

### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
# 默认端口5173，访问 http://localhost:5173
```

### 3. 生产部署建议
- 前端打包：`npm run build`，产物在 `frontend/dist/`
- 推荐用 Nginx 部署前端静态资源，并反向代理 `/api` 到后端
- 参考 `deploy/nginx.conf`，将前端 `dist` 目录内容拷贝到 Nginx 静态目录

### 4. 主要API接口
- POST /api/register：注册
- POST /api/login：登录
- GET /api/user/profile：获取用户信息
- PUT /api/user/profile：修改个人信息
- GET /api/user/points/logs：积分明细
- GET/POST /api/post：帖子列表/发帖
- GET/POST /api/comment/{post_id}：评论列表/发评论
- POST /api/like：点赞/取消点赞
- GET /api/shop/items：商城商品列表
- POST /api/shop/order：兑换商品
- GET /api/shop/orders：我的兑换记录
- POST /api/group：创建群组
- GET /api/group/search：搜索群组
- POST /api/group/{id}/join：加入群组
- GET /api/group/{id}/members：群成员列表
- WebSocket /chat：私信/群聊
- ...（详见后端代码）

## 主要技术栈
- 后端：Flask、Flask-SQLAlchemy、Flask-SocketIO、MySQL、PyJWT、Bcrypt
- 前端：Vue 3、TypeScript、Pinia、Vue Router、Tailwind CSS、Vite、socket.io-client
- 部署：Docker Compose、Nginx

## 贡献指南
1. Fork 本仓库，创建新分支
2. 提交 PR 前请确保通过测试
3. 详细描述你的更改内容

## License
MIT 