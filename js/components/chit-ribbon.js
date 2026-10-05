class ChitRibbon extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  async connectedCallback() {
    this.renderLoading();
    
    try {
      const response = await fetch('/api/home/summary');
      if (response.status === 401) {
        window.location.href = '/login.html?next=' + encodeURIComponent(window.location.pathname);
        return;
      }
      if (!response.ok) throw new Error('Failed to fetch summary');
      
      const data = await response.json();
      if (data.state === 'unconfigured') {
        if (window.location.pathname !== '/dashboard/household-setup.html') {
          window.location.href = '/dashboard/household-setup.html';
        } else {
          this.renderReady({ name: 'Household Setup', members: [] });
        }
        return;
      }
      
      this.renderReady(data.household);
    } catch (e) {
      console.error(e);
      this.renderError();
    }
  }

  getStyles() {
    return `
      :host {
        display: block;
        --ink: #20332e;
        --muted: #697873;
        --line: #d9e1dc;
        --surface: #fffefa;
        --green: #276957;
        --green-dark: #194c40;
        --mint: #e5f0e8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      * { box-sizing: border-box; }

      .ribbon-container {
        background: var(--surface);
        border-bottom: 1px solid var(--line);
      }

      .top-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px clamp(18px, 4vw, 58px);
        border-bottom: 1px solid var(--line);
      }

      .brand { 
        display: flex; 
        align-items: center; 
        gap: 11px; 
        font-weight: 800; 
        letter-spacing: .02em; 
        color: var(--ink);
        text-decoration: none;
      }

      .brand-mark { 
        width: 32px; 
        height: 32px; 
        display: grid; 
        place-items: center; 
        border-radius: 9px; 
        color: white; 
        background: var(--green); 
        font-size: 16px; 
      }

      .right-actions {
        display: flex;
        align-items: center;
        gap: 16px;
      }

      .members-list {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .member {
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--ink);
        font-size: 13px;
        font-weight: 600;
      }

      .member-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--mint);
        color: var(--green-dark);
        display: grid;
        place-items: center;
        font-size: 14px;
        border: 1px solid var(--line);
      }

      .divider {
        width: 1px;
        height: 24px;
        background: var(--line);
        margin: 0 4px;
      }

      .icon-btn {
        background: none;
        border: 1px solid transparent;
        border-radius: 8px;
        color: var(--muted);
        cursor: pointer;
        padding: 6px;
        display: grid;
        place-items: center;
        font-size: 18px;
        transition: all 0.2s;
        text-decoration: none;
      }

      .icon-btn:hover {
        background: var(--mint);
        color: var(--green-dark);
      }

      .icon-btn.logout {
        border-color: var(--line);
        font-size: 13px;
        font-weight: 700;
        padding: 6px 12px;
        display: flex;
        gap: 6px;
      }

      .nav-row {
        display: flex;
        padding: 0 clamp(18px, 4vw, 58px);
        gap: 8px;
        background: #fafafa;
      }

      .nav-link {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        color: var(--muted);
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
      }

      .nav-link:hover, .nav-link.active {
        color: var(--green-dark);
        border-bottom-color: var(--green);
        background: rgba(229, 240, 232, .72);
      }

      .nav-link.active {
        background: rgba(229, 240, 232, 1);
      }

      @media (max-width: 700px) {
        .members-list { display: none; }
      }
    `;
  }

  renderLoading() {
    this.shadowRoot.innerHTML = `
      <style>${this.getStyles()}</style>
      <div class="ribbon-container">
        <div class="top-row">
          <div class="brand">
            <div class="brand-mark">🏠</div>
            <div>Loading...</div>
          </div>
        </div>
      </div>
    `;
  }

  renderError() {
    this.shadowRoot.innerHTML = `
      <style>${this.getStyles()}</style>
      <div class="ribbon-container">
        <div class="top-row">
          <div class="brand">
            <div class="brand-mark" style="background:var(--coral)">!</div>
            <div>Error loading household</div>
          </div>
        </div>
      </div>
    `;
  }

  renderReady(household) {
    // Get active page from attribute
    const activePage = this.getAttribute('active') || 'home';
    
    // Sort members: adults first, then kids (just visual)
    const members = household.members || [];
    
    this.shadowRoot.innerHTML = `
      <style>${this.getStyles()}</style>
      <div class="ribbon-container">
        <!-- TOP RIBBON -->
        <div class="top-row">
          <a href="/dashboard/home.html" class="brand">
            <div class="brand-mark">🏠</div>
            <div>${this.escapeHtml(household.name)}</div>
          </a>
          
          <div class="right-actions">
            <div class="members-list">
              ${members.map(m => `
                <div class="member" title="${this.escapeHtml(m.role)}">
                  <div class="member-avatar">👤</div>
                  <span>${this.escapeHtml(m.name)}</span>
                </div>
              `).join('')}
            </div>

            <div class="divider"></div>

            <a href="/dashboard/household-setup.html" class="icon-btn" title="Household Settings">
              ⚙️
            </a>
            
            <button class="icon-btn logout" id="logout-btn" title="Sign out">
              <span>🚪</span> Sign out
            </button>
          </div>
        </div>

        <!-- NAVIGATION RIBBON -->
        <div class="nav-row">
          <a href="/dashboard/home.html" class="nav-link ${activePage === 'home' ? 'active' : ''}">
            Dashboard
          </a>
          <a href="/dashboard/calendar-home.html" class="nav-link ${activePage === 'calendar' ? 'active' : ''}">
            Calendar
          </a>
          <a href="/dashboard/household-setup.html" class="nav-link ${activePage === 'settings' ? 'active' : ''}">
            Settings
          </a>
        </div>
      </div>
    `;

    // Attach logout event
    this.shadowRoot.getElementById('logout-btn').addEventListener('click', async () => {
      const csrf = sessionStorage.getItem('chit_csrf') || '';
      try {
        await fetch('/api/auth/logout', { method: 'POST', headers: { 'X-CSRF-Token': csrf } });
      } catch (e) {
        console.error('Logout request failed', e);
      }
      sessionStorage.removeItem('chit_csrf');
      window.location.href = '/login.html';
    });
  }

  escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}

customElements.define('chit-ribbon', ChitRibbon);
