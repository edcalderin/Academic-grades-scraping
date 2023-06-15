import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import pandas as pd

USERNAME: str = os.getenv('USERNAME')
PASSWORD: str = os.getenv('PASSWORD')

HOME_PAGE: str = 'https://sinai.net.co/Web/Default.aspx'
GRADES_PAGE: str = 'https://sinai.net.co/Docente/018/Calificaciones.aspx'

def read_data(path: str)-> pd.DataFrame:
    grades_df = pd.read_csv(path, sep=';')
    return grades_df.loc[:,~grades_df.columns.str.contains('Unnamed')]

def login(username: str, password: str, driver)-> None:
    driver.find_element(by=By.ID, value='UsernameTxt').send_keys(username)
    driver.find_element(by=By.ID, value='PasswordTxt').send_keys(password)
    driver.find_element(by=By.ID, value='Entrar').click()

def edit_grade(i: int, grade:float, driver)-> None:
    grade_element_id = f'ctl00_ContentPlaceHolder1_ParcialesRpt_ctl{i:02d}_Nota1'
    grade_element = driver.find_element(by=By.ID, value=grade_element_id)
    grade_element.clear()
    grade_element.send_keys(grade)

def save_grades(dataframe: pd.DataFrame, driver)-> None:
    for item in dataframe.items():
        element = driver.find_element(by=By.ID, value='ctl00_ContentPlaceHolder1_AsignaturaLst')
        select = Select(element)
        select.select_by_visible_text(item[0])
        sleep(2)
        driver.find_element(by=By.LINK_TEXT, value='Generar Planilla').click()
        sleep(2)

        for i, grade in enumerate(item[1], 1):
            edit_grade(i, grade, driver)

        driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
        driver.find_element(by=By.LINK_TEXT, value='Guardar').click()
        sleep(3)

def main()-> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(HOME_PAGE)

    login(USERNAME, PASSWORD, driver)

    driver.get(GRADES_PAGE)

    grades_df = read_data('grades.csv')

    save_grades(grades_df, driver)

main()