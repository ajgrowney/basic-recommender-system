kubectl get secret psql-local-postgresql -o jsonpath="{.data.postgres-password}" | base64 --decode | clip.exe