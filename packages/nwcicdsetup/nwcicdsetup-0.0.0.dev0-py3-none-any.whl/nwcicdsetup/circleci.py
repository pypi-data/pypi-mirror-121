import json
import os
from pathlib import Path
from typing import List

import aiohttp

from .import dotnetdependencyresolver
from .circleciapiclient import CircleCIAPIClient
from .circlecicontext import CircleCIContext
from .githubapiclient import GitHubAPIClient


async def init_async(dummy_env: bool = False) -> CircleCIContext:
    context = CircleCIContext.create_dummy_env(
    ) if dummy_env else CircleCIContext.create_from_environ()
    async with aiohttp.ClientSession() as session:
        circleci_client = CircleCIAPIClient(session, context)
        current_job = await circleci_client.load_job_async(context.build_num)
        last_successful_vcs = await circleci_client.load_previous_successful_vcs(current_job)
        context.current_vcs_revision = current_job.vcs_revision
        context.last_successful_vcs_revision = last_successful_vcs

        print(
            f"Current build url '{current_job.web_url}' for job '{current_job.name}'")
        if last_successful_vcs:
            print(
                f"Last successful vcs '{last_successful_vcs}'")

        await session.close()

    return context


async def check_changes_async(
        circleci_context: CircleCIContext,
        project_dir: str,
        custom_dependencies: List[str] = []) -> bool:

    if not circleci_context.last_successful_vcs_revision:
        print(
            f"No previous successful build found - Assume {project_dir} changed!!!")
        return True

    try:
        dependencies = dotnetdependencyresolver.fetch_dependencies(
            root_dir=circleci_context.working_directory,
            project_dir=project_dir)
    except Exception as e:
        print(f"{e.args}")
        abs_root_path = str(
            Path(circleci_context.working_directory).expanduser().resolve())
        project_dependency = project_dir[len(abs_root_path) + 1:].replace(
            "\\\\", "/").replace("\\", "/").replace(os.sep, "/") + "/*"
        print(f"Using dependency '{project_dependency}' instead")
        dependencies = [project_dependency]

    dependencies += custom_dependencies
    dependencies = list(set(dependencies))  # cut duplicates
    if len(dependencies) <= 0:
        return False

    dependencies.sort()

    async with aiohttp.ClientSession() as session:

        github_client = GitHubAPIClient(session, circleci_context.github_token)

        # don't... just don't: https://youtu.be/KD_1Z8iUDho?t=216
        # if not await github_client.check_dependencies_async(context.project_username, context.project_reponame, context.branch, custom_dependencies):
        #     print("Invalid given custom dependencies - Interrupting")
        #     raise Exception(
        #         f"Invalid given dependencies {json.dumps(custom_dependencies, indent=4)}")

        changeset = await github_client.get_changeset(
            circleci_context.current_vcs_revision,
            circleci_context.last_successful_vcs_revision,
            circleci_context.project_reponame,
            circleci_context.project_username)

        print(
            f"Check-changes on branch '{circleci_context.branch}' for job '{circleci_context.job_name}' on '{project_dir}' with the following dependencies: {json.dumps(dependencies, indent=4)}")
        relevant_changes: List[str] = changeset.find_relevant_changes(
            dependencies)
        relevant_changes.sort()

        if len(relevant_changes):
            print(
                f"Detected relevant changes for {project_dir}: {json.dumps(relevant_changes, indent=4)}")
        else:
            print(f"No relevant changes for {project_dir}")
        await session.close()

        return len(relevant_changes) > 0


async def check_change_async(
        circleci_context: CircleCIContext,
        project_name: str,
        dependencies: List[str] = []) -> bool:
    if not circleci_context.last_successful_vcs_revision:
        print(
            f"No previous successful build found - Assume {project_name} changed!!!")
        return True
    if len(dependencies) <= 0:
        return False

    dependencies.sort()

    async with aiohttp.ClientSession() as session:
        github_client = GitHubAPIClient(session, circleci_context.github_token)

        changeset = await github_client.get_changeset(
            circleci_context.current_vcs_revision,
            circleci_context.last_successful_vcs_revision,
            circleci_context.project_reponame,
            circleci_context.project_username)

        print(
            f"Dependencies for {project_name}: {json.dumps(dependencies, indent=4)}")
        relevant_changes: List[str] = changeset.find_relevant_changes(
            dependencies)
        relevant_changes.sort()

        if len(relevant_changes):
            print(
                f"Detected changes for {project_name}: {json.dumps(relevant_changes, indent=4)}")
        else:
            print(
                f"No relevant changes for {project_name}")
        await session.close()

        return len(relevant_changes) > 0
