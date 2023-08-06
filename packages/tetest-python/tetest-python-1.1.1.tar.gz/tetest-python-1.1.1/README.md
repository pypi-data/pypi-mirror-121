# Information
TeTest-python is a plugin for user to build the connection to Te-Test testing platform.

## Table of Contents

- [Information](#information)
  - [Table of Contents](#table-of-contents)
  - [Publish](#publish)
  - [Install](#install)
    - [Configration](#configration)
    - [Add paramter for PyTest: conftest.py](#add-paramter-for-pytest-conftestpy)
    - [Local debug for project](#local-debug-for-project)

## Publish
```sh
pip install .
python setup.py sdist build
sudo pip install twine
twine upload dist/*
```

## Install

[pip][]:

```sh
pip install tetest-python && pip freeze > requirements.txt
```

### Configration
```js
{
    "Server": "http://localhost:8080",
    "Token": "",
    "Project": "",
    "TaskID": "",
    "BuildID": "",
    "TimeSpan": "",
    "Paramerter": {},
    "TaskInfo": {},
    "JobInfo": {},
    "Data": [],
    "Report": {
        "ReportGroupName": "TeTest-LocalTest",
        "File": "report.xml",
        "Path": "/",
        "ImagePath": "webdriver_screenshots"
    },
    "Agent": "PYTEST"
}
```

### Add paramter for PyTest: conftest.py
```python
from tetest_python import te_pytest_config

def pytest_addoption(parser):
	# add TE option === Start will support taskid, token, build id for pytest when execute on TE client
	te = te_pytest_config()
	te.pytest_addoption(parser)
	# add TE option === End
```

### Local debug for project
```python
sys.path.append("/Users/username/Documents/python/TE")
from {foldername}.tetest_python import te_services
te = te_pytest_config()
```

### Test data (Add / Get / Update / Delete)
```python
from tetest_python import te_services
te = te_services(confJSONPath # Optional)
# Add data (Only available for Project data and Master data)
data_dict = {"key1": "Value1", "Key2": "Value2"}
te.addProjectData(table_name, bodyJSON=data_dict)
# Get sign data function (Will consume after get)
query_dict = {"key1": "Value1", "Key2": "Value2"}
te.getProjectData(table_name, queryJSON=query_dict)
# Get multiple data (Will consume by default, could choice not consume for read only test case)
te.getPerformanceProjectData(table_name, count, consumed=True, queryJSON=query_dict)
# Update data
data_id = te.getProjectData(table_name, queryJSON=query_dict)['body']['_id']
te.updateProjectData(table_name, data_id, bodyJSON=updated_data_dict)
# Delete data
te.deleteProjectData(table_name, data_id)
```

### Login with SSO
```python
from tetest_python import te_login
initial_url = "SSO url which is static or dynamic generated"
# Cookies is optional when previous cookies is not require 
auth_response = te_login.loginSsoWithTeslaAccount(initial_url, user_name, password, cookies=response.cookies)
```

### Login with Auth (e.g. MyTesla)
```python
from tetest_python import te_login
response = requests.get("Site url which will redirect to Auth")
# Cookies is optional when previous cookies is not require 
auth_response = te_login.loginAuthWithExternalAccount(response.url, user_name, password, cookies=response.cookies)
```
