# SFI nextgen webpage

## Development setup
### Shell (quick setup)
```shell script
git clone https://git.sfi.pl/scm/www/wwwsfi.git
cd enroll
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### (alternative) setup with PyCharm
* (from start screen) `Get from version control`
* Git -> url `https://git.sfi.pl/scm/www/wwwsfi.git`
* Select `manage.py` in project tree
* `Configure Python interpreter` (just on top of the editor)
* `Add interpreter` -> `New environment` -> `OK`
* Wait for the project to get indexed
* Open `Terminal` (not Python Console) in PyCharm
* Verify that the prompt starts with `(venv)`
* (in terminal) `pip install -r requirements.txt`
* (in terminal) `python manage.py migrate`
* Click on the `manage.py`, PyCharm should reindex the project
* `Add Configuration...` -> `+` -> `Django Server` -> `OK`


