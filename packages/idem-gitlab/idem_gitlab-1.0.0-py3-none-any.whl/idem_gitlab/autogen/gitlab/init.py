import pathlib

from dict_tools.data import NamespaceDict

try:
    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)

    ctx.servers = ["https://gitlab.com/api/v4/"]

    # We already have an acct plugin
    ctx.has_acct_plugin = False
    ctx.service_name = ctx.service_name or "gitlab_auto"
    version = "v4"
    docs_api = "https://docs.gitlab.com/ee/api/"

    plugins = hub.pop_create.gitlab.resource.parse(docs_api)

    # Initialize cloud spec
    ctx.cloud_spec = NamespaceDict(
        api_version=version,
        project_name=ctx.project_name,
        service_name=ctx.service_name,
        request_format={
            "present": hub.pop_create.gitlab.template.PRESENT_REQUEST_FORMAT,
            "absent": hub.pop_create.gitlab.template.ABSENT_REQUEST_FORMAT,
            "describe": hub.pop_create.gitlab.template.DESCRIBE_REQUEST_FORMAT,
        },
        plugins=plugins,
    )

    hub.cloudspec.init.run(
        ctx,
        directory,
        create_plugins=["state_modules"],
    )
    hub.pop_create.init.run(
        directory=directory,
        subparsers=["cicd"],
        **ctx,
    )

    ctx.cloud_spec.plugins = {}
    return ctx
