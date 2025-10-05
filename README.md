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

3. Test/verify that you are rightly connected to your postgresql network
4. Read and test through Swagger UI docs by visiting http://yourhost:port/docs
5. Apply necessary request body for each route
6. Refer to .env.example file to see variables you may need to run this application
7. Run locally on terminal: uvicorn app.main:app --port 'your-port' --reload

## Connection Verification

This tests connection to your PostgreSQL server and returns a lightweight test query result

## Joiners

This includes queries for inner, right, left, and full joins. There is also a query template for checking if sub queries exist or not.

## Mutators

This set of queries lets you run various create, delete, and update statements. While creating new tables, make sure to include
data types and character limits for each column. These are to be provided as comma separated strings in the request bodt.

## General Select Statements

This set of queries help you run various general select statements

## Specific Select Statements

This allows you query tables to extract information for specific columns
