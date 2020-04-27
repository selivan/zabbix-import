Utility to import exported XML configuration(templates, hosts, host groups) into Zabbix using it's [API](https://www.zabbix.com/documentation/3.4/manual/api).

Tested with Zabix 3.4 and 4.0, probably will work with older versions up to 2.0. Written in pure python 3, no additional libraries are required.

```
$ zbx-import.py -u Admin -p ****** --url https://zabbix.local/api_jsonrpc.php zbx_export_templates.xml
SUCCESS: configuration import
```

```
$ zbx-import.py --help
usage: zbx-import.py [-h] -u USER -p PASSWORD [-s URL]
                     [--create-new CREATE_NEW]
                     [--update-existing UPDATE_EXISTING]
                     [--delete-missing DELETE_MISSING]
                     template_file

Import XML configuration files using Zabbix API

positional arguments:
  template_file

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  user name
  -p PASSWORD, --password PASSWORD, --pass PASSWORD
                        password
  -s URL, --url URL     Zabbix API URL, default is
                        http://127.0.0.1:80/api_jsonrpc.php
  --create-new CREATE_NEW
                        Add new elements using data from the import file.
                        Default: yes. See https://www.zabbix.com/documentation
                        /3.4/manual/xml_export_import/templates#importing
  --update-existing UPDATE_EXISTING
                        Existing elements will be updated with data taken from
                        the import file. Default: yes. See the link above
  --delete-missing DELETE_MISSING
                        Remove existing elements not present in the import
                        file. Default: no. See the link above
```
