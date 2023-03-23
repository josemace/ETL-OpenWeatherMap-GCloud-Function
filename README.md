# ETL OpenWeatherMap data [GCloud Functions version]

## Table of Contents

- [About](#about)
- [Requirements](#requirements)
- [Installation](#installation)
- [Schedule](#schedule)

## About <a name="about"></a>

This is a simplified version of [ETL-OpenWeatherMap-GCP](https://github.com/josemace/ETL-OpenWeatherMap-GCP) for GCloud functions.

## Requirements for local deployment <a name = "requirements"></a>

These requirements are only needed if the deployment is made from your local machine.

1. [gcloud CLI](https://cloud.google.com/sdk/docs/install)
2. You'll need to have authentication set up for your Google Cloud account. You can do this by following the instructions in the [official documentation](https://cloud.google.com/docs/authentication/application-default-credentials#personal)
3. This script is programmed with [Python 3.9](https://www.python.org/downloads/release/python-390/)

## Installation <a name = "installation"></a>

1. Open a terminal window and navigate to the directory where your function files are stored.
2. Create a virtual environment using the command: `python3.9 -m virtualenv venv`
3. Activate the virtual environment using the command: `source venv/bin/activate`
4. Install the necessary dependencies by running: `pip install -r requirements.txt`
5. Create a config.ini with the config schema, fill the variables.
6. (Optional) Test your function locally by running: `functions-framework --target=main --debug`. This should start a local server that you can use to test your function by accessing the IP returned.
7. Once you've confirmed that your function is working correctly, deploy it to Google Cloud Functions using the command:\
`gcloud functions deploy <FUNCTION_NAME> --entry-point=main --runtime=python39 --trigger-http --allow-unauthenticated --region=<REGION>`\
Replace `<FUNCTION_NAME>` with the name you want to give your function and `<REGION>` with the region you want to deploy it (in my case `europe-west1`)\
This command will deploy your function to Google Cloud Functions using Python 3.9 and trigger it with an HTTP request. The --allow-unauthenticated flag will allow anyone to access your function without authentication, so use this flag with caution.

### Config Schema <a name = "config_schema"></a>

Make a copy of `config-default.py` named `config.py` and replace values between <> with your variables

```
config_vars = {
    'owm_apikey': '<OWM API KEY>',
    'cities': ['city1','city2'],
    'units': 'metric',
    'project_id': '<GCP PROJECT-ID>',
    'bucket_id': '<GCLOUD STORAGE BUCKET-ID>',
    'output_filename': '<GCLOUD STORAGE CSV FILENAME>',
    'output_dataset_id': '<GOOGLE BIGQUERY DATASET-ID>',
    'output_table_name': '<GOOGLE BIGQUERY TABLENAME>'
}
```

## Schedule <a name = "schedule"></a>

To schedule your deployed Cloud Function to run daily using Google Cloud Scheduler, use the gcloud scheduler command like this:\
`gcloud scheduler jobs create http <JOB_NAME> --schedule="0 0 * * *" --uri=<FUNCTION_URL> --http-method=POST --headers=Content-Type=application/json`\
Replace `<JOB_NAME>` and `<FUNCTION_URL>` with the appropriate values. The --schedule flag specifies the cron expression for the schedule (in this case, running at midnight every day).

You can also schedule the job within the Google Cloud Console following these steps:

1. Open the Cloud Scheduler page in the Google Cloud Console.
2. Click the "Create Job" button to create a new job.
3. Enter a name for the job and a description (optional).
4. In the "Frequency" section, enter `0 0 * * *`
5. Select your Time zone
6. In the "Target" section, select "HTTP" as the target type.
7. In the "URL" field, enter the URL of your Cloud Function. The URL should be in the format: `https://REGION-PROJECT_ID.cloudfunctions.net/FUNCTION_NAME`. Replace REGION, PROJECT_ID, and FUNCTION_NAME with the appropriate values.
8. In the "HTTP Method" field, select "POST".
9. In the "Headers" section, click "Add header" and add a header with the name "Content-Type" and the value "application/json".
10. Click the "Create" button to create the job.
