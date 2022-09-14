__author__ = 'tinglev@kth.se'

import os
from os import environ
import sys
import logging
from modules.pipelines.docker_deploy_pipeline import DockerDeployPipeline
from modules.pipelines.npm_pipeline import NpmPipeline
from modules.util import environment, file_util, slack
import modules.util.log as log


def select_and_run_pipeline():

    logger = logging.getLogger(__name__)
    docker_conf = file_util.get_absolue_path('/docker.conf')
    has_docker_conf = os.path.isfile(docker_conf)
    npm_conf = file_util.get_absolue_path('/npm.conf')
    has_npm_conf = os.path.isfile(npm_conf)

    if has_docker_conf:
        logger.info("Has docker.conf")
        docker_pipeline = DockerDeployPipeline()
        docker_pipeline.run_pipeline()

    if has_npm_conf:
        logger.info("Has npm.conf")
        npm_pipeline = NpmPipeline()
        npm_pipeline.run_pipeline()

    if has_docker_conf is False and has_npm_conf is False:
        clone_path = environment.get_clone_path()
        workspace = environment.get_project_root()
        text = f'Could not find any `docker.conf` or `npm.conf` in {workspace} (local path for repo clone {clone_path}).'
        slack.send(text)
        logger.error(text)
        sys.exit(1)


def main():
    log.init_logging()
    evo_dir = environment.get_evolene_directory()
    if not evo_dir:
        logging.getLogger(__name__).fatal(
            'Missing EVOLENE_DIRECTORY environment')
        sys.exit(1)
    os.chdir(evo_dir)
    select_and_run_pipeline()


if __name__ == '__main__':
    main()
