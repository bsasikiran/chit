workspace "Chit Containers" "Pilot container view" {
  model {
    user = person "Household member"
    chit = softwareSystem "Chit" {
      dashboard = container "Dashboard UI" "Shared, screen-safe household view" "Web application"
      api = container "Dashboard API" "Authorised read models and configuration endpoints" "HTTP API"
      ingestion = container "Connector runtime" "Retrieves and normalizes provider data" "Service"
      insights = container "Insight service" "Creates bounded, explainable read-only insights" "Service"
      db = container "Household data store" "Normalized records, policies and insight state" "Local database"
      dashboard -> api "Reads dashboard and configuration data" "HTTPS/JSON"
      ingestion -> db "Writes normalized records"
      api -> db "Reads authorised projections"
      insights -> db "Reads evidence and writes insights"
      api -> insights "Reads explainable insights"
    }
    user -> chit.dashboard "Views household dashboard"
  }
  views {
    container chit "Containers" { include *; autolayout lr }
  }
}
