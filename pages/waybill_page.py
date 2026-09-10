"""
运单管理页面 Page Object
封装运单的创建、查询、状态流转等操作
"""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class WaybillPage(BasePage):
    """运单管理页面"""

    # ===== 元素定位器 =====
    # 运单列表
    BTN_CREATE = (By.CSS_SELECTOR, ".btn-create-waybill")
    INPUT_SEARCH = (By.ID, "search-waybill-no")
    BTN_SEARCH = (By.ID, "btn-search")
    INPUT_DATE_START = (By.ID, "date-start")
    INPUT_DATE_END = (By.ID, "date-end")
    TABLE_ROWS = (By.CSS_SELECTOR, ".waybill-table tbody tr")
    LABEL_NO_DATA = (By.CSS_SELECTOR, ".el-table__empty-text")

    # 创建运单表单
    INPUT_SENDER_NAME = (By.ID, "sender-name")
    INPUT_SENDER_PHONE = (By.ID, "sender-phone")
    INPUT_SENDER_ADDR = (By.ID, "sender-address")
    INPUT_RECEIVER_NAME = (By.ID, "receiver-name")
    INPUT_RECEIVER_PHONE = (By.ID, "receiver-phone")
    INPUT_RECEIVER_ADDR = (By.ID, "receiver-address")
    INPUT_GOODS_NAME = (By.ID, "goods-name")
    INPUT_GOODS_WEIGHT = (By.ID, "goods-weight")
    SELECT_TRANSPORT = (By.ID, "transport-type")
    BTN_SUBMIT = (By.ID, "btn-submit")
    MSG_CREATE_SUCCESS = (By.CSS_SELECTOR, ".el-message--success")

    # 运单详情
    LABEL_STATUS = (By.CSS_SELECTOR, ".waybill-status")
    BTN_UPDATE_STATUS = (By.ID, "btn-update-status")

    # ===== 页面操作 =====
    def open_waybill_page(self):
        """打开运单管理页面"""
        self.open("/waybill")
        return self

    @allure.step("查询运单号: {waybill_no}")
    def search_by_waybill_no(self, waybill_no: str):
        """按运单号搜索"""
        self.send_keys(self.INPUT_SEARCH, waybill_no)
        self.click(self.BTN_SEARCH)
        return self

    @allure.step("按时间范围查询: {start} 至 {end}")
    def search_by_date_range(self, start: str, end: str):
        """按时间范围搜索"""
        self.send_keys(self.INPUT_DATE_START, start)
        self.send_keys(self.INPUT_DATE_END, end)
        self.click(self.BTN_SEARCH)
        return self

    def get_table_row_count(self) -> int:
        """获取运单列表行数"""
        if self.is_element_visible(self.LABEL_NO_DATA, timeout=3):
            return 0
        return len(self.find_elements(self.TABLE_ROWS))

    @allure.step("创建新运单")
    def create_waybill(self, sender: dict, receiver: dict, goods: dict):
        """
        填写并提交运单表单
        :param sender: 寄件人信息 {"name": "", "phone": "", "address": ""}
        :param receiver: 收件人信息
        :param goods: 货物信息 {"name": "", "weight": "", "transport": ""}
        """
        self.click(self.BTN_CREATE)

        # 寄件人信息
        self.send_keys(self.INPUT_SENDER_NAME, sender["name"])
        self.send_keys(self.INPUT_SENDER_PHONE, sender["phone"])
        self.send_keys(self.INPUT_SENDER_ADDR, sender["address"])

        # 收件人信息
        self.send_keys(self.INPUT_RECEIVER_NAME, receiver["name"])
        self.send_keys(self.INPUT_RECEIVER_PHONE, receiver["phone"])
        self.send_keys(self.INPUT_RECEIVER_ADDR, receiver["address"])

        # 货物信息
        self.send_keys(self.INPUT_GOODS_NAME, goods["name"])
        self.send_keys(self.INPUT_GOODS_WEIGHT, goods["weight"])

        # 选择运输方式
        select = Select(self.find_element(self.SELECT_TRANSPORT))
        select.select_by_visible_text(goods.get("transport", "陆运"))

        self.click(self.BTN_SUBMIT)
        return self

    def is_create_success(self) -> bool:
        """判断运单创建是否成功"""
        return self.is_element_visible(self.MSG_CREATE_SUCCESS)

    def get_waybill_status(self) -> str:
        """获取当前运单状态"""
        return self.get_text(self.LABEL_STATUS)

    @allure.step("更新运单状态")
    def update_status(self):
        """点击状态流转按钮"""
        self.click(self.BTN_UPDATE_STATUS)
        return self
