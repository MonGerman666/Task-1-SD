# Task 1: Scaling Distributed Systems using Direct and Indirect Communication Middleware

## Descripció del Projecte
Aquest projecte té com a objectiu implementar dos serveis distribuïts escalables:
- **InsultService:** rep insults remotament, els emmagatzema (sense duplicats) i ofereix un broadcaster que publica un insult aleatori cada 5 segons.
- **InsultFilter:** rep textos, filtra els insults substituint-los per "CENSORED" i emmagatzema els textos filtrats.

Aquests serveis es desenvoluparan utilitzant quatre tecnologies de middleware:
- **XMLRPC**
- **PyRO**
- **Redis**
- **RabbitMQ**

A més, es realitzaran proves de rendiment en tres escenaris:
- **Single Node:** stress test per mesurar el nombre de peticions processades.
- **Escalat Estàtic:** proves amb 1, 2 i 3 nodes per calcular el speedup.
- **Escalat Dinàmic:** implementació d'un mecanisme d'escalat basat en la càrrega (usant Python multiprocessing).

## Estructura de Carpetes
La estructura del projecte és la següent:
Task1/ ├── README.md ├── requirements.txt ├── xmlrpc/ │ ├── insult_service_xmlrpc.py │ └── client_insult_service_xmlrpc.py ├── pyro/ │ ├── insult_service_pyro.py │ └── client_insult_service_pyro.py ├── redis/ │ ├── insult_service_redis.py │ └── client_insult_service_redis.py ├── rabbitmq/ │ ├── insult_service_rabbitmq.py │ └── client_insult_service_rabbitmq.py └── docs/ └── informe.pdf (documentació, diagrames, i resultats experimentals)
