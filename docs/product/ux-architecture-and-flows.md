## UX Architecture & Mermaid Flow Diagrams

### Dashboard visual architecture

#### Layout structure

- **Global shell:** Persistent left navigation on desktop; collapsible navigation drawer on tablet and mobile.
- **Top bar:** Current workspace or household selector, global search, notifications, help, and user profile.
- **Page header:** Dashboard title, date or context selector, primary action, and optional secondary actions.
- **Main canvas:** Responsive 12-column grid with a consistent spacing scale and card-based modules.
- **Context rail:** Optional right-side panel for activity, reminders, recommendations, or details; hidden below desktop breakpoints.
- **Mobile layout:** Single-column stacking with bottom navigation for the highest-frequency destinations and a floating primary-action button.

#### Widget hierarchy

1. **Orientation layer**
   - Page title and current context.
   - Status summary.
   - Primary next action.

2. **Priority layer**
   - Attention-required items.
   - Overdue or blocked items.
   - Time-sensitive reminders.
   - Exceptions and unresolved conflicts.

3. **Planning layer**
   - Today or upcoming view.
   - Agenda, tasks, events, and commitments.
   - Progress toward active goals.

4. **Coordination layer**
   - Shared activity.
   - Assigned responsibilities.
   - Recent updates.
   - Requests requiring acknowledgement.

5. **Discovery layer**
   - Suggestions.
   - Frequently used actions.
   - Recent or favourite items.
   - Optional insights.

#### Information density

- Use **high density** only for lists, schedules, and operational status where scanning is the primary task.
- Use **medium density** for summary cards containing one headline metric, a short status label, and one supporting detail.
- Use **low density** for onboarding, empty states, confirmations, and decision points.
- Display no more than **three primary priorities** above the first scroll on desktop.
- Use progressive disclosure for secondary metadata, history, permissions, and advanced settings.
- Make state visible through text labels and icons; do not rely on colour alone.
- Reserve strong accent colours for actionable status, warnings, and completion feedback.
- Keep one dominant action per page or major card.
- Preserve user context when opening details by using drawers or modal panels for short tasks and full-page views for complex workflows.
- Maintain consistent states for loading, empty, error, offline, permission denied, and successful completion.
- Support keyboard focus order that follows the visual hierarchy and ensure all actionable elements have explicit labels.

```mermaid
flowchart TD
    A[Application shell] --> B[Global navigation]
    A --> C[Top bar]
    A --> D[Dashboard canvas]
    A --> E[Context rail]

    B --> B1[Primary destinations]
    B --> B2[Workspace or household switcher]
    B --> B3[Settings and permissions]

    C --> C1[Current context]
    C --> C2[Global search]
    C --> C3[Notifications]
    C --> C4[Help]
    C --> C5[Profile]

    D --> D1[Page header]
    D --> D2[Priority summary]
    D --> D3[Attention-required items]
    D --> D4[Today or upcoming view]
    D --> D5[Shared activity]
    D --> D6[Suggested actions]

    D1 --> D1a[Title and context]
    D1 --> D1b[Primary action]
    D1 --> D1c[Filters or date selector]

    D2 --> D2a[Status metrics]
    D2 --> D2b[Progress indicators]
    D2 --> D2c[Exception count]

    E --> E1[Reminders]
    E --> E2[Recent activity]
    E --> E3[Recommendations]

    D3 --> F[Detail drawer or full-page detail]
    D4 --> F
    D5 --> F
    D6 --> F
```

### Core navigation and orientation

```mermaid
flowchart TD
    A[User opens application] --> B{Authenticated?}
    B -- No --> C[Sign in or create account]
    C --> D{Access available?}
    D -- No --> E[Show access or invitation guidance]
    D -- Yes --> F[Load selected workspace]
    B -- Yes --> F

    F --> G{First visit or incomplete setup?}
    G -- Yes --> H[Show guided setup]
    H --> I[Confirm preferences and permissions]
    I --> J[Open personalized dashboard]
    G -- No --> J

    J --> K[Review priorities]
    K --> L{Choose destination}
    L --> M[Open item or task]
    L --> N[Open calendar or schedule]
    L --> O[Open shared activity]
    L --> P[Open settings]
    L --> Q[Use global search]
```

### Dashboard review and action completion

```mermaid
flowchart TD
    A[Open dashboard] --> B[Load current context]
    B --> C{Data available?}
    C -- No, loading --> D[Show skeleton placeholders]
    D --> B
    C -- No, error --> E[Show error state and retry action]
    E --> B
    C -- Yes --> F[Present priority summary]

    F --> G{Attention item exists?}
    G -- Yes --> H[Select highest-priority item]
    G -- No --> I[Review today's plan]

    H --> J[Open item detail]
    J --> K[Review status, owner, timing, and related items]
    K --> L{Action required?}
    L -- No --> M[Mark as reviewed]
    L -- Yes --> N[Choose action]

    N --> O[Complete item]
    N --> P[Assign or reassign]
    N --> Q[Change date or priority]
    N --> R[Add note or update]
    N --> S[Dismiss or snooze]

    O --> T[Validate changes]
    P --> T
    Q --> T
    R --> T
    S --> T

    T --> U{Saved successfully?}
    U -- No --> V[Show validation or conflict message]
    V --> K
    U -- Yes --> W[Show confirmation feedback]
    W --> X[Refresh dashboard priorities]
    X --> Y[Continue with next priority or exit]
    M --> X
    I --> Y
```

### Create, schedule, or assign an item

```mermaid
flowchart TD
    A[Select primary action] --> B[Choose item type]
    B --> C[Enter title or request]
    C --> D[Add optional details]
    D --> E[Choose date or time]
    E --> F[Choose owner or participants]
    F --> G[Set priority, recurrence, or reminders]
    G --> H[Review item summary]

    H --> I{Information complete?}
    I -- No --> J[Highlight missing or invalid fields]
    J --> C
    I -- Yes --> K{Potential conflict?}

    K -- Yes --> L[Show conflict explanation and alternatives]
    L --> M{Adjust item?}
    M -- Yes --> E
    M -- No --> N[Continue with explicit acknowledgement]

    K -- No --> N
    N --> O[Save item]
    O --> P{Save successful?}
    P -- No --> Q[Show recoverable error and preserve input]
    Q --> O
    P -- Yes --> R[Show success confirmation]
    R --> S[Open item detail or return to dashboard]
```

### Shared coordination and acknowledgement

```mermaid
flowchart TD
    A[Open shared activity or coordination view] --> B[Load updates, assignments, and requests]
    B --> C{Items available?}
    C -- No --> D[Show empty state with suggested action]
    C -- Yes --> E[Group items by urgency and status]

    E --> F[Select an item]
    F --> G[Review context and requested action]
    G --> H{User response required?}

    H -- No --> I[Read update]
    I --> J[Optionally react or add a note]
    H -- Yes --> K{Accept assignment or request?}

    K -- Yes --> L[Confirm acceptance]
    K -- No --> M[Decline, delegate, or request clarification]

    L --> N[Update ownership and status]
    M --> O[Record response and notify relevant participants]
    J --> P[Return to activity list]
    N --> P
    O --> P

    P --> Q{More pending items?}
    Q -- Yes --> F
    Q -- No --> R[Show coordination summary]
```

### Search and retrieval

```mermaid
flowchart TD
    A[Activate global search] --> B[Enter keyword or phrase]
    B --> C[Show suggested matches and recent searches]
    C --> D{Select suggestion or submit search}
    D --> E[Display grouped results]

    E --> F[Filter by type, status, person, date, or workspace]
    F --> G[Sort by relevance or recency]
    G --> H[Select result]
    H --> I[Open result detail]

    I --> J{Required action?}
    J -- No --> K[Review information]
    J -- Yes --> L[Perform contextual action]
    L --> M[Save or confirm change]
    M --> N[Return to result context]
    K --> N
```

### Notifications and reminders

```mermaid
flowchart TD
    A[Open notifications] --> B[Load unread and recent notifications]
    B --> C{Notifications available?}
    C -- No --> D[Show clear inbox state]
    C -- Yes --> E[Group by urgency and source]

    E --> F[Select notification]
    F --> G[Open linked context]
    G --> H{Action needed?}

    H -- Yes --> I[Complete, acknowledge, snooze, or dismiss]
    H -- No --> J[Review linked update]

    I --> K[Update notification state]
    J --> K
    K --> L{More unread notifications?}
    L -- Yes --> F
    L -- No --> M[Mark remaining notifications as read]
    M --> N[Return to previous context]
```

### Empty, error, and permission states

```mermaid
flowchart TD
    A[User opens a feature] --> B{State available?}
    B -- Data loading --> C[Show skeleton state]
    C --> B

    B -- Empty --> D[Explain what is missing]
    D --> E[Offer one relevant primary action]
    E --> F[Guide user through creation or setup]

    B -- Error --> G[Explain impact in plain language]
    G --> H[Offer retry]
    H --> I{Retry successful?}
    I -- Yes --> J[Render feature]
    I -- No --> K[Offer recovery path or support guidance]

    B -- Permission denied --> L[Explain required access]
    L --> M{Can user request access?}
    M -- Yes --> N[Submit access request]
    M -- No --> O[Identify administrator or owner]
```
