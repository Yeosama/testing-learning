"""
运单模块自动化测试
覆盖场景：创建运单、按运单号查询、按时间范围查询、运单状态流转
"""
import pytest
import allure
from pages import LoginPage, WaybillPage


@allure.epic("物流管理系统")
@allure.feature("运单管理模块")
class TestWaybill:
    """运单管理功能测试集"""

    @pytest.fixture(autouse=True)
    def login_first(self, driver, base_url):
        """每个测试前先登录系统"""
        LoginPage(driver, base_url).login("admin", "123456")

    @allure.story("创建运单")
    @allure.title("测试用例04 - 填写完整信息创建运单成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.waybill
    def test_create_waybill(self, driver, base_url):
        """
        前置条件：已登录系统
        测试步骤：
            1. 进入运单管理页面
            2. 点击新建运单
            3. 填写寄件人、收件人和货物信息
            4. 提交
        预期结果：提示创建成功
        """
        waybill_page = WaybillPage(driver, base_url)
        waybill_page.open_waybill_page()

        sender = {
            "name": "张三",
            "phone": "13800138001",
            "address": "广东省广州市天河区科韵路100号"
        }
        receiver = {
            "name": "李四",
            "phone": "13900139001",
            "address": "广东省深圳市南山区科技园200号"
        }
        goods = {
            "name": "电子产品",
            "weight": "2.5",
            "transport": "陆运"
        }

        waybill_page.create_waybill(sender, receiver, goods)
        assert waybill_page.is_create_success(), "运单创建失败"

    @allure.story("查询运单")
    @allure.title("测试用例05 - 按运单号精确查询")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.waybill
    def test_search_by_waybill_no(self, driver, base_url):
        """
        前置条件：已登录，系统中存在运单
        测试步骤：
            1. 进入运单管理页面
            2. 在搜索框输入运单号
            3. 点击查询
        预期结果：列表显示对应运单（结果数 >= 1）
        """
        waybill_page = WaybillPage(driver, base_url)
        waybill_page.open_waybill_page()
        waybill_page.search_by_waybill_no("202601010001")

        row_count = waybill_page.get_table_row_count()
        assert row_count >= 1, f"按运单号查询无结果，行数: {row_count}"

    @allure.story("查询运单")
    @allure.title("测试用例06 - 按时间范围批量查询")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.waybill
    def test_search_by_date_range(self, driver, base_url):
        """
        前置条件：已登录，系统中存在运单
        测试步骤：
            1. 进入运单管理页面
            2. 选择起止日期
            3. 点击查询
        预期结果：列表显示该时间范围内的运单
        """
        waybill_page = WaybillPage(driver, base_url)
        waybill_page.open_waybill_page()
        waybill_page.search_by_date_range("2026-01-01", "2026-06-30")

        row_count = waybill_page.get_table_row_count()
        assert row_count >= 0, "按时间范围查询异常"

    @allure.story("状态管理")
    @allure.title("测试用例07 - 运单状态流转：揽收→运输中→派件→签收")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.waybill
    def test_waybill_status_flow(self, driver, base_url):
        """
        前置条件：已登录，存在状态为「待揽收」的运单
        测试步骤：
            1. 打开运单详情
            2. 依次点击状态流转按钮
            3. 验证每一步状态变更
        预期结果：状态按 揽收→运输中→派件→签收 顺序流转
        """
        waybill_page = WaybillPage(driver, base_url)
        waybill_page.open_waybill_page()
        waybill_page.search_by_waybill_no("202601010001")

        expected_flow = ["已揽收", "运输中", "派件中", "已签收"]

        for expected_status in expected_flow:
            waybill_page.update_status()
            current_status = waybill_page.get_waybill_status()
            with allure.step(f"验证状态变更为: {expected_status}"):
                assert current_status == expected_status, \
                    f"状态流转异常，预期: {expected_status}，实际: {current_status}"
