// ----- Смена языка -----
let lang = 'ru';
const langBtn = document.getElementById('changeLang');
langBtn.addEventListener('click', () => {
    lang = lang === 'ru' ? 'en' : lang === 'en' ? 'de' : 'ru';
    langBtn.textContent = `🌐 ${lang.toUpperCase()}`;

    const translations = {
        ru: { placeholder: "Введите город...", show: "Показать", forecast: "📅 Прогноз на 5 дней", title: "🌩️ Прогноз погоды" },
        en: { placeholder: "Enter city...", show: "Show", forecast: "📅 5-Day Forecast", title: "🌩️ Weather Forecast" },
        de: { placeholder: "Stadt eingeben...", show: "Anzeigen", forecast: "📅 5-Tages-Prognose", title: "🌩️ Wettervorhersage" }
    };

    document.querySelector('input[name="city"]').placeholder = translations[lang].placeholder;
    document.getElementById('showBtn').textContent = translations[lang].show;
    if(document.getElementById('forecastTitle')) document.getElementById('forecastTitle').textContent = translations[lang].forecast;
    document.getElementById('title').textContent = translations[lang].title;
});


