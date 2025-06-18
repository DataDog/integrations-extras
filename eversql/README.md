# EverSQL

## Overview

[EverSQL][1] is a way to speed up your database and optimize SQL queries, providing automatic SQL tuning and indexing for developers, DBAs, and DevOps engineers.

EverSQL is non-intrusive, and doesn't access any of your databases' sensitive data.

### Usage

Slow SQL queries found in the Datadog Database Monitoring dashboard can be optimized using EverSQL. Copy the slow SQL query from Datadog and paste it directly into EverSQL's [SQL Optimization][2] process. Learn more about troubleshooting a slow query in the [Getting Started with Database Monitoring][5] guide.

### Supported Databases: 
MySQL, PostgreSQL, AWS Aurora, Google Cloud SQL, Azure DB, Percona, MariaDB.

## Setup

### Configuration
To speed up slow SQL queries identified by Datadog:
1. Navigate to the [Datadog Database Monitoring][4] dashboard and locate the slow SQL queries table.
2. Add a filter for the relevant database, and sort by a relevant performance metric, such as Average Latency.
3. Once you identify the SQL query you'd like to speed up, copy it from Datadog.
4. Navigate to [EverSQL][2] and paste the SQL query as part of the query optimization process.
5. From the optimization report, copy and create the optimal indexes in your database.
6. Copy the rewritten optimized query to your application code.

## Data Collected

### Metrics

EverSQL does not include any metrics.

### Service Checks

EverSQL does not include any service checks.

### Events

EverSQL does not include any events.

## Support

Need help? Contact [EverSQL support][3].

[1]: https://www.eversql.com/
[2]: https://www.eversql.com/sql-query-optimizer/ 
[3]: https://eversql.freshdesk.com/support/tickets/new
[4]: /databases/
[5]: https://docs.datadoghq.com/getting_started/database_monitoring/#troubleshoot-a-slow-query
