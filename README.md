# 软件测试学习仓库

个人测试技术学习与实践的代码仓库，包含 Web UI 自动化测试脚本、接口测试集合以及学习笔记。

## 项目结构

```
├── pages/                    # Page Object 页面对象
│   ├── base_page.py          # 基类 - 封装通用操作
│   ├── login_page.py         # 登录页面
│   └── waybill_page.py       # 运单管理页面
├── tests/                    # Pytest 测试用例
│   ├── test_login.py         # 登录模块测试（用例01-03, 08）
│   ├── test_waybill.py       # 运单模块测试（用例04-07）
│   └── test_logout.py        # 退出登录测试（用例09）
├── postman/                  # Postman 接口测试
│   ├── 物流管理系统接口测试.postman_collection.json
│   ├── 开发环境.postman_environment.json
│   └── 测试环境.postman_environment.json
├── docs/                     # 学习笔记
├── conftest.py               # Pytest 全局配置（浏览器管理、失败截图）
├── pytest.ini                # Pytest 配置文件
├── requirements.txt          # Python 依赖
└── .gitignore
```

## 技术栈

- **UI 自动化**: Selenium WebDriver + Python
- **测试框架**: Pytest（参数化、fixture、marker）
- **测试报告**: Allure（可视化报告 + 失败自动截图）
- **设计模式**: Page Object Model (POM)
- **接口测试**: Postman（Collection + Environment + 断言）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行全部测试

```bash
pytest
```

### 3. 运行冒烟测试

```bash
pytest -m smoke
```

### 4. 生成 Allure 报告

```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## 测试用例覆盖

| 编号 | 场景 | 文件 | 标记 |
|------|------|------|------|
| 01 | 正确账号密码登录成功 | test_login.py | smoke, login |
| 02 | 错误密码登录失败 | test_login.py | login |
| 03 | 空字段登录（参数化） | test_login.py | login |
| 04 | 填写完整信息创建运单 | test_waybill.py | smoke, waybill |
| 05 | 按运单号精确查询 | test_waybill.py | waybill |
| 06 | 按时间范围批量查询 | test_waybill.py | waybill |
| 07 | 运单状态流转验证 | test_waybill.py | waybill |
| 08 | 登录后首页欢迎信息 | test_login.py | smoke, login |
| 09 | 退出登录跳转验证 | test_logout.py | smoke, login |

## Postman 接口测试

导入 `postman/` 目录下的 Collection 和 Environment 文件到 Postman 即可使用。

包含以下测试场景：
- 登录认证 & Token 获取
- 未认证访问拦截（401）
- 运单 CRUD 操作
- 参数校验（必填字段缺失、手机号格式）
- 权限控制（普通员工无权删除 → 403）
- 分页查询验证

## 学习记录

- Selenium 元素定位八大方式（id、name、class、tag、link text、partial link、xpath、css selector）
- 显式等待 vs 隐式等待的使用场景
- Page Object 设计模式的优势与实践
- Pytest fixture 作用域（function / class / module / session）
- Allure 报告定制（epic / feature / story / step）
