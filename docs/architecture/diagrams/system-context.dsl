workspace "Chit System Context" "Pilot system context" {
  model {
    household = person "Household member" "Uses a shared display to understand plans, chores and energy context."
    admin = person "Household administrator" "Configures local deployment, integrations and privacy."
    chit = softwareSystem "Chit" "Local-first household overview and explainable insight platform."
    calendar = softwareSystem "Calendar provider" "Provides authorised household events." "External"
    weather = softwareSystem "Weather provider" "Provides current conditions and forecasts." "External"
    ha = softwareSystem "Home Assistant" "Provides allowlisted device and energy states." "External"
    display = softwareSystem "Shared TV/tablet" "Renders the screen-safe dashboard." "External"
    household -> chit "Views household context"
    admin -> chit "Configures household and integrations"
    chit -> calendar "Reads events"
    chit -> weather "Reads weather"
    chit -> ha "Reads approved entities"
    chit -> display "Serves screen-safe dashboard"
  }
  views {
    systemContext chit "SystemContext" { include *; autolayout lr }
  }
}
