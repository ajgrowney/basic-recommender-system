CREATE USER activity_ingest_svc WITH PASSWORD 'basic_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public to activity_ingest_svc;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to activity_ingest_svc;