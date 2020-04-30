Utility to import exported XML configuration(templates, hosts, ...) into Zabbix using it's [API](https://www.zabbix.com/documentation/3.4/manual/api).

```
$ zbx-import.py -u Admin -p ****** --url https://zabbix.local/api_jsonrpc.php zbx_export_templates.xml
SUCCESS: configuration import
```

Tested with Zabix 3.4 and 4.0, probably will work with older versions up to 2.0. Written in pure python 3, no additional libraries are required.

Allows to control import options:

* create new - add new elements from the import file. Default: True
* update existing - update existing elements from the import file. Default: True
* delete missing - remove existing elements not present in the import file. Default: False. *NOTE*: without this option importing existing template with changed triggers will create new triggers, but old ones with the same name and different value will remain.

You can set this options for all elements or precisely select list of elements for the option: `--delete-missing 'triggers graphs'`. Check `--help` for available elements.

```
$ zbx-import.py -u Admin -p ****** --url https://zabbix.local/api_jsonrpc.php --delete-missing zbx_export_templates.xml
SUCCESS: configuration import
```


**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/zabbix-import).
