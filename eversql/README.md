# EverSQL - Your Database, Just Faster™

## Overview
- Looking to speed up slow SQL queries?
- Reached 100% CPU on your database, and you are unsure how to fix it?
- Database storage is out of space and looking for redundant indexes that you can delete?
**

[EverSQL][1] is the fastest way to automatically speed up your database and optimize SQL queries.
80,000+ developers, DBAs, and DevOps engineers use EverSQL for automatic SQL tuning and indexing.
Our customers report their queries are 5X faster on average, just minutes after getting started.
Save your team 35 weekly hours on average by optimizing your SQL queries online for free.

EverSQL is 100% non-intrusive, and doesn't access any of your databases' sensitive data.

![snapshot][8]

### Usage

The EverSQL integration has two options:

- A manual method, where you copy your queries from Datadog dashboard and paste them to EverSQL’s [optimize a query][2] action.
- An automatic method, where you add the EverSQL Sensor to your [RDS][3] or your [on-prem database][4].

### Supported Databases: 
MySQL, PostgreSQL, Aurora,Cloud SQL, Azure DB, Percona, MariaDB.

## Setup

### Configuration
In order to use the manual workflow, just start at [EverSQL][2].

In order to enable the automatic workflow, please follow these steps:

**Step 1:** Enable the slow query log
The performance sensor requires slow query logs to be enabled.
Click here for instructions if you don't have them enabled.

**Step 2**: Install the performance sensor
If you are using RDS, You can now deploy the performance sensor from the [Amazon Serverless Application repository][4].
Your personal API key (required as part of the installation) can be found [here][5]

To install the performance sensor on other environment, please run the following these [steps][6]


## Data Collected

### Metrics

EverSQL does not include any metrics.

### Service Checks

EverSQL does not include any service checks.

### Events

EverSQL does not include any events.

## Troubleshooting

Need help? Contact [EverSQL support][7].

[1]: https://www.eversql.com/
[2]: https://www.eversql.com/sql-query-optimizer/ 
[3]: https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-2:196422412051:applications~EverSQL-Performance-Sensor

[4]: https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-2:196422412051:applications~EverSQL-Performance-Sensor

[5]: https://www.eversql.com/edit-user-profile/ 
[6]: https://www.eversql.com/sensors/ 
[7]: https://eversql.freshdesk.com/support/tickets/new 
[8]: https://www.eversql.com/wp-content/uploads/2022/04/Datadog-EverSQL-SQL-Optimization.png
