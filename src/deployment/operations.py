import os
import os.path
from pathlib import Path
import json
from datetime import datetime
from .utilities import ResourceDeployer, CosmosDbManager

class CloudDeploymentOperations(object):
    
    def __init__(self, settings, templates_path):
        self.settings = settings
        self.templates_path = templates_path
        self.cosmosdb = CosmosDbManager(settings)

    def deploy_cloud_resources(self):
        deployer = ResourceDeployer(settings = self.settings)

        deployer.ensure_resource_group()
        
        print("\nPrimary resources.")
        deployer.deploy(
            template_path = self.__get_template_file_path('resources.json'), 
            template_parameters = self.__get_resources_parameters()
        )
        # deploy API Management separately since it takes 15-20 minutes to complete
        print("\nAPI Management.")
        deployer.deploy(
            template_path = self.__get_template_file_path('apim.json'), 
            template_parameters = self.__get_apim_parameters(),
            wait = False
        )

    def deploy_cosmosdb_database_graph():
        cosmosdb.create_database()
        cosmosdb.create_graph()

    def deploy_cosmosdb_data():
        cosmosdb.seed_data_into_graph()

    def __get_resources_parameters(self):
        params = self.__get_template_parameters('resources.parameters.json')

        params['databaseAccountName']['value'] = self.settings.resources.cosmosdb.name
        params['functionAppName']['value'] = self.settings.resources.functionApp.name

        return params
    
    def __get_apim_parameters(self):
        params = self.__get_template_parameters('apim.parameters.json')

        params['apiManagementServiceName']['value'] = self.settings.resources.apiManagement.name
        params['apiManagementAdminName']['value'] = self.settings.resources.apiManagement.admin.name
        params['apiManagementAdminEmail']['value'] = self.settings.resources.apiManagement.admin.email

        return params

    def __get_template_parameters(self, param_file):
        template_parameters_path = self.__get_template_file_path(param_file)
        template_parameters = self.__get_json(template_parameters_path)
        return template_parameters['parameters']

    def __get_json(self, file_path):
        with open(file_path, 'r') as file_fd:
            content = json.load(file_fd)
            return content

    def __get_template_file_path(self, file_name):
        path = os.path.join(self.templates_path, file_name)
        return path