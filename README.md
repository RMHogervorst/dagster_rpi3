# dagster on my local rpi3

This is a project to run dagster on my rpi3.

### the modern datastack
The 'modern data stack' is usually:

```
[E]                       [L]                 [T]
[extraction/ingestion]->[load in warehouse]->[transform in warehouse]

(bi on top of outer layers of transformation)
```

[Extraction / ingestion]:
- ingestion with fivetran, singer, stitch etc, or orchestration tool

[Load and transform]:
- a datawarehouse in the cloud like Bigquery, Snowflake, or Redshift
- or a datalake such as databricks, delta lake, or plain old s3

- data transformation with dbt, aided by airflow or another scheduler

[BI layer]:
- some sort of BI layer on top of the warehouse: looker, mode, tableau
- (optionally) ML capabilities somewhere too
- (optionally) data catalog & governance / lineage tracking


I'm not doing that, this project is the 'smoller data stack'[^2].


## Smoll data stack
![a mouse balancing on two wheat shoots](nick-fewings--dtKoaHpi9M-unsplash.jpg)
The Small, Minimal, Open, Low effort, Low power (SMOLL) datastack[^1], is
a pun with ambitions to grow into something larger, and more educational.
I wanted a cheap platform to work on improving my data engineering skills and
so I repurposed some hardware for this project. A raspberry pi 3 with ubuntu & a NAS that I've installed a postgres database into.

Goals:
- it should work similarly to the modern datastack
- it should be useful to me

[Extraction/ingestion]:
- use dagster for getting data and putting it into the database.

[Load and transform]:
- Postgres on my NAS can handle a lot of data
- So dagster pushes data to a raw_* table and dbt will build models[^3] _(which I will call dbt-models from now on)_ on top of that.

[BI layer]:
- I don't have a BI layer yet, I might make some reports later but I think most tools are too heavy on the rpi3.


### Modern data stack vs SMOLL data stack
- much better name 'Modern data stack' --> 'SMOLL data stack'
- cloud data warehouse (Bigquery, Snowflake) --> A postgres database on a NAS
- orchestration with airflow, prefect, dagster or argo --> dagster on rpi
- kubernetes deployment --> installation on a single raspberry pi
- dbt for transformations --> dbt for transformations
- looker / other BI tool --> 'nothing yet'

So it's very much the same except for the database, and I don't have a BI layer.


### Run the project locally

From the folder dagster_home run `dagit` and go to <http://localhost:3000> .
Run the dbt project `dbt run --profiles-dir .` # I put the profile setting in the same folder.

### Deployment
To be honest, I just move the stuff over from my macbook to the device.

### Settings
I've moved all of the secret information, or information I'm not comfortable
sharing with you in a .env file that lives in the root folder 'dagster_rpi3'


```
openweathermapapikey=
PG_DATABASE=
user=
password=
PG_HOST=
PG_PORT=
DBTUSER=
GEOlat=
GEOlon=
DBTPASSWORD=
NETLIFYBLOG=
NETLIFYNOTES=
```


## Abbreviations
- NAS: network attached Storage. in my case a synology machine.
- rpi3: [a raspberry pi 3b ](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)
- dbt: data build tool; an amazing piece of python code that generates sql and lineage information for you.

## Notes:
[^1]: I'm forcing some sort of backcronym here, I'm fun at parties as you can see.
[^2]: Smoll, as in small, but wrongly spelled, and so adorable. "I'm a smoll boy" says the puppy.
[^3]: I love everything about dbt, except their use of the word 'model', this becomes very confusing very fast when you are also doing machine learning with 'models'.
* picture of mouse by <a href="https://unsplash.com/@jannerboy62?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nick Fewings</a> on <a href="https://unsplash.com/s/photos/small-animal?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
