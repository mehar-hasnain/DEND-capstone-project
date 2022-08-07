from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2022, 4, 14),
    'depends_on_past': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('restaurants_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@daily',
          catchup=False
       )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_restaurants_to_redshift = StageToRedshiftOperator(
    task_id='Stage_restaurants',
    dag=dag,
    table="staging_restaurants",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="s3://mehar-hasnain/restaurants_dedup.csv",
    region="us-east-1",
    truncate_table=True
)

load_restaurants_dimension_table = LoadDimensionOperator(
    task_id='Load_restaurants_dim_table',
    dag=dag,
    table='restaurants',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_dim_sql=SqlQueries.restaurants_table_insert
)

load_reviews_dimension_table = LoadDimensionOperator(
    task_id='Load_reviews_dim_table',
    dag=dag,
    table='reviews',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_dim_sql=SqlQueries.reviews_table_insert
)

load_features_dimension_table = LoadDimensionOperator(
    task_id='Load_features_dim_table',
    dag=dag,
    table='features',
    redshift_conn_id="redshift",
    truncate_table=True,
    load_dim_sql=SqlQueries.features_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    dq_checks=[
        { 'check_sql': 'SELECT COUNT(DISTINCT "state") FROM public.restaurants', 'expected_result': 12 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.restaurants WHERE name IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.reviews WHERE review_score IS NULL', 'expected_result': 0 },
        { 'check_sql': 'SELECT COUNT(*) FROM public.features WHERE delivery IS NULL', 'expected_result': 0 },
    ],
    redshift_conn_id="redshift"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_restaurants_to_redshift

stage_restaurants_to_redshift >> load_restaurants_dimension_table
stage_restaurants_to_redshift >> load_features_dimension_table
stage_restaurants_to_redshift >> load_reviews_dimension_table


load_restaurants_dimension_table >> run_quality_checks
load_features_dimension_table >> run_quality_checks
load_reviews_dimension_table >> run_quality_checks

run_quality_checks >> end_operator
