#!/usr/bin/env python3

from aws_cdk import core

from mssql_to_rds_mssql.mssql_to_rds_mssql_stack import MssqlToRdsMssqlStack


app = core.App()
MssqlToRdsMssqlStack(app, "mssql-to-rds-mssql")

app.synth()
