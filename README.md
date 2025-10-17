# PostgreSQL Query Service

You can use this service to perform common DML operations in PostgreSQL
using custom query builders that can manipulate your database and return
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

This tests connection to your PostgreSQL server and returns a lightweight test query result

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

```json
{
  "table": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllOrderBy</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllLimitAndOffset</strong></summary>

```json
{
  "limit": 123,
  "offset": 123
}
```

</details>

<details>
<summary><strong>POST /GetAllWithLimit</strong></summary>

```json
{
  "limit": 123
}
```

</details>

<details>
<summary><strong>POST /GetAllWhere</strong></summary>

```json
{
  "conditions": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereOrderBy</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllBetween</strong></summary>

```json
{
  "column": "example_string",
  "start": "example_string",
  "end": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereMatches</strong></summary>

```json
{
  "column": "example_string",
  "wild_card": "example"
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereIn</strong></summary>

```json
{
  "column": "example_string",
  "search_parameters": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereAndCount</strong></summary>

```json
{
  "primary_column": "example_string",
  "secondary_column": "example_string",
  "search_parameter": "example"
}
```

</details>

<details>
<summary><strong>POST /GetAllWhereAverage</strong></summary>

```json
{}
```

</details>

<details>
<summary><strong>POST /GetAllGroupBy</strong></summary>

```json
{
  "primary_column": "example_string",
  "secondary_column": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetByColumns</strong></summary>

```json
{
  "columns": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /GetByColumnsAndOrder</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /GetByColumnsAndLimit</strong></summary>

```json
{
  "limit": 123
}
```

</details>

<details>
<summary><strong>POST /TableJoin</strong></summary>

```json
{
  "columns": ["example_string"],
  "primary_table": "example_string",
  "secondary_table": "example_string",
  "common_key": "example_string"
}
```

</details>

<details>
<summary><strong>POST /SubQueryExists</strong></summary>

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

<details>
<summary><strong>POST /CreateRow</strong></summary>

```json
{
  "columns": ["example_string"],
  "table": "example_string",
  "values": ["example"]
}
```

</details>

<details>
<summary><strong>POST /CreateMany</strong></summary>

```json
{
  "columns": ["example_string"],
  "table": "example_string",
  "values": [["example"]]
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

<details>
<summary><strong>POST /DeleteMany</strong></summary>

```json
{
  "table": "example_string",
  "primary_key": ["example"]
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

<details>
<summary><strong>POST /UpdateRow</strong></summary>

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

<details>
<summary><strong>POST /UpdateMany</strong></summary>

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

<details>
<summary><strong>POST /CreateTable</strong></summary>

```json
{
  "table_name": "example_string",
  "column_names_with_properties": ["example_string"]
}
```

</details>

<details>
<summary><strong>POST /QueryDownload</strong></summary>

```json
{
  "query": "example_string",
  "file_name": "example_string",
  "recipient": "example_string",
  "sender": "example_string",
  "password": "example_string",
  "role": "example_string",
  "subject": "example_string",
  "message": "example_string",
  "email_server": "example_string"
}
```

</details>

<details>
<summary><strong>SQLi Considerations</strong></summary>
<section>Query Builders might be susceptible to SQL injections, and to combat this, an SQLi validator is
called at the top level of every route to track if failing the rules of parameterized queries. Normally,
you should try to prevent using various dangerous PostgreSQL statements which are set aside to trigger 
query failure from the onset within any given route. This error is sent to either your logger or HTTP Response.
</section>

<p>1. Define SQLi patterns you would like to catch: </p>

```json
SQLI_PATTERNS = [
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC|--|#|;)\b",
    r"' OR '1'='1",
    r"(?i)(\bor\b|\band\b)\s+\d+=\d+",
]

```

<p>2. Validation issue template which sends log or response with validation feedback: </p>

```json
def get_validation_log(key: str, issues: str | list[str]):
    return {
            "timestamp": datetime.datetime.now().__str__(),
            "validation_warning": f"Validation failed! Unsupported content. Attempted SQLi attack using parameter: {key}.",
            "rejected_value": issues,
            "status": True
            }

```

<p>Returns true is query template has potential SQLi: </p>

```json
def is_potential_sqli(param: str) -> bool:
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, param, flags=re.IGNORECASE):
            return True
    return False
```

<p>Performs full validation by for single value parameters of list of parameters: </p>

```json
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
