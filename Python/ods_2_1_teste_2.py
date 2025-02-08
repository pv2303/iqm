from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

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
wait = WebDriverWait(driver, 10)


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
        if ($('#{selector}').hasClass('selectpicker')) {{
            $('#{selector}').selectpicker('refresh');
        }}
    """)

    print(f"{selector} selected successfully via JavaScript\n {value[1]} {value[0]} selected.")

age_group_selector = {
    'nu_ciclo_vida': [age_group, 'Age Group'],
    'nu_intervalo_idade_inicio': [age_int_start, 'Age Interval Start'],
    'nu_intervalo_idade_fim': [age_int_end, 'Age Interval End'],
    'nu_indice_cri': []
}

# Selecting the age group
driver.execute_script('document.getElementsByName("nu_ciclo_vida")[0].scrollIntoView();')


# PAREI AQUI. TALVEZ COLOCAR TUDO NO FOR E COLOCAR O DISPACH EVENT ALEM DO REFRESH
driver.execute_script("""""")
driver.execute_script('$("#nu_ciclo_vida").selectpicker("refresh");')

# Selecting the age interval
#driver.execute_script()

sleep(5)

driver.quit()