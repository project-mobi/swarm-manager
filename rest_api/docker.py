import docker

class Docker:
    def __init__(self, base_url='unix://var/run/docker.sock', client_cert=('/Users/fabianvolkers/Developer/mobi/backend/docker.cert', '/Users/fabianvolkers/Developer/mobi/backend/docker.key')):
        self.tls_config = docker.tls.TLSConfig(client_cert=client_cert)
        print(self.tls_config)
        self.client = docker.DockerClient(base_url, tls=self.tls_config)
        self.errors = docker.errors

    def init_swarm(self):
        if len(self.client.swarm.attrs) == 0:
            self.client.swarm.init()
        else:
            print('This node is already part of a swarm, skipping initialisation')

        return self.client.swarm

    def join_swarm(self, addrs, join_token):
        return self.client.swarm.join(
            remote_addrs=[addrs],
            join_token=join_token
        )
    
    def leave_swarm(self, force=False):
        return self.client.swarm.leave(force=force)

    def create_service(self, **data):
        self.client.services.create(**data)


