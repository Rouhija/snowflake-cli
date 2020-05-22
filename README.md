# Description
A cli tool for automating tasks in Snowflake Database written in Python3

### Installation
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
  -s, --safe           ask for confirmation before executing any operations
  -c, --configuration  re-input configuration values
  -e, --echo           echo configuration values
```

### Commands
| CMD | ACTION |
|---------|---------|
| **help** | Display help |
| **use** database/schema/warehouse name | change context |
| **copy views** | copy views across schemas |
| **copy views filter** | copy views across schemas with column filtering |
| **show views** | show views in current context |
| **sql** query | execute sql query |
| **exit** | Exit |