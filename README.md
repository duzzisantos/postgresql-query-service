# PostgreSQL Query Service

This service performs common DML operations in PostgreSQL
using custom query builders which interact with your database and return
desired data.

## Use

1. Query Builders are called inside routes directly to avoid deeply passing connection properties
2. Routes include:

- connection verification
- joiners
- mutators
- general select statements
- specific select statements

3. Test/verify that you are rightly connected to your postgresql network and run **docker compose up --build -d**
4. Read fuller API documentation and test through Swagger UI docs by visiting http://localhost:your-port/docs
5. Apply necessary request body for each route
6. Refer to .env.example file to see variables you may need to run this application
7. Run locally on terminal: uvicorn app.main:app --port 'your-port' --reload

## Connection Verification

This tests connection to your PostgreSQL server and returns a lightweight test query result. How do you connect? It's
simple: plug in your PostgreSQL connection string here if you are connecting from a cloud service:

```code
def get_connection():
    conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
    conn.autocommit = True
    return conn
```

For every database operation you would then consume the connection's cursor. For example:

```code
cursor = get_connection().cursor()
cursor.execute(my_parameterized_query_template, variables)
result = cursor.fetchone()
```

In alternative, you may provide database connection parameters this way if you have those credentials available:

```code
def get_connection():
    conn = psycopg2.connect(os.getenv(dbname=name, password=password, host=host, port=port ))
    conn.autocommit = True
    return conn
```

## Joiners

This includes queries for inner, right, left, and full joins. There is also a query template for checking if sub queries exist or not.

## Mutators

This set of queries lets you run various create, delete, and update statements. While creating new tables, make sure to include
data types and character limits for each column. These are to be provided as comma separated strings in the request body.

## General Select Statements

This set of queries help you run various general select statements

## Specific Select Statements

This allows you query tables to extract information for specific columns. With a crontab set - powered by Celery, you can schedule query downloads as CSV/Excel files fired to selected email addresses. It is up to you

## API Illustrations & Examples

<details>
<summary><strong>POST /GetAll</strong></summary>

<p>Gets all rows in a table based on table name</p>

```json
{
  "table": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllOrderBy</strong></summary>

<p>Gets all rows in a table based on table name and orders by a certain column</p>

```json
{
  "table": "example_string",
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllLimitAndOffset</strong></summary>

<p>Gets all rows in a table based on table name and sets a limit and offset</p>

```json
{
  "table": "string",
  "limit": 123,
  "offset": 123
}
```

</details>

<details>
<summary><strong>POST /GetAllWithLimit</strong></summary>

<p>Gets all rows in a table based on table name with specified limit.</p>

```json
{
  "table": "string",
  "limit": 123
}
```

</details>

<details>
<summary><strong>POST /GetAllWhere</strong></summary>

<p>Gets all rows in a table based on table name and columns that match the value of the WHERE clause. 
Conditions are parameters plugged into to query's WHERE clauses.
</p>

```json
{
  "table": "string",
  "conditions": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereOrderBy</strong></summary>

<p>Gets all rows in a table based on table name and columns that match the value of the WHERE clause. 
Conditions are parameters plugged into to query's WHERE clauses. Additionally, you could order by specified column.
</p>

```json
{
  "table": "string",
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllBetween</strong></summary>

<p>Gets all rows in a table and specifies starting and end rows where result must be produced from.
</p>

```json
{
  "table": "string",
  "column": "example_string",
  "start": "example_string",
  "end": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereMatches</strong></summary>
<p>Gets all rows in a table based on table name and where column value matches specific wild card. Wild cards could be in from of "%A%" (contains 'A'), "en%" (starts with 'en'), and what have you:

</p>

```json
{
  "table": "string",
  "column": "example_string",
  "wild_card": "example"
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereIn</strong></summary>
<p>Gets all data from based on WHERE search parameters could be found in column.</p>

```json
{
  "column": "example_string",
  "search_parameters": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereAndCount</strong></summary>
<p>Gets data from based on WHERE clauses from two columns and counts matching query.</p>

```json
{
  "primary_column": "example_string",
  "secondary_column": "example_string",
  "search_parameter": "example"
}
```

</details>

<details> <summary><strong>POST /GetAllWhereAverage</strong></summary> <p>Gets aggregated average for a column with optional search parameters (search_parameters may be an array, a single string, or an integer). Example shows an array.</p>

```json
{
    "table": "string",
    "column": "string",
    "search_parameters": ["string"] or "string" or 123
}
```

</details>

 <details> <summary><strong>POST /GetAllGroupBy</strong></summary> <p>Groups results by primary and secondary columns for a given table.</p>

```json
{
  "table": "example_string",
  "primary_column": "example_string",
  "secondary_column": "example_string"
}
```

</details>

 <details> <summary><strong>POST /GetByColumns</strong></summary> <p>Selects only the provided columns from a table.</p>

```json
{
  "table": "example_string",
  "columns": ["example_string"]
}
```

</details>

<details> <summary><strong>POST /GetByColumnsAndOrder</strong></summary> <p>Selects given columns from a table and orders the result.</p>

```json
{
  "table": "example_string",
  "columns": ["example_string"],
  "order": "created_at DESC"
}
```

</details>

 <details> <summary><strong>POST /GetByColumnsAndLimit</strong></summary> <p>Selects specified columns from a table and limits the number of results.</p>

```json
{
  "table": "example_string",
  "columns": ["example_string"],
  "limit": 100
}
```

</details>

 <details> <summary><strong>POST /GetTableJoin</strong></summary> <p>Join two tables on a common key and return the specified columns.</p>

```json
{
  "columns": ["example_string"],
  "primary_table": "example_string",
  "secondary_table": "example_string",
  "common_key": "example_string"
}
```

</details>

<details> <summary><strong>POST /SubQueryExists</strong></summary> <p>Runs a subquery check using EXISTS and returns rows where the subquery condition is satisfied.</p>

```json
{
  "primary_column": "example_string",
  "primary_table": "example_string",
  "sub_query_select": "example_string",
  "sub_query_table": "example_string",
  "sub_query_where_column": "example_string",
  "sub_query_where_value": "example_string"
}
```

</details>

<details> <summary><strong>POST /CreateRow</strong></summary> <p>Inserts a single row into a table. `columns` and `values` must align by index.</p>

```json
{
  "columns": ["example_string"],
  "table": "example_string",
  "values": ["example"]
}
```

</details>

<details> <summary><strong>POST /CreateMany</strong></summary> <p>Inserts multiple rows into a table. Each entry in `values` is a row (list) matching `columns`.</p>

```json
{
  "table": "users",
  "columns": ["name", "email", "age"],
  "values": [
    ["Jane Doe", "jane@example.com", 29],
    ["John Smith", "john@example.com", 35]
  ]
}
```

</details>

<details>
<summary><strong>POST /DeleteRow</strong></summary>

```json
{
  "table": "example_string",
  "id": "example",
  "primary_column": "example_string"
}
```

</details>

<details> <summary><strong>POST /DeleteRow</strong></summary> <p>Deletes a single row identified by `id` and `primary_column` from `table`.</p>

```json
{
  {
  "table": "users",
  "id": 123,
}
}
```

</details>

<details>
<summary><strong>POST /DeleteByParams</strong></summary>

```json
{
  "conditions": ["example_string"]
}
```

</details>

 <details> <summary><strong>POST /DeleteByParams</strong></summary> <p>Deletes rows matching the provided conditions. Conditions should be provided in the format expected by your query builder (e.g. `"status = 'inactive'"`).</p>

```json
{
  "table": "example_string",
  "primary_column": "example_string",
  "set_value": "example_string",
  "secondary_column": "example_string",
  "where_value": "example_string"
}
```

</details>

<details> <summary><strong>POST /UpdateRow</strong></summary> <p>Updates a single row. Use `primary_column` when applicable; `set_value` is applied to `secondary_column` where `where_value` matches.</p>

```json
{
  "table": "example_string",
  "set_columns": ["example_string"],
  "set_values": ["example"],
  "where_value": "example",
  "where_column": "example_string"
}
```

</details>

<details> <summary><strong>POST /UpdateMany</strong></summary> <p>Updates many rows using parallel `set_columns` / `set_values`. `where_column` and `where_value` determine rows to update.</p>

```json
{
  "table": "users",
  "set_columns": ["status", "updated_at"],
  "set_values": ["active", "2024-01-01"],
  "where_column": "country",
  "where_value": "USA"
}
```

</details>

<details> <summary><strong>POST /CreateTable</strong></summary> <p>Creates a new table with column definitions supplied as comma-separated property strings.</p>

```json
{
  "table_name": "new_table",
  "column_names_with_properties": [
    "id SERIAL PRIMARY KEY",
    "name VARCHAR(255) NOT NULL",
    "email VARCHAR(255) UNIQUE",
    "created_at TIMESTAMP DEFAULT now()"
  ]
}
```

</details>

<details> <summary><strong>POST /QueryDownload</strong></summary> <p>Run a query and email the resulting CSV/Excel file to recipients. `recipient` and `role` accept a string or an array of strings.</p>

```json
{
  "query": "SELECT id, name, email FROM users WHERE created_at >= '2024-01-01';",
  "file_name": "users_jan_2024.csv",
  "recipient": ["ops@example.com"],
  "sender": "no-reply@example.com",
  "password": "example_password",
  "role": ["admin"],
  "subject": "Monthly Users Export",
  "message": "Attached is the users export for January 2024.",
  "email_server": "smtp.example.com"
}
```

</details>

<details>
<summary><strong>SQLi Considerations</strong></summary>

<p>Query Builders might be susceptible to SQL injections, and to combat this, an SQLi validator is
called at the top level of every route to track if failing the rules of parameterized queries. Normally,
you should try to prevent using various dangerous PostgreSQL statements which are set aside to trigger 
query failure from the onset within any given route. This error is sent to either your logger or HTTP Response.
</p>

<p>1. Define SQLi patterns you would like to catch: </p>

```code
SQLI_PATTERNS = [
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC|--|#|;)\b",
    r"' OR '1'='1",
    r"(?i)(\bor\b|\band\b)\s+\d+=\d+",
]

```

<p>2. Validation issue template which sends log or response with validation feedback: </p>

```code
def get_validation_log(key: str, issues: str | list[str]):
    return {
            "timestamp": datetime.datetime.now().__str__(),
            "validation_warning": f"Validation failed! Unsupported content. Attempted SQLi attack using parameter: {key}.",
            "rejected_value": issues,
            "status": True
            }

```

<p>Returns true is query template has potential SQLi: </p>

```code
def is_potential_sqli(param: str) -> bool:
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, param, flags=re.IGNORECASE):
            return True
    return False
```

<p>Performs full validation by for single value parameters of list of parameters: </p>

```code
async def validate_params_against_sqli(params: dict):
    try:
        issues = []
        for key, value in params.items():
           if isinstance(value, str) and is_potential_sqli(value):
              await handle_logging("error", get_validation_log(key, value))
           elif isinstance(value, list) and len(value) != 0:
               for element in value:
                   if(is_potential_sqli(element)):
                       issues.append(element)
                       await handle_logging("error", get_validation_log(key, value))

        return issues

    except errors.SyntaxError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation Error Occurred While Processing Request")
```

</details>

<details>
<summary><strong>Error Handling Considerations</strong></summary>

<p>Error is handled during validations and requests considering the following types of errors
from psycopg2: </p>

- Syntax error
- Connection error
- Undefined table
- Duplicate table
- Unique Violation
- Internal error

<p>Two-pronged approaches to communicating error involve: </p>

- Logging them via loguru, from where data could be further extracted to other observability services
- Sending appropriate HTTP response status and accompanying message.
</p>
