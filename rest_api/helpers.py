from .models import Swarm, Node

def get_swarm_id(request):
    swarm_arr = request.data['swarm'].split('/')
    swarm_id = swarm_arr[len(swarm_arr)-2]
    return swarm_id

def get_swarm_manager(swarm_id):
    nodes = Swarm.objects.get(id=swarm_id)