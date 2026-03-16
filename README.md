### 项目说明

这是一个基于 **FastAPI + SQLAlchemy + MySQL** 的后端项目。  
代码主要在 `app/` 目录下，依赖列表在 `requirements.txt` 中。

---

### 环境要求

- **Python**：建议 `Python 3.10+`
- **数据库**：本地或远程 MySQL 实例
- **操作系统**：Windows / macOS / Linux 均可

---

### 1. 克隆代码并进入目录

```bash
git clone <your-repo-url>
cd softs_backend   # 或你的仓库目录
```

仓库结构大致如下：

```text
.
├─ app/
└─ requirements.txt
```

---

### 2. 创建并激活虚拟环境（推荐）

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
# python3 -m venv .venv
# source .venv/bin/activate
```

---

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

### 4. 配置环境变量（可选但推荐）

项目的配置在 `app/config.py` 中，通过环境变量加载，默认配置为：

- **DEBUG**：`False`
- **MYSQL_URL**：`mysql+pymysql://root:password@localhost:3306/softs_db?charset=utf8mb4`
- **JWT_SECRET_KEY**：`your-secret-key-change-in-production`
- **JWT_ALGORITHM**：`HS256`
- **ACCESS_TOKEN_EXPIRE_MINUTES**：`10080`（7 天）
- **OPENAI_API_KEY / DEEPSEEK_API_KEY**：默认空字符串

推荐在项目根目录创建一个 `.env` 文件（与 `requirements.txt` 同级），例如：

```env
DEBUG=true

# 根据自己本地 MySQL 信息修改
MYSQL_URL=mysql+pymysql://root:your_password@localhost:3306/softs_db?charset=utf8mb4

JWT_SECRET_KEY=please-change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# 如需对接大模型 API，在这里填入
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
```

> `.env` 会被 `app/config.py` 自动加载。

---

### 5. 准备数据库

1. 保证 MySQL 已启动，并且 `MYSQL_URL` 中指定的数据库存在，例如：

```sql
CREATE DATABASE softs_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 首次启动应用时，代码会自动根据模型创建表，并尝试把数据库和已有表字符集转为 `utf8mb4` 以支持中文。

---

### 6. 启动服务

在项目根目录执行（确保虚拟环境已激活）：

```bash
uvicorn app.main:app --reload
```

- 默认监听：`http://127.0.0.1:8000`
- 根路径测试接口：`GET /` 返回 `{"Hello": "World"}`

---

### 7. 调试与开发

- 开启调试：在 `.env` 中设置

```env
DEBUG=true
```

当 `DEBUG=true` 时，如果后端抛出未捕获异常，接口会返回详细错误信息，便于开发排查。

---

### 8. 常见问题

- **无法连接数据库**  
  检查：
  - MySQL 是否启动
  - `.env` 中的 `MYSQL_URL` 用户名、密码、库名是否正确
  - 端口和主机是否可达（例如 `localhost:3306`）

- **启动时报依赖缺失**  
  确保使用的是虚拟环境，并重新执行：

  ```bash
  pip install -r requirements.txt
  ```
