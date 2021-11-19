__author__ = 'tinglev'

import json, sys

from modules.pipeline_steps.abstract_pipeline_step import AbstractPipelineStep
from modules.util import environment
from modules.util.exceptions import PipelineException
from modules.util import nvm, pipeline_data, semver


class NpmVersionChangedStep(AbstractPipelineStep):

    name = "Calculate if a new version should be published later in the pipeline"

    def __init__(self):
        AbstractPipelineStep.__init__(self)


    def get_required_env_variables(self):
        return [environment.PROJECT_ROOT]


    def get_required_data_keys(self):
        return [pipeline_data.NPM_PACKAGE_VERSION, pipeline_data.NPM_PACKAGE_NAME]


    def run_step(self, data):
        '''
        Determins if publishing is based on static version i package.json or 
        if the version should be auto incremented by Evolene.
        '''
        
        data[pipeline_data.NPM_MAJOR_MINOR_LATEST] = self.get_latest_version(data)

        if self.use_automatic_publish(data):
            self.log.info(f'Will automatic publish with increased patch version based on major.minor {data[pipeline_data.NPM_MAJOR_MINOR_LATEST]} in package.json.')
            data = self.increase_version(data)
        
        else:
            self.log.info('No automatic publish, using version in package.json')
            data = self.static_version(data)
        
        self.step_ok()
        return data
    

    def static_version(self, data):
        '''
        Use the version in package.json.
        1. Look in the npm registry to see if the version is al
        '''
        data[pipeline_data.NPM_VERSION_CHANGED] = False
        if not self.version_exists(data):
            data[pipeline_data.NPM_VERSION_CHANGED] = True

        return data


    def increase_version(self, data):
        '''
        If "automaticPublish" is set to true in package.json then increase the patch number for
        the "major.minor" specified in "version".

        Ex:
        package.json
        {
            version : "2.4.8",
            automaticPublish: "true"
        }

        This will happen.
        1. We ingore the patch version "8"
        2. Get the major and minor versoin, "2.4" in package.json version.
        3. Get the latest published version for that major.minor from the NPM Registry. Maybe 2.4.[99]
        4. We increase the patch version 99 by one, to 2.4.100 
        5. New version "2.4.100" is stored in pipeline_data.PACKAGE_JSON
        6. In the publish step the package.json is overwitten with the PACKAGE_JSON content.
        '''

        next_version = semver.get_next(self.get_version_to_increment(data))
        self.log.info(f'Automatic publish will use {next_version}')

        data[pipeline_data.NPM_PACKAGE_VERSION] = next_version
        data[pipeline_data.PACKAGE_JSON]["version"] = next_version
        data[pipeline_data.PACKAGE_JSON]["se.kth.automaticPublish"] = "true"
        data[pipeline_data.NPM_VERSION_CHANGED] = True

        return data


    def get_version_to_increment(self, data):
        '''
        Get the latest published version major.minor.patch from npm,
        or if this is a new branch, only return the major.minor version
        from the package.json
        '''
        published_version = data[pipeline_data.NPM_MAJOR_MINOR_LATEST]

        if published_version:
            return published_version

        return semver.get_major_minor(data[pipeline_data.NPM_PACKAGE_VERSION])


    def version_exists(self, data):
        '''
        Is the version already published?
        '''
        result = False
        name = data[pipeline_data.NPM_PACKAGE_NAME]
        version = data[pipeline_data.NPM_PACKAGE_VERSION]
        found_version = self.get_version(data, name, version)

        if found_version:
            result = True
            self.log.info("%s %s is already published on npm registry.", name, found_version)
        else:
            self.log.info("%s %s does not exist in the npm registry.", name, version)

        return result


    def use_automatic_publish(self, data):
        '''
        To tell Evolene to use automatic publishing to NPM the developer has to
        add the attribute "automaticPublish" to the package.json and set its value
        to true.

        When the automaticPublish is set, Evolene will pushlish using an incremented
        patch. The major and minor version will be the one specified in package.jsons "version".
        '''

        result = False
        try:
            automatic_publish = data[pipeline_data.PACKAGE_JSON]["automaticPublish"]
            result = environment.is_true_value(automatic_publish)
        except:
            self.log.debug("No automaticPublish used")
        
        return result


    def get_latest_version(self, data):
        '''
        Gets the latest version for a specific major.minor version from npm registry.
        '''
        result = None
        try:
            name = data[pipeline_data.NPM_PACKAGE_NAME]
            major_minor = semver.get_major_minor(data[pipeline_data.NPM_PACKAGE_VERSION])

            versions = self.get_versions(data, name, major_minor)

            if versions:
                result = versions[-1] # last element
                
            self.log.info("Latest published version is '%s'", result)

        except:
            self.log.info("Could not find any previous published versions.")

        return result


    def get_version(self, data, name, version):
        '''
        Gets major.minor.patch version. Returns None if no version matches in the npm registry.
        '''
        result = None
        try:
            result = str(nvm.exec_npm_command(data, f'view {name}@"{version}" version', '-json'))
        except:
            self.log.error("Faild to read find any version for %s %s. \n %s", name, version)

        self.log.debug("Got version %s %s", name, version)

        return result


    def get_versions(self, data, name, major_minor):
        '''
        Gets the latest versionws for a specific major.minor version from npm registry as an array.
        '''
        result = []
        try:
            # npm view @babel/core@'7.9' version -json
            #
            # [
            #   "7.9.0",
            #   "7.9.6"
            # ]
            # Note! that if there is only on version matching the result will be a
            # string not an array.
            #
            cli_result = nvm.exec_npm_command(data, f'view -q {name}@"{major_minor}" version', '-json')
            list_or_string = json.loads(cli_result)

            if list_or_string:
                if isinstance(list_or_string, list):
                    result = list_or_string
                else:
                    result.append(list_or_string)

            self.log.info(
                "Published versions for npm view %s@'%s' version -json are %s", name, major_minor, result)

        except json.decoder.JSONDecodeError:
            self.log.info("Found no previous versions for %s.", major_minor)

        return result