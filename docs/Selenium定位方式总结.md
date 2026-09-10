# Selenium 元素定位方式总结

## 八大定位方式

| 方式 | 方法 | 示例 | 适用场景 |
|------|------|------|---------|
| ID | `By.ID` | `find_element(By.ID, "username")` | 有唯一 ID 时优先使用 |
| Name | `By.NAME` | `find_element(By.NAME, "pwd")` | 表单元素常用 |
| Class Name | `By.CLASS_NAME` | `find_element(By.CLASS_NAME, "btn-login")` | 样式类名唯一时 |
| Tag Name | `By.TAG_NAME` | `find_element(By.TAG_NAME, "input")` | 标签类型唯一时 |
| Link Text | `By.LINK_TEXT` | `find_element(By.LINK_TEXT, "忘记密码")` | 完整链接文本 |
| Partial Link | `By.PARTIAL_LINK_TEXT` | `find_element(By.PARTIAL_LINK_TEXT, "忘记")` | 部分链接文本 |
| XPath | `By.XPATH` | `find_element(By.XPATH, "//input[@id='user']")` | 复杂定位，万能 |
| CSS Selector | `By.CSS_SELECTOR` | `find_element(By.CSS_SELECTOR, "#user")` | 性能优于 XPath |

## 优先级建议

1. **ID** > CSS Selector > XPath > 其他
2. 有唯一 ID 就用 ID，最稳定
3. CSS Selector 性能比 XPath 好，优先选
4. XPath 适合复杂层级关系或需要用文本定位时

## 显式等待 vs 隐式等待

```python
# 隐式等待 - 全局设置，所有 find_element 都会等
driver.implicitly_wait(10)

# 显式等待 - 针对特定元素，更精确
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "btn-submit"))
)
```

**实际使用建议**：项目中两者结合使用。隐式等待设一个较短的全局值（如 5 秒），关键元素用显式等待。
