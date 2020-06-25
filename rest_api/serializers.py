from rest_framework import serializers
from .models import Swarm, Service, Node, Deployment

class SwarmSerializer(serializers.ModelSerializer):
    nodes = serializers.HyperlinkedRelatedField(many=True, view_name='node-detail', read_only=True)
    class Meta:
        model = Swarm
        fields = ['url', 'id','organisation', 'manager_join_token', 'worker_join_token', 'base_url', 'nodes']

class NodeSerializer(serializers.ModelSerializer):
    swarm = serializers.HyperlinkedRelatedField(view_name='swarm-detail', queryset=Swarm.objects.all(), allow_null=True)
    class Meta:
        model = Node
        fields = ['url', 'id', 'docker_url', 'swarm_manager', 'hostname', 'swarm']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['url', 'id', 'name', 'description', 'image', 'version', 'active', 'date_added', 'source', 'website']

class DeploymentSerializer(serializers.ModelSerializer):
    swarm = serializers.HyperlinkedRelatedField(view_name='swarm-detail', queryset=Swarm.objects.all())
    service = serializers.HyperlinkedRelatedField(view_name='service-detail', queryset=Service.objects.all())
    class Meta:
        model = Deployment
        fields = ['url', 'id', 'created', 'swarm', 'service']