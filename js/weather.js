// Configure your location (default: Munich)
const LAT = 48.1351;
const LON = 11.582;

async function fetchWeather() {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code&hourly=temperature_2m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&forecast_days=7&timezone=auto`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Weather error');
  return res.json();
}

function weatherCodeToSymbol(code) {
  if (code === 0 || code === 1) return '☀';
  if (code === 2) return '◒';
  if (code === 3 || code === 45 || code === 48) return '☁';
  if (code >= 71 && code <= 77) return '❄';
  if (code >= 51 && code <= 67 || code >= 80 && code <= 82) return '☂';
  if (code >= 95) return '⚡';
  return '·';
}

function appendWeatherItem(container, className, values) {
  const item = document.createElement('div');
  item.className = className;

  values.forEach(({ text, className: valueClass, tag = 'span' }) => {
    const value = document.createElement(tag);
    if (valueClass) value.className = valueClass;
    value.textContent = text;
    item.append(value);
  });

  container.append(item);
}

function renderHourly(data) {
  const container = document.getElementById('weather-hourly');
  if (!container) return;

  container.replaceChildren();
  const now = new Date(data.current.time).getTime();
  const firstIndex = data.hourly.time.findIndex((time) => new Date(time).getTime() >= now);
  const start = Math.max(0, firstIndex);
  const times = data.hourly.time.slice(start, start + 8);

  times.forEach((time, index) => {
    const hourIndex = start + index;
    appendWeatherItem(container, 'hour-point', [
      { text: new Date(time).toLocaleTimeString([], { hour: '2-digit' }), tag: 'span' },
      { text: weatherCodeToSymbol(data.hourly.weather_code[hourIndex]), tag: 'strong', className: 'weather-symbol' },
      { text: `${Math.round(data.hourly.temperature_2m[hourIndex])}°`, tag: 'span' }
    ]);
  });
}

function renderWeek(data) {
  const container = document.getElementById('weather-week');
  if (!container) return;

  container.replaceChildren();
  data.daily.time.forEach((date, index) => {
    appendWeatherItem(container, 'forecast-day', [
      { text: new Date(`${date}T12:00:00`).toLocaleDateString([], { weekday: 'short' }), tag: 'strong' },
      { text: weatherCodeToSymbol(data.daily.weather_code[index]) },
      { text: `${Math.round(data.daily.temperature_2m_max[index])}° / ${Math.round(data.daily.temperature_2m_min[index])}°`, className: 'range' }
    ]);
  });
}

function weatherCodeToText(code) {
  const map = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    71: 'Slight snow',
    73: 'Moderate snow',
    75: 'Heavy snow',
    95: 'Thunderstorm',
  };
  return map[code] || 'Unknown';
}

export function initWeather() {
  fetchWeather()
    .then((data) => {
      const c = data.current;
      const d = data.daily;
      const container = document.getElementById('weather-view');
      if (!container) return;
      const current = document.createElement('div');
      const temperature = document.createElement('div');
      const condition = document.createElement('div');
      const details = document.createElement('div');
      const range = document.createElement('div');
      temperature.textContent = `${Math.round(c.temperature_2m)} °C`;
      condition.textContent = weatherCodeToText(c.weather_code);
      details.textContent = `Feels like ${Math.round(c.apparent_temperature)} °C · Humidity ${c.relative_humidity_2m}%`;
      range.textContent = `High ${Math.round(d.temperature_2m_max[0])} °C · Low ${Math.round(d.temperature_2m_min[0])} °C`;
      current.append(temperature, condition, details);
      container.replaceChildren(current, range);
      const state = document.getElementById('weather-state');
      if (state) state.textContent = 'Forecast available';
      renderHourly(data);
      renderWeek(data);
    })
    .catch((e) => {
      console.error('Weather failed', e);
      const container = document.getElementById('weather-view');
      if (container) container.textContent = 'Current conditions unavailable';
      const state = document.getElementById('weather-state');
      if (state) state.textContent = 'Unavailable';
      ['weather-hourly', 'weather-week'].forEach((id) => {
        const forecast = document.getElementById(id);
        if (forecast) forecast.textContent = 'Forecast unavailable';
      });
    });
}