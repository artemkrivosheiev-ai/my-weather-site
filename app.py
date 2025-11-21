from flask import Flask, render_template, request, redirect, url_for, session
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Для сессий

# Главный экран
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    main_weather = "Clear"  # default

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        city = request.form["city"].strip()
        if not city:
            weather_data = {"error": "Введите название города!"}
        else:
            try:
                url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
                response = requests.get(url)
                data = response.json()

                if data.get("cod") != "200":
                    weather_data = {"error": "Город не найден 😔"}
                else:
                    # Сохраняем в историю
                    if city not in session["history"]:
                        session["history"].append(city)
                        session.modified = True

                    current = data["list"][0]
                    weather_data = {
                        "city": data["city"]["name"],
                        "country": data["city"]["country"],
                        "temp": round(current["main"]["temp"]),
                        "feels_like": round(current["main"]["feels_like"]),
                        "humidity": current["main"]["humidity"],
                        "wind": current["wind"]["speed"],
                        "desc": current["weather"][0]["description"].capitalize(),
                        "icon": current["weather"][0]["icon"]
                    }
                    main_weather = current["weather"][0]["main"]

                    forecast_data = []
                    for i in range(0, len(data["list"]), 8):
                        item = data["list"][i]
                        date_obj = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                        forecast_data.append({
                            "date": date_obj.strftime("%a %d.%m"),
                            "temp": round(item["main"]["temp"]),
                            "desc": item["weather"][0]["description"].capitalize(),
                            "icon": item["weather"][0]["icon"]
                        })

            except requests.exceptions.RequestException as e:
                weather_data = {"error": f"Ошибка сервера: {e}"}

    return render_template("index.html", weather=weather_data, forecast=forecast_data, mainWeather=main_weather)

# Страница истории
@app.route("/history", methods=["GET", "POST"])
def history():
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        # Очистка истории
        session["history"] = []
        session.modified = True
        return redirect(url_for("history"))

    return render_template("history.html", history=session["history"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



\







