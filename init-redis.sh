#!/bin/bash

# Esperar a que Redis esté en funcionamiento
until redis-cli -h redis1 -p 6379 ping | grep -q "PONG"; do
  echo "Esperando a que Redis1 esté listo..."
  sleep 2
done

echo "Redis está listo. Aplicando configuraciones..."

# Asignar límite de memoria y política de remoción
redis-cli -h redis1 -p 6379 CONFIG SET maxmemory 2mb
redis-cli -h redis1 -p 6379 CONFIG SET maxmemory-policy allkeys-lru

echo "Configuraciones aplicadas exitosamente."

until redis-cli -h redis2 -p 6379 ping | grep -q "PONG"; do
  echo "Esperando a que Redis2 esté listo..."
  sleep 2
done

echo "Redis está listo. Aplicando configuraciones..."

redis-cli -h redis2 -p 6379 CONFIG SET maxmemory 2mb
redis-cli -h redis2 -p 6379 CONFIG SET maxmemory-policy allkeys-lru

until redis-cli -h redis3 -p 6379 ping | grep -q "PONG"; do
  echo "Esperando a que Redis3 esté listo..."
  sleep 2
done

echo "Redis está listo. Aplicando configuraciones..."

redis-cli -h redis3 -p 6379 CONFIG SET maxmemory 2mb
redis-cli -h redis3 -p 6379 CONFIG SET maxmemory-policy allkeys-lru

until redis-cli -h redis4 -p 6379 ping | grep -q "PONG"; do
  echo "Esperando a que Redis4 esté listo..."
  sleep 2
done

echo "Redis está listo. Aplicando configuraciones..."

redis-cli -h redis4 -p 6379 CONFIG SET maxmemory 2mb
redis-cli -h redis4 -p 6379 CONFIG SET maxmemory-policy allkeys-lru
#
#until redis-cli -h redis5 -p 6379 ping | grep -q "PONG"; do
#  echo "Esperando a que Redis5 esté listo..."
#  sleep 2
#done
#
#echo "Redis está listo. Aplicando configuraciones..."
#
#redis-cli -h redis5 -p 6379 CONFIG SET maxmemory 2mb
#redis-cli -h redis5 -p 6379 CONFIG SET maxmemory-policy allkeys-lru
#
#until redis-cli -h redis6 -p 6379 ping | grep -q "PONG"; do
#  echo "Esperando a que Redis6 esté listo..."
#  sleep 2
#done
#
#echo "Redis está listo. Aplicando configuraciones..."
#
#redis-cli -h redis6 -p 6379 CONFIG SET maxmemory 2mb
#redis-cli -h redis6 -p 6379 CONFIG SET maxmemory-policy allkeys-lru
#
#until redis-cli -h redis7 -p 6379 ping | grep -q "PONG"; do
#  echo "Esperando a que Redis7 esté listo..."
#  sleep 2
#done
#
#echo "Redis está listo. Aplicando configuraciones..."
#
#redis-cli -h redis7 -p 6379 CONFIG SET maxmemory 2mb
#redis-cli -h redis7 -p 6379 CONFIG SET maxmemory-policy allkeys-lru
#
#until redis-cli -h redis8 -p 6379 ping | grep -q "PONG"; do
#  echo "Esperando a que Redis8 esté listo..."
#  sleep 2
#done
#
#echo "Redis está listo. Aplicando configuraciones..."
#
#redis-cli -h redis8 -p 6379 CONFIG SET maxmemory 2mb
#redis-cli -h redis8 -p 6379 CONFIG SET maxmemory-policy allkeys-lru
