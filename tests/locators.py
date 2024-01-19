from selenium.webdriver.common.by import By

locators = {
    "btn_login": (By.XPATH, "//span[.='LOGIN']"),
    "txt_username": (By.XPATH, "//input[@formcontrolname='username']"),
    "txt_password": (By.XPATH, "//input[@formcontrolname='password']"),
    "all_requests": (By.XPATH, "//div[.='All Requests']"),
    "my_requests": (By.XPATH, "//div[.='My Requests']"),
    "create_request": (By.XPATH, "//div//mat-select[@formcontrolname='selectDropdown']/following::mat-label"),
    "service_group":(By.XPATH, "//mat-select[@formcontrolname='serviceGroupId']"),
    "service_name":(By.XPATH, "//mat-select[@placeholder='Service N']"),
    "search":(By.XPATH, "//input[@placeholder='Search']"),
    "source_input":(By.XPATH, "//input[@formcontrolname='sourceId']"),
    "remarks_input":(By.XPATH, "//textarea[@formcontrolname='remarks']"),
    "send_request":(By.XPATH,"//button/span[.='Send Request']"),
    "waiting_confirmation": (By.XPATH, "//div[.='Confirmation']"),
    "yes":(By.XPATH,"//div[@class='custom-dialog-box']//mat-dialog-actions//button[.='Yes']"),
    "success_message":(By.XPATH,"//div[.='Request Details Saved successfully']"),
    "request_id":(By.XPATH,"//th//div//div//span[contains(text(),'RequestID')]"),
    "pickup_time":(By.XPATH,"//input[@formcontrolname='startTime']"),
    "hamburger":(By.XPATH,"//img[contains(@src, 'hamburger')]/parent::div"),
    "workflows":(By.XPATH,"(//img[contains(@src, 'Menus')]/following-sibling::div[contains(normalize-space(),'Workflows')])[2]")

}
