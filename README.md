# Description
A cli tool for automating tasks in Snowflake Database. Mainly for copying views with column filtering at the moment.

### Installation
Install python3 (version 3.6 and higher)
- [Windows installation](https://www.python.org/downloads/release/python-385/)
- [Linux installation](https://docs.python-guide.org/starting/install3/linux/)

Use Python's pip installer to install snowctl
```sh
pip install snowctl
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
| **help** | Display help |
| **use** database/schema/warehouse name | change context |
| **copy views** | copy views across schemas |
| **copy views rename** | copy views across schemas with new name |
| **copy views filter** | copy views across schemas with column filtering |
| **list views** filter | list views in current context with an optional filter |
| **peek** view | display first row from a view |
| **sql** query | execute sql query |
| **exit** | Exit |
