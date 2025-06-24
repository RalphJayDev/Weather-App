#cc66ca0d43596c17c4d7b66dfc2cd536
import sys
import requests
from PyQt5.QtWidgets import (QApplication , QLabel , QWidget , 
                            QLineEdit , QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RalphJay's Weather App")
        self.city_label = QLabel("Enter City name",self)
        self.city_input = QLineEdit(self)

        
        self.city_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description = QLabel(self)
        self.initUI()
    
    def initUI(self):        
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.city_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("city_temperature")
        self.description.setObjectName("description")
        self.emoji_label.setObjectName("emoji_label")
        self.city_button.setObjectName("city_button")

        self.setStyleSheet("""
                QWidget {
                background-color: #9497ff; 
                }
                QLabel#city_label {
                    font-style: italic;
                    font-weight: bold;
                    font-size: 40px;
                    color: #43d169;
                    font-family: Calibri;
                    background-color: #f0bd24;
                }
                QLineEdit#city_input {
                    font-size: 40px;
                    font-family: cuyrtffnalibri;
                    background-color: #f0bd24;
                }
                QPushButton#city_button {
                    font-size: 40px;
                    font-weight: bold;
                    font-family: arial;
                    background-color: #f0bd24;
                }
                QLabel#emoji_label {
                    font-size: 80px;
                    font-family: Segoe UI emoji;
                    background-color: #f0bd24;
                }
                QLabel#city_temperature {
                    font-size: 75px;
                    font-family: arial;
                    background-color: #f0bd24;
                }  
                QLabel#description {
                    font-size: 50px;
                    font-weight: bold;
                    font-family: calibri;
                    background-color: #f0bd24;
                }
                """)

        self.city_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "cc66ca0d43596c17c4d7b66dfc2cd536"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)   
        except requests.exceptions.HTTPError as http_error:
                match response.status_code:
                    case 400: 
                        self.display_error("Bad Request\nPlease Check your input")
                    case 401:
                        self.display_error("Unauthorized\nInvalid API Key")
                    case 403:
                        self.display_error("Forbidden\nAccess is Denied!")
                    case 404:
                        self.display_error("Not Found\nCity not found")
                    case 500:
                        self.display_error("Internal Server Erorr\nPlease try again later.")
                    case 502:
                        self.display_error("Bad Gateway\nInvalid response from the server.")
                    case 503:
                        self.display_error("Service Unavailablet\nServer is down.")
                    case 504:
                        self.display_error("Gateway Timeout\nNo response from the server.")
                    case _:
                        self.display_error("HTTP error occured\n{http_error}")

        except requests.exceptions.ConnectionErorr:
             self.display_error("Connection Error\nCheck your internet")
        except requests.exceptions.Timeout:
             self.display_error("Timeout Error\n The request timed out")
        except requests.exceptions.ToomanyRedirects:
             self.display_error("Too many Redirects:\nCheck the url")
        except requests.exceptions.RequestException as req_error:
             self.display_error(f"Request Error:\n{req_error}")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("""font-size:18    px;
                                                color: red;
                                                font-weight: bold; """)
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description.clear()
    def display_weather(self,data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        self.temperature_label.setStyleSheet("font-size:75px;")
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        weather_description = data["weather"][0]["description"]
        self.description.setText(weather_description)
        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))


    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️⛈️"
        elif 300 <= weather_id <= 321:
            return "☁☁"
        elif 500 <= weather_id <= 531:
            return "🌧️🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️🌫️"
        elif weather_id == 762:
            return "🌋🌋"
        elif weather_id == 771:
            return "💨💨"
        elif weather_id == 781:
            return "🌪️🌪️"
        elif weather_id == 800:
            return "☀️☀️"
        elif 801 <= weather_id <= 804:
            return "☁️☁️"
        else: 
            return ""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = Weather()
    weather_app.show()
    sys.exit(app.exec_())



