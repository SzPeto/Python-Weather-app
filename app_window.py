# TODO - make exception handling for deepl API

import datetime
import os.path
import platform
import stat
import subprocess
import sys
import webbrowser

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QKeyEvent, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QAction, QMenuBar, QMenu, QPushButton, QLabel, QFrame, QComboBox
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout

import deepl


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()

        # Menu
        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("File")
        self.options_menu = QMenu("Options")
        self.help_menu = QMenu("Help")
        self.exit_action = QAction("Exit")
        self.help_action = QAction("Help")
        self.about_action = QAction("About")

        # Dimensions and geometry
        self.monitor = QGuiApplication.primaryScreen().geometry()
        self.window_width = 800
        self.window_height = 600

        #Layouts
        self.h_box_main = QHBoxLayout()
        self.v_box_left = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.h_box_wind = QHBoxLayout()
        self.h_box_temperature = QHBoxLayout()
        self.h_box_humidity = QHBoxLayout()
        self.h_box_pressure = QHBoxLayout()

        # Labels, buttons, line edit and other
        self.sun_icon = QIcon(self.resource_path("sun-icon.png"))
        self.sunny_icon = QIcon(self.resource_path("Weather_Icons\\sun - minimalist.png"))
        self.sunny_icon_pixmap = self.sunny_icon.pixmap(100, 100)
        self.cloudy_icon = QIcon(self.resource_path("Weather_Icons\\cloud - minimalist.png"))
        self.cloudy_icon_pixmap = self.cloudy_icon.pixmap(100, 100)
        self.suncloud_icon = QIcon(self.resource_path("Weather_Icons\\cloud - sun - minimalist.png"))
        self.suncloud_icon_pixmap = self.suncloud_icon.pixmap(100, 100)
        self.overcast_icon = QIcon(self.resource_path("Weather_Icons\\overcast - minimalist.png"))
        self.overcast_icon_pixmap = self.overcast_icon.pixmap(100, 100)
        self.rain_icon = QIcon(self.resource_path("Weather_Icons\\rain - minimalist.png"))
        self.rain_icon_pixmap = self.rain_icon.pixmap(100, 100)
        self.thunderstorm_icon = QIcon(self.resource_path("Weather_Icons\\thunderstorm - minimalist.png"))
        self.thunderstorm_icon_pixmap = self.thunderstorm_icon.pixmap(100, 100)
        self.fog_icon = QIcon(self.resource_path("Weather_Icons\\fog - minimalist.png"))
        self.fog_icon_pixmap = self.fog_icon.pixmap(100, 100)
        self.snow_icon = QIcon(self.resource_path("Weather_Icons\\snowfall - minimalist.png"))
        self.snow_icon_pixmap = self.snow_icon.pixmap(100, 100)
        self.pressure_icon = QIcon(self.resource_path("Weather_Icons\\pressure - minimalist.png"))
        self.pressure_icon_pixmap = self.pressure_icon.pixmap(40, 40)
        self.humidity_icon = QIcon(self.resource_path("Weather_Icons\\humidity.png"))
        self.humidity_icon_pixmap = self.humidity_icon.pixmap(40, 40)
        self.wind_icon = QIcon(self.resource_path("Weather_Icons\\wind - minimalist.png"))
        self.wind_icon_pixmap = self.wind_icon.pixmap(40, 40)
        self.temperature_icon = QIcon(self.resource_path("Weather_Icons\\temperature - minimalist.png"))
        self.temperature_icon_pixmap = self.temperature_icon.pixmap(40, 40)
        self.text_field = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.description_label = QLabel()
        self.temperature_icon_label = QLabel()
        self.temperature_label = QLabel()
        self.emoji_label = QLabel()
        self.city_label = QLabel()
        self.humidity_icon_label = QLabel()
        self.humidity_label = QLabel()
        self.pressure_icon_label = QLabel()
        self.pressure_label = QLabel()
        self.wind_icon_label = QLabel()
        self.wind_label = QLabel()
        self.wind_direction_label = QLabel()
        self.date_time_label = QLabel()
        self.separator = QFrame()
        self.temperature = 0
        self.humidity = 0
        self.wind_speed = 0
        self.wind_direction = "⬆️"
        self.pressure = 0
        self.unix_timestamp = 0
        self.utc_time = 0
        self.time_zone_correction = 0
        self.weather_code = 0
        self.language = "en"
        self.API_key_deepl = "567820c6-2932-495c-b0a8-db41851577c1:fx"
        self.translate = deepl.Translator(self.API_key_deepl)
        self.support_me_button = QPushButton("Support me")
        self.temperature_combo = QComboBox()
        self.speed_combo = QComboBox()

        # Units
        self.temp_unit = "°C"
        self.speed_unit = "km/h"

        # Method calls
        self.register_fonts()
        self.initUI()

    # UI initialization method *******************************************************************************
    def initUI(self):

        # Main
        self.setCentralWidget(self.central_widget)

        # Menu
        self.setMenuBar(self.menu_bar)
        self.menu_bar.addMenu(self.file_menu)
        #self.menu_bar.addMenu(self.options_menu)
        self.menu_bar.addMenu(self.help_menu)
        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.about_action)
        self.exit_action.triggered.connect(self.close_app)
        self.help_action.triggered.connect(self.open_help)
        self.about_action.triggered.connect(self.open_about)

        # Layout
        self.central_widget.setLayout(self.h_box_main)
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(2)
        self.h_box_wind.addWidget(self.wind_icon_label)
        self.h_box_wind.addWidget(self.wind_label, alignment = Qt.AlignRight)
        self.h_box_wind.addWidget(self.wind_direction_label, alignment = Qt.AlignLeft)
        self.h_box_wind.addWidget(self.speed_combo, alignment = Qt.AlignRight)
        self.h_box_temperature.addWidget(self.temperature_icon_label)
        self.h_box_temperature.addWidget(self.temperature_label, alignment = Qt.AlignHCenter)
        self.h_box_temperature.addWidget(self.temperature_combo, alignment = Qt.AlignRight)
        self.h_box_humidity.addWidget(self.humidity_icon_label)
        self.h_box_humidity.addWidget(self.humidity_label)
        self.h_box_pressure.addWidget(self.pressure_icon_label)
        self.h_box_pressure.addWidget(self.pressure_label)
        self.v_box_left.addWidget(self.text_field, alignment = Qt.AlignHCenter)
        self.v_box_left.addWidget(self.submit_button, alignment = Qt.AlignTop | Qt.AlignHCenter)
        self.v_box_left.addWidget(self.date_time_label, alignment = Qt.AlignHCenter)
        self.v_box_left.addWidget(self.support_me_button, alignment = Qt.AlignHCenter)
        self.v_box_right.addWidget(self.city_label, alignment = Qt.AlignHCenter)
        self.v_box_right.addWidget(self.emoji_label, alignment = Qt.AlignHCenter)
        self.v_box_right.addWidget(self.description_label, alignment=Qt.AlignHCenter)
        self.v_box_right.addLayout(self.h_box_temperature)
        self.v_box_right.addLayout(self.h_box_humidity)
        self.v_box_right.addLayout(self.h_box_pressure)
        self.v_box_right.addLayout(self.h_box_wind)
        self.h_box_main.addLayout(self.v_box_left)
        self.h_box_main.addWidget(self.separator)
        self.h_box_main.addLayout(self.v_box_right)

        # Dimensions and geometry
        self.center_window()

        # Labels, buttons, line edit
        self.setWindowIcon(self.sun_icon)
        self.setWindowTitle("Weather app by Peter Szepesi v 0.8")
        self.text_field.setPlaceholderText("Enter a city name")
        self.text_field.setObjectName("textField")
        self.text_field.setFixedWidth(int(self.width() * 0.4))
        self.description_label.setText("Waiting for city name")
        self.description_label.setObjectName("descriptionLabel")
        self.emoji_label.setPixmap(self.sunny_icon_pixmap)
        self.pressure_icon_label.setPixmap(self.pressure_icon_pixmap)
        self.humidity_icon_label.setPixmap(self.humidity_icon_pixmap)
        self.temperature_icon_label.setPixmap(self.temperature_icon_pixmap)
        self.emoji_label.setObjectName("emojiLabel")
        self.temperature_label.setPixmap(self.temperature_icon_pixmap)
        self.temperature_label.setText("0°C")
        self.temperature_label.setObjectName("temperatureLabel")
        self.city_label.setText("")
        self.city_label.setObjectName("cityLabel")
        self.submit_button.clicked.connect(self.get_weather)
        self.humidity_label.setText("0%")
        self.humidity_label.setObjectName("humidityLabel")
        self.pressure_label.setText("0hPa")
        self.pressure_label.setObjectName("pressureLabel")
        self.wind_icon_label.setPixmap(self.wind_icon_pixmap)
        self.wind_label.setText("0km/h")
        self.wind_label.setObjectName("windLabel")
        self.wind_direction_label.setText("⬆️")
        self.wind_direction_label.setObjectName("windDirectionLabel")
        self.date_time_label.setObjectName("dateTimeLabel")
        self.support_me_button.clicked.connect(self.support_me)
        self.support_me_button.setObjectName("supportMeButton")
        self.temperature_combo.addItems(["°C", "°F", "K"])
        self.speed_combo.addItems(["km/h", "mph", "m/s"])
        self.temperature_combo.currentIndexChanged.connect(self.temp_unit_change)
        self.speed_combo.currentIndexChanged.connect(self.speed_unit_change)

        # Styling
        self.setStyleSheet("""
            QLineEdit#textField{
                font-size: 25px;
                font-family: Bahnschrift;
                border-radius: 10px;
                background-color: white;
            }
            
            QWidget{
                background-color: rgb(235, 235, 250);
            }
            
            QMenuBar, QMenu{
                background-color: white;
            }
            
            QPushButton{
                font-family: Segoe UI;
                font-size: 25px;
                background-color: white;
                margin: 10px;
                padding: 5px;
                border: 2px solid #cccccc;
                border-radius: 10px;
            }
            
            QPushButton:hover{
                border: 2px solid #aaaaaa;
                border-radius: 10px;
                background-color: rgb(248, 248, 248);
            }
            
            QPushButton:pressed{
                border: 2px inset #888888;
                background-color: rgb(215, 215, 215);
                padding-top: 10px;
                padding-bottom: 6px;
            }
            
            QLineEdit{
                margin: 10px;
            }
            
            QLabel#emojiLabel{
                font-family: Segoe UI Emoji;
                font-size: 100px;
            }
            
            QLabel#descriptionLabel{
                font-family: Bahnschrift;
                font-size: 25px;
            }
            
            QLabel#temperatureLabel{
                font-family: Bahnschrift;
                font-size: 35px;
            }
            
            QLabel#cityLabel{
                font-family: Bahnschrift;
                font-size: 45px;
            }
            
            QLabel#humidityLabel{
                font-family: Bahnschrift;
                font-size: 35px;
            }
            
            QLabel#pressureLabel{
                font-family: Bahnschrift;
                font-size: 35px;
            }
            
            QLabel#windLabel{
                font-family: Bahnschrift;
                font-size: 35px;
                margin: 10px;
            }
            
            QLabel#windDirectionLabel{
                font-family: Segoe UI Emoji;
                font-size: 45px;
            }
            
            QLabel#dateTimeLabel{
                font-family: Bahnschrift;
                font-size: 25px;
            }
            
            QPushButton#supportMeButton{
                font-family: Bahnschrift;
                font-size: 20px;
            }
            
        """)

    # Event handling and signal-slot related methods *********************************************************
    def get_weather(self):
        api_key = "f0130aa9896b42e7eec767c74fbb474b"
        city = self.text_field.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        self.button_click_counter("submit")

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") == 200:
                data: dict
                self.format_data(data)
            else:
                print(f"Network error : {response.status_code}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error : {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error : {e}")

    def close_app(self):
        sys.exit(0)

    def keyPressEvent(self, event):
        event: QKeyEvent
        key = event.key()
        if key == 16777220 or 16777221:
            self.get_weather()

    def support_me(self):
        webbrowser.open("https://www.paypal.me/szpeto")
        self.button_click_counter("support_me")

    def button_click_counter(self, button_name):
        url = f"https://api.counterapi.dev/v1/szpeto_weather_app/{button_name}/up"

        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                print(f"The {data.get("name")} button clicked count for weather app is : {data.get("count")}")
            else:
                print("Cannot connect to the counter API")
        except Exception as e:
            print(f"Error getting the counter request : {e}")

    def temp_unit_change(self):
        self.temp_unit = self.temperature_combo.currentText()
        self.get_weather()

    def speed_unit_change(self):
        self.speed_unit = self.speed_combo.currentText()
        self.get_weather()
    # Layout and dimension related methods ********************************************************************
    def center_window(self):
        x = int((self.monitor.width() - self.window_width) / 2)
        y = int((self.monitor.height() - self.window_height) / 2)
        self.setGeometry(x, y, self.window_width, self.window_height)

    # Data management and formatting methods *****************************************************************
    def format_data(self, data):

        # Getting the temperature
        temp_temperature = float(data.get("main").get("temp"))
        if self.temp_unit == "°C":
            self.temperature = temp_temperature - 273.15
        elif self.temp_unit == "°F":
            self.temperature = (temp_temperature - 273.15) * 1.8 + 32
        elif self.temp_unit == "K":
            self.temperature = temp_temperature

        # Getting the humidity
        self.humidity = int(data.get("main").get("humidity"))

        # Getting the pressure
        self.pressure = int(data.get("main").get("pressure"))

        # Getting the wind
        temp_speed = float(data.get("wind").get("speed"))
        if self.speed_unit == "km/h":
            self.wind_speed = int(temp_speed * 3.6)
        elif self.speed_unit == "mph":
            self.wind_speed = int(temp_speed * 2.23694)
        elif self.speed_unit == "m/s":
            self.wind_speed = int(temp_speed)

        self.set_wind_direction(data)

        # Getting the date and time
        self.unix_timestamp = int(data.get("dt"))
        self.time_zone_correction = int(data.get("timezone"))
        self.utc_time = datetime.datetime.fromtimestamp(self.unix_timestamp, datetime.UTC)
        local_time = self.utc_time + datetime.timedelta(seconds=self.time_zone_correction)

        # Getting the weather code
        self.weather_code = data.get("weather")[0].get("id")

        # Formatting the data
        description_en = data.get("weather")[0].get("description")
        if self.language != "en":
            description_translated = self.translate.translate_text(description_en, target_lang = "SK").text
            self.description_label.setText(description_translated)
        else:
            self.description_label.setText(description_en)
        self.city_label.setText(f"{data.get("name")}, {data.get("sys").get("country")}")
        self.temperature_label.setText(f"{self.temperature:.1f}{self.temp_unit}")
        self.pressure_label.setText(f"{self.pressure}hPa")
        self.humidity_label.setText(f"{self.humidity}%")
        self.wind_label.setText(f"{self.wind_speed}{self.speed_unit}")
        self.wind_direction_label.setText(self.wind_direction)
        self.date_time_label.setText(
            f"Local date and time in {data.get("name")} : \n{local_time.strftime("%d.%m.%Y %H:%M:%S")}")
        self.set_emoji_label()

    def set_wind_direction(self, data):
        wind_degree = int(data.get("wind").get("deg"))

        wind_symbols = ("⬇️", "↙️", "⬅️", "↖️", "⬆️", "↗️", "➡️", "↘️")

        wind_index = int(((wind_degree + 22) % 360) // 45)
        self.wind_direction = wind_symbols[wind_index]

    def set_emoji_label(self):
        if 200 <= self.weather_code <= 232:
            self.emoji_label.setPixmap(self.thunderstorm_icon_pixmap)
        elif 300 <= self.weather_code <= 321:
            self.emoji_label.setPixmap(self.rain_icon_pixmap)
        elif 500 <= self.weather_code <= 504:
            self.emoji_label.setPixmap(self.rain_icon_pixmap)
        elif self.weather_code == 511:
            self.emoji_label.setPixmap(self.snow_icon_pixmap)
        elif 520 <= self.weather_code <= 522 or self.weather_code == 531:
            self.emoji_label.setPixmap(self.rain_icon_pixmap)
        elif 600 <= self.weather_code <= 622:
            self.emoji_label.setPixmap(self.snow_icon_pixmap)
        elif 701 <= self.weather_code <= 781:
            self.emoji_label.setPixmap(self.fog_icon_pixmap)
        elif self.weather_code == 800:
            self.emoji_label.setPixmap(self.sunny_icon_pixmap)
        elif 801 <= self.weather_code <= 804:
            self.emoji_label.setPixmap(self.cloudy_icon_pixmap)

    # Getting the resource paths
    def resource_path(self, relative_path):
        # This method return either the absolute, or the relative file path, depending on whether it is
        # run by IDE or by a packaged exe file
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path) # In case of exe return the absolute path
        else:
            return os.path.join(os.path.abspath("."), relative_path) # In case of IDE return the relative path

    # Registering the fonts ***********************************************************************************
    def register_fonts(self):
        font_id = ( QFontDatabase.addApplicationFont(self.resource_path("Fonts\\bahnschrift.ttf")),
                    QFontDatabase.addApplicationFont(self.resource_path("Fonts\\seguiemj.ttf")) )

        for i in range(0, len(font_id)):
            if font_id[i] == -1:
                print(f"Failed to load the font at index : {i}")
            else:
                font_family = QFontDatabase.applicationFontFamilies(font_id[i])[0]

    # File opening methods ***********************************************************************************
    def open_help(self):
        help_file_path = "Help.txt"

        try:
            if platform.system() == "Windows":
                os.startfile(help_file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", help_file_path])
            else:
                subprocess.call(["xdg-open", help_file_path])

            with open(help_file_path, "r") as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("You don't have permission to open this file")
        except Exception as e:
            print(f"Something went wrong, error message : {e}")

    def open_about(self):
        about_file_path = "About.txt"

        try:
            if platform.system() == "Windows":
                os.startfile(about_file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", about_file_path])
            else:
                subprocess.call(["xdg-open", about_file_path])

            with open(about_file_path, "r") as file:
                content = file.read()
                print(content)
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("You don't have permission to open this file")
        except Exception as e:
            print(f"Something went wrong, error message : {e}")