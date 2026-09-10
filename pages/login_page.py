"""
登录页面 Page Object
封装登录页面的元素定位和业务操作
"""
import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """登录页面"""

    # ===== 元素定位器 =====
    INPUT_USERNAME = (By.ID, "username")
    INPUT_PASSWORD = (By.ID, "password")
    BTN_LOGIN = (By.ID, "btn-login")
    MSG_ERROR = (By.CSS_SELECTOR, ".login-error-msg")
    MSG_SUCCESS = (By.CSS_SELECTOR, ".el-message--success")
    LABEL_WELCOME = (By.CSS_SELECTOR, ".welcome-text")

    # ===== 页面操作 =====
    def open_login_page(self):
        """打开登录页面"""
        self.open("/login")
        return self

    @allure.step("输入用户名: {username}")
    def input_username(self, username: str):
        self.send_keys(self.INPUT_USERNAME, username)
        return self

    @allure.step("输入密码")
    def input_password(self, password: str):
        self.send_keys(self.INPUT_PASSWORD, password)
        return self

    @allure.step("点击登录按钮")
    def click_login(self):
        self.click(self.BTN_LOGIN)
        return self

    def login(self, username: str, password: str):
        """
        完整的登录操作
        :param username: 用户名
        :param password: 密码
        """
        with allure.step(f"执行登录操作 - 用户名: {username}"):
            self.open_login_page()
            self.input_username(username)
            self.input_password(password)
            self.click_login()
        return self

    def get_error_message(self) -> str:
        """获取登录错误提示信息"""
        return self.get_text(self.MSG_ERROR)

    def is_login_success(self) -> bool:
        """判断是否登录成功（跳转到首页）"""
        return "/dashboard" in self.get_current_url()

    def get_welcome_text(self) -> str:
        """获取首页欢迎文本"""
        return self.get_text(self.LABEL_WELCOME)
