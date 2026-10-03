import { CHIT_CONFIG } from './config.js';
import { initEnergy } from './tibber.js';
import { initWeather } from './weather.js';
import { initCalendar } from './calendar.js';

function initDateLine() {
  const element = document.getElementById('date-line');

  if (!element) return;

  element.textContent = new Date().toLocaleDateString('en-GB', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

function initHomeLabel() {
  const element = document.getElementById('home-label');

  if (!element) return;

  element.textContent = CHIT_CONFIG.homeName || 'Home';
}

async function init() {
  initDateLine();
  initHomeLabel();
  initCalendar();
  initWeather();
  await initEnergy();
}

init().catch((error) => {
  console.error('Dashboard initialization failed:', error);
});