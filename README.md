# Recommender System
Goal: Basic intro to building an end-to-end recommendation system

## System Architecture
### PostgreSQL
`helm install psql-local bitnami/postgresql --set persistence.existingClaim=postgresql-pv-claim --set volumePermissions.enable=true`

### RabbitMQ
https://github.com/bitnami/charts/tree/master/bitnami/rabbitmq/#installing-the-chart

RabbitMQ can be accessed within the cluster on port 5672 at recommender-mq-rabbitmq.default.svc.cluster.local
#### Setup
Username: user
Password: $(kubectl get secret --namespace default recommender-mq-rabbitmq -o jsonpath="{.data.rabbitmq-password}" | base64 -d)"
