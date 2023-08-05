import requests

try:
    import bs4

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)
from typing import List


def __virtual__(hub):
    return HAS_LIBS


def parse(hub, link: str, path: str, clean_path: str):
    result = {"create": {}, "delete": {}, "get": {}, "list": {}, "update": {}}
    # Parse the path
    with requests.get(link) as response:
        html = response.text

    soup = bs4.BeautifulSoup(html, "lxml")
    main = soup.find("div", {"role": "main"})

    for table in main.find_all("table", {"thead": {}}):
        body: bs4.Tag = table.tbody

        try:
            example = table.find_previous_sibling("div").find("code").text
            if path not in example:
                continue
        except AttributeError:
            example = ""
        function_doc = table.find_previous_sibling("p").text

        params = {}
        for row in body.find_all("tr"):
            cells: List[bs4.Tag] = row.find_all("td")
            if len(cells) < 4:
                continue
            name = cells[0].text.strip()
            target = "kwargs"
            if f":{name}" in path:
                target = "hardcoded"
                if name == "id":
                    name = "id_"

            required = cells[2].text.startswith("yes")
            params[name] = {
                "required": required,
                "default": None,
                "target_type": "mapping",
                "target": target,
                "param_type": hub.pop_create.gitlab.param.type(cells[1].text.strip()),
                "doc": cells[3].text.strip(),
            }

        function_data = {
            "doc": function_doc,
            "params": params,
        }
        if "POST" in example and not result["create"]:
            result["create"] = function_data
        elif "PUT" in example and not result["update"]:
            result["update"] = function_data
        elif "DELETE" in example and not result["delete"]:
            result["delete"] = function_data
        elif "GET" in example:
            head = table.find_previous_sibling("h2").text
            if "list" in head.lower():
                get_params = {}
                for name, param_data in function_data.get("params", {}).items():
                    if name in clean_path:
                        continue
                    get_params[name] = param_data
                function_data["params"] = get_params
                if not result["list"]:
                    result["list"] = function_data
                elif not result["get"]:
                    result["get"] = function_data

        elif "PATCH" in example and not result["update"]:
            result["update"] = function_data

    # This will usually work
    if not result["get"]:
        result["get"] = result["list"]

    return result
