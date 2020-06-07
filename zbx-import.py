#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Import XML configuration files using Zabbix API.
Detailed information about zabbix templates import/export using the
Zabbix Web-UI and Zabbix API usage for import configurations,
available at:
    https://www.zabbix.com/documentation/4.0/manual/xml_export_import/templates#importing
    https://www.zabbix.com/documentation/4.0/manual/api/reference/configuration/import
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import json
import os
import io  # for handling file encoding in python2
from pprint import pformat
import sys

try:  # python3
    from urllib.request import Request, urlopen
except:  # python2
    from urllib2 import Request, urlopen
import traceback

DEFAULT_ZABBIX_API_URL = 'http://127.0.0.1:80/api_jsonrpc.php'
ELEMENTS_OPTIONS_DICT = {
    'createMissing': ['applications', 'discoveryRules', 'graphs', 'groups',
                      'hosts', 'httptests', 'images', 'items', 'maps',
                      'screens', 'templateLinkage', 'templates',
                      'templateScreens', 'triggers', 'valueMaps'],
    'updateExisting': ['discoveryRules', 'graphs',
                       'hosts', 'httptests', 'images', 'items', 'maps',
                       'screens', 'templates',
                       'templateScreens', 'triggers', 'valueMaps'],
    'deleteMissing': ['applications', 'discoveryRules', 'graphs',
                      'httptests', 'items', 'templateScreens', 'triggers'],
}


def __create_parser():
    cm_list = ELEMENTS_OPTIONS_DICT['createMissing']
    ue_list = ELEMENTS_OPTIONS_DICT['updateExisting']
    dm_list = ELEMENTS_OPTIONS_DICT['deleteMissing']
    # Number of displayed element values per line (on help description)
    BRKLN_NUM_EL = 6
    # Parse command line arguments
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('template_file',
                        help='Zabbix exported template xml file\n')
    parser.add_argument(
        '-u', '--user',
        help='Use the --user flag to provide the Zabbix API user name.\n'
             'Alternatively you can set the ZABBIX_API_USER environment '
             'variable.\nOne of the two methods is required. '
             'In case you are using both,\nthe flag value takes '
             'precedence over the environment variable\n'
    )
    parser.add_argument(
        '-p', '--passwd', metavar='PASSWORD',
        help='Use the --passwd flag to provide the Zabbix API password.\n'
             'Alternatively you can set the ZABBIX_API_PASSWD environment '
             'variable.\nOne of the two methods is required. '
             'In case you are using both,\nthe flag value takes '
             'precedence over the environment variable\n'
    )
    parser.add_argument('-s', '--url', default=DEFAULT_ZABBIX_API_URL,
                        help='Zabbix API URL\nDefault value is: {}\n'
                             ''.format(DEFAULT_ZABBIX_API_URL))
    parser.add_argument(
        '--no-create-missing', nargs='*', default=None,
        help='All the elements in the xml file that are missing in the zabbix'
             '\ndatabase are being created by default.\nTo unselect the '
             'createMissing option (i.e set false), use this flag\n followed'
             ' by a list of space separated values to be excluded.\nThe '
             'available element values are:\n\n{}\n\nIf not any value is '
             'provided, all of them will be excluded for the\ncreateMissing '
             'option\n'.format('\n'.join(
            [', '.join(cm_list[idx:idx + BRKLN_NUM_EL])
             for idx in range(len(cm_list))[::BRKLN_NUM_EL]]))
    )
    parser.add_argument(
        '--no-update-existing', nargs='*', default=None,
        help='All the elements in the xml file that already exists in the '
             'zabbix\ndatabase are being updated by default.\nTo unselect the '
             'updateExisting option (i.e set false), use this flag\n followed '
             'by a list of space separated values to be excluded.\nThe '
             'available element values are:\n\n{}\n\nIf not any value is '
             'provided, all of them will be excluded for the\nupdateExisting '
             'option\n'.format('\n'.join(
            [', '.join(ue_list[idx:idx + BRKLN_NUM_EL])
             for idx in range(len(ue_list))[::BRKLN_NUM_EL]]
        ))
    )
    parser.add_argument(
        '--delete-missing', nargs='*', default=None,
        help='All the elements that existes in the zabbix database that are '
             'not\npresent in the xml file are being preserved by default.\n'
             'To select the deleteMissing option (i.e set true), use this flag'
             '\nfollowed by a list of space separated values to be included.\n'
             'The available element values are:\n\n{}\n\nIf not any value is '
             'provided, all of them will be included for the\ndeleteMissing '
             'option\n'.format('\n'.join(
            [', '.join(dm_list[idx:idx + BRKLN_NUM_EL])
             for idx in range(len(dm_list))[::BRKLN_NUM_EL]]
        ))
    )
    return parser


def __build_rules(no_create_missing, no_update_existing, delete_missing):
    # https://www.zabbix.com/documentation/3.4/manual/api/reference/configuration/import
    if no_create_missing is None:
        no_create_missing = []
    elif not any(no_create_missing):
        no_create_missing = ELEMENTS_OPTIONS_DICT['createMissing']

    if no_update_existing is None:
        no_update_existing = []
    elif not any(no_update_existing):
        no_update_existing = ELEMENTS_OPTIONS_DICT['updateExisting']

    if delete_missing is None:
        delete_missing = []
    elif not any(delete_missing):
        delete_missing = ELEMENTS_OPTIONS_DICT['deleteMissing']

    rules = {el: {'createMissing': el not in no_create_missing}
             for el in ELEMENTS_OPTIONS_DICT['createMissing']}
    for el in ELEMENTS_OPTIONS_DICT['updateExisting']:
        rules[el]['updateExisting'] = el not in no_update_existing
    for el in ELEMENTS_OPTIONS_DICT['deleteMissing']:
        rules[el]['deleteMissing'] = el in delete_missing

    return rules


def zbxrequest(url, method, auth, params):
    if params is None:
        params = {}
    data = {"jsonrpc": "2.0", "id": 1, "method": method,
            "auth": auth, "params": params}
    headers = {'Content-Type': 'application/json'}
    # Convert to string and then to byte
    data = json.dumps(data).encode('utf-8')
    req = Request(args.url, headers=headers, data=data)
    resp = urlopen(req)
    # Get string
    resp = resp.read().decode('utf-8')
    # Convert to object
    resp = json.loads(resp, encoding='utf-8')
    return resp


def import_zabbix_template(template_file, user, passwd, url,
                           no_create_missing=None,
                           no_update_existing=None, delete_missing=None):
    rules = __build_rules(no_create_missing,
                          no_update_existing, delete_missing)

    # TODO: add API version check
    # r=zbxrequest(args.url, method="apiinfo.version", auth=None, params={})
    # print(r)

    # Get authentication token
    # https://www.zabbix.com/documentation/3.4/manual/api/reference/user/login
    auth_result = zbxrequest(url, method="user.login", auth=None,
                             params={"user": user, "password": passwd})

    # If authentication was not OK
    if 'result' not in auth_result:
        raise ZbxImportError('auth failed\n{}'
                             ''.format(pformat(auth_result)))

    global auth_token
    auth_token = auth_result['result']

    # Read template file content
    with io.open(template_file, 'r', encoding='utf-8') as f:
        source = f.read()

    # Set import parameters, including template file content
    params = {'format': 'xml', 'rules': rules, 'source': source}

    import_result = zbxrequest(url, method="configuration.import",
                               auth=auth_token, params=params)
    # Something like: {'id': 1, 'jsonrpc': '2.0', 'result': True}

    if 'result' in import_result and import_result['result']:
        print('SUCCESS: configuration import')
    else:
        raise ZbxImportError('configuration import failed\n{}'
                             ''.format(pformat(import_result)))


class ZbxImportError(Exception):
    def __init__(self, message, errors=1):
        traceback.print_exc()
        super(ZbxImportError, self).__init__(message)
        self.errors = errors


if __name__ == '__main__':

    parser = __create_parser()
    args = parser.parse_args()
    auth_token = None

    # Get user/password values from the environment variable,
    # in case the respective argument is missing:
    if args.user is None:
        try:
            args.user = os.environ['ZABBIX_API_USER']
        except KeyError as err:
            raise ZbxImportError('Missing zabbix API user name.\n{}'
                                 ''.format(parser.__dict__[
                                               '_option_string_actions'
                                           ]['--user'].help))
    if args.passwd is None:
        try:
            args.passwd = os.environ['ZABBIX_API_PASSWD']
        except KeyError as err:
            raise ZbxImportError('Missing zabbix API password.\n{}'
                                 ''.format(parser.__dict__[
                                               '_option_string_actions'
                                           ]['--passwd'].help))
    try:
        import_zabbix_template(args.template_file, args.user, args.passwd,
                               args.url, args.no_create_missing,
                               args.no_update_existing, args.delete_missing)

    except Exception as e:
        raise ZbxImportError(str(e))

    finally:
        # Logout to prevent generation of unnecessary open sessions
        # https://www.zabbix.com/documentation/3.4/manual/api/reference/user/logout
        if auth_token is not None:
            zbxrequest(args.url, method="user.logout",
                       auth=auth_token, params={})
