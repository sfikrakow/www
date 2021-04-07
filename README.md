# SFI nextgen webpage

## Development setup

### Shell (quick setup)

```shell script
git clone https://git.sfi.pl/scm/www/wwwsfi.git
cd wwwsfi
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py sync_page_translation_fields
python manage.py update_translation_fields
yarn install
yarn dev
python manage.py runserver #in second terminal
```

### (alternative) setup with PyCharm

- (from start screen) `Get from version control`
- Git -> url `https://git.sfi.pl/scm/www/wwwsfi.git`
- Select `manage.py` in project tree
- `Configure Python interpreter` (just on top of the editor)
- `Add interpreter` -> `New environment` -> `OK`
- Wait for the project to get indexed
- Open `Terminal` (not Python Console) in PyCharm
- Verify that the prompt starts with `(venv)`
- (in terminal)

```shell script
pip install -r requirements.txt
python manage.py migrate
python manage.py sync_page_translation_fields
python manage.py update_translation_fields
yarn install
yarn dev &
```

- Click on the `manage.py`, PyCharm should reindex the project
- `Add Configuration...` -> `+` -> `Django Server` -> `OK`
