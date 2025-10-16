#!/usr/bin/env Rscript

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


#	/opt/local/lib/postgresql17/bin/pg_dump -U postgres -d synthea10 -f sourcedb.sql
#	-rw-r--r--  1 jake  staff  30244418799 Oct 16 07:40 sourcedb.sql

