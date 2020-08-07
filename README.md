# Snowctl
A cli tool for automating tasks in Snowflake Database.

### Installation
Install python3 (version 3.6 and higher)
- [Windows installation](https://www.python.org/downloads/release/python-385/)
- [Linux installation](https://docs.python-guide.org/starting/install3/linux/)

Use Python's pip installer to install or update snowctl
```sh
pip install snowctl
pip install snowctl --upgrade
```

### Usage
Run in interactive mode (prompts for configuration on the first run)
```sh
snowctl
```

Optional arguments
```
usage: snowctl [-h] [-d] [-s] [-c] [-e]

optional arguments:
  -h, --help           show this help message and exit
  -d, --debug          log to console
  -s, --safe           ask for confirmation before executing copy operations
  -c, --configuration  re-input configuration values
  -e, --echo           echo configuration values
  -v, --version        display snowctl version
```

### Commands
| CMD | ACTION |
|---------|---------|
| **help** | display help |
| **use** db/schema/warehouse name | change context |
| **copy** [-h] [-d] [-f] [-r] | copy views across schemas, see flags below |
| **list** filter | list views in current context with an optional filter |
| **peek** view | display first row from a view |
| **sql** query | execute sql query |
| **exit** | Exit |

```
usage: copy

optional arguments:
  -h, --help    show this help message
  -d, --derive  create new view by selecting all cols from source view instead of copying ddl
  -f, --filter  filter out columns of target view when copying
  -r, --rename  rename target views
```