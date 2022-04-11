
-- make sure the column value is between two values inclusive.

{% test column_between_values_incl(model, column_name, low, high) %}

    select *
    from {{ model }}
    where {{ column_name }} > {{ high }}
    and {{ column_name }} > {{ low }}

{% endtest %}
