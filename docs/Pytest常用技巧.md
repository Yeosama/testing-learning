# Pytest 常用技巧

## 参数化测试

```python
@pytest.mark.parametrize("username, password, expected", [
    ("admin", "123456", True),
    ("admin", "wrong", False),
    ("", "123456", False),
])
def test_login(username, password, expected):
    result = do_login(username, password)
    assert result == expected
```

## fixture 作用域

| 作用域 | 说明 | 场景 |
|--------|------|------|
| function | 每个测试函数执行一次（默认） | 浏览器实例 |
| class | 每个测试类执行一次 | 登录状态 |
| module | 每个模块执行一次 | 数据库连接 |
| session | 整个测试会话执行一次 | 全局配置 |

## 常用命令

```bash
# 运行全部测试
pytest

# 运行指定文件
pytest tests/test_login.py

# 运行指定标记的用例
pytest -m smoke

# 详细输出
pytest -v

# 失败后立即停止
pytest -x

# 生成 Allure 数据
pytest --alluredir=./allure-results

# 查看 Allure 报告
allure serve ./allure-results
```

## Allure 装饰器

```python
@allure.epic("项目名称")        # 最高层级
@allure.feature("模块名称")     # 功能模块
@allure.story("用户故事")       # 具体场景
@allure.title("用例标题")       # 用例名称
@allure.severity(severity_level.CRITICAL)  # 严重程度
@allure.step("操作步骤描述")    # 测试步骤
```
