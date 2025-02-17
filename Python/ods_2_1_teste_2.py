from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd


# Setting up the common search
year = 2008 
month = 1
group = 'M'
state = '99'
city = '99'
age_group = '1' # 0-5 years old
age_int_start = '0' # from 0 year old
age_int_end = '5' # up to 5 years old
age_index = '2' # Weight X Height

if month < 10:
    month = f"0{month}"
else:
    month = f"{month}"

# Set up WebDriver
driver_path = "Python/Chrome Driver/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the page
driver.get("https://sisaps.saude.gov.br/sisvan/relatoriopublico/index")

# Establishing the waiting time for 10 secs
wait = WebDriverWait(driver, 20)


target_div = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.info-box-content'))
)

# Wait for the button inside the div
target_button = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.info-box-text > a[target="1"]'))
)

target_button.click()

main_selectors = {
    'nuAno': [year, 'year'],
    'nuMes[]': [month, 'month'],
    'tpFiltro': [group, 'Group Filter'],
    'coUfIbge': [state, 'Group state filter'],
    'coMunicipioIbge': [city, 'Group city filter']
}

# Itering over the main selectors
for selector, value in main_selectors.items():
    driver.execute_script(f"""
        var elements = document.getElementsByName('{selector}');
        if (elements.length > 0) {{
        elements[0].value = '{value[0]}';
        var event = new Event('change', {{ bubbles: true }});
        elements[0].dispatchEvent(event);
        }}
    """)
    
    # Refresh Bootstrap dropdown if necessary
    driver.execute_script(f"""
        if ($('#arguments[0]').hasClass('selectpicker')) {{
            $('#arguments[0]').selectpicker('refresh');
        }}
    """, selector)

    print(f"{selector} selected successfully via JavaScript\n {value[1]} {value[0]} selected.")

age_group_selector = {
    'nu_ciclo_vida': [age_group, 'Age Group'],
    'nu_idade_inicio': [age_int_start, 'Age Interval Start'],
    'nu_idade_fim': [age_int_end, 'Age Interval End'],
    'nu_indice_cri': [age_index, 'Index']
}


# Itering over the age group selectors
for selector, value in age_group_selector.items():

    # Scroll the element into view and select the dropdown option
    driver.execute_script(f"""
        var elements = document.getElementsByName('{selector}');
        if (elements.length > 0) {{
            elements[0].scrollIntoView();
        }}
        if (elements.length > 0) {{
            elements[0].value = '{value[0]}';
            var event = new Event('change', {{ bubbles: true }});
            elements[0].dispatchEvent(event);
            }}
    """)

    if selector == 'nu_ciclo_vida':
        wait.until(
            EC.presence_of_element_located((By.NAME, 'nu_idade_inicio'))
        )
    elif selector == 'nu_idade_inicio':
        wait.until(
            EC.presence_of_element_located((By.NAME, 'nu_idade_fim'))
        )

    # Refresh Bootstrap dropdown if necessary
    driver.execute_script(f"""
        if ($('#arguments[0]').hasClass('selectpicker')) {{
            $('#arguments[0]').selectpicker('refresh');
        }}
    """, selector)

    print(f"{selector} selected successfully via JavaScript\n {value[1]} {value[0]} selected.")

sleep(2)

# Click on the search button

target_button_table = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'button#verTela'))
)

target_button_table.click()

sleep(2)

# Switching to the new window
wait.until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])

print("Switched to the HTML table's tab")

table = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
)

table_html = table.get_attribute('outerHTML')

soup = BeautifulSoup(table_html, 'html.parser')

print("Table HTML retrieved successfully")

table = soup.find('table')

df = pd.read_html(str(table))[0]

#Flattening the columns
df.columns = ['_'.join(col).strip() for col in df.columns]

# saving the df_teste_2 to a csv file
df.to_csv('Python/ods_2_1_teste_2.csv', index=False, sep=';', encoding='utf-8')

print(df.head())
print(df.info())
print(df.shape)

# Optional: Close the new tab & switch back to main
driver.switch_to.window(driver.window_handles[0]) # Back to main page
driver.close()

print("Switched back to the main report page")

sleep(5)

driver.quit()