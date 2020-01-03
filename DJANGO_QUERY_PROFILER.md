This is a good article to learn about [Select & Prefetch related](https://medium.com/@lucasmagnum/djangotip-select-prefetch-related-e76b683aa457)

We are going to follow the article, and run the queries and see how django_query_profiler can be:
1. Used on a command line
2. Help with debugging issues like this


Before you run this query, run the below on command line to have some seed data

```bash
make setup;
make tests;
python app/manage.py load_products
```

* List of products

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel
from products.queries import products_list

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    products_list()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 500,
  "total_query_execution_time_in_micros": 21171,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 500,
  "SELECT": 501,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```

* List of products - more detailed output from django_query_profiler

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel
from products.queries import products_list

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    products_list()

for query_signature, query_signature_statistics in qp.query_profiled_data.query_signature_to_query_signature_statistics.items():
    print(query_signature_statistics)
    print('\n')
    print(query_signature.query_without_params)
    print(query_signature.analysis)
    print('==' * 80)
```

```
SELECT "products_product"."id", "products_product"."title", "products_product"."category_id" FROM "products_product"
QuerySignatureAnalyzeResult.UNKNOWN
================================================================================================================================================================
QuerySignatureStatistics(frequency=500, query_execution_time_in_micros=20807, db_row_count=None)


SELECT "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category" WHERE "products_category"."id" = %s
QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED
================================================================================================================================================================
```

* Select related

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import products_list_select_related

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    products_list_select_related()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 0,
  "total_query_execution_time_in_micros": 149,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 0,
  "SELECT": 1,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```


* List of categories

###### see the summary first

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import categories_list

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 0,
  "total_query_execution_time_in_micros": 3098,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 50,
  "SELECT": 51,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```

###### Investigate more with analysis

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel
from products.queries import categories_list

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list()

for query_signature, query_signature_statistics in qp.query_profiled_data.query_signature_to_query_signature_statistics.items():
    print(query_signature_statistics)
    print('\n')
    print(query_signature.query_without_params)
    print(query_signature.analysis)
    print('==' * 80)
```

```
QuerySignatureStatistics(frequency=1, query_execution_time_in_micros=115, db_row_count=None)


SELECT "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category"
QuerySignatureAnalyzeResult.UNKNOWN
================================================================================================================================================================
QuerySignatureStatistics(frequency=50, query_execution_time_in_micros=3313, db_row_count=None)


SELECT "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category" INNER JOIN "products_category_subcategories" ON ("products_category"."id" = "products_category_subcategories"."to_category_id") WHERE "products_category_subcategories"."from_category_id" = %s
QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED
================================================================================================================================================================
```

* Prefetch related

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import categories_list_prefetch_related

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list_prefetch_related()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 0,
  "total_query_execution_time_in_micros": 505,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 0,
  "SELECT": 2,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```

* filter with prefetch_related


```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import categories_list_active_subcategories

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list_active_subcategories()

for query_signature, query_signature_statistics in qp.query_profiled_data.query_signature_to_query_signature_statistics.items():
    print(query_signature_statistics)
    print('\n')
    print(query_signature.query_without_params)
    print(query_signature.analysis)
    print('==' * 80)
```

```
QuerySignatureStatistics(frequency=1, query_execution_time_in_micros=109, db_row_count=None)
SELECT "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category"
QuerySignatureAnalyzeResult.UNKNOWN

================================================================================================================================================================

QuerySignatureStatistics(frequency=1, query_execution_time_in_micros=175, db_row_count=None)
SELECT ("products_category_subcategories"."from_category_id") AS "_prefetch_related_val_from_category_id", "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category" INNER JOIN "products_category_subcategories" ON ("products_category"."id" = "products_category_subcategories"."to_category_id") WHERE "products_category_subcategories"."from_category_id" IN (%s)
QuerySignatureAnalyzeResult.PREFETCHED_RELATED

================================================================================================================================================================
QuerySignatureStatistics(frequency=50, query_execution_time_in_micros=3047, db_row_count=None)
SELECT "products_category"."id", "products_category"."name", "products_category"."is_active" FROM "products_category" INNER JOIN "products_category_subcategories" ON ("products_category"."id" = "products_category_subcategories"."to_category_id") WHERE ("products_category_subcategories"."from_category_id" = %s AND "products_category"."is_active" = %s)
QuerySignatureAnalyzeResult.FILTER
================================================================================================================================================================
```

* Using Prefetch with to_attr

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import categories_list_active_subcategories_using_prefetch_attr

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list_active_subcategories_using_prefetch_attr()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 0,
  "total_query_execution_time_in_micros": 248,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 0,
  "SELECT": 2,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```

* Using Prefetch without to_attr

```python
from django_query_profiler.client.context_manager import QueryProfiler
from django_query_profiler.query_profiler_storage import QueryProfilerLevel

from products.queries import categories_list_active_subcategories_using_prefetch_queryset

with QueryProfiler(QueryProfilerLevel.QUERY_SIGNATURE) as qp:
    categories_list_active_subcategories_using_prefetch_queryset()

print(qp.query_profiled_data.summary)
```

```json
{
  "exact_query_duplicates": 0,
  "total_query_execution_time_in_micros": 412,
  "total_db_row_count": null,
  "potential_n_plus1_query_count": 0,
  "SELECT": 2,
  "INSERT": 0,
  "UPDATE": 0,
  "DELETE": 0,
  "TRANSACTIONALS": 0,
  "OTHER": 0
}
```
