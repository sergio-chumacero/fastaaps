docker network create aapsnetwork # Crea red interna entre contenedores Docker
docker volume create sheets       # Crea directorio compartido para planillas
touch /var/acme.json              # Crea archivo para certificados TLS
chmod 600 /var/acme.json          # Aplica los permisos adecuados 