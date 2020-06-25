from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import SwarmSerializer, NodeSerializer, ServiceSerializer, DeploymentSerializer
from .models import Swarm, Service, Node, Deployment
from .docker import Docker
from .helpers import get_swarm_id, get_swarm_manager


# Create your views here.
class SwarmViewSet(viewsets.ModelViewSet):
    queryset = Swarm.objects.all()
    serializer_class = SwarmSerializer

    def perform_create(self, serializer):

        base_url = self.request.data['base_url']

        docker = Docker(base_url=base_url)
        swarm = docker.init_swarm()
        
        manager_token = swarm.attrs['JoinTokens']['Manager']
        worker_token = swarm.attrs['JoinTokens']['Worker']

        serializer.save(manager_join_token=manager_token, worker_join_token=worker_token)

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def perform_update(self, serializer):
        if self.request.data['docker_url'] is not None:
            base_url = self.request.data['docker_url']
            docker = Docker(base_url=base_url)
        else:
            serializer.save()
            return Response(
                'No docker url specified, unable to interact with docker daemon.',
                status=404
                )

        swarm_manager = self.request.data['swarm_manager']

        if len(self.request.data['swarm']) > 0:
            swarm_arr = self.request.data['swarm'].split('/')
            swarm_id = swarm_arr[len(swarm_arr)-2]

            
            
            if swarm_manager:
                join_token = Swarm.objects.get(id=swarm_id).manager_join_token
                manager_hostname = self.request.data['hostname']
            else:
                join_token = Swarm.objects.get(id=swarm_id).worker_join_token
                manager_hostname = Node.objets.get(swarm=self.request.data['swarm'], swarm_manager=True)

            
            try:
                swarm = docker.join_swarm(f"{manager_hostname}:2377", join_token)
                serializer.save()
            except docker.errors.APIError:
                serializer.save()
                return Response({
                'message': "This node already belongs to a swarm. Remove it from its existing swarm to proceed",
                'swarm': self.request.data['swarm']
                })
                
        else:
            docker.leave_swarm(force=swarm_manager)
            serializer.save()


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer

    def perform_create(self, serializer):
        swarm_id = get_swarm_id(self.request)
        manager_node = Node.objects.get(swarm=swarm_id, swarm_manager=True)
        base_url = manager_node.docker_url

        service_dict = {
            'image': self.request.data['image'],
            'command': '',
            'args': [''],
            'constraints': [''],
            'preferences': [('', '')],
            'platforms': [('', '')],
            'container_labels': {},
            'endpoint_spec': '',
            'env': [''],
            'hostname': '',
            'init': False,
            'labels': {},
            'log_driver': '',
            'log_driver_options': {},
            'mode': None,
            'mounts': [''],
            'name': self.request.data['name'],
            'networks': [],
            'resources': '',
            'restart_policy': '',
            'secrets': '',
            'stop_grace_period': '',
            'update_config': None,
            'rollback_config': None,
            'user': '',
            'workdir': '',
            'tty': '',
            'groups': [],
            'open_stdin': False,
            'read_only': False,
            'stop_signal': '',
            'healthcheck': '',
            'hosts': {},
            'dns_config': None,
            'configs': [],
            'privileges': None
        }
        
        docker = Docker(base_url=base_url)
        docker.create_service(**service_dict)
        serializer.save()