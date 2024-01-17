from appium.webdriver.common.appiumby import AppiumBy

mlocators = {
    "search_product": (AppiumBy.XPATH, '//android.widget.TextView[@text="SEARCH PRODUCT"]'),
    "application_dropdown": (AppiumBy.XPATH, "//android.view.View[@resource-id='ddlApplicatrion']"),
    "home_tile_btn": (AppiumBy.XPATH, '//android.view.View[@content-desc=" Home"]'),
    "home_textiles_radio_btn":(AppiumBy.XPATH, '//android.widget.CheckedTextView[@text="Home Textiles"]'),
    "range_dropdown":(AppiumBy.XPATH, '//android.view.View[@resource-id="ddlRange"]'),
    "home_furnishing_radio_btn":(AppiumBy.XPATH,'//android.widget.CheckedTextView[@text="Home Furnishing"]'),
    "submit_btn":(AppiumBy.XPATH,'//android.widget.Button[@text="SUBMIT "]'),
    "view_more_btn":(AppiumBy.XPATH,'//android.widget.Button[@text="View More"]'),
    "details_tab":(AppiumBy.XPATH,'//android.widget.TextView[@text="Details"]'),
}