import { CHIT_CONFIG } from './config.js';

const TIBBER_URL = 'https://api.tibber.com/v1-beta/gql';

const query = `
  query DashboardEnergy {
    viewer {
      homes {
        id
        currentSubscription {
          priceInfo {
            current {
              total
              energy
              tax
              startsAt
              currency
            }
            today {
              total
              energy
              tax
              startsAt
              currency
            }
            tomorrow {
              total
              energy
              tax
              startsAt
              currency
            }
          }
        }
        consumption(resolution: HOURLY, last: 48) {
          nodes {
            from
            to
            consumption
            cost
            unitPrice
          }
        }
      }
    }
  }
`;

async function tibberRequest() {
  const token = CHIT_CONFIG.tibberToken?.trim();

  if (!token || token === 'YOUR_TIBBER_TOKEN_HERE') {
    throw new Error('Tibber token is missing in js/config.js');
  }

  const response = await fetch(TIBBER_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  });

  const body = await response.json();

  if (!response.ok) {
    throw new Error(`Tibber HTTP ${response.status}`);
  }

  if (body.errors?.length) {
    throw new Error(body.errors.map((error) => error.message).join('; '));
  }

  return body.data.viewer.homes[0];
}

function formatPrice(value, currency = 'EUR') {
  if (typeof value !== 'number') return '–';

  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 4
  }).format(value);
}

function setValue(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function renderEnergy(home) {
  const priceInfo = home.currentSubscription?.priceInfo;

  if (!priceInfo) {
    throw new Error('No Tibber price information returned');
  }

  const current = priceInfo.current;
  const today = (priceInfo.today ?? []).filter((price) => typeof price.total === 'number');
  const tomorrow = priceInfo.tomorrow ?? [];
  const prices = [...today, ...tomorrow];

  const now = Date.now();

  const next = prices
    .filter((price) => new Date(price.startsAt).getTime() > now)
    .sort(
      (a, b) =>
        new Date(a.startsAt).getTime() - new Date(b.startsAt).getTime()
    )[0];

  const average =
    today.length > 0
      ? today.reduce((sum, price) => sum + price.total, 0) / today.length
      : null;

  const consumptionNodes = home.consumption?.nodes ?? [];
  const consumption24h = consumptionNodes
    .slice(-24)
    .reduce((sum, item) => sum + (item.consumption ?? 0), 0);

  const estimatedCost =
    average !== null ? consumption24h * average : null;

  setValue(
    'price-current',
    current ? `${formatPrice(current.total, current.currency)} / kWh` : '–'
  );

  setValue(
    'price-next',
    next
      ? `${formatPrice(next.total, next.currency)} at ${new Date(
          next.startsAt
        ).toLocaleTimeString('de-DE', {
          hour: '2-digit',
          minute: '2-digit'
        })}`
      : '–'
  );

  setValue(
    'price-average',
    average !== null
      ? `${formatPrice(average, current?.currency)} / kWh`
      : '–'
  );

  const priceChart = document.getElementById('price-chart');
  if (priceChart) {
    priceChart.replaceChildren();
    const maxPrice = Math.max(...today.map((price) => price.total), 0);
    const minPrice = Math.min(...today.map((price) => price.total), 0);
    const range = maxPrice - minPrice || 1;

    today.forEach((price) => {
      const hour = document.createElement('div');
      const bar = document.createElement('div');
      const time = document.createElement('span');
      const value = document.createElement('strong');
      const hourLabel = new Date(price.startsAt).toLocaleTimeString('de-DE', {
        hour: '2-digit'
      });
      const formattedPrice = formatPrice(price.total, price.currency ?? current?.currency);
      const height = Math.max(4, ((price.total - minPrice) / range) * 90 + 10);

      hour.className = 'price-hour';
      hour.setAttribute('aria-label', `${hourLabel}: ${formattedPrice} per kWh`);
      bar.className = 'price-bar';
      bar.style.height = `${height}%`;
      time.textContent = hourLabel;
      value.textContent = price.total.toFixed(2);
      hour.append(bar, time, value);
      priceChart.append(hour);
    });

    if (today.length === 0) priceChart.textContent = 'Today’s prices unavailable';
  }

  setValue('energy-state', today.length > 0 ? 'Tariff available' : 'Unavailable');
  setValue('price-unit', `${current?.currency ?? 'EUR'} / kWh`);

  setValue(
    'consumption-24h',
    `${consumption24h.toFixed(2)} kWh`
  );

  setValue(
    'cost-daily',
    estimatedCost !== null
      ? formatPrice(estimatedCost, current?.currency)
      : '–'
  );

  setValue('co2-intensity', 'Not provided by Tibber query');
}

export async function initEnergy() {
  try {
    const home = await tibberRequest();
    renderEnergy(home);
  } catch (error) {
    console.error('Tibber error:', error);

    setValue('price-current', 'Unavailable');
    setValue('price-next', 'Unavailable');
    setValue('price-average', 'Unavailable');
    setValue('consumption-24h', 'Unavailable');
    setValue('cost-daily', 'Unavailable');
    setValue('co2-intensity', 'Unavailable');
    setValue('energy-state', 'Unavailable');
    setValue('price-chart', 'Today’s prices unavailable');
  }
}