from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Setting up the common search
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

wait = WebDriverWait(driver, 5)

# wait untill ESTADO NUTRICIONAL report div is present

# Wait for the main div
wait = WebDriverWait(driver, 10)
target_div = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.info-box-content'))
)

# Wait for the button inside the div
target_button = WebDriverWait(target_div, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.info-box-text > a[target="1"]'))
)

target_button.click()

# Set the value via JavaScript
driver.execute_script("document.getElementById('nuAno').value = arguments[0];", year)
# Trigger change event to notify Bootstrap UI
driver.execute_script("$('#nuAno').selectpicker('refresh');")
# Set the value via JavaScript
driver.execute_script("document.getElementById('nuMes').value = arguments[0];", month)
# Trigger change event to notify Bootstrap UI
driver.execute_script("$('#nuMes').selectpicker('refresh');")

print(f"Year {year} selected successfully via JavaScript!")
print(f"Month {month} selected successfully via JavaScript!")
sleep(5)

driver.quit()