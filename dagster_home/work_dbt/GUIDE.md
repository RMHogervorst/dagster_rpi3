# Guide for dbt projects

Emily Riederer [wrote a nice post](https://emilyriederer.netlify.app/post/column-name-contracts/) about controlled vocabularies that I really like to follow.
She suggests using column names as contracts for what kind of data lives in the column.
I will not use all of her suggestions, and I will use it slightly different.


### Controlled vocabulary
I will use this Controlled vocabulary:

Units of measurement at the end:

- _ID: Unique identifier of entity with no other semantic meaning (test for Non-null)
- _N: Count of quantity or event occurrence, Always a non-negative integer (Test for Integer, Non-null, larger then 0)
- _DT: Date (Test for date_format YYYY-MM-DD)
- _at: Time stamp of some event (Always cast as a YYYY-MM-DD HH:MM:SS time stamp)
- _IND: Binary indicator (Test for Values of 0 or 1, Non-null)
- _PROP: Proportion (Test for Numeric, Bounded between 0 and 1)
- _PCT: Percent (test for between 0 and 100, but not always)
- _CAT: Categorical variable as a character string (potentially encoded from an ID field)
- _NM: human readable name


Descriptors:

    ACTL: Actual observed value
    PRED: Predicted value

## where goes what?
- raw data always lands in the raw_* table of the schema.
- Schema is named after the source. data from openweathermap lives in openweathermap.
- Always use the ref function when selecting from another dbtmodel
- We go from left to right, from raw (raw_), to staging (stg_) to mart
- marts can only reference other marts or staging dbtmodels

sql lives in folders:
```
work_dbt/
├── dbt_project.yml (1. contains settings)
├── models/
|   ├── {schemaname}/
|   |   ├── {schemaname}.yml (2. contains the metadata)
|   |   ├── staging/
|   |   |   ├── stg_{table/viewname}.sql
|   |   ├── marts/
|   |   |   ├── fct_{topic}.sql
|   |   |   ├── dim_{topic}.sql
```
Add tags to sources in {schemaname}.yml
Add tags to dbtmodels in dbt_project.yml (this is hierarchical, so in the example below the dbtmodel stg_daily_values has the tag 'daily' AND the tag 'weather').

```yaml
models:
  work_dbt:
    # Config indicated by + and applies to all files under models/example/
    openweathermap:
      +materialized: view
      +tags: weather
      +schema: openweathermap
      staging:
        stg_daily_values:
          +tags: "daily"
```

### Raw
Only ever select from raw_* tables. Raw tables are defined and described as source.
Renaming and further steps come further on.

### staging
- Select from only one source
- Rename fields and tables to fit the conventions you wish to use within your project, for example, ensuring all timestamps are named <event>_at.
- Recast fields into the correct data type, for example, changing dates into UTC and prices into euro amounts.
- All subsequent data models should be built on top of these models, reducing the amount of duplicated code.

### Macros & tests
Macros live under macros as sql files, and are documented in a schema.yml file.
- generate_schema_name is a modification of the dbt_core generate schema name so I always create the dbtmodels in the schema that is defined in the dbt_project.yml. (I work alone and so I don't need the experimental room that dbt offers with custom schemas)

Generic tests live under tests/generic/ (can also live under macros).
- test_column_between_values_incl tests if a column is between two values
