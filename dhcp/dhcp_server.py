class DHCPServer:
    def __init__(self, start_ip, end_ip):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.ip_pool = self.generate_ip_pool()
        self.allocated_ips = {}

    def generate_ip_pool(self):
        start_octets = list(map(int, self.start_ip.split('.')))
        end_octets = list(map(int, self.end_ip.split('.')))
        ip_pool = []
        for i in range(start_octets[-1], end_octets[-1] + 1):
            ip_pool.append(f"{start_octets[0]}.{start_octets[1]}.{start_octets[2]}.{i}")
        return ip_pool

    def allocate_ip(self, peer_id):
        if peer_id in self.allocated_ips:
            return self.allocated_ips[peer_id]
        if not self.ip_pool:
            raise Exception("No available IP addresses")
        allocated_ip = self.ip_pool.pop(0)
        self.allocated_ips[peer_id] = allocated_ip
        return allocated_ip

    def release_ip(self, peer_id):
        if peer_id in self.allocated_ips:
            released_ip = self.allocated_ips.pop(peer_id)
            self.ip_pool.append(released_ip)
