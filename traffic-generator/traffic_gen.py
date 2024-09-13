import requests
import csv
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Función para generar tráfico y registrar métricas
def generate_traffic(api_url, dataset_path, iterations=5):
    # Leer todos los dominios del dataset en una lista
    with open(dataset_path, 'r') as file:
        reader = csv.reader(file)
        domains = [row[0].strip() for row in reader]

    if not domains:
        print("No domains found in the dataset.")
        return

    # Inicializar las métricas
    hit_count = 0
    miss_count = 0
    response_times = []
    partition_requests = defaultdict(int)  # Contar peticiones por partición

    # Empezar el tráfico
    total_requests = 0
    for iteration in range(iterations):
        print(f"Starting iteration {iteration + 1} of {iterations}")
        steps = random.randint(10000, 15000)
        print(f"Generated {steps} steps for iteration {iteration + 1}.")

        for step in range(steps):
            domain = domains[step % len(domains)]  # Seleccionar un dominio
            print(f"Selected domain: {domain} (Step {step + 1} of {steps})")

            # Realizar la solicitud a la API
            start_time = time.time()
            try:
                response = requests.get(f"{api_url}/resolve", params={"domain": domain})
                end_time = time.time()

                total_requests += 1
                response_times.append(end_time - start_time)

                if response.status_code == 200:
                    result = response.json()
                    print(f"Resolved {domain}: {result} from {result['source']}")
                    
                    # Actualizar métricas de hit/miss
                    if result["source"] == "cache":
                        hit_count += 1
                    else:
                        miss_count += 1

                    # Contar las peticiones por partición
                    partition = result.get("partition", "unknown")
                    partition_requests[partition] += 1
                else:
                    print(f"Failed to resolve {domain}: {response.status_code}")
                    miss_count += 1

            except Exception as e:
                print(f"Error sending request for {domain}: {e}")
                miss_count += 1

    # Calcular métricas
    calculate_metrics(hit_count, miss_count, response_times, partition_requests)

# Función para calcular las métricas
def calculate_metrics(hit_count, miss_count, response_times, partition_requests):
    total_requests = hit_count + miss_count
    if total_requests == 0:
        print("No valid requests made.")
        return

    hit_rate = (hit_count / total_requests) * 100
    miss_rate = (miss_count / total_requests) * 100
    avg_response_time = np.mean(response_times)
    std_response_time = np.std(response_times)

    print(f"\nTotal Requests: {total_requests}")
    print(f"Hit Rate: {hit_rate:.2f}%")
    print(f"Miss Rate: {miss_rate:.2f}%")
    print(f"Average Response Time: {avg_response_time:.4f} seconds")
    print(f"Standard Deviation of Response Time: {std_response_time:.4f} seconds")

    # Mostrar recuento de peticiones por partición
    partition_df = create_partition_df(partition_requests)
    print("\nRecuento de peticiones por partición:")
    print(partition_df)

    # Generar gráficos
    generate_graphs(hit_rate, miss_rate, response_times, partition_requests)

# Función para crear un DataFrame de las peticiones por partición
def create_partition_df(partition_requests):
    partitions = list(partition_requests.keys())
    requests_per_partition = list(partition_requests.values())
    total_requests = sum(requests_per_partition)

    if total_requests == 0:
        return None

    percentages = [(req / total_requests) * 100 for req in requests_per_partition]
    return {"Partition": partitions, "Requests": requests_per_partition, "Percentage": percentages}

# Función para generar gráficos
def generate_graphs(hit_rate, miss_rate, response_times, partition_requests):
    # Gráfico de hit/miss rate
    labels = ['Hits', 'Misses']
    sizes = [hit_rate, miss_rate]
    colors = ['#66b3ff', '#ff6666']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Asegura que el gráfico sea un círculo
    plt.title("Hit vs Miss Rate")
    plt.show()

    # Gráfico de peticiones por partición
    partitions = list(partition_requests.keys())
    requests_per_partition = list(partition_requests.values())

    if sum(requests_per_partition) == 0:
        print("No requests were made to any partition. Skipping graph generation.")
        return

    plt.figure(figsize=(8, 6))
    plt.bar(partitions, requests_per_partition, color='skyblue')
    plt.xlabel("Particiones")
    plt.ylabel("Número de Peticiones")
    plt.title("Peticiones por Partición")
    plt.show()

if __name__ == "__main__":
    api_url = "http://localhost:5000"
    dataset_path = "./dataset.csv"
    generate_traffic(api_url, dataset_path, iterations=2)
