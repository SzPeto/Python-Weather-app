import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QAction, QMenuBar, QMenu, QPushButton, QLabel, QFrame
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout


class AppWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        app: QApplication
        self.app = app
        self.central_widget = QWidget()

        # Menu
        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("File")
        self.options_menu = QMenu("Options")
        self.help_menu = QMenu("Help")
        self.exit_action = QAction("Exit")
        self.read_me_action = QAction("Read me")

        # Dimensions and geometry
        self.monitor = QGuiApplication.primaryScreen().geometry()
        self.window_width = 800
        self.window_height = 600

        #Layouts
        self.h_box_main = QHBoxLayout()
        self.v_box_left = QVBoxLayout()
        self.v_box_right = QVBoxLayout()
        self.separator = QFrame()

        # Line edit
        self.text_field = QLineEdit()

        # Buttons
        self.submit_button = QPushButton("Submit")

        # Labels
        self.description_label = QLabel()
        self.emoji_label = QLabel()

        # Files
        self.help_file_path = "Help.txt"

        # Method calls
        self.initUI()


    def initUI(self):

        # Main
        self.setCentralWidget(self.central_widget)

        # Menu
        self.setMenuBar(self.menu_bar)
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.options_menu)
        self.menu_bar.addMenu(self.help_menu)
        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.read_me_action)
        self.exit_action.triggered.connect(self.close_app)
        self.read_me_action.triggered.connect(self.open_read_me)

        # Layout
        self.central_widget.setLayout(self.h_box_main)

        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(2)
        self.v_box_left.addWidget(self.text_field, alignment = Qt.AlignHCenter)
        self.v_box_left.addWidget(self.submit_button, alignment = Qt.AlignTop | Qt.AlignHCenter)
        self.v_box_right.addWidget(self.emoji_label, alignment = Qt.AlignHCenter)
        self.v_box_right.addWidget(self.description_label, alignment = Qt.AlignHCenter)
        self.h_box_main.addLayout(self.v_box_left)
        self.h_box_main.addWidget(self.separator)
        self.h_box_main.addLayout(self.v_box_right)

        # Dimensions and geometry
        self.center_window()

        # Other
        self.setWindowTitle("Weather app by Peter Szepesi")
        self.text_field.setPlaceholderText("Enter a city name")
        self.text_field.setObjectName("textField")
        self.text_field.setFixedWidth(int(self.width() * 0.4))
        self.description_label.setText("This is the weather description")
        self.description_label.setObjectName("descriptionLabel")
        self.emoji_label.setText("☀️")
        self.emoji_label.setObjectName("emojiLabel")

        # Styling
        self.setStyleSheet("""
            QLineEdit#textField{
                font-size: 25px;
                font-family: Bahnschrift;
                background-color: white;
            }
            
            QWidget{
                background-color: rgb(235, 235, 250);
            }
            
            QMenuBar, QMenu{
                background-color: white;
            }
            
            QPushButton{
                font-family: Bahnschrift;
                font-size: 20px;
                font-weight: bold;
                background-color: white;
                margin: 10px;
                padding: 5px;
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
        """)

    def center_window(self):
        x = int((self.monitor.width() - self.window_width) / 2)
        y = int((self.monitor.height() - self.window_height) / 2)
        self.setGeometry(x, y, self.window_width, self.window_height)

    def close_app(self):
        sys.exit(0)

    def open_read_me(self):
        if os.path.exists(self.help_file_path):
            print("The file exists")
        else:
            print("Error, the readme file doesn't exist!")