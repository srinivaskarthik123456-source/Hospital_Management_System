from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================================
# SETTINGS
# ============================================================

MAIN_URL = "http://127.0.0.1:5000"
ADMIN_URL = "http://127.0.0.1:5001"

driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 10)

passed = 0
failed = 0


# ============================================================
# COMMON FUNCTIONS
# ============================================================

def open_page(url):
    driver.get(url)
    time.sleep(1)


def fill(name, value):
    element = wait.until(
        EC.presence_of_element_located(
            (By.NAME, name)
        )
    )
    element.clear()
    element.send_keys(value)


def choose(name, value):
    element = wait.until(
        EC.presence_of_element_located(
            (By.NAME, name)
        )
    )

    if element.tag_name.lower() == "select":
        try:
            Select(element).select_by_visible_text(value)
        except:
            Select(element).select_by_value(value)
    else:
        element.clear()
        element.send_keys(value)


def submit():
    driver.find_element(
        By.TAG_NAME,
        "form"
    ).submit()

    time.sleep(1)


def login_admin():

    open_page(
        ADMIN_URL + "/admin-login"
    )

    fill("username", "admin")
    fill("password", "admin123")

    submit()

    wait.until(
        EC.url_contains("/admin")
    )


def test(number, name, function):

    global passed, failed

    try:

        function()

        print(
            f"TC{number:02d} PASS - {name}"
        )

        passed += 1

    except Exception as e:

        print(
            f"TC{number:02d} FAIL - {name}"
        )

        print(
            "   Error:",
            type(e).__name__,
            str(e)
        )

        failed += 1


# ============================================================
# TC01 - HOME PAGE
# ============================================================

def tc01():

    open_page(MAIN_URL)

    assert driver.current_url.startswith(
        MAIN_URL
    )

    print("   Home page opened")


# ============================================================
# TC02 - PATIENT REGISTRATION
# ============================================================

def tc02():

    open_page(
        MAIN_URL + "/patient-registration"
    )

    fill(
        "name",
        "Selenium Patient"
    )

    fill(
        "age",
        "21"
    )

    choose(
        "gender",
        "Male"
    )

    fill(
        "phone",
        "9999999999"
    )

    fill(
        "email",
        "selenium@gmail.com"
    )

    fill(
        "address",
        "Tirupati"
    )

    fill(
        "problem",
        "Fever"
    )

    choose(
        "doctor",
        "Dr. Ravi Kumar"
    )

    fill(
        "date",
        "2026-08-20"
    )

    submit()

    assert "/success" in driver.current_url

    assert (
        "Patient Registered Successfully"
        in driver.page_source
    )


# ============================================================
# TC03 - PATIENT FORM REQUIRED FIELDS
# ============================================================

def tc03():

    open_page(
        MAIN_URL + "/patient-registration"
    )

    form = driver.find_element(
        By.TAG_NAME,
        "form"
    )

    required = form.find_elements(
        By.CSS_SELECTOR,
        "[required]"
    )

    assert len(required) > 0

    names = []

    for field in required:

        name = field.get_attribute("name")

        if name:
            names.append(name)

    assert "name" in names
    assert "age" in names
    assert "phone" in names
    assert "email" in names


# ============================================================
# TC04 - APPOINTMENT BOOKING
# ============================================================

def tc04():

    open_page(
        MAIN_URL + "/appointments"
    )

    fill(
        "patient_name",
        "Selenium Patient"
    )

    fill(
        "phone",
        "9999999999"
    )

    choose(
        "doctor",
        "Dr. Ravi Kumar"
    )

    fill(
        "appointment_date",
        "2026-08-25"
    )

    fill(
        "appointment_time",
        "10:00"
    )

    fill(
        "reason",
        "General Checkup"
    )

    submit()

    assert (
        "/appointment-success"
        in driver.current_url
    )


# ============================================================
# TC05 - APPOINTMENT FORM
# ============================================================

def tc05():

    open_page(
        MAIN_URL + "/appointments"
    )

    form = driver.find_element(
        By.TAG_NAME,
        "form"
    )

    fields = form.find_elements(
        By.CSS_SELECTOR,
        "input, select, textarea"
    )

    assert len(fields) >= 5


# ============================================================
# TC06 - PATIENT RECORDS
# ============================================================

def tc06():

    open_page(
        MAIN_URL + "/patients"
    )

    assert "/patients" in driver.current_url

    assert (
        "Patient" in driver.page_source
        or "Name" in driver.page_source
    )


# ============================================================
# TC07 - APPOINTMENT RECORDS
# ============================================================

def tc07():

    open_page(
        MAIN_URL + "/appointment-records"
    )

    assert (
        "/appointment-records"
        in driver.current_url
    )

    assert (
        "Appointment" in driver.page_source
        or "Patient Name" in driver.page_source
    )


# ============================================================
# TC08 - ADMIN LOGIN
# ============================================================

def tc08():

    login_admin()

    assert "/admin" in driver.current_url

    assert (
        "Admin Dashboard"
        in driver.page_source
    )


# ============================================================
# TC09 - INVALID ADMIN LOGIN
# ============================================================

def tc09():

    open_page(
        ADMIN_URL + "/admin-logout"
    )

    open_page(
        ADMIN_URL + "/admin-login"
    )

    fill(
        "username",
        "wrong"
    )

    fill(
        "password",
        "wrong"
    )

    submit()

    assert (
        "Invalid username or password"
        in driver.page_source
    )


# ============================================================
# TC10 - ADMIN DASHBOARD
# ============================================================

def tc10():

    login_admin()

    assert (
        "Welcome, Admin"
        in driver.page_source
    )

    assert (
        "Total Patients"
        in driver.page_source
    )

    assert (
        "Total Appointments"
        in driver.page_source
    )


# ============================================================
# TC11 - PATIENT SEARCH
# ============================================================

def tc11():

    login_admin()

    search = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "search")
        )
    )

    search.clear()

    search.send_keys(
        "Srinivas"
    )

    buttons = driver.find_elements(
        By.CSS_SELECTOR,
        ".search-btn"
    )

    if buttons:

        buttons[0].click()

    else:

        search.submit()

    time.sleep(1)

    assert (
        "Srinivas" in driver.page_source
        or "Patient" in driver.page_source
    )


# ============================================================
# TC12 - PATIENT EDIT
# ============================================================

def tc12():

    login_admin()

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/admin/edit-patient/']"
    )

    assert len(links) > 0

    links[0].click()

    time.sleep(1)

    assert (
        "/admin/edit-patient/"
        in driver.current_url
    )


# ============================================================
# TC13 - APPOINTMENT EDIT
# ============================================================

def tc13():

    login_admin()

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/admin/edit-appointment/']"
    )

    assert len(links) > 0

    links[0].click()

    time.sleep(1)

    assert (
        "/admin/edit-appointment/"
        in driver.current_url
    )


# ============================================================
# TC14 - PATIENT DELETE BUTTON
# ============================================================

def tc14():

    login_admin()

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/admin/delete-patient/']"
    )

    assert len(links) > 0

    href = links[0].get_attribute(
        "href"
    )

    assert (
        "/admin/delete-patient/"
        in href
    )


# ============================================================
# TC15 - ADMIN LOGOUT
# ============================================================

def tc15():

    login_admin()

    buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "a.logout"
    )

    if not buttons:

        buttons = driver.find_elements(
            By.PARTIAL_LINK_TEXT,
            "Logout"
        )

    assert len(buttons) > 0

    buttons[0].click()

    time.sleep(1)

    assert (
        "/admin-login"
        in driver.current_url
    )


# ============================================================
# START TESTING
# ============================================================

print()
print("=" * 60)
print("🏥 CITY CARE HOSPITAL")
print("SELENIUM AUTOMATION")
print("=" * 60)
print()


test(1, "Home Page", tc01)
test(2, "Patient Registration", tc02)
test(3, "Patient Required Fields", tc03)
test(4, "Appointment Booking", tc04)
test(5, "Appointment Form", tc05)
test(6, "Patient Records", tc06)
test(7, "Appointment Records", tc07)
test(8, "Valid Admin Login", tc08)
test(9, "Invalid Admin Login", tc09)
test(10, "Admin Dashboard", tc10)
test(11, "Patient Search", tc11)
test(12, "Patient Edit", tc12)
test(13, "Appointment Edit", tc13)
test(14, "Patient Delete Button", tc14)
test(15, "Admin Logout", tc15)


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 60)
print("FINAL TEST RESULT")
print("=" * 60)

print(
    "Total Test Cases : 15"
)

print(
    "Passed           :",
    passed
)

print(
    "Failed           :",
    failed
)

print(
    "Pass Percentage  :",
    f"{passed / 15 * 100:.2f}%"
)

print("=" * 60)


if passed == 15:

    print()
    print("🎉 15/15 TEST CASES PASSED")
    print("✅ SELENIUM TESTING SUCCESSFUL")
    print()

else:

    print()
    print(
        f"❌ {failed} TEST CASE(S) FAILED"
    )
    print()


driver.quit()