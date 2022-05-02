This is an overview of what my 'Smoll data stack' is actually delivering.

The dbt project is run every night (for dbt models with a daily tag)
and weekly (for dbt models with weekly tag)

At moment of writing there is one raw table, a staging daily values dbtmodel and a daily dbtmodel
![lineageoverview](images/lineage_graph.png)

![dbt overview](images/dbt_overview.png)

This is the normal stg_current_weather sql
![](images/stg_current_weather.png)

and this the compiled sql
![](images/stg_current_weather_compiled.png)



### writing recipes to calendar
The job write recipes to calendar works on my computer.


![](images/calendar_filled_in.png)

All recipes:
![source sheet](images/recipe_all.png)

Selection for this week
![this week selection of meals](images/recipe_fill_in.png)


Future improvements:
Suggest recipes automatically
