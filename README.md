[![pypi package](https://img.shields.io/pypi/v/zabbix-import?color=%233fb911&label=pypi%20package)](https://pypi.org/project/zabbix-import/)

Utility to import exported XML configuration(templates, hosts, ...) into Zabbix using it's [API](https://www.zabbix.com/documentation/3.4/manual/api).

```
$ zbx-import.py -u Admin -p *** --url https://zabbix.local/api_jsonrpc.php exported_templates.xml
SUCCESS: configuration import
```

Tested with Zabbix 3.4 and 4.0, probably will work with older versions up to 2.0. Written in pure python, no additional libraries are required. Works with both python 3 and python 2.

Allows to control import options:

* create new - add new elements from the import file. Default: True
* update existing - update existing elements from the import file. Default: True
* delete missing - remove existing elements not present in the import file. Default: False. *NOTE*: without this option importing existing template with changed triggers will create new triggers, but old ones with the same name and different value will remain.

You can set this options for all elements or precisely select list of elements for the option: `--delete-missing 'triggers graphs'`. Check `--help` for available elements.

```
$ zbx-import.py -u Admin -p *** --url https://zabbix.local/api_jsonrpc.php --delete-missing exported_templates.xml
SUCCESS: configuration import
```

### Installation

Simplest option - just use `zbx-import.py` directly, it does not have any dependencies.

From [pypi.org](https://pypi.org):

`pip install zabbix-import`

Or create a Docker image and use it:

```bash
docker build -t zabbix-import .
# No options to get help on usage
docker run -it --rm zabbix-import [options]
```

**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/zabbix-import).
