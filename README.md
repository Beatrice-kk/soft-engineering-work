# ✈️ 飞机票务管理系统 (Flight Ticket Booking System)

一个基于 Django + Vue.js + MySQL 的现代化飞机票务管理系统，提供完整的票务预订、用户管理、航班管理等功能。

[![Django](assets/badges/django-badge.svg)](https://www.djangoproject.com/)
[![Vue.js](assets/badges/vue-badge.svg)](https://vuejs.org/)
[![MySQL](assets/badges/mysql-badge.svg)](https://www.mysql.com/)
[![Python](assets/badges/python-badge.svg)](https://www.python.org/)
## 📋 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [安装部署](#安装部署)
- [使用指南](#使用指南)
- [API文档](#api文档)
- [开发指南](#开发指南)
- [测试说明](#测试说明)
- [维护指南](#维护指南)
- [更新日志](#更新日志)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🎯 项目简介

本系统是一个完整的飞机票务管理系统，采用前后端分离架构，为乘客提供便捷的飞机票预订服务，同时为管理员提供全面的系统管理功能。

### 主要特点

- ✅ **现代化架构**：前后端分离，接口规范
- ✅ **用户友好**：直观的Web界面，操作简单
- ✅ **功能完整**：涵盖票务全生命周期管理
- ✅ **安全可靠**：完善的认证和权限控制
- ✅ **易于维护**：模块化设计，代码规范
- ✅ **测试完善**：全面的自动化测试覆盖

## 🚀 核心功能

### 👤 用户功能
- 用户注册登录
- 个人资料管理
- 关联旅客管理
- 飞机票查询预订
- 订单管理
- 票务打印

### 👨‍💼 管理员功能
- 用户账号管理
- 乘客信息管理
- 飞机信息管理
- 航班安排管理
- 经停点管理
- 票务信息管理

### 🔧 系统功能
- 数据一致性保证
- 候补队列管理
- 动态票价调整
- 座位分配优化
- 实时状态更新

## 🏗️ 技术架构

### 后端技术栈
```
Django 4.2.7
├── Django ORM (对象关系映射)
├── Django REST Framework (API开发)
├── Django Auth (用户认证)
├── Django Sessions (会话管理)
├── Django Middleware (中间件系统)
└── Django Testing (测试框架)
```

### 前端技术栈
```
Vue.js 2.6.14
├── Vue Router 3.5.1 (路由管理)
├── Vuex 3.6.2 (状态管理)
├── Element UI 2.15.13 (UI组件库)
├── Axios 1.7.9 (HTTP客户端)
├── ECharts 5.4.2 (图表可视化)
└── FullCalendar 6.1.5 (日历组件)
```

### 数据库设计
```
MySQL 8.0
├── 用户管理 (passenger, p_account, m_account)
├── 飞机管理 (flight, arrange, stop)
├── 票务管理 (ticket, waiting_list)
├── 关系管理 (relationships)
└── 座位管理 (seat)
```

## 🚀 快速开始

### 系统要求
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Git

### 一键启动 (推荐)

```bash
# 1. 克隆项目
git clone <repository-url>
cd soft-engineering-work

# 2. 启动后端
cd flight
python manage.py runserver

# 3. 启动前端 (新终端)
cd vue
npm install
npm run serve
```

访问 http://localhost:8080 开始使用系统。

## 📦 安装部署

### 后端部署

#### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 2. 数据库配置
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE train CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入初始数据
mysql -u root -p train < mysql.sql
```

#### 3. Django配置
```python
# flight/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'train',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 4. 启动服务
```bash
cd flight
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### 前端部署

#### 1. 安装依赖
```bash
cd vue
npm install
```

#### 2. 开发模式
```bash
npm run serve  # 开发服务器，热重载
```

#### 3. 生产构建
```bash
npm run build  # 构建生产版本
```

### Docker部署 (可选)

```dockerfile
# Dockerfile 示例
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📖 使用指南

### 用户操作流程

#### 1. 注册账户
1. 访问系统首页
2. 点击"注册"按钮
3. 填写个人信息（姓名、手机号、身份证等）
4. 设置登录账号和密码

#### 2. 预订飞机票
1. 登录系统
2. 选择"航班预订"
3. 输入出发地、目的地、日期
4. 选择合适的飞机和座位
5. 确认预订并支付

#### 3. 管理订单
1. 进入"我的订单"页面
2. 查看订单状态
3. 可进行退票、改签等操作

### 管理员操作流程

#### 1. 航班管理
1. 登录管理员账户
2. 进入"航班安排"
3. 添加新的飞机信息
4. 设置起飞时间和票价

#### 2. 用户管理
1. 进入"用户管理"页面
2. 查看用户列表
3. 管理用户权限和状态

## 📚 API文档

### 认证相关

#### 用户登录
```http
GET /login/?name={username}&pass={password}
```

**响应示例：**
```json
{
  "res": 1,
  "p_id": "P0001",
  "username": "testuser"
}
```

#### 用户注册
```http
POST /register/
Content-Type: application/json

{
  "account": "newuser",
  "pass": "password123",
  "name": "张三",
  "phone": "13800138000",
  "sex": "1",
  "age": 25,
  "card": "123456789012345678"
}
```

### 用户管理

#### 获取用户资料
```http
GET /getProfile/?p_id={passenger_id}
```

#### 更新用户资料
```http
GET /changeProfile/?p_id={id}&p_name={name}&p_sex={sex}&...
```

### 票务管理

#### 查询飞机票
```http
GET /getTicket/?start={city}&end={city}&date={date}
```

#### 预订飞机票
```http
GET /book/?p_ids={ids}&a_id={arrange_id}&p_main={main_id}
```

#### 删除飞机票
```http
GET /delTicket/?t_id={ticket_id}
```

### 管理员功能

#### 获取所有用户
```http
GET /mgetPassenger/
```

#### 添加飞机
```http
GET /saveFlight/?f_id={id}&f_s_place={start}&f_e_place={end}
```

#### 删除航班安排
```http
GET /delArrange/?f_id={flight_id}
```

## 💻 开发指南

### 项目结构
```
soft-engineering-work/
├── flight/                 # Django后端
│   ├── flight/            # Django配置
│   │   ├── settings.py    # 配置文件
│   │   ├── urls.py       # URL配置
│   │   └── wsgi.py       # WSGI配置
│   └── myapp/            # 主应用
│       ├── models.py     # 数据模型
│       ├── views.py      # 视图函数
│       ├── tests/        # 测试文件
│       └── admin.py      # 管理后台
├── vue/                   # Vue前端
│   ├── src/
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面视图
│   │   ├── router/       # 路由配置
│   │   └── store/        # 状态管理
│   ├── public/           # 静态资源
│   └── dist/             # 构建输出
├── mysql.sql             # 数据库初始化
├── manage.py             # Django管理脚本
└── README.md             # 项目文档
```

### 开发环境设置

#### 1. 后端开发
```bash
cd flight
python manage.py makemigrations  # 生成迁移文件
python manage.py migrate         # 执行迁移
python manage.py createsuperuser # 创建管理员用户
python manage.py runserver       # 启动开发服务器
```

#### 2. 前端开发
```bash
cd vue
npm run serve    # 启动开发服务器
npm run build    # 构建生产版本
npm run lint     # 代码检查
```

### 代码规范

#### Python代码规范
- 遵循PEP 8规范
- 使用Black代码格式化
- 使用isort导入排序

#### JavaScript代码规范
- 使用ESLint代码检查
- 遵循Vue.js风格指南
- 使用Prettier代码格式化

### 数据库设计

#### 核心数据表
- `passenger` - 乘客信息
- `p_account` - 乘客账户
- `m_account` - 管理员账户
- `flight` - 飞机信息
- `arrange` - 航班安排
- `stop` - 经停点
- `ticket` - 票务信息
- `relationships` - 关联关系

## 🧪 测试说明

### 测试覆盖

项目包含8个测试文件，覆盖主要功能模块：

- `test_auth.py` - 用户认证测试
- `test_profile.py` - 用户资料管理测试
- `test_relation.py` - 关联关系测试
- `test_ticket.py` - 票务管理测试
- `test_train.py` - 飞机管理测试
- `test_train_with_stops.py` - 经停点管理测试
- `test_data_alignment.py` - 数据一致性测试

### 运行测试

```bash
# 运行所有测试
cd flight
python manage.py test

# 运行特定测试文件
python manage.py test myapp.tests.test_auth

# 运行单个测试方法
python manage.py test myapp.tests.test_auth.UserAuthTests.test_login_success

# 查看测试覆盖率
coverage run manage.py test
coverage report
```

### 测试策略

- **单元测试**：测试单个函数和方法
- **集成测试**：测试API接口和数据库操作
- **功能测试**：测试完整业务流程
- **数据一致性测试**：测试复杂业务规则

## 🔧 维护指南

### 日常维护

#### 1. 日志管理
```python
# settings.py 中的日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

#### 2. 数据库维护
```sql
-- 定期备份数据库
mysqldump -u root -p train > backup_$(date +%Y%m%d).sql

-- 清理过期数据
DELETE FROM ticket WHERE t_paytime < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- 优化表性能
OPTIMIZE TABLE passenger, ticket, arrange;
```

#### 3. 性能监控
- 使用Django Debug Toolbar监控查询性能
- 定期分析慢查询日志
- 监控服务器资源使用情况

### 故障排除

#### 常见问题

**1. 数据库连接失败**
```bash
# 检查MySQL服务状态
sudo systemctl status mysql

# 检查连接配置
python manage.py dbshell
```

**2. 前端构建失败**
```bash
# 清理node_modules
rm -rf node_modules
npm install

# 检查Node.js版本
node --version
npm --version
```

**3. 静态文件无法访问**
```bash
# 收集静态文件
python manage.py collectstatic

# 检查文件权限
chmod -R 755 static/
```

### 备份恢复

#### 数据备份
```bash
# 完整备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/train_system"

# 数据库备份
mysqldump -u root -p train > $BACKUP_DIR/db_backup_$DATE.sql

# 代码备份
tar -czf $BACKUP_DIR/code_backup_$DATE.tar.gz /path/to/project

# 日志记录
echo "Backup completed at $DATE" >> $BACKUP_DIR/backup.log
```

#### 数据恢复
```bash
# 停止服务
sudo systemctl stop train-service

# 恢复数据库
mysql -u root -p train < backup_file.sql

# 恢复代码
tar -xzf code_backup.tar.gz -C /path/to/project

# 重启服务
sudo systemctl start train-service
```

## 📝 更新日志

### [v2.1.0] - 2025-01-04 🆕 **最新版本**

#### ✨ 新增功能
- **候补队列管理**：新增智能候补队列系统，提升用户体验
- **动态票价调整**：支持根据需求动态调整票价
- **座位分配优化**：改进座位分配算法，提高资源利用率
- **数据可视化**：集成ECharts图表，展示系统统计数据
- **日历组件集成**：使用FullCalendar优化日期选择体验

#### 🔧 技术改进
- **测试覆盖率提升**：新增17个测试类，覆盖复杂业务逻辑
- **API优化**：改进响应格式，增强错误处理
- **数据库优化**：添加更多索引，提升查询性能
- **前端组件升级**：更新Element UI至最新版本

#### 🐛 修复问题
- 修复跨域请求配置问题
- 优化用户注册流程
- 改进订单状态管理

#### 📚 文档更新
- 完善API文档
- 添加部署指南
- 补充维护手册

### [v2.0.0] - 2024-12-01

#### 🚀 重大更新
- **前后端分离重构**：采用Vue.js重写前端，Django提供API
- **数据库迁移**：从SQLite迁移至MySQL
- **用户体验优化**：全新UI设计，更直观的操作流程

#### ✨ 新增功能
- 用户注册登录系统
- 个人资料管理
- 关联旅客功能
- 飞机票预订
- 订单管理
- 管理员后台

### [v1.5.0] - 2024-10-15

#### 🔧 改进
- 添加基础的飞机信息管理
- 实现简单的票务查询功能
- 完善用户认证机制

### [v1.0.0] - 2024-09-01

#### 🎉 初始版本
- 基础的飞机票务管理系统
- 支持基本的CRUD操作
- 简单的用户界面

---

## 🤝 贡献指南

### 开发流程

1. **Fork项目**：点击GitHub右上角Fork按钮
2. **创建分支**：`git checkout -b feature/new-feature`
3. **提交代码**：`git commit -m "Add new feature"`
4. **推送分支**：`git push origin feature/new-feature`
5. **创建PR**：在GitHub上创建Pull Request

### 代码提交规范

```bash
# 提交信息格式
<type>(<scope>): <subject>

# 示例
feat(auth): add user registration API
fix(ticket): resolve booking conflict issue
docs(readme): update installation guide
test(profile): add user profile tests
```

### 分支管理

- `main` - 主分支，稳定版本
- `develop` - 开发分支，新功能开发
- `feature/*` - 功能分支
- `hotfix/*` - 紧急修复分支

### 代码审查

- 所有PR都需要至少一人审查
- 确保测试通过
- 遵循代码规范
- 更新相关文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 联系我们

如有问题或建议，请通过以下方式联系：

- 📧 邮箱：admin@trainsystem.com
- 🐛 问题反馈：GitHub Issues
- 📖 文档：https://trainsystem.com/docs

---

**最后更新时间：** 2025年1月4日
**版本：** v2.1.0