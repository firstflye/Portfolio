import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                            QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.location_label = QLabel("Enter location name: ", self)
        self.location_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.location_label)
        vbox.addWidget(self.location_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.location_label.setAlignment(Qt.AlignCenter)
        self.location_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.location_label.setObjectName("location_label")
        self.location_input.setObjectName("location_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
        QLabel, QPushButton{
        font-family: calibri;
        }
        QLabel#location_label{
        font-size: 40px;
        font-style: italic;
        }
        QLineEdit#location_input{
        font-size: 40px;
        }
        QPushButton#get_weather_button{
        font-size: 30px;
        font-weight: bold;
        }
        QLabel#temperature_label{
        font-size: 75px;
        }
        QLabel#emoji_label{
        font-size: 100px;
        font-family: seqoe UI emoji;
        }
        QLabel#description_label{
        font-size: 50px;
        }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "02f002cbe9b9a23988dbc91f96e5f0d5"
        location = self.location_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\n Please Check your input")
                case 401:
                    self.display_error("Unauthorized:\n Invalid API key")
                case 403:
                    self.display_error("Forbidden:\n Access is denied")
                case 404:
                    self.display_error("Not found:\n location not found")
                case 500:
                    self.display_error("Internal server Error:\n Please try again later")
                case 502:
                    self.display_error("Bad gateway:\n Invalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\n Server is down")
                case 400:
                    self.display_error("Gateway timeout:\n No response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\n Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n The request is timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\n Check the url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]


        self.temperature_label.setText(f"{temperature_c:.1f}0C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "☁"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return " "


if __name__=="__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())