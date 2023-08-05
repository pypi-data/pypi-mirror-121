import re
from typing import Any
from typing import Dict

__func_alias__ = {"type_": "type"}


def parse(hub, name: str, path: str, link: str, ref: str):
    clean_path = re.sub(
        r":(\w+)", lambda m: f"{{{hub.tool.format.keyword.unclash(m.group(1))}}}", path
    )
    # Gitlab defines path parameters as ":param", transform that into "{param}"
    functions: Dict[str, Any] = hub.pop_create.gitlab.functions.parse(
        link, path, clean_path
    )
    if not all(func_data for func_data in functions.values()):
        hub.log.info(
            f"Missing functions for {ref}: "
            + ", ".join(k for k, v in functions.items() if not v)
        )
        return {}

    match = re.match(r"(.+)/{(.+)}", clean_path)
    if match:
        short_list_path = match.group(1)
    else:
        short_list_path = ""

    shared_func_data = {
        "hardcoded": {
            "path": clean_path,
            "ref": ref,
            "create_ref": f"{ref}.present",
            "create_function": "hub.exec.request.json.post",
            "delete_function": "hub.exec.request.json.delete",
            "update_function": "hub.exec.request.json.put",
            "get_function": "hub.exec.request.json.get",
            "list_function": "hub.exec.request.json.get",
            "short_list_path": short_list_path,
        },
    }

    create_params = functions["create"].get("params")
    if "name" not in create_params:
        create_params["name"] = hub.pop_create.gitlab.template.NAME_PARAMETER
    delete_params = functions["delete"].get("params")
    if "name" not in delete_params:
        delete_params["name"] = hub.pop_create.gitlab.template.NAME_PARAMETER

    # Fully define the plugin
    plugin = {
        "doc": name,
        "imports": [
            "from typing import Any, Dict, List, Text",
            "import dict_tools.differ as differ",
        ],
        "functions": {
            "present": dict(
                doc=functions["create"].get("doc"),
                params=dict(name=create_params.pop("name"), **create_params),
                **shared_func_data,
            ),
            "absent": dict(
                doc=functions["create"].get("doc"),
                params=dict(name=delete_params.pop("name"), **delete_params),
                **shared_func_data,
            ),
            "describe": dict(
                doc=functions["list"].get("doc"),
                params=functions["get"].get("params", {}),
                **shared_func_data,
            ),
        },
    }
    return plugin
