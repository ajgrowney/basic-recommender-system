ai-build:
	docker build -t activity-ingest:latest -f ./apps/activity_ingest/Dockerfile  .	
ai-deploy:
	kubectl apply -f manifests/ingest.yaml
ai-re:
	kubectl rollout restart deploy activity-ingest
