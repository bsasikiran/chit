/**
 * CALENDAR INTEGRATION
 *
 * OPTION A – Apple (iCloud) Calendar via a widget provider (recommended)
 * 1. On your Mac/iPhone:
 *    - Open Calendar app.
 *    - Right-click the calendar you want → Share / Public URL.
 *    - Copy the public URL (webcal:// or https://).
 * 2. Go to a widget provider like:
 *    - https://www.indycalendar.com/
 *    - https://www.elfsight.com/apple-calendar-embed-web/
 * 3. Paste your iCloud URL, configure style (month view, colors).
 * 4. Copy the embed snippet they give you.
 * 5. Replace the content of this function with that snippet.
 *
 * OPTION B – FullCalendar + iCloud iCal feed (more control, more work)
 * - Include FullCalendar via CDN in home.html.
 * - Use your iCloud public URL as an iCal feed.
 * - Initialize FullCalendar here with that feed (may need a small proxy to convert iCal to JSON).
 */

export function initCalendar() {
  const container = document.getElementById('calendar-view');
  if (!container) return;

  const message = document.createElement('p');
  const detail = document.createElement('p');
  message.textContent = 'Family calendar unavailable';
  detail.textContent = 'No calendar source is configured, so events are not shown.';
  container.replaceChildren(message, detail);

  const week = document.getElementById('important-events');
  if (!week) return;

  week.replaceChildren();
  Array.from({ length: 7 }, (_, offset) => {
    const date = new Date();
    date.setDate(date.getDate() + offset);

    const tile = document.createElement('div');
    const day = document.createElement('strong');
    const state = document.createElement('span');
    tile.className = 'event-tile';
    day.textContent = date.toLocaleDateString([], { weekday: 'short', day: 'numeric' });
    state.textContent = 'Unavailable';
    tile.append(day, state);
    week.append(tile);
  });

  /* EXAMPLE – what it might look like with a widget (pseudo-code):
  container.innerHTML = `
    <div id="elfsight-app-xxxx"></div>
    <script src="https://static.elfsight.com/setup.js" defer></script>
  `;
  */
}