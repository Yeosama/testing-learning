"""
Page Object 基类 - 封装通用的页面操作方法
所有页面类继承此基类，复用元素定位、点击、输入等操作
"""
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """页面对象基类"""

    def __init__(self, driver: WebDriver, base_url: str = "http://localhost:8080"):
        self.driver = driver
        self.base_url = base_url

    def open(self, path: str = ""):
        """打开指定路径的页面"""
        url = f"{self.base_url}{path}"
        with allure.step(f"打开页面: {url}"):
            self.driver.get(url)
        return self

    def find_element(self, locator: tuple, timeout: int = 10) -> WebElement:
        """显式等待并查找单个元素"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: tuple, timeout: int = 10) -> list:
        """显式等待并查找多个元素"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple, timeout: int = 10):
        """等待元素可点击后执行点击"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return self

    def send_keys(self, locator: tuple, text: str, clear_first: bool = True):
        """向输入框输入文本"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator: tuple) -> str:
        """获取元素文本内容"""
        return self.find_element(locator).text

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """判断元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def wait_for_element_disappear(self, locator: tuple, timeout: int = 10):
        """等待元素消失（如 loading 动画）"""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        return self

    def get_current_url(self) -> str:
        """获取当前页面 URL"""
        return self.driver.current_url

    def get_title(self) -> str:
        """获取页面标题"""
        return self.driver.title
