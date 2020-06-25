from django.db import models
import uuid

# Create your models here.
class Swarm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    organisation = models.CharField(max_length=100)
    manager_join_token = models.CharField(max_length=86, editable=False)
    worker_join_token = models.CharField(max_length=86, editable=False)
    base_url = models.URLField(default='https://localhost:4433')
    #manager_node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='swarm')
    #nodes = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='swarm')

    def __str__(self):
        return f"{self.organisation}"


class Node(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    docker_url = models.URLField()
    swarm_manager = models.BooleanField()
    hostname = models.CharField(max_length=100)
    swarm = models.ForeignKey(
        'Swarm',
        on_delete=models.SET_NULL,
        related_name='nodes',
        related_query_name='node',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.hostname}"


class Service(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.CharField(max_length=100)
    version = models.CharField(max_length=12, default='v0.0.0', help_text='Version must follow semantic versioning pattern (e.g.: v0.0.0)')
    date_added = models.DateTimeField(auto_now_add=True)
    """ added_by = models.ForeignKey(
        'User',
        related_name='services',
        on_delete=models.CASCADE
    ) """
    
    active = models.BooleanField(default=False)
    source = models.URLField()
    website = models.URLField()
    def __str__(self):
        return f"{self.name} - {self.version}"


class Deployment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    swarm = models.ForeignKey('Swarm', on_delete=models.CASCADE, related_name='deployments')
    created = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='deployments'
    )

    def __str__(self):
        return f"{self.swarm} - {self.service}"

"""     organisation = models.ForeignKey(
        'Organisation',
        on_delete=models.CASCADE,
        related_name='deployments'
    ) """

