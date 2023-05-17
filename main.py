from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import timedelta, datetime
from dateutil.relativedelta import *
import pandas as pd
import time

#Definindo parametros e opções
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_experimental_option("detach", True)
navegator = webdriver.Chrome('C:/Users/natan/Desktop/webscraping/chromedriver.exe', chrome_options=chrome_options)
navegator.maximize_window()
navegator.get('https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&currentJobId=3543890909&position=3&pageNum=0')

time.sleep(3)

#Pesquisando pais: Brasil

locate = navegator.find_element(By.ID,'job-search-bar-location')
locate.clear()
locate.send_keys('Brasil')
time.sleep(2)
list_id = navegator.find_element(By.ID,'job-search-bar-location-typeahead-list')
element_list = list_id.find_elements(By.TAG_NAME,'li')
element_list[0].click()
time.sleep(1)
locate.clear

time.sleep(3)

#Filtrando vagas: Serviços de publicidade ou Marketing e publicidade

searchBar = navegator.find_element(By.ID,'job-search-bar-keywords')
searchBar.send_keys('Serviços de publicidade ou Marketing e publicidade ')
time.sleep(3)
searchBar.submit()


time.sleep(3)

#Filtrando Tipo de Vaga: Tempo integral

vacancy__first_btn = navegator.find_element(By.XPATH,'//button[@data-tracking-control-name="public_jobs_f_JT"]').click()
time.sleep(3)
vacancy__checkBox = navegator.find_element(By.ID,'f_JT-0').click()
vacancy__sbmt_btn = navegator.find_element(By.XPATH,'//button[@data-tracking-control-name="public_jobs_f_JT"]').submit()

time.sleep(4)

#Filtrando Nivel de Experiencia: Estagiario

xpLevel__first_btn = navegator.find_element(By.XPATH,'//button[@data-tracking-control-name="public_jobs_f_E"]').click()
time.sleep(2)
xpLevel__checkBox = navegator.find_element(By.ID,'f_E-0').click()
xpLevel__checkBox = navegator.find_element(By.XPATH,'//button[@data-tracking-control-name="public_jobs_f_E"]').submit()

time.sleep(4)

searchBar = navegator.find_element(By.ID,'job-search-bar-keywords').click()
searchBar = navegator.find_element(By.ID,'job-search-bar-keywords').clear()
showMore__btn = navegator.find_element(By.XPATH,'//button[@data-tracking-control-name="public_jobs_show-more-html-btn"]').click()

#Fazendo o Web Scraping#

page_content = navegator.page_source
site = BeautifulSoup(page_content,'html.parser')
resultSector = site.find('ul',class_="jobs-search__results-list")
resultAreas = resultSector.find_all('li')
resultArea_info = site.find('div', class_='details-pane__content details-pane__content--show')

vacancy_datas = []


for resultArea in resultAreas:
    urlVacancy = resultArea.find('a', {'data-tracking-control-name':"public_jobs_jserp-result_search-card"})
    nameVacancy = resultArea.find('h3',class_ = 'base-search-card__title')
    nameCompany = resultArea.find('h4',class_='base-search-card__subtitle')
    nameCompany__url = resultArea.find('a',{'data-tracking-control-name':"public_jobs_jserp-result_job-search-card-subtitle"})
    companyCity = resultArea.find('span', class_= 'job-search-card__location')
    dateTime_vacancy = resultArea.find('time').text.split()
    
    if dateTime_vacancy[-1] == 'semana' or dateTime_vacancy[-1]== 'semanas':
        dt = timedelta(days = int(dateTime_vacancy[1]) * 7)
        dateTime_result = datetime.now() - dt
    elif dateTime_vacancy[-1] == 'hora' or dateTime_vacancy[-1]== 'horas':
        dt = timedelta(hours= int(dateTime_vacancy[1]))
        dateTime_result = datetime.now() - dt
    elif dateTime_vacancy[-1] == 'minuto' or dateTime_vacancy[-1]== 'minutos':
        dt = timedelta(minutes=int(dateTime_vacancy[1]))
        dateTime_result = datetime.now() - dt
    elif dateTime_vacancy[-1] == 'dia' or dateTime_vacancy[-1]== 'dias':
        dt = timedelta(days=int(dateTime_vacancy[1]))
        dateTime_result = datetime.now() - dt
    elif dateTime_vacancy[-1] == 'mês' or dateTime_vacancy[-1]== 'meses':
        dt = relativedelta (months = int(dateTime_vacancy[1]))
        dateTime_result = datetime.now() - dt     
    else:
        print('Não existe nenhuma dessas opções')
    array_info = resultArea_info.find('ul',class_= 'description__job-criteria-list').find_all('span')
    array_info = [type_.text for type_ in array_info]
    contractModel = resultArea_info.find('div', class_= 'show-more-less-html__markup')
    contractModel = [model.text for model in contractModel]
    nameVacancy = nameVacancy.text.strip()
    concType_scrap = array_info[1].replace('\n            ','').strip()
    xpLevel_scrap = array_info[0].replace('\n            ','').strip()
    urlVacancy = urlVacancy['href']
    nameCompany = nameCompany.text.strip()
    if nameCompany__url:
        nameCompany__url = nameCompany__url['href']
    companyCity = companyCity.text.strip()
    dateTime_result = dateTime_result.strftime("%Y-%m-%d")


    vacancy_datas.append([nameVacancy,urlVacancy,nameCompany,nameCompany__url,companyCity,concType_scrap,xpLevel_scrap,dateTime_result])

datas_pd = pd.DataFrame(vacancy_datas, columns= ['Nome', 'Url Vaga','Empresa','Url empresa','Sede','Tipo','Experiencia','Data'])
print(datas_pd)


datas_pd.to_csv('Scraping - Natan Risso Epifanio.csv', index = False, sep='\t')
