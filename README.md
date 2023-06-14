# POC-Great-Expectations
This repository provides a practical demonstration of using Great Expectations in an end-to-end pipeline with Airflow and dbt.<br><br>
This project is an adaptation of the official Great Expectations [tutorial](https://github.com/great-expectations/gx_tutorials/tree/main/gx_dbt_airflow_tutorial) available on their GitHub repository. However, the original tutorial was based on an older version of GX. To provide you with the most up-to-date experience, this project has been updated to align with the latest version, which is 0.16.8 at the time of writing.

## Overview
The pipeline loads data from files into a database and then transforms it. Airflow is used to orchestrate the pipeline, and dbt is used to transform for the "T" step of ELT. Specifically, this tutorial directory contains:
- [airflow](https://github.com/syntio/POC-Great-Expectations/tree/master/airflow) - A folder containing the Airflow DAG file for this data pipeline.
- [data](https://github.com/syntio/POC-Great-Expectations/tree/master/data) - A folder containing two datasets used in the tutorial.
- [dbt](https://github.com/syntio/POC-Great-Expectations/tree/master/dbt) - A folder with the dbt project structure.
- [great_expectations](https://github.com/syntio/POC-Great-Expectations/tree/master/great_expectations) - A folder containing the Great Expectations configuration files.

## Instructions
To use this repository, follow these steps:

1. Install the required dependencies by running the following commands:
   ```bash
   pip install great_expectations==0.16.8
   pip install sqlalchemy==1.4.16
   pip install apache-airflow==2.6.1
   pip install psycopg2==2.9.6
   pip install airflow-provider-great-expectations==0.1.1
   ```

2. Update the following variables in the [pipeline.py](airflow/pipeline.py) file:
   - `DATABASE_URL`: Set this to your database connection string.
   - `PROJECT_ROOT_PATH`: Set this to the root directory of this repository on your local machine.

3. Create a `config_variables.yml` file inside the `uncommitted` folder, and store your PostgreSQL database credentials in this file. Use the following template, replacing `<username>` and `<password>` with your actual database username and password, and modifying other fields if necessary:
   ```yaml
   my_postgres_db_yaml_creds:
     drivername: postgresql
     username: <username>
     password: <password>
     host: localhost
     database: tutorials_db
     port: '5432'
    ```

4. Once everything is set up, you can run the entire DAG or individual tasks in the Airflow DAG. 

   - To run the DAG, use the following command:

     ```bash
     airflow dags test pipeline_with_gx
     ```

   - To run a specific task within the DAG, use the following command:

     ```bash
     airflow tasks test pipeline_with_gx <task_name>
     ```

   Replace `<task_name>` with the name of the specific task you want to run.


For more detailed instructions on how to use this repository, please refer to the blog post.
