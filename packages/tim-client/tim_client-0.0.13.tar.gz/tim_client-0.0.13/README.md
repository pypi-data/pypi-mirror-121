# TIM Python Client v5

Python SDK to use the TIM Engine v5. This includes methods to:

- upload a dataset,
- retrieve a list of datasets,
- retrieve a list of dataset versions,
- create a forecasting build model job,
- execute a forecasting build model job,
- create and execute a forecasting build model job,
- retrieve the results of a forecasting job,
- create an anomaly detection build model job,
- execute an anomaly detection build model job,
- create and execute an anomaly detection build model job,
- retrieve the results of an anomaly detection job,
- retrieve a list of workspaces.

## Usage

### Installation

To install the package run: `pip install tim-client`

### Initiation

```
from tim import Tim

client = Tim(email='',password='')
```

### Methods

Tim provides the following methods:

- `client.upload_dataset`
- `client.delete_dataset`
- `client.get_datasets`
- `client.get_dataset_versions`
- `client.build_forecasting_model`
- `client.execute_forecast`
- `client.build_forecasting_model_and_execute`
- `client.get_forecast_results`
- `client.delete_forecast`
- `client.build_anomaly_detection_model`
- `client.execute_anomaly_detection`
- `client.build_anomaly_detection_model_and_execute`
- `client.create_anomaly_detection`
- `client.create_anomaly_detection_and_execute`
- `client.get_anomaly_detection_results`
- `client.delete_anomaly_detection`
- `client.get_workspaces`

### Error handling

Minimal validation is performed by the Tim client, errors will be raised by the server.

### Documentation

Full documentation of the API can be found at: https://docs.tangent.works
