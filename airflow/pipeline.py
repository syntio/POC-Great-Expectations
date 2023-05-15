import os
import subprocess

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils.types.enriched_datetime.pendulum_date import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator


DATABASE_URL = 'postgresql://<your_user>:<your_password>@localhost:5432/npi_db'
PROJECT_ROOT_PATH = '<your_project_path>'
GX_CONTEXT_PATH = os.path.join(PROJECT_ROOT_PATH, 'great_expectations')


def load_files_into_db():
    """
        Load CSV files into a database using SQLAlchemy.
    """

    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute('DROP TABLE IF EXISTS npi_small CASCADE')
        conn.execute('DROP TABLE IF EXISTS state_abbreviations CASCADE')

        df_npi_small = pd.read_csv(os.path.join(PROJECT_ROOT_PATH, 'data', 'npi_small.csv'))
        column_rename_dict = {old_column_name: old_column_name.lower() for old_column_name in df_npi_small.columns}
        df_npi_small.rename(columns=column_rename_dict, inplace=True)
        df_npi_small.to_sql('npi_small', engine,
                            schema=None,
                            if_exists='replace',
                            index=False,
                            index_label=None,
                            chunksize=None,
                            dtype=None)

        df_state_abbreviations = pd.read_csv(os.path.join(PROJECT_ROOT_PATH, 'data', 'state_abbreviations.csv'))
        df_state_abbreviations.to_sql('state_abbreviations', engine,
                                      schema=None,
                                      if_exists='replace',
                                      index=False,
                                      index_label=None,
                                      chunksize=None,
                                      dtype=None)

    return 'Loaded files into the database'


def transform_data_in_db():
    """
        Run a dbt command to transform data in the database.
    """
    command_activate = r'.\venv\Scripts\activate'
    command_dbt = f'''dbt run --project-dir {os.path.join(PROJECT_ROOT_PATH, 'dbt')}'''
    subprocess.run(f'{command_activate} && {command_dbt}', shell=True, check=True)


def publish_to_prod():
    """
        Rename a table in the database to promote it.
    """
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        conn.execute('DROP TABLE IF EXISTS prod_count_providers_by_state')
        conn.execute('ALTER TABLE count_providers_by_state RENAME TO prod_count_providers_by_state')


with DAG(
        dag_id='pipeline_with_gx',
        default_args={
            'owner': 'Airflow',
            'start_date': pendulum.today('UTC').add(days=-1)
        },
        schedule=None,
) as dag:

    task_validate_source_data = GreatExpectationsOperator(
        task_id='task_validate_source_data',
        data_context_root_dir=GX_CONTEXT_PATH,
        checkpoint_name='npi_small_file_checkpoint',
        return_json_dict=True,
        dag=dag
    )

    task_load_files_into_db = PythonOperator(
        task_id='task_load_files_into_db',
        python_callable=load_files_into_db,
        dag=dag
    )

    task_validate_source_data_load = GreatExpectationsOperator(
        task_id='task_validate_source_data_load',
        data_context_root_dir=GX_CONTEXT_PATH,
        checkpoint_name='npi_small_db_checkpoint',
        return_json_dict=True,
        dag=dag
    )

    task_transform_data_in_db = PythonOperator(
        task_id='task_transform_data_in_db',
        python_callable=transform_data_in_db,
        dag=dag
    )

    task_validate_analytical_output = GreatExpectationsOperator(
        task_id='task_validate_analytical_output',
        data_context_root_dir=GX_CONTEXT_PATH,
        checkpoint_name='providers_by_state_checkpoint',
        return_json_dict=True,
        dag=dag
    )

    task_publish = PythonOperator(
        task_id='task_publish',
        python_callable=publish_to_prod,
        dag=dag
    )


# DAG dependencies
task_validate_source_data >> task_load_files_into_db >> task_validate_source_data_load >> task_transform_data_in_db >> task_validate_analytical_output >> task_publish
