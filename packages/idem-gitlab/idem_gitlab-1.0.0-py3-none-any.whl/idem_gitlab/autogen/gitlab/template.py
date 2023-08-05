NAME_PARAMETER = {
    "default": None,
    "doc": "The identifier for this state",
    "param_type": "Text",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}


PRESENT_REQUEST_FORMAT = r"""
    result = dict(comment="", changes= None, name=name, result=True)

    before = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
        data={{ get_params }},
        success_codes=[200],
    )
    if before["status"]:
        result["comment"] = f"'{name}' already exists"
    else:
        ret = await {{ function.hardcoded.create_function }}(
            ctx,
            success_codes=[201, 304, 204],
            url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
            **{{ parameter.mapping.kwargs|default({}) }}
        )
        result["result"] = ret["status"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = f"Created '{name}'"

    # Now that the resource exists, update it
    ret = await {{ function.hardcoded.update_function }}(
        ctx,
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
        success_codes=[200, 204, 304],
    )

    if not ret["status"]:
        result["status"] = False
        result["comment"] = f"Unable to update '{name}': {ret['comment']}"

    after = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
        data={{ get_params }},
        success_codes=[200],
    )
    result["changes"] = differ.deep_diff(before["ret"], after["ret"])
    return result
"""

ABSENT_REQUEST_FORMAT = r"""
    result = dict(comment="", changes= None, name=name, result=True)
    before = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
        data={{ get_params }},
        success_codes=[204, 304, 404],
    )

    if before["status"]:
        result["comment"] = f"'{name}' already absent"
    else:
        ret = await {{ function.hardcoded.delete_function }}(
            ctx,
            url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
            success_code=[204],
            **{{ parameter.mapping.kwargs|default({}) }}
        )
        result["result"] = ret["status"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = f"Deleted '{name}'"

    after = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}",
        data={{ get_params }},
        success_codes=[204, 304, 404],
    )

    result["changes"] = differ.deep_diff(before["ret"], after["ret"])
    return result
"""

DESCRIBE_REQUEST_FORMAT = r"""
    result = {}
    {% if function.hardcoded.short_list_path %}

    async for project in hub.exec.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.short_list_path }}"):
        project_id = project["id"]

        async for ret in hub.exec.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}"):
            result[f"{{ function.hardcoded.short_list_path }}-{project_id}-{{ function.hardcoded.ref }}-{ret['id']}"] = {
                "{{ service_name }}.{{ function.hardcoded.create_ref }}": [
                    {%- for k,v in present_parameter.items() %}
                    {"{{ k }}": ret.get("{{ v.rstrip("_") }}")},
                    {%- endfor %}
                ]
            }
    {% else %}
    async for ret in hub.exec.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}"):
        result[f"{{ function.hardcoded.ref }}-{ret['id']}"] = {
            "{{ service_name }}.{{ function.hardcoded.create_ref }}": [
                {%- for k,v in present_parameter.items() %}
                {"{{ k }}": ret.get("{{ v.rstrip('_') }}")},
                {%- endfor %}
            ]
        }
    {% endif %}
    return result
"""
