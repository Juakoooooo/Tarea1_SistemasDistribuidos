from flask import Flask, request, jsonify
import redis
import grpc
import dns_resolver_pb2
import dns_resolver_pb2_grpc
import logging
import hashlib

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Conexión a la instancia Redis cuando es única
#redis_node = redis.StrictRedis(host='redis1', port=6379, decode_responses=True)

# Conexión a las instancias Redis (aquí se ajusta en base a los casos solicitados)
redis_nodes = {
    'redis1': redis.StrictRedis(host='redis1', port=6379, decode_responses=True),
    'redis2': redis.StrictRedis(host='redis2', port=6379, decode_responses=True),
    'redis3': redis.StrictRedis(host='redis3', port=6379, decode_responses=True),
    'redis4': redis.StrictRedis(host='redis4', port=6379, decode_responses=True)
    #'redis5': redis.StrictRedis(host='redis5', port=6379, decode_responses=True),
    #'redis6': redis.StrictRedis(host='redis6', port=6379, decode_responses=True),
    #'redis7': redis.StrictRedis(host='redis7', port=6379, decode_responses=True),
    #'redis8': redis.StrictRedis(host='redis8', port=6379, decode_responses=True)
}


def get_redis_node_by_hash(key):
    """Devuelve el nodo Redis correspondiente basado en un hash de la clave"""
    hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
    node_index = hash_value % len(redis_nodes)
    node_name = list(redis_nodes.keys())[node_index]
    logging.debug(f"Clave {key} asignada a {node_name} usando hash")
    return redis_nodes[node_name], node_name 

def get_redis_node_by_range(key, num_partitions=4):
    """Devuelve el nodo Redis correspondiente basado en rangos de la clave y el número de particiones"""
    first_char = key[0].lower()
    node_name = None
    
    # Distribución en 2 particiones
    if num_partitions == 2:
        if 'a' <= first_char <= 'm':
            node_name = 'redis1'
        else:
            node_name = 'redis2'
    
    # Distribución en 4 particiones
    elif num_partitions == 4:
        if 'a' <= first_char <= 'f':
            node_name = 'redis1'
        elif 'g' <= first_char <= 'l':
            node_name = 'redis2'
        elif 'm' <= first_char <= 'r':
            node_name = 'redis3'
        else:
            node_name = 'redis4'

    # Distribución en 8 particiones (por defecto)
    elif num_partitions == 8:
        if 'a' <= first_char <= 'd':
            node_name = 'redis1'
        elif 'e' <= first_char <= 'h':
            node_name = 'redis2'
        elif 'i' <= first_char <= 'l':
            node_name = 'redis3'
        elif 'm' <= first_char <= 'p':
            node_name = 'redis4'
        elif 'q' <= first_char <= 't':
            node_name = 'redis5'
        elif 'u' <= first_char <= 'w':
            node_name = 'redis6'
        elif 'x' <= first_char <= 'z':
            node_name = 'redis7'
        else:
            node_name = 'redis8'

    if node_name not in redis_nodes:
        logging.error(f"Error: El nodo {node_name} no está definido en redis_nodes")
        raise KeyError(f"El nodo {node_name} no está definido en redis_nodes")

    logging.debug(f"Clave {key} asignada a {node_name} usando rangos con {num_partitions} particiones")
    return redis_nodes[node_name], node_name


@app.route('/resolve', methods=['GET'])
def resolve_domain():
    domain = request.args.get('domain')
    logging.debug(f"Received request to resolve domain: {domain}")
    
    if not domain:
        logging.error("No domain provided")
        return jsonify({"error": "No domain provided"}), 400

    # Esto se utiliza en el caso de asignación a particiones

    # Asignación por Hash
    #redis_node, redis_partition = get_redis_node_by_hash(domain)
    
    # Asignación por Rango (Comentar si se usa hash)
    redis_node, redis_partition = get_redis_node_by_range(domain)

    # Revisar si existe en cache
    if redis_node.exists(domain):
        ip_address = redis_node.get(domain)
        logging.debug(f"Domain {domain} found in cache with IP {ip_address}")

        #Esto se utiliza en el caso de asignación a particiones
        return jsonify({"domain": domain, "ip": ip_address, "source": "cache", "partition": redis_partition}), 200

        #Esto se utiliza en el caso de asignación a una única instancia
        #return jsonify({"domain": domain, "ip": ip_address, "source": "cache", "partition": "redis1"}), 200
    
    logging.debug(f"Domain {domain} not found in cache. Querying gRPC server.")
    try:
        # Conexión con gRPC para resolver el dominio
        with grpc.insecure_channel('grpc-dns-server:50051') as channel:
            stub = dns_resolver_pb2_grpc.DNSResolverStub(channel)
            response = stub.Resolve(dns_resolver_pb2.DNSRequest(domain=domain))
            ip_address = response.ip
            logging.debug(f"gRPC server returned IP {ip_address} for domain {domain}")
        
            if ip_address == "":
                return jsonify({"error": f"Domain {domain} not found"}), 404

            redis_node.set(domain, ip_address)

            #Esto se utiliza en el caso de asignación a particiones
            logging.debug(f"Cached {domain} with IP {ip_address} in {redis_partition}")

            #Esto se utiliza en el caso de asignación a una única instancia
            #logging.debug(f"Cached {domain} with IP {ip_address}")

            #Esto se utiliza en el caso de asignación a particiones
            return jsonify({"domain": domain, "ip": ip_address, "source": "gRPC", "partition": redis_partition}), 200

            #Esto se utiliza en el caso de asignación a una única instancia
            #return jsonify({"domain": domain, "ip": ip_address, "source": "gRPC", "partition": "redis1"}), 200
    except grpc.RpcError as e:
        logging.error(f"gRPC call failed: {e}")
        return jsonify({"error": f"gRPC call failed: {e}"}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Error al iniciar el servidor Flask: {e}")
