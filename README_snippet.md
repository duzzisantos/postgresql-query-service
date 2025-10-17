<details>
<summary><strong>POST /GetAll</strong></summary>

```json
{
  "table": "example_string"
}
```

</details>

<details>
<summary><strong>POST /OrderBy</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /LimitAndOffset</strong></summary>

```json
{
  "limit": 123,
  "offset": 123
}
```

</details>

<details>
<summary><strong>POST /WithLimit</strong></summary>

```json
{
  "limit": 123
}
```

</details>

<details>
<summary><strong>POST /AllWhere</strong></summary>

```json
{
  "conditions": [
    "example_string"
  ]
}
```

</details>

<details>
<summary><strong>POST /AllWhereOrderBy</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /AllBetween</strong></summary>

```json
{
  "column": "example_string",
  "start": "example_string",
  "end": "example_string"
}
```

</details>

<details>
<summary><strong>POST /AllWhereMatches</strong></summary>

```json
{
  "column": "example_string",
  "wild_card": "example"
}
```

</details>

<details>
<summary><strong>POST /AllWhereIn</strong></summary>

```json
{
  "column": "example_string",
  "search_parameters": [
    "example_string"
  ]
}
```

</details>

<details>
<summary><strong>POST /AllWhereAndCount</strong></summary>

```json
{
  "primary_column": "example_string",
  "secondary_column": "example_string",
  "search_parameter": "example"
}
```

</details>

<details>
<summary><strong>POST /AllWhereAverageModel</strong></summary>

```json
{}
```

</details>

<details>
<summary><strong>POST /AllGroupByModel</strong></summary>

```json
{
  "primary_column": "example_string",
  "secondary_column": "example_string"
}
```

</details>

<details>
<summary><strong>POST /ByColumns</strong></summary>

```json
{
  "columns": [
    "example_string"
  ]
}
```

</details>

<details>
<summary><strong>POST /ByColumnsAndOrder</strong></summary>

```json
{
  "order": "example_string"
}
```

</details>

<details>
<summary><strong>POST /ByColumnsAndLimit</strong></summary>

```json
{
  "limit": 123
}
```

</details>

<details>
<summary><strong>POST /TableJoinModel</strong></summary>

```json
{
  "columns": [
    "example_string"
  ],
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
  "columns": [
    "example_string"
  ],
  "table": "example_string",
  "values": [
    "example"
  ]
}
```

</details>

<details>
<summary><strong>POST /CreateMany</strong></summary>

```json
{
  "columns": [
    "example_string"
  ],
  "table": "example_string",
  "values": [
    [
      "example"
    ]
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

<details>
<summary><strong>POST /DeleteMany</strong></summary>

```json
{
  "table": "example_string",
  "primary_key": [
    "example"
  ]
}
```

</details>

<details>
<summary><strong>POST /DeleteByParams</strong></summary>

```json
{
  "conditions": [
    "example_string"
  ]
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
  "set_columns": [
    "example_string"
  ],
  "set_values": [
    "example"
  ],
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
  "column_names_with_properties": [
    "example_string"
  ]
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
