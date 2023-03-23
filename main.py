import functions_framework
from owm import collect_weather_data
from gcp import df_to_bucket, blob_to_bigquery

@functions_framework.http
def main(request):
    # Save the weather data from OWM API into a pandas dataframe
    df = collect_weather_data()

    # Upload the dataframe as a csv file to Google Cloud Storage
    blob_uri = df_to_bucket(df)

    # Load the data from the Google Cloud Storage file into a BigQuery table
    blob_to_bigquery(blob_uri)

    return "OK"

if __name__ == "__main__":
    main('data')
