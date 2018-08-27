from deployment import CloudDeploymentOperations
from settings import Settings, SettingsProvider

settings_provider = SettingsProvider()

def main():
  settings = get_settings()
  templates_path = get_templates_path()

  ops = CloudDeploymentOperations(settings = settings, templates_path = templates_path)

  #ops.deploy_cloud_resources()
  #ops.deploy_cosmosdb_database_graph()
  #ops.deploy_cosmosdb_data()

def get_settings():
  settings = settings_provider.get_settings()
  update_settings_with_prefix_to_ensure_unique_names(settings)

  return settings

def update_settings_with_prefix_to_ensure_unique_names(settings):
    suffix = settings_provider.get_param_suffix()
    settings.resourceGroup.name = settings.resourceGroup.name + '-' + suffix
    settings.resources.cosmosdb.name = settings.resources.cosmosdb.name + suffix
    settings.resources.functionApp.name = settings.resources.functionApp.name + suffix
    settings.resources.apiManagement.name = settings.resources.apiManagement.name + suffix

def get_templates_path():
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    path = current_path.parents[0] / 'templates'
    return path

if __name__ == "__main__":
    main()