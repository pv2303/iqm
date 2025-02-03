from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# Setting up the commong search
year = '2008'
month = 'JANEIRO'
group = 'MUNICÍPIO'
state = 'TODOS'
city = 'TODOS'

# Set up WebDriver
driver_path = "Python/Chrome Driver/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the page
driver.get("https://sisaps.saude.gov.br/sisvan/relatoriopublico/index")

# Wait for page to load
sleep(3)  # Give time for full page load

# Wait until the div containing 'Estado Nutricional' is present
wait = WebDriverWait(driver, 5)

target_div = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'info-box-content') and .//span[@title='Estado Nutricional']]")
    )
)
print("Found target div!")

# Locate the button inside the div
target_button = target_div.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")

sleep(.5)

# Click using JavaScript (if normal click fails)
try:
    target_button.click()
    print("Clicked button using normal click")
except:
    print("Normal click failed, using JavaScript click...")
    driver.execute_script("arguments[0].click();", target_button)

# Sleep to see the effect
sleep(2)

# Click de dropdowns
year_drop_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-id='nuAno']")
    )
)

print("Target Dropdown Year Button Found")

year_drop_button.click()

sleep(1)

# Try finding the option dynamically
# Select the year
year_option = wait.until(
    EC.presence_of_element_located((By.XPATH, f"//span[text()='{year}']"))
)

# Scroll and click using JavaScript
driver.execute_script("arguments[0].scrollIntoView(true);", year_option)
sleep(.5)

driver.execute_script("arguments[0].click();", year_option)
print(f"Selected year: {year}")

sleep(.5)

# Month Drop
month_drop_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@data-id='nuMes']")
    )
)

print("Target Dropdown Month Button Found")

driver.execute_script('arguments[0].scrollIntoView(true);', month_drop_button)
sleep(.5)

driver.execute_script('arguments[0].click();', month_drop_button)
sleep(.5)

# Month Option
month_option = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, f"//span[text()='{month}']")
    )
)

driver.execute_script('arguments[0].scrollIntoView(true);', month_option)
sleep(.5)

driver.execute_script('arguments[0].click();', month_option)
sleep(.5)

print(f'Selected month: {month}')
sleep(.5)

# Group Drop
group_drop_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='form-group']//button[@title='MUNICÍPIO']")
    )
)

print("Target Dropdown Group Button Found")

driver.execute_script('arguments[0].scrollIntoView(true);', group_drop_button)
sleep(.5)

driver.execute_script('arguments[0].click();', group_drop_button)
sleep(.5)

# Group Option
group_option = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, f"//span[text()='{group}']")
    )
)

# Selecting the group

driver.execute_script('arguments[0].scrollIntoView(true);', group_option)
sleep(.5)

driver.execute_script('arguments[0].click();', group_option)
sleep(.5)

print(f'Selected group: {group}')

sleep(5)

# Close browser
driver.quit()
