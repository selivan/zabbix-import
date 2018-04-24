Utility to import exported XML configuration(templates, hosts, host groups) into Zabbix using it's [API](https://www.zabbix.com/documentation/3.4/manual/api).

Tested with Zabix 3.4, probably will work with older versions up to 2.0. Written in python 3, no additional libraries are required.

```
$ zbx-import.py -u Admin -p ****** --url https://zabbix.local/api_jsonrpc.php zbx_export_templates.xml
SUCCESS: configuration import
```

```
$ zbx-import.py --help

Usage: zbx-import.py [-h] -u USER -p PASSWORD [-s URL] template_file

Import XML configuration files using Zabbix API

positional arguments:
  template_file

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  user name
  -p PASSWORD, --password PASSWORD, --pass PASSWORD
                        password
  -s URL, --url URL     Zabbix API URL
```
