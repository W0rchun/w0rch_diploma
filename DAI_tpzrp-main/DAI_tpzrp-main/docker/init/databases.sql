DROP DATABASE IF EXISTS db_organizations;
CREATE DATABASE db_organizations;
DROP DATABASE IF EXISTS db_org_management;
CREATE DATABASE db_org_management;
DROP DATABASE IF EXISTS authentificate_db;
CREATE DATABASE authentificate_db;
DROP DATABASE IF EXISTS db_appointments;
CREATE DATABASE db_appointments;
DROP DATABASE IF EXISTS db_catalog;
CREATE DATABASE db_catalog;
DROP DATABASE IF EXISTS db_patient_service;
CREATE DATABASE db_patient_service;
DROP DATABASE IF EXISTS auth_db;
CREATE DATABASE auth_db;

CREATE USER root WITH PASSWORD 'pass';
ALTER ROLE root WITH SUPERUSER;

GRANT pg_read_all_data TO root;
GRANT pg_write_all_data TO root;

ALTER DATABASE db_organizations OWNER TO root;
ALTER DATABASE db_org_management OWNER TO root;
ALTER DATABASE authentificate_db OWNER TO root;
ALTER DATABASE db_appointments OWNER TO root;
ALTER DATABASE db_catalog OWNER TO root;
ALTER DATABASE db_patient_service OWNER TO root;
ALTER DATABASE auth_db OWNER TO root;
