# Mexico Search Object Store



This is a library to provide abstraction of object storage between our model training pipeline and ML services

## Installation

```
pip install -i https://repository.walmart.com/repository/pypi-proxy/simple/ mxsearchstorage
```

## Usage

```python
from mxsearchstorage.blob import BlobStorage
from mxsearchstorage.schema import Type, BatchError
# provide connection string for primary data center and secondary data center
blob_storage = BlobStorage("primary_connection", "secondary_connection")
# upload object to selected data center
blob_storage.upload_objects_single(Type.primary, "container_name", "file_name", "absolute_file_path")
# pload object to both data center
blob_storage.upload_objects("container_name", "file_name", "absolute_file_path")
# download object into target file from selected data center
blob_storage.download_objects(Type.primary, "container_name", "file_name", "target_file_path")
# list objects from selected data center
blob_list = blob_storage.list_objects(Type.primary, "container_name")
for blob in blob_list:
  print(blob.name)

```

## Upload
You first need to install twine
```
pip install twine
```
Then you can upload the new version of lib into PyPI using the following command. It will require you to input acount info,
please contact Blake Li(HuiBlake.li@walmart.com) for the account info
```
twine upload dist/*
```

