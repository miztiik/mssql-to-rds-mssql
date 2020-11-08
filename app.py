#!/usr/bin/env python3

from mssql_to_rds_mssql.stacks.back_end.vpc_stack import VpcStack
from mssql_to_rds_mssql.stacks.back_end.database_migration_prerequisite_stack import DatabaseMigrationPrerequisiteStack
from mssql_to_rds_mssql.stacks.back_end.mssql_on_windows_ec2_stack import MsSqlOnWindowsEc2Stack
from aws_cdk import core


app = core.App()

env_MSSQL = core.Environment(region="us-east-1")

# VPC Stack for hosting Secure API & Other resources
vpc_stack = VpcStack(
    app,
    f"{app.node.try_get_context('service_name')}-vpc-stack",
    description="Miztiik Automation: VPC to host resources for DB Migration",
    env=env_MSSQL
)


# Build the pre-reqs for MSSQL on EC2
database_migration_stack = DatabaseMigrationPrerequisiteStack(
    app,
    f"{app.node.try_get_context('service_name')}-database-migration-prerequisite-stack",
    stack_log_level="INFO",
    vpc=vpc_stack.vpc,
    description="Miztiik Automation: DMS Best Practice Demonstration. This stack will create roles and security groups to assist in database migration",
    env=env_MSSQL
)

# Deploy MSSQL on EC2
mssql_on_ec2 = MsSqlOnWindowsEc2Stack(
    app,
    f"{app.node.try_get_context('service_name')}-mssql-on-windows-ec2",
    vpc=vpc_stack.vpc,
    ec2_instance_type="m5.large",
    ssh_key_name=database_migration_stack.custom_ssh_key_name,
    stack_log_level="INFO",
    description="Miztiik Automation: Deploy MSSQL on EC2",
    env=env_MSSQL
)


# Stack Level Tagging
core.Tag.add(app, key="Owner",
             value=app.node.try_get_context("owner"))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context("github_profile"))
core.Tag.add(app, key="Project",
             value=app.node.try_get_context("service_name"))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context("github_repo_url"))
core.Tag.add(app, key="Udemy",
             value=app.node.try_get_context("udemy_profile"))
core.Tag.add(app, key="SkillShare",
             value=app.node.try_get_context("skill_profile"))
core.Tag.add(app, key="AboutMe",
             value=app.node.try_get_context("about_me"))
core.Tag.add(app, key="BuyMeACoffee",
             value=app.node.try_get_context("ko_fi"))
app.synth()
