import grpc
from concurrent import futures
import subprocess
import dns_resolver_pb2
import dns_resolver_pb2_grpc

class DNSResolver(dns_resolver_pb2_grpc.DNSResolverServicer):
    def Resolve(self, request, context):
        domain = request.domain
        result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True)
        ip_address = result.stdout.strip()
        return dns_resolver_pb2.DNSResponse(ip=ip_address)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_resolver_pb2_grpc.add_DNSResolverServicer_to_server(DNSResolver(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
