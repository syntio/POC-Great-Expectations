# dbt project structure
This folder provides a project structure that is created when initializing dbt. It contains the following subfolders:
- [analyses](dbt/analyses) - This folder is used for ad hoc scripts in dbt, where you can combine SQL and Jinja (templating language) to perform exploratory analysis or run custom queries.
- [macros](dbt/macros) - This folder stores reusable code snippets known as macros, which are similar to user-defined functions in a database. Macros enable modularity and can be shared across different models.
- [models](dbt/models) - This directory contains SQL files that define the transformations for your data. Each model represents a specific task or analysis and is written in SQL syntax. These models are the core building blocks of your dbt project.
- [seeds](dbt/seeds) - This folder is used to store .csv files. This is the only place where you use dbt to store data.
- [snapshots](dbt/snapshots) - This folder provides a way to create tables in your database that function similarly to Slowly Changing Dimensions (SCD). Snapshots store point-in-time references of records, capturing historical changes by preserving both the original and updated records along with additional metadata.
- [tests](dbt/tests) - This folder contains SQL scripts used for data testing. These tests validate the quality, consistency, and accuracy of the transformed data produced by your dbt models.
- [dbt_project.yml](dbt/dbt_project.yml) - This file is the most important file in your project. It serves as the configuration file and holds metadata for your dbt project. It allows you to configure various project settings.
