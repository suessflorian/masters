# Parsing `ls` Output
For your convenience we keep everything dockerized to avoid any system requirement discrepency issues.

## Building the `csv` file for the database
```sh
awk '/:$/{gsub(":",""); dir=$0; next} $9{print $9 "," dir "," $5 "," $6 " " $7 "," $8}' ls_output.txt > ./data/intermediate.csv
docker compose up date_processor --build --detach
cat ./data/intermediate.csv | docker compose exec -i date_processor ./processDate > ./data/files.csv
```

## Database to ingest this generated csv
```sh
docker compose up db --build --detach
docker-compose exec db /bin/sh -c "(echo '.mode csv' && echo '.import /data/files.csv files') | sqlite3 /data/files.db"
```

Now one can begin an interactive shell
```
docker-compose exec db sqlite3 /data/files.db
```
