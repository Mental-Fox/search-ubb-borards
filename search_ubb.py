import csv, os
import PySimpleGUI as sg
from pathlib import Path
import tkinter as ttk
import pyglet
import pandas as pd


DICT_3G = {
    "UBBPe3": 12,
    "UBBPe4": 12,
    "UBBPd1": 6,
    "UBBPd5": 6,
    "UBBPe6": 12,
    "UBBPg1a": 12,
}

DICT_4G = {
    "UBBPe3": 6,
    "UBBPe4": 6,
    "UBBPd1": 3,
    "UBBPd5": 3,
    "UBBPe6": 12,
    "UBBPg1a": 6,
    "UBBPg2a": 12
}

class CSVReader():
    def __init__(self, csv_file_r: csv.DictReader, site: str, cell_3g: int, cell_4g: int, cell_5g: int) -> None:
        self.csv_file_r = csv_file_r
        self.site_info: dict = {}
        self.site = self.check_site_existence(site)
        self.new_site_info = {"Site Name": self.site, 
                              1: "", 
                              2: "UBBPg1a", 
                              3: "", 
                              4: "", 
                              5: ""}
        self.cell_3g = cell_3g
        self.cell_4g = cell_4g
        self.cell_5g = cell_5g
        

    def check_site_existence(self, site):
        for row in self.csv_file_r:
            if row["Site Name"] == site:
                self.site_info["Site Name"] = site

                for x in range(0, 6):
                    self.site_info[x] = row[str(x)]

                return site

        return None


    def deal_with_3G(self):
        for key, value in self.site_info.items():
            if value == "UBBPe3" or value == "UBBPe4":
                self.new_site_info[0] = value
                self.site_info[key] = ""
                break
            
        if not self.new_site_info[0]:
            for key, value in self.site_info.items():
                if value == "UBBPg1a":
                    self.new_site_info[0] = value
                    self.site_info[key] = ""
                    break
        
        if not self.new_site_info[0]:
            self.new_site_info[0] = "UBBPg1a"

        if DICT_3G[self.new_site_info[0]] < self.cell_3g:
            for key, value in self.site_info.items():
                if value == "UBBPe3" or value == "UBBPe4":
                    self.new_site_info[5] = value
                    self.site_info[key] = ""
                    break
            
            if not self.new_site_info[5]:
                for key, value in self.site_info.items():
                    if value == "UBBPd1":
                        self.new_site_info[5] = value
                        self.site_info[key] = ""
                        break
        
            if not self.new_site_info[5]:
                self.new_site_info[5] = "UBBPd1"


    def deal_with_4G(self):
        for key, value in self.site_info.items():
            if value == "UBBPe3" or value == "UBBPe4" or value == "UBBPe6":
                self.new_site_info[1] = value
                self.site_info[key] = ""
                break
        
        if not self.new_site_info[1]:
            for key, value in self.site_info.items():
                if value == "UBBPg2a":
                    self.new_site_info[1] = value
                    self.site_info[key] = ""
                    break
        
        if not self.new_site_info[1]:
            self.new_site_info[1] = "UBBPg2a"
        
        if DICT_4G[self.new_site_info[1]] < self.cell_4g:
            for key, value in self.site_info.items():
                if value == "UBBPe3" or value == "UBBPe4" or value == "UBBPe6":
                    self.new_site_info[3] = value
                    self.site_info[key] = ""
                    break
            
            if not self.new_site_info[3]:
                for key, value in self.site_info.items():
                    if value == "UBBPg2a":
                        self.new_site_info[3] = value
                        self.site_info[key] = ""
                        break
        
            if not self.new_site_info[3]:
                self.new_site_info[3] = "UBBPg2a"

        if self.new_site_info[3] and DICT_4G[self.new_site_info[1]] + DICT_4G[self.new_site_info[3]] < self.cell_4g:
            if not self.new_site_info[5]:
                for key, value in self.site_info.items():
                    if value == "UBBPe3" or value == "UBBPe4" or value == "UBBPe6":
                        self.new_site_info[5] = value
                        self.site_info[key] = ""
                        break
                
                if not self.new_site_info[5]:
                    for key, value in self.site_info.items():
                        if value == "UBBPg2a":
                            self.new_site_info[5] = value
                            self.site_info[key] = ""
                            break
            
                if not self.new_site_info[5]:
                    self.new_site_info[5] = "UBBPg2a"
    
    def deal_with_04_slot(self):
        if self.cell_5g:
            self.new_site_info[4] = "UBBPg3a"
                

def main():
    working_directory = os.getcwd()
    font_Regular = working_directory + "\\img\\font\\Tele2Slab-Bold.ttf"
    pyglet.font.add_file(font_Regular)
    font_Regular = ("Tele2 Slab", 13)
    
    font_old = ("Arial Bold", 13)
    # sg.ChangeLookAndFeel("Dark")
    sg.SetOptions(
                  background_color="#313131", 
                  text_element_background_color="#313131", 
                  text_color="#ffffff",  
                  input_text_color ="#ffffff",  
                  element_background_color="#313131", 
                  input_elements_background_color="#595959",
                  button_color=( "White", "#006cd8"),
                  border_width = False,
                  margins = (15, 15))
    
    # USERNAME = "user_rnp"
    # PASSWORD = "2023"
    USERNAME = ""
    PASSWORD = ""
    
    login_layout = [
        [sg.Text("Программа по расположения плат", size=(30,2), key="-TEXT-", justification="center", font=font_Regular)],
        [sg.Text("Имя пользователя:",  size=(15)), sg.Input(key="-USERNAME-", size=(18))],
        [sg.Text("Пароль:", size=(15)), sg.Input(key="-PASSWORD-", size=(18), password_char="*")],
        [sg.Text("", size=(24, 0)), sg.Button("Войти", size=(8,1), use_ttk_buttons=True, border_width = False, key="-SIGN_IN-")]
    ]

    login_window = sg.Window("Вход RNP",  login_layout, ttk_theme = "alt", border_depth = None, auto_size_buttons=True, auto_size_text = True, icon=r"img/RN.ico", element_justification="center",  font=font_old, finalize=True)

    while True:
        login_event, login_values = login_window.read()
        if login_event == sg.WIN_CLOSED:
            login_window.close()
            break

        elif login_event == "-SIGN_IN-":
            if login_values["-USERNAME-"] == USERNAME and login_values["-PASSWORD-"] == PASSWORD:
                login_window.close()
                break
            else:
                sg.popup_error("Неверное имя пользователя или пароль.\nПожалуйста, повторите попытку.", title="Ошибка")
    
    information = """
Цель программы: Эта программа предназначена для обработки данных из CSV-файлов, связанных с информацией о местоположении плат внутри определенных мест (сайтов) и сотовых сетей (3G, 4G и возможно 5G).
    
– Загрузка CSV-файла –
Выберите CSV-файл, содержащий данные о местоположении плат.
Введите название сайта, к которому относятся данные из файла.
Введите количество селлов для каждой из сотовых сетей (3G, 4G и 5G), если это необходимо.

– Обработка данных –
После ввода данных и нажатия кнопки "Обработать данные", программа выполнит следующие действия:
Анализ данных из файла и их обработка в соответствии с заданными правилами.
Генерация новых данных, которые будут отображены в таблице в программе.
Если введено количество селлов для 3G и/или 4G, то программа может перераспределить платы в соответствии с заданными ограничениями.

– Отображение данных в таблице –
Обработанные данные отображаются в таблице на главном экране программы.
Таблица содержит информацию о местоположении плат в сотовых сетях.

– Сохранение результата –
После обработки данных программа сохранит новые данные в CSV-файл с названием сайта.
Новый файл будет содержать информацию о местоположении плат с учетом проведенных изменений.
    """

    headings_ubb = ["#", "board1", "board2", "##"]
    headings = list(headings_ubb)
    
    file_list_column = [
        [sg.Text("Выберите CSV файл для обработки и вывода в таблицу:")],
        [sg.In(size=(40, 1), enable_events=True, key="-FILE_PATH-"),
        sg.FilesBrowse(button_text = "Выбрать файл", initial_folder=working_directory, file_types=[("CSV Files", "*.csv"), ("ALL Files", "*.*")])],
        [sg.Text("Введите название сайта:")],
        [sg.In(size=(20, 1), key="-SITE_NAME-")],
        [sg.Text("Количество селлов для 3G:"), sg.In(size=(20, 1), pad=(10, 5), enable_events=True, key="-CELL_3G-")],
        [sg.Text("Количество селлов для 4G:"), sg.In(size=(20, 1), pad=(10, 5), enable_events=True, key="-CELL_4G-")],
        [sg.Text("Количество селлов для 5G:"), sg.In(size=(20, 1), pad=(10, 5), enable_events=True, key="-CELL_5G-")],
    ]
    
    table_list_column = [
        [sg.Table(values=[], justification="center", enable_events=True, header_background_color="#777777", header_text_color="#ffffff", visible=False, headings=headings_ubb, header_border_width=None, vertical_scroll_only = True, hide_vertical_scroll=True, expand_x=True, auto_size_columns=False, display_row_numbers=False, key="-TABLE-")]]
    
    layout = [
        [sg.Text("\nДля отдела RNP обработчик по расположения плат", enable_events=True, key="-TEXT-", pad=(15, 0), font=font_Regular)],
        [sg.Frame("1. Загрузка Файла CSV", file_list_column, size=(520, 250), title_color="#007fff", pad=(15, 20))],
        # sg.VSeperator(),
        [sg.Frame("2. Вывод в таблицу", table_list_column, size=(520, 190), title_color="#007fff", pad=(15, 20))],
        [sg.Text("", size=(17, 1)), 
            sg.Button("Обработать данные", use_ttk_buttons=True, border_width = False, key="-UPDATE_FILE-"),  
            sg.Button("Информация", use_ttk_buttons=True, border_width = False, key="-INFO-"), 
            sg.Button("Выйти", use_ttk_buttons=True, border_width = False, key="-EXIT_APP-")]
    ]

    window = sg.Window("RNP Обработчик по расположения плат", layout, ttk_theme = "alt", finalize=True, icon=r"img/RN.ico", font=font_old, element_justification="center", auto_size_buttons=True, auto_size_text = True, border_depth = None,)
    
    if login_values["-USERNAME-"] == USERNAME and login_values["-PASSWORD-"] == PASSWORD:
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-EXIT_APP-"):
                break
            
            elif event == "-INFO-":
                sg.popup_ok(information, sg.version, line_width = 100, font=("Arial Bold", 12), grab_anywhere=True)
                
            elif event == "-UPDATE_FILE-":
                file_name = values["-FILE_PATH-"]
                site_name = values["-SITE_NAME-"]
                if not file_name:
                    sg.popup_error("Ошибка: Выберите файл CSV.", title="Ошибка")
                    
                elif not site_name:
                    sg.popup_error("Ошибка: Введите название сайта.", title="Ошибка")
                else:
                    cell_3g = int(values["-CELL_3G-"]) if values["-CELL_3G-"] else 0
                    cell_4g = int(values["-CELL_4G-"]) if values["-CELL_4G-"] else 0
                    cell_5g = int(values["-CELL_5G-"]) if values["-CELL_5G-"] else 0

                    if not (cell_3g or cell_4g or cell_5g):
                        sg.popup_error("Ошибка: Введите количество селлов для 3G, 4G, 5G.", title="Ошибка")
                    else:
                        with open(file_name, mode="r", newline="", encoding="utf-8-sig") as csvfile:
                            csv_file_reader = csv.DictReader(csvfile, delimiter=";")

                            csv_reader = CSVReader(csv_file_reader, site_name, cell_3g, cell_4g, cell_5g)

                            if not csv_reader.site:
                                sg.popup_error("Такого сайта нет. \nПожалуйста, введите существующий сайт.")
                            else:
                                if cell_3g != 0:
                                    csv_reader.deal_with_3G()
                                    
                                if cell_4g != 0:
                                    csv_reader.deal_with_4G()
                                    
                                if cell_5g != 0:
                                    csv_reader.deal_with_04_slot()

                                # Получить значения для столбцов 00 и 01
                                data = {
                                    0: ["00", "02", "04"],
                                    1: [csv_reader.new_site_info[0], csv_reader.new_site_info[2], csv_reader.new_site_info[4]],
                                    2: [csv_reader.new_site_info[1], csv_reader.new_site_info[3], csv_reader.new_site_info[5]],
                                    3: ["01", "03", "05"]
                                }

                                df = pd.DataFrame(data)
                                new_file_name = f'{csv_reader.site}.csv'
                                df.to_csv(new_file_name, index=False, header=False)
                                table_data = df.values.tolist()
                                # data_without_header = table_data[1:]
                                window["-TABLE-"].update(values=table_data, visible=True)

    window.close()
if __name__ == "__main__":
    main()