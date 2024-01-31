import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AutomationPracticeFormPage:
    def __init__(self, driver):
        self.driver = driver

    # Elements
    FIRST_NAME_FIELD = (By.CSS_SELECTOR, "#firstName")
    LAST_NAME_FIELD = (By.XPATH, "//*[@id='lastName']")
    EMAIL_FIELD = (By.ID, "userEmail")
    MALE_RADIO_BUTTON = (By.ID, "gender-radio-1")
    MOBILE_FIELD = (By.ID, "userNumber")
    DATE_OF_BIRTH_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_FIELD = (By.ID, "react-select-3-input")
    CITY_FIELD = (By.ID, "react-select-4-input")
    SUBMIT_BUTTON = (By.ID, "submit")
    CONSENT_BUTTON = (By.CLASS_NAME, "fc-cta-consent")

    # Methods
    def give_consent_if_needed(self):
        try:
            consent_button = self.driver.find_element(*self.CONSENT_BUTTON)
            consent_button.click()
        except NoSuchElementException:
            pass

    def enter_text(self, locator, text):
        self.driver.find_element(*locator).send_keys(text)

    def click_element(self, locator):
        self.driver.execute_script(
            "arguments[0].click();", self.driver.find_element(*locator)
        )

    def upload_file(self, locator, file_path):
        self.driver.find_element(*locator).send_keys(file_path)

    def select_date_of_birth(self, year, month, day):
        self.driver.find_element(*self.DATE_OF_BIRTH_INPUT).click()
        self.driver.find_element(By.CSS_SELECTOR, f"option[value='{year}']").click()
        self.driver.find_element(By.CSS_SELECTOR, f"option[value='{month}']").click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            f"div.react-datepicker__day--0{day}:not(.react-datepicker__day--outside-month)",
        ).click()

    def submit_form(self):
        self.click_element(self.SUBMIT_BUTTON)

    def get_confirmation_message(self):
        return self.driver.find_element(By.ID, "example-modal-sizes-title-lg").text

    def get_table_data(self, label):
        return self.driver.find_element(By.XPATH, f"//tr[td='{label}']/td[2]").text


# Test Function
def test_form_submission():
    chrome_options = Options()
    adblock_path = "ublock_origin.crx"
    chrome_options.add_extension(adblock_path)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://demoqa.com/automation-practice-form")

    form_page = AutomationPracticeFormPage(driver)
    form_page.give_consent_if_needed()

    form_page.enter_text(form_page.FIRST_NAME_FIELD, "John")
    form_page.enter_text(form_page.LAST_NAME_FIELD, "Doe")
    form_page.enter_text(form_page.EMAIL_FIELD, "johndoe@gmail.com")
    form_page.click_element(form_page.MALE_RADIO_BUTTON)
    form_page.enter_text(form_page.MOBILE_FIELD, "9162345780")
    form_page.select_date_of_birth("1986", "8", "02")

    form_page.enter_text(form_page.SUBJECTS_INPUT, "Computer Science")
    form_page.driver.find_element(*form_page.SUBJECTS_INPUT).send_keys(
        Keys.ARROW_DOWN, Keys.ENTER
    )

    current_dir = os.path.abspath(os.path.dirname(__file__))
    upload_file = os.path.join(current_dir, "johndoe.jpeg")
    form_page.upload_file(form_page.UPLOAD_PICTURE, upload_file)

    form_page.enter_text(
        form_page.CURRENT_ADDRESS,
        "4986, Ramdwara Rd, Aram Bagh, Bharat Nagar, Paharganj",
    )
    form_page.enter_text(form_page.STATE_FIELD, "NCR")
    form_page.driver.find_element(*form_page.STATE_FIELD).send_keys(
        Keys.ARROW_DOWN, Keys.ENTER
    )
    form_page.enter_text(form_page.CITY_FIELD, "Delhi")
    form_page.driver.find_element(*form_page.CITY_FIELD).send_keys(
        Keys.ARROW_DOWN, Keys.ENTER
    )

    form_page.submit_form()

    assert "Thanks for submitting the form" in form_page.get_confirmation_message()
    assert form_page.get_table_data("Student Name") == "John Doe"
    assert form_page.get_table_data("Student Email") == "johndoe@gmail.com"
    assert form_page.get_table_data("Gender") == "Male"
    assert form_page.get_table_data("Mobile") == "9162345780"
    assert form_page.get_table_data("Date of Birth") == "02 September,1986"
    assert form_page.get_table_data("Subjects") == "Computer Science"
    assert form_page.get_table_data("Hobbies") == ""
    assert form_page.get_table_data("Picture") == "johndoe.jpeg"
    assert (
        form_page.get_table_data("Address")
        == "4986, Ramdwara Rd, Aram Bagh, Bharat Nagar, Paharganj"
    )
    assert form_page.get_table_data("State and City") == "NCR Delhi"

    driver.quit()
