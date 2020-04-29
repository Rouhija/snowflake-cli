# Description
A cli tool for automating tasks in Snowflake Database for python3

### Installation
```sh
pip install snowflake-cli
```

### Usage
Run in interactive mode (prompts for conf on the first run)
```sh
snowctl
```

Optional arguments
```
usage: snowctl [-h] [-d] [-s] [-c]

optional arguments:
  -h, --help           show this help message and exit
  -d, --debug          debug logs to console
  -s, --safe           ask for confirmation before executing any potentially destructive operations
  -c, --configuration  re-enter Snowflake configuration
```

### Commands
| CMD | ACTION |
|---------|---------|
| **help** | Display help |
| **copy views** | copy views across schemas |
| **show views** | show views in current context |
| **use** database|schema|warehouse name | change context |
| **exit** | Exit |