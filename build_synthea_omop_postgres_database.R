#!/usr/bin/env Rscript


#	The intention of this was to test in addition to the Eunomia database
#	but its kinda diverged away from AI and more with OHDSI


devtools::install_github("OHDSI/ETL-Synthea")

library(ETLSyntheaBuilder)

# We are loading a version 5.4 CDM into a local PostgreSQL database called "synthea10".
# The ETLSyntheaBuilder package leverages the OHDSI/CommonDataModel package for CDM creation.
# Valid CDM versions are determined by executing CommonDataModel::listSupportedVersions().
# The strings representing supported CDM versions are currently "5.3" and "5.4". 
# The Synthea version we use in this example is 2.7.0.
# However, at this time we also support 3.0.0, 3.1.0, 3.2.0 and 3.3.0.
# Please note that Synthea's MASTER branch is always active and this package will be updated to support
# future versions as possible.
# The schema to load the Synthea tables is called "native".
# The schema to load the Vocabulary and CDM tables is "cdm_synthea10".  
# The username and pw are "postgres" and "lollipop".
# The Synthea and Vocabulary CSV files are located in /tmp/synthea/output/csv and /tmp/Vocabulary_20181119, respectively.

# For those interested in seeing the CDM changes from 5.3 to 5.4, please see: http://ohdsi.github.io/CommonDataModel/cdm54Changes.html



#	#	Download the data. This includes json, xml and csv. Just using the csv here.
#	#	https://synthea.mitre.org/downloads
#	#	SyntheticMass Data, Version 2 (24 May, 2017): 21GB. FHIR 3.0.1, CSV, C-CDA
#	#	https://mitre.box.com/shared/static/3bo45m48ocpzp8fc0tp005vax7l93xji.gz
#
#	#	Extract the internal 12 output_*.tar.gz files ...
#	tar xvfz synthea_1m_fhir_3_0_May_24.tar.gz
#
#	#	Extract just the csv data ...
#	for f in output_*; do echo $f; tar xvfz $f \*/csv/ ; done
#
#	#	Make a couple corrections ...
#	for d in output_*/csv; do
#	echo $d
#	#	Need to change DATE to START and STOP in the header of encounters.csv and procedures.csv
#	mv ${d}/procedures.csv ${d}/procedures.original ; awk 'BEGIN{FS=OFS=","}{print $1,$1,$2,$3,$4,$5,$6,$7}' ${d}/procedures.original > ${d}/procedures.csv
#	sed -i '' '1s/DATE,DATE/START,STOP/' ${d}/procedures.csv
#	mv ${d}/encounters.csv ${d}/encounters.original ; awk 'BEGIN{FS=OFS=","}{print $1,$2,$2,$3,$4,$5,$6,$7}' ${d}/encounters.original > ${d}/encounters.csv
#	sed -i '' '1s/DATE,DATE/START,STOP/' ${d}/encounters.csv
#	#	patients.csv files are all "corrupt" need to select only those records with 17 fields.
#	mv ${d}/patients.csv ${d}/patients.original ; awk -F, '(NF==17){print}' ${d}/patients.original > ${d}/patients.csv 
#	done


#	#	Download vocab files.
#	Where to get vocab Files?
#	Need to create a user 
#	https://athena.ohdsi.org/vocabulary/download-history
#	There are many different sets of data.
#	Its not clear how many or which are actually needed.
#	#	Unzip the downloaded file ...
#	unzip vocabulary_download_v5_{4cb70d34-c931-4018-9198-99afa4d0bace}_1760570025269.zip
#	#	Rename and/or move the folder to whereever it is needed


#	#	Prepare the receiving postgres database ...
#	/opt/local/lib/postgresql17/bin/psql -U postgres
#	CREATE DATABASE synthea10;
#	\c synthea10;
#	CREATE SCHEMA cdm_synthea10;
#	CREATE SCHEMA native;




#	DatabaseConnector::downloadJdbcDrivers("postgresql",pathToDriver="~/Downloads/")

cd <- DatabaseConnector::createConnectionDetails(
  dbms     = "postgresql", 
  server   = "localhost/synthea10", 
  user     = "postgres", 
  password = "", 
  port     = 5432,
  pathToDriver = "~/Downloads/"
)

cdmSchema      <- "cdm_synthea10"
cdmVersion     <- "5.4"
syntheaVersion <- "3.0.0"
syntheaSchema  <- "native"
vocabFileLoc   <- "~/Downloads/synthea_1m_fhir_3_0_May_24/vocabulary_download_v5"

ETLSyntheaBuilder::CreateCDMTables(connectionDetails = cd, cdmSchema = cdmSchema, cdmVersion = cdmVersion)

ETLSyntheaBuilder::CreateSyntheaTables(connectionDetails = cd, syntheaSchema = syntheaSchema, syntheaVersion = syntheaVersion)

ETLSyntheaBuilder::LoadVocabFromCsv(connectionDetails = cd, cdmSchema = cdmSchema, vocabFileLoc = vocabFileLoc)

#	Should correct this function call ... ? They appear to be just warnings.
#	1: `type_convert()` only converts columns of type 'character'.
#	- `df` has no columns of type 'character' 
#	2: In data.table::fread(file = paste0(vocabFileLoc, "/", csv), stringsAsFactors = FALSE,  :
#	  Found and resolved improper quoting out-of-sample. First healed line 51465: <<44833612	"ventilation" pneumonit	4180186>>. If the fields are not quoted (e.g. field separator does not appear within any field), try quote="" to avoid this warning.
#	3: In data.table::fread(file = paste0(vocabFileLoc, "/", csv), stringsAsFactors = FALSE,  :
#	  Found and resolved improper quoting out-of-sample. First healed line 9139: <<44829276	"Light-for-dates" without mention of fetal malnutrition, unspecified [weight]	Condition	ICD9CM	5-dig billing code		764.00	19700101	20991231	>>. If the fields are not quoted (e.g. field separator does not appear within any field), try quote="" to avoid this warning.
#	4: `type_convert()` only converts columns of type 'character'.
#	- `df` has no columns of type 'character' 




syntheaFileLocs <- c(
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_1/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_2/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_3/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_4/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_5/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_6/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_7/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_8/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_9/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_10/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_11/csv",
"~/Downloads/synthea_1m_fhir_3_0_May_24/output_12/csv"
)
#syntheaFileLoc <- "~/Downloads/synthea_1m_fhir_3_0_May_24/output_1/csv"


#	Do this one more time, but loop over all synthea dirs
for( syntheaFileLoc in syntheaFileLocs ){
	print(syntheaFileLoc)
	ETLSyntheaBuilder::LoadSyntheaTables(connectionDetails = cd, syntheaSchema = syntheaSchema, syntheaFileLoc = syntheaFileLoc)
}

ETLSyntheaBuilder::CreateMapAndRollupTables(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, cdmVersion = cdmVersion, syntheaVersion = syntheaVersion)

## Optional Step to create extra indices
ETLSyntheaBuilder::CreateExtraIndices(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, syntheaVersion = syntheaVersion)

ETLSyntheaBuilder::LoadEventTables(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, cdmVersion = cdmVersion, syntheaVersion = syntheaVersion)




#	Move this to a different server

#	IF VERSIONS ARE SYNCHRONIZED OR THE TARGET IS NEWER




#	#	SHOULD use -Fc option. This creates a .backup file
#	#	which is compressed, binary, and can be used with pgAdmin -> Restore
#	#	sudo port load postgresql17-server
#	pg_dump -U postgres -d synthea -Fc -C -f synthea10.backup
#	#	sudo port unload postgresql17-server
#	#	Much smaller
#	#	-r--r--r--   1 jake  staff  30244418805 Oct 16 16:38 synthea10.sql
#	#	-rw-r--r--   1 jake  staff   4048907542 Oct 16 20:32 synthea10.backup


#	This only works if the versions are close to synchronized. Going from 17.6 to 15.2 won't work.
#	Need to stick the SQL style dump.
#	docker cp synthea10.backup broadsea-atlasdb:/synthea10.backup
#	docker ps -a
#	817c40d616f3   ohdsi/broadsea-atlasdb:2.1.0-secret
#	docker exec -it 817c40d616f3 /bin/sh
#	pg_restore -U postgres -d synthea -f /synthea10.backup
#	pg_restore -U postgres --clean --create -d synthea /synthea10.backup


#	#	MUST then use pg_restore
#	pg_restore -U postgres --clean --create -d synthea synthea10.backup


#	OTHERWISE DUMP TO SQL

#	/opt/local/lib/postgresql17/bin/pg_dump -U postgres -d synthea10 -f synthea10.sql
#	-rw-r--r--  1 jake  staff  30244418799 Oct 16 07:40 synthea10.sql


#	docker cp synthea10.sql broadsea-atlasdb:/synthea10.sql
#	
#	docker ps -a
#	97daf8a059da   ohdsi/broadsea-atlasdb:2.1.0-secret
#	docker exec -it 97daf8a059da /bin/sh
#	psql -U postgres -d synthea -f /synthea10.sql









# NOTE pgadmin is run on one container, but postgres is actually being run on the atlasdb container


#	Make it visible to atlas

#	there also may be some version differences here

#	From pgadmin / postgres Tools > Query Tool
#	
#	INSERT INTO webapi.source (source_id, source_name, source_key, source_connection, source_dialect)
#	VALUES (
#	    2,
#	    'Synthea CDM',
#	    'SYNTHEA',
#	    'jdbc:postgresql://broadsea-atlasdb:5432/synthea?user=postgres&password=mypass',
#	    'postgresql'
#	);
#	
#	INSERT INTO webapi.source_daimon (source_daimon_id, source_id, daimon_type, table_qualifier, priority)
#	VALUES
#	    (4, 2, 0, 'cdm_synthea10', 0),   -- CDM schema
#	    (5, 2, 1, 'cdm_synthea10', 0),   -- Vocabulary schema (same for Synthea)
#	    (6, 2, 2, 'results_synthea10', 0); -- Results schema (create this if missing)
#	
#	
#	From pgadmin / synthea Tools > Query Tool
#	
#	CREATE SCHEMA results_synthea10;
#	#CREATE SCHEMA results_synthea10 AUTHORIZATION postgres; - perhaps ?




#	Now seeing that there are no achilles reports

#	HADES (Rstudio)

#	R doesn't install these to persist

#	install.packages("remotes")  # if not already installed
#	remotes::install_github("OHDSI/Achilles")
#	
#	library(DatabaseConnector)
#	library(Achilles)
#	
#	
#	connectionDetails <- DatabaseConnector::createConnectionDetails(
#	  dbms = "postgresql",
#	  server = "broadsea-atlasdb/synthea",
#	  user = "postgres",
#	  password = "mypass",
#	  port = 5432
#	)
#	
#	
#	
#	
#
#	analysisDetails <- getAnalysisDetails()
#	> dim(analysisDetails)
#	[1] 294  11
#	> max(analysisDetails$analysis_id)
#	[1] 2201
#
#	#	create all of the reports

achilles(
	connectionDetails,
	cdmDatabaseSchema = "cdm_synthea10",
	resultsDatabaseSchema = "results_synthea10",
	vocabDatabaseSchema = "cdm_synthea10",
	numThreads = 2,
	sourceName = "Synthea CDM",
	cdmVersion = "5.4"
)
#	analysisIds = c(101, 102, 103) # Replace with your desired analysis IDs


#	# takes quite a while
#	
#	
#	org.postgresql.util.PSQLException: ERROR: relation "results_synthea10.achilles_results" does not exist


DO $$
DECLARE
	r RECORD;
BEGIN
	FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'results_synthea10' AND tablename LIKE 'tmp%') LOOP
		EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident('results_synthea10') || '.' || quote_ident(r.tablename) || ' CASCADE';
	END LOOP;
END $$;


CREATE TABLE IF NOT EXISTS results_synthea10.achilles_results
(
	analysis_id integer,
	stratum_1 character varying COLLATE pg_catalog."default",
	stratum_2 character varying COLLATE pg_catalog."default",
	stratum_3 character varying COLLATE pg_catalog."default",
	stratum_4 character varying COLLATE pg_catalog."default",
	stratum_5 character varying COLLATE pg_catalog."default",
	count_value bigint
)

#	
#	
#	An error report has been created at  output/errorReportR.txt
#	Connected to your session in progress, last started 2025-Oct-18 03:14:07 UTC (1 hour ago)
#	Error in `.createErrorReport()`:
#	! Error executing SQL:
#	org.postgresql.util.PSQLException: ERROR: relation "results_synthea10.achilles_results" does not exist
#	An error report has been created at  /home/ohdsi/errorReportSql.txt
#	Run `rlang::last_error()` to see where the error occurred.
#	An error occurred while the 'DatabaseConnector' package was updating the RStudio Connections pane:
#	Error in NULL: host must be a single element of type 'character'
#	If necessary, these warnings can be squelched by setting `options(rstudio.connectionObserver.errorsSuppressed = TRUE)`.
#	> 
#	
#	gonna try to reset the content page and reset the results schema
#	
#	
#	
#	
#	
#	
#	
#	remotes::install_github("OHDSI/DataQualityDashboard")
#	#	fails install
#	
#	library(DataQualityDashboard)
#	
#	executeDqChecks(
#	  connectionDetails = connectionDetails,
#	  cdmDatabaseSchema = "cdm_synthea10",
#	  resultsDatabaseSchema = "results_synthea10",
#	  vocabDatabaseSchema = "cdm_synthea10",
#	  outputFolder = "output",
#	  checkLevel = "TABLE",
#	  numThreads = 2,
#	  sqlOnly = FALSE,
#	  verboseMode = TRUE,
#	  cdmVersion = "5.4"
#	)

