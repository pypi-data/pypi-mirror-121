import json
import sys
from argparse import Namespace

import colorama
from requests import request
from tabulate import tabulate

from dstack.cli.common import sensitive
from dstack.config import get_config, ConfigurationError


def unpause_func(_: Namespace):
    try:
        data = {
            "paused": False
        }
        response = do_post("auto-scale/config/update", data)
        if response.status_code == 200:
            print("Unpausing succeeded")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def pause_rules_func(_: Namespace):
    try:
        data = {
            "paused": True
        }
        response = do_post("auto-scale/config/update", data)
        if response.status_code == 200:
            print("Pausing succeeded")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def init_func(args: Namespace):
    try:
        data = {
            "aws_access_key_id": args.aws_access_key_id,
            "aws_secret_access_key": args.aws_secret_access_key,
            "aws_region": args.aws_region,
        }
        response = do_post("auto-scale/config/update", data)
        if response.status_code == 200:
            print("Initialization succeeded")
        if response.status_code == 400 and response.json().get("message") == "non-cancelled requests":
            sys.exit(f"Call 'dstack rules clear' first")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def info_func(_: Namespace):
    try:
        response = do_post("auto-scale/config/info")
        if response.status_code == 200:
            response_json = response.json()
            print("aws_access_key_id: " + (sensitive(response_json.get("aws_access_key_id")) or "no"))
            print("aws_secret_access_key: " + (sensitive(response_json.get("aws_secret_access_key")) or "no"))
            print("aws_region: " + (response_json.get("aws_region") or "no"))
            print("paused: " + str(response_json.get("paused")).lower())
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def do_post(api, data=None):
    dstack_config = get_config()
    profile = dstack_config.get_profile("default")
    headers = {}
    if profile.token is not None:
        headers["Authorization"] = f"Bearer {profile.token}"
    if data is not None:
        data_bytes = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = f"application/json; charset=utf-8"
        response = request(method="POST", url=f"{profile.server}/{api}", data=data_bytes, headers=headers,
                           verify=profile.verify)
    else:
        response = request(method="POST", url=f"{profile.server}/{api}", headers=headers,
                           verify=profile.verify)
    return response


def do_get(api, params=None):
    if params is None:
        params = {}
    dstack_config = get_config()
    profile = dstack_config.get_profile("default")
    headers = {}
    if profile.token is not None:
        headers["Authorization"] = f"Bearer {profile.token}"
    response = request(method="GET", url=f"{profile.server}/{api}", params=params, headers=headers,
                       verify=profile.verify)
    return response


def set_rule_func(args: Namespace):
    try:
        data = {
            "instance_type": args.instance_type,
            "number": args.number
        }
        response = do_post("auto-scale/rules/set", data)
        if response.status_code == 200:
            print("Succeeded")
        if response.status_code == 400 and response.json().get("message") == "auto-scale is not configured":
            sys.exit(f"Call 'dstack auto-scale init' first")
        if response.status_code == 404 and response.json().get("message") == "instance type not found":
            sys.exit(f"Instance type is not supported")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def clear_rules_func(_: Namespace):
    try:
        response = do_post("auto-scale/rules/clear")
        if response.status_code == 200:
            print("Succeeded")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def list_rules_func(_: Namespace):
    try:
        response = do_get("auto-scale/rules/list")
        if response.status_code == 200:
            table_headers = [
                f"{colorama.Fore.LIGHTMAGENTA_EX}INSTANCE TYPE{colorama.Fore.RESET}",
                f"{colorama.Fore.LIGHTMAGENTA_EX}NUMBER{colorama.Fore.RESET}"
            ]
            table_rows = []
            for rule in response.json()["rules"]:
                table_rows.append([
                    rule["instance_type"],
                    rule["number"]
                ])
            print(tabulate(table_rows, headers=table_headers, tablefmt="plain"))
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def register_parsers(main_subparsers):
    parser = main_subparsers.add_parser("auto-scale", help="Manage auto-scale settings")

    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser("init", help="Authorizing dstack to access an AWS account")
    init_parser.add_argument("--aws-access-key-id", type=str, dest="aws_access_key_id", required=True)
    init_parser.add_argument("--aws-secret-access-key", type=str, dest="aws_secret_access_key", required=True)
    init_parser.add_argument("--aws-region", type=str, dest="aws_region", required=True)
    init_parser.set_defaults(func=init_func)

    unpause_parser = subparsers.add_parser("info", help="Display configuration")
    unpause_parser.set_defaults(func=info_func)

    unpause_parser = subparsers.add_parser("unpause", help="Pause all rules")
    unpause_parser.set_defaults(func=unpause_func)

    unpause_parser = subparsers.add_parser("pause", help="Pause all rules")
    unpause_parser.set_defaults(func=pause_rules_func)

    rules_parser = subparsers.add_parser("rules", help="Manage rules")

    rules_subparsers = rules_parser.add_subparsers()
    set_rule_parser = rules_subparsers.add_parser("set", help="Set number of instances per type")
    set_rule_parser.add_argument("--instance-type", type=str, dest="instance_type", required=True)
    set_rule_parser.add_argument("--number", type=str, help="Number of instances", required=True)
    set_rule_parser.set_defaults(func=set_rule_func)

    clear_rules_parser = rules_subparsers.add_parser("clear", help="Clear all rules")
    clear_rules_parser.set_defaults(func=clear_rules_func)

    list_rules_parser = rules_subparsers.add_parser("list", help="List rules")
    list_rules_parser.set_defaults(func=list_rules_func)
