"""
Pytest 全局配置 - 管理浏览器实例的生命周期
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def base_url():
    """测试环境基础 URL"""
    return "http://localhost:8080"


@pytest.fixture(scope="function")
def driver():
    """
    每个测试函数独立的浏览器实例
    测试结束后自动关闭，避免资源泄漏
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    # 无头模式（CI 环境下启用）
    # chrome_options.add_argument("--headless")

    _driver = webdriver.Chrome(options=chrome_options)
    _driver.implicitly_wait(10)

    yield _driver

    _driver.quit()


@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    """测试失败时自动截图并附加到 Allure 报告"""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="失败截图",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取测试结果用于截图判断"""
    import pytest
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
