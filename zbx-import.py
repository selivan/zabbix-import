#!/usr/bin/env python3
"""
Import XML configuration files using Zabbix API:
https://www.zabbix.com/documentation/3.4/manual/api/reference/configuration/import
"""
import argparse
from urllib import request
import json
import sys
from pprint import pformat


def zbxrequest(url, method, auth, params):

    if params is None:
        params = {}
    data = { "jsonrpc": "2.0", "id": 1, "method": method, "auth": auth, "params": params }
    # Convert to string and then to byte
    data = json.dumps(data).encode('utf-8')
    req = request.Request(args.url, headers={'Content-Type': 'application/json'}, data=data)
    resp = request.urlopen(req)
    # Get string
    resp = resp.read().decode('utf-8')
    # Convert to object
    resp = json.loads(resp, encoding='utf-8')
    return resp

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Parse command line arguments
parser = argparse.ArgumentParser(description='Import XML configuration files using Zabbix API')
parser.add_argument('template_file')
parser.add_argument('-u', '--user', required=True, help='user name')
parser.add_argument('-p', '--password', '--pass', required=True, help='password', metavar='PASSWORD')
parser.add_argument('-s', '--url', default='http://127.0.0.1:80/api_jsonrpc.php',
                    help='Zabbix API URL, default is http://127.0.0.1:80/api_jsonrpc.php')
parser.add_argument('--create-new', type=str2bool, default=True,
                    help='Add new elements using data from the import file. Default: yes. See https://www.zabbix.com/documentation/3.4/manual/xml_export_import/templates#importing')
parser.add_argument('--update-existing', type=str2bool, default=True,
                    help='Existing elements will be updated with data taken from the import file. Default: yes. See the link above')
parser.add_argument('--delete-missing', type=str2bool, default=False,
                    help='Remove existing elements not present in the import file. Default: no. See the link above')
args = parser.parse_args()

try:
    exit_code=1
    # TODO: add API version check
    # r=zbxrequest(args.url, method="apiinfo.version", auth=None, params={})
    # print(r)

    # Get authentication token
    # https://www.zabbix.com/documentation/3.4/manual/api/reference/user/login
    auth_result = zbxrequest(args.url, method="user.login", auth=None,
                             params={"user": args.user, "password": args.password})

    # If authentication was not OK
    if 'result' not in auth_result:
        raise Exception('ERROR: auth failed\n' + pformat(auth_result))

    auth_token = auth_result['result']

    # Read template file content
    with open(args.template_file, 'r', encoding='utf-8') as f:
        source = f.read()

    # Set import parameters, including template file content
    # https://www.zabbix.com/documentation/3.4/manual/api/reference/configuration/import
    params = {'format': 'xml',
              'rules': {
                        'applications': {
                            'createMissing': args.create_missing,
                            'deleteMissing': args.delete_missing
                            },
                        'discoveryRules': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'graphs': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'groups': {
                            'createMissing': args.create_missing
                            },
                        'hosts': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        'httptests': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'images': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        'items': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'maps': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        'screens': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        'templateLinkage': {
                            'createMissing': args.create_missing
                            },
                        'templates': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        'templateScreens': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'triggers': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing,
                            'deleteMissing': args.delete_missing
                            },
                        'valueMaps': {
                            'createMissing': args.create_missing,
                            'updateExisting': args.update_existing
                            },
                        },
              'source': source
              }

    # https://www.zabbix.com/documentation/3.4/manual/api/reference/configuration/import
    import_result = zbxrequest(args.url, method="configuration.import", auth=auth_token, params=params)
    # Something like: {'id': 1, 'jsonrpc': '2.0', 'result': True}

    if 'result' in import_result and import_result['result']:
        print('SUCCESS: configuration import')
    else:
        raise Exception('ERROR: configuration import failed\n' + pformat(import_result))

    exit_code = 0

except Exception as e:

    print(str(e), file=sys.stderr)

finally:
    # Logout to prevent generation of unnecessary open sessions
    # https://www.zabbix.com/documentation/3.4/manual/api/reference/user/logout
    if 'auth_token' in vars():
        zbxrequest(args.url, method="user.logout", auth=auth_token, params={})

    sys.exit(exit_code)
