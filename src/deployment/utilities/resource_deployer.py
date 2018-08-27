"""A deployer class to deploy a template on Azure"""
import os.path
import json
from datetime import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

class ResourceDeployer(object):
    def __init__(self, settings):
        self.settings = settings
        self.subscription_id = settings.account.subscriptionId
        self.resource_group = {
            'name': settings.resourceGroup.name,
            'params': {'location': settings.resourceGroup.location}
        }

        self.credentials = ServicePrincipalCredentials(
            client_id = settings.account.client.id,
            secret = settings.account.client.secret,
            tenant = settings.account.tenantId
        )
        self.client = ResourceManagementClient(self.credentials, self.subscription_id)
    
    def __get_json(self, file_path):
        with open(file_path, 'r') as file_fd:
            content = json.load(file_fd)
            return content

    def ensure_resource_group(self):
        print('Creating / Updating Resource Group')
        print(self.resource_group)

        self.client.resource_groups.create_or_update(
            self.resource_group['name'], self.resource_group['params']
        )

    def deploy(self, template_parameters, template_path, wait = True):
        deployment_properties = {
            'mode': DeploymentMode.incremental,
            'template': self.__get_json(template_path),
            'parameters': template_parameters
        }
        deployment_name = self.__get_deployment_name()

        print('\nExecuting deployment operation...')
        
        deployment_async_operation = self.client.deployments.create_or_update(
            self.settings.resourceGroup.name,
            deployment_name,
            deployment_properties
        )
        if wait is True:
            deployment_async_operation.wait()
            print('Deployment complete.')
        else:
            print('Deployment continuing....')

    def destroy(self):
        """Destroy the given resource group"""
        self.client.resource_groups.delete(self.resource_group)
    
    def __get_deployment_name(self):
        name = self.settings.resourceGroup.name
        return name + '-' + datetime.now().strftime("%I%M%S")