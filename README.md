# nba_props
Data for NBA Games

python3 will need to already be installed on the users device to create a virtual environment. 

**Create a Virtual Environment**
python3 virtual environments allow you to create dependency spaces per project so that projects only use required packages and new installs are simple. 

**To create a virtual environment**:

```
$python3 -m venv --without-pip $(pwd)/venv
$source $(pwd)/venv/bin/activate
$curl https://bootstrap.pypa.io/get-pip.py | python
$deactivate
```

**Activate virtual environment and install requirements**

```
$source $(pwd)/venv/bin/activate
$(venv) pip install -r requirements.txt
```

