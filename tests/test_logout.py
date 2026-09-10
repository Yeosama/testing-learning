"""
退出登录测试
"""
import allure
import pytest
from pages import LoginPage


@allure.epic("物流管理系统")
@allure.feature("登录模块")
class TestLogout:
    """退出登录测试"""

    @allure.story("退出登录")
    @allure.title("测试用例09 - 点击退出后跳转回登录页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_logout(self, driver, base_url):
        """
        前置条件：已登录系统
        测试步骤：
            1. 登录系统
            2. 点击退出登录
        预期结果：跳转回登录页 /login
        """
        from selenium.webdriver.common.by import By

        login_page = LoginPage(driver, base_url)
        login_page.login("admin", "123456")

        with allure.step("点击退出登录按钮"):
            driver.find_element(By.CSS_SELECTOR, ".btn-logout").click()

        with allure.step("验证跳转到登录页"):
            assert "/login" in driver.current_url, \
                f"退出后未跳转到登录页，当前URL: {driver.current_url}"
