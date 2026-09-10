"""
登录模块自动化测试
覆盖场景：登录成功、登录失败（密码错误）、登录后首页验证
"""
import pytest
import allure
from pages import LoginPage


@allure.epic("物流管理系统")
@allure.feature("登录模块")
class TestLogin:
    """登录功能测试集"""

    @allure.story("正常登录")
    @allure.title("测试用例01 - 使用正确账号密码登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_success(self, driver, base_url):
        """
        前置条件：系统已部署，测试账号 admin/123456 可用
        测试步骤：
            1. 打开登录页面
            2. 输入正确的用户名和密码
            3. 点击登录按钮
        预期结果：成功跳转到首页 /dashboard
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("admin", "123456")

        assert login_page.is_login_success(), "登录后未跳转到首页"

    @allure.story("异常登录")
    @allure.title("测试用例02 - 使用错误密码登录失败")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    def test_login_wrong_password(self, driver, base_url):
        """
        前置条件：系统已部署
        测试步骤：
            1. 打开登录页面
            2. 输入正确用户名和错误密码
            3. 点击登录按钮
        预期结果：显示错误提示「用户名或密码错误」
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("admin", "wrong_password")

        error_msg = login_page.get_error_message()
        assert "用户名或密码错误" in error_msg, f"错误提示不正确: {error_msg}"

    @allure.story("异常登录")
    @allure.title("测试用例03 - 用户名和密码为空时登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize("username, password, expected_msg", [
        ("", "123456", "请输入用户名"),
        ("admin", "", "请输入密码"),
        ("", "", "请输入用户名"),
    ])
    def test_login_empty_fields(self, driver, base_url, username, password, expected_msg):
        """参数化测试 - 验证空字段的提示信息"""
        login_page = LoginPage(driver, base_url)
        login_page.login(username, password)

        error_msg = login_page.get_error_message()
        assert expected_msg in error_msg, f"预期提示「{expected_msg}」，实际: {error_msg}"

    @allure.story("正常登录")
    @allure.title("测试用例08 - 登录后首页显示欢迎信息")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_welcome_text(self, driver, base_url):
        """
        前置条件：使用 admin 账号成功登录
        测试步骤：
            1. 登录系统
            2. 检查首页欢迎文本
        预期结果：页面显示「欢迎」字样
        """
        login_page = LoginPage(driver, base_url)
        login_page.login("admin", "123456")

        welcome = login_page.get_welcome_text()
        assert "欢迎" in welcome, f"首页未显示欢迎信息: {welcome}"
