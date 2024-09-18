from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import pandas as pd
from pandas import DataFrame
import pyarrow
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """

    for date in sorted(df["lpep_pickup_date"].unique()):
        #table = pyarrow.Table.from_pandas(df.loc[df["lpep_pickup_date"] == date])
        df_temp = df.loc[df["lpep_pickup_date"] == date]
        #pyarrow.parquet.write_table(table, f"xxx.parquet")

        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'
        bucket_name = 'green_taxi_alex'
        object_key = f'{date.year}/{date.month}/{date.day}.parquet'
        #print(f"Bucket name: {bucket_name}")
        #print(f"Object name: {object_key}")
        GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df_temp,
            bucket_name,
            object_key,
            DataFrame.to_parquet
        )
