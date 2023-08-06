import sys

import click

import vessl
from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    choices_prompter,
    format_bool,
    format_string,
    generic_prompter,
    print_data,
    print_table,
    prompt_choices,
)
from vessl.cli.organization import organization_name_option
from vessl.project import clone_project, create_project, list_projects, read_project
from vessl.util.constant import (
    PROJECT_TYPE_VERSION_CONTROL,
    PROJECT_TYPES,
)
from vessl.util.exception import InvalidProjectError


def project_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str,
) -> str:
    projects = list_projects()
    return prompt_choices("Project", [x.name for x in projects])


def version_control_project_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str,
) -> str:
    projects = [p for p in list_projects() if p.type == PROJECT_TYPE_VERSION_CONTROL]
    if not projects:
        raise click.ClickException(f'No version-control project found.')
    return prompt_choices("Project", [x.name for x in projects])


def github_owner_prompter(
    ctx: click.Context, param: click.Parameter, value: str,
) -> str:
    type = ctx.params.get("type")
    if type == PROJECT_TYPE_VERSION_CONTROL:
        return click.prompt("Github owner", type=click.STRING)


def github_repo_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    type = ctx.params.get("type")
    if type == PROJECT_TYPE_VERSION_CONTROL:
        return click.prompt("Github repository name", type=click.STRING)


@click.command(name="project", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=project_name_prompter
)
@organization_name_option
def read(name: str):
    project = read_project(project_name=name)

    git_data = "-"
    if project.type == PROJECT_TYPE_VERSION_CONTROL:
        git_data = {
            "Owner": project.cached_git_owner_slug,
            "Repository": project.cached_git_repo_slug,
            "URL": project.cached_git_http_url_to_repo,
            "Provider": format_string(project.git_provider),
        }

    print_data(
        {
            "ID": project.id,
            "Name": project.name,
            "Type": project.type,
            "Experiments": project.experiment_summary.total,
            "Public": format_bool(project.is_public),
            "Git": git_data,
        }
    )


@cli.vessl_command()
@organization_name_option
def list():
    projects = list_projects()
    print_table(
        projects,
        ["ID", "Name", "Type", "Experiments"],
        lambda x: [x.id, x.name, x.type, x.experiment_summary.total],
    )


@cli.vessl_command()
@vessl_argument(
    "type",
    type=click.Choice(PROJECT_TYPES),
    required=True,
    prompter=choices_prompter("Project type", PROJECT_TYPES),
)
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=generic_prompter("Project name")
)
@vessl_option(
    "--github-owner",
    type=click.STRING,
    prompter=github_owner_prompter,
    help="Owner of github repository.",
)
@vessl_option("--github-repo", type=click.STRING, prompter=github_repo_prompter)
@click.option("-m", "--description", type=click.STRING)
@organization_name_option
def create(type: str, name: str, github_owner: str, github_repo: str, description: str):
    project = create_project(
        project_type=type,
        project_name=name,
        github_owner=github_owner,
        github_repo=github_repo,
        description=description,
    )
    print(
        f"Created '{project.name}'.\n"
        f"For more info: {Endpoint.project.format(project.organization.name, project.name)}"
    )


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=version_control_project_name_prompter,
)
@organization_name_option
def clone(name: str):
    clone_project(project_name=name)


def project_name_callback(
    ctx: click.Context, param: click.Parameter, value: str,
):
    if vessl.vessl_api.organization is None:
        vessl.vessl_api.set_organization()

    try:
        vessl.vessl_api.set_project(value)
    except InvalidProjectError:
        print("Invalid project. Please choose a project using `vessl configure`.")
        sys.exit(1)


# Ensure this is called before other options with `is_eager=True` for
# other callbacks that need organization to be preconfigured.
project_name_option = click.option(
    "--project",
    "project_name",
    type=click.STRING,
    hidden=True,
    is_eager=True,
    expose_value=False,
    callback=project_name_callback,
    help="Override default project.",
)
