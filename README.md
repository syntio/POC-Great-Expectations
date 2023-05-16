# POC-Great-Expectations
This repository provides a practical demonstration of using Great Expectations in an end-to-end pipeline with Airflow and dbt.<br><br>
This project is an adaptation of the official Great Expectations [tutorial](https://github.com/great-expectations/gx_tutorials/tree/main/gx_dbt_airflow_tutorial) available on their GitHub repository. However, the original tutorial was based on an older version of GX. To provide you with the most up-to-date experience, this project has been updated to align with the latest version, which is 0.16.8 at the time of writing.

## Overview
The pipeline loads data from files into a database and then transforms it. Airflow is used to orchestrate the pipeline, and dbt is used to transform for the "T" step of ELT. Specifically, this tutorial directory contains:
- [airflow](https://github.com/syntio/POC-Great-Expectations/tree/master/airflow) - A folder containing the Airflow DAG file for this data pipeline.
- [data](https://github.com/syntio/POC-Great-Expectations/tree/master/data) - A folder containing two datasets used in the tutorial.
- [dbt](https://github.com/syntio/POC-Great-Expectations/tree/master/dbt) - A folder with the dbt project structure.
- [great_expectations](https://github.com/syntio/POC-Great-Expectations/tree/master/great_expectations) - A folder containing the Great Expectations configuration files.

To use this repository, update the following variables in the [pipeline.py](airflow/pipeline.py) file:
- `DATABASE_URL`: Set this to your database connection string.
- `PROJECT_ROOT_PATH`: Set this to the root directory of this repository on your local machine.

For more detailed instructions on how to use this repository, please refer to the blog post.
