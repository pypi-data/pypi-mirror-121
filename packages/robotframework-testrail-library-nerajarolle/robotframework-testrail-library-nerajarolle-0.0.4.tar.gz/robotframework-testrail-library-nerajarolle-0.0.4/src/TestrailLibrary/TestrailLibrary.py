import datetime
import os
from pathlib import Path
from robot.api import logger
from time import sleep
from .apiclient import Apiclient

TEST_TEMPLATE_ID = 1
TEST_TYPE_ID = 3
PRIORITY_DO_NOT_TEST = 1
PRIORITY_CRITICAL = 4

TEST_STATUS_PASSED = 1
TEST_STATUS_FAILED = 5
TEST_STATUS_BLOCKED = 2
TEST_STATUS_UNTESTED = 3
TEST_STATUS_RETEST = 4
TEST_STATUS_CUSTOM_6 = 6
TEST_STATUS_CUSTOM_7 = 7

VERSION = "1.0.0"

class TestrailLibrary:
    
    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    class TestCaseResult:

        def __init__(self):
            self.include_all = True
            self.description = None
            self.project_id = None
            self.run_id = None
            self.run_name = None
            self.section_id = None
            self.section_name = None
            self.suite_id = None
            self.suite_name = None
            self.test_id = None
            self.test_name = None
            self.elapsed = None
            self.comment = None
            self.status_id = TEST_STATUS_UNTESTED
            self.template_id = None
            self.type_id = None
            self.priority_id = None

        def __setitem__(self, item, value):
            setattr(self, item, value)

        def __getitem__(self, key):
            return getattr(self, key)

    def __init__(self, server=None, username=None, key=None):

        self.server = server
        self.client = None
        self.expect_duplicates = False
        if server:
            self.client = Apiclient(server)
            self.client.user = username
            self.client.password = key
        self.test_case_result = self.TestCaseResult()

    def __handle_duplicates(self, msg):
        if self.expect_duplicates:
            logger.warn(msg)
        else:
            raise DuplicateException(msg)

    def connect_to_testrail(self, server, username, key):
        self.client = Apiclient(server)
        self.client.user = username
        self.client.password = key
        self.__check_credentials()
    
    def set_expect_duplicates(self, state):
        self.expect_duplicates = state

    def set_test_case_result(self, **kwargs):
        for key, value in kwargs.items():
            self.test_case_result[f"{key}"] = value

    def __check_credentials(self):
        if not self.client.user or not self.client.password:
           raise AssertionError('Both testrail username and api key should be passed to the library. \
           Please use the "set testrail credentials" keyword to assign them.')

    def __get_with_offset(self, base_url, attribute, **kwargs):
        
        offset = kwargs.get('offset') or 0
        try:
            offset = int(offset)
        except (ValueError):
            offset = 0
        limit = kwargs.get('limit') or 250
        try:
            limit = int(limit)
        except (ValueError):
            limit = 250
        results = []
        url = base_url
        for key, value in kwargs.items():
            if key != 'offset':
                url = f'{url}&{key}={value}'
        count = 0
        while True and count < 50:
            response = self.client.send_get(f'{url}&offset={offset}')
            if not response or not response.get(attribute):
                break
            assert response.get('offset') == offset, f"{response.get('offset')} != {offset}"
            if limit:
                assert response.get('limit') == limit, f"{response.get('limit')} != {limit}"
            results.extend(response.get(attribute))
            offset += limit
            if response.get('size') and response.get('size') < 250 or limit < 250:
                break
            count += 1
            sleep(0.5)
        if len(results) > 50:
            info = f'{results[:20]}\n...truncated...\n{results[:-20]}'
        else:
            info = results
        logger.info(info)  
        return results 

    # PROJECTS
    def get_project_by_name(self, project_name):
        projects = self.get_projects()
        if not isinstance(projects, list): 
            projects = []   
        project = list(filter(lambda x:x.get('name')==project_name, projects))
        logger.info(project)
        if project and len(project) == 1:
            return project[0]
        elif project and len(project) > 1:
            #logger.info(project)
            raise Exception(f'More than 1 projects found with name {project_name}')
        else:
            pass
        return {}

    def get_projects(self, **kwargs):
        url = f'get_projects/'
        return self.__get_with_offset(url, "projects", **kwargs)

    def get_project(self, project_id):
        response = self.client.send_get(f'get_project/{project_id}')
        logger.info(response)
        return response
    
    def add_project(self, project_name, description, show=True, suite_mode=3):
        data = {
            "name": project_name,
            "announcement": description,
            "show_announcement": show,
            "suite_mode": suite_mode
        }
        url = 'add_project'
        response = self.client.send_post(url, data=data)
        return response

    # def update_project(self, project_id, project_name=None, description=None, show=True, is_completed=False):
    #     data = {
    #         "show_announcement": show,
    #         "is_completed": is_completed
    #     }
    #     if project_name:
    #         data["name"] = project_name
    #     if description:
    #         data['announcement'] = description
    #     url = f'update_project/{project_id}'
    #     response = self.client.send_post(url, data=data)
    #     return response

    # def delete_project(self, project_id):
    #     url = f'delete_project/{project_id}'
    #     self.client.send_post(url, data={})

    # TEST SUITES
    def get_suite(self, suite_id):
        url = f'get_suite/{suite_id}'
        response = self.client.send_get(url)
        return response

    def get_suites_in_project(self, project_id):
        url = f'get_suites/{project_id}'
        response = self.client.send_get(url)
        return response

    def get_suites_by_name(self, project_id, suite_name, expect_duplicates=False):
        suites = self.get_suites_in_project(project_id)
        if not isinstance(suites, list): suites = []
        suite = list(filter(lambda x: x.get('name') == suite_name, suites))
        if suite and len(suite) > 1:
            msg = f'More than 1 suite found with name {suite_name} for project {project_id}'
            self.__handle_duplicates(msg)
        return suite

    def add_suite(self, project_id, suite_name, description):
        suite = self.get_suites_by_name(project_id, suite_name)
        if suite:
            return suite[0]
        else:
            url = f'add_suite/{project_id}'
            # logger.console(url)
            data = {
                "name": suite_name,
                "description": description
            }
            response = self.client.send_post(url, data=data)
            return response
    
    def update_suite(self, suite_id, name=None, description=None):
        url = f'update_suite/{suite_id}'
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if data:
            response = self.client.send_post(url, data=data)
            return response
        return {}

    # def delete_suite(self, suite_id):
    #     url = f'delete_suite/{suite_id}'
    #     response = self.client.send_post(url, data={})
    #     return response
    
    # TEST SECTIONS
    def get_sections(self, project_id, suite_id, **kwargs):
        url = f'get_sections/{project_id}&suite_id={suite_id}'
        return self.__get_with_offset(url, "sections", **kwargs)

    def get_section(self, section_id):
        url = f'get_section/{section_id}'
        response = self.client.send_get(url)
        return response

    def get_sections_by_name(self, project_id, suite_id, section_name):
        sections = self.get_sections(project_id, suite_id)
        if not isinstance(sections, list): sections = []
        section = list(filter(lambda x: x.get('name') == section_name, sections))
        if section and len(section) > 1:
            msg = f'Found more than 1 section with name {section_name} for ' \
                  f'project {project_id}, suite {suite_id}...returning first section'
            self.__handle_duplicates(msg)
        return section
        
    def add_section(self, project_id, name, description, suite_id, parent_id=None):
        section = self.get_sections_by_name(project_id, suite_id, name) 
        if section:
            return section[0]
        else:
            url = f'add_section/{project_id}'
            data = {
                "name": name,
                "description": description,
                "suite_id": suite_id
            }
            if parent_id:
                data["parent_id"] = parent_id
            response = self.client.send_post(url, data=data)
            return response

    def add_section_to_suite(self, project_id, name, description, suite_name, parent_id=None):
        suite = self.get_suite_by_name(project_id, name)
        if suite:
            response = self.add_section(name=name, description=description, 
                             project_id=project_id, 
                             suite_id=suite.get("id"),
                             parent_id=parent_id
                             )
            return response
        logger.error(f'Failed to add section "{name}". Suite {suite_name} not found in project {project_id}')
        return {}
    
    def update_section(self, section_id, name=None, description=None):
        url = f'update_section/{section_id}'
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if data:
            response = self.client.send_post(url, data=data)
            return response
        return {}

    # def delete_section(self, section_id):
    #     url = f'delete_section/{section_id}'
    #     response = self.client.send_post(url, data={})
    #     return response

    # CASES
    def get_case(self, test_id, **kwargs):
        url = f'get_case/{test_id}'
        response = self.client.send_get(url, **kwargs)
        logger.info(response)
        return response

    def get_cases(self, project_id, suite_id, **kwargs):
        url = f'get_cases/{project_id}&suite_id={suite_id}'
        return self.__get_with_offset(url, "cases", **kwargs)
    
    def get_cases_by_name(self, project_id, suite_id, section_id, title):
        cases = self.get_cases(project_id, suite_id=suite_id)
        if not isinstance(cases, list): cases = []
        case = list(filter(lambda x: x.get('title') == title and x.get('section_id') == section_id,
                                           cases))
        if case and len(case) > 1:
            msg = f'More than 1 case found with name {title} for project {project_id} ' \
                    f'suite {suite_id} and section {section_id}: {case}'
            self.__handle_duplicates(msg)
        return case

    def add_case(self, project_id, suite_id, title, section_id=None, **kwargs):
        section_name = kwargs.get('section_name') or 'New Section'
        if not section_id:
            sections = self.get_sections_by_name(project_id, suite_id, section_name)
            if not sections:
                section = self.add_section(project_id, name=section_name, description=kwargs.get('description') or 
                'New Section', suite_id=suite_id, parent_id=kwargs.get('parent_id'))
            else:
                if len(sections) > 1:
                    return {}
                section = sections[0]
            section_id = section.get('id')
        case = self.get_cases_by_name(project_id, suite_id, section_id, title) 
        if case: 
            if len(case) > 1:
                return {}
            response = case[0]
        else:
            response = self.add_case_to_section(section_id, title, **kwargs)
        logger.info(response)
        return response

    def add_case_to_section(self, section_id, title, **kwargs):
        template_id = kwargs.get('template_id') or TEST_TEMPLATE_ID
        type_id = kwargs.get('type_id') or TEST_TYPE_ID
        priority_id = kwargs.get('priority_id') or PRIORITY_CRITICAL
        url = f'add_case/{section_id}'
        data = {
            "title": title,
            "template_id": template_id,
            "type_id": type_id,
            "priority_id": priority_id
        }
        response = self.client.send_post(url, data=data)
        logger.info(response)
        return response

    # TESTS
    def get_test(self, test_id):
        url = f'get_test/{test_id}'
        response = self.client.send_get(url)
        logger.info(response)
        return response

    def get_tests(self, run_id, **kwargs):
        url = f'get_tests/{run_id}'
        return self.__get_with_offset(url, "tests", **kwargs)
    
    def get_tests_by_case_name(self, run_id, title):
        tests = self.get_tests(run_id)
        if not isinstance(tests, list): tests = []
        tests_for_title = list(filter(lambda x: x.get('title') == title, tests))
        return tests_for_title

    # RUNS
    def get_runs(self, project_id, **kwargs):
        url = f'get_runs/{project_id}'
        return self.__get_with_offset(url, "runs", **kwargs)

    def get_run(self, run_id):
        """
        """
        url = f'get_run/{run_id}'
        response = self.client.send_get(url)
        logger.info(response)
        return response

    def get_runs_by_name(self, project_id, run_name):
        runs = self.get_runs(project_id)
        if not isinstance(runs, list): runs = []
        run = list(filter(lambda x: x.get('name')== run_name, runs))
        if run and len(run) > 1: 
            msg = f'Found more than 1 test runs with name {run_name} for project {project_id}'
            self.__handle_duplicates(msg)
        return run
    
    def add_run(self, project_id, suite_id, name, description, include_all=True, refs=None, case_ids=None):
        if case_ids and not isinstance(case_ids, list):
            logger.error(f'{case_ids} should be a list')
        run = self.get_runs_by_name(project_id, name)
        if run:
            if len(run) > 1:
                return {}
            return run[0]
        description = description
        include_all = include_all
        url = f'add_run/{project_id}'
        data = {
            "suite_id": suite_id,
            "name": name,
            "description": description,
            "include_all": include_all
            }
        if refs:
            data['refs'] = refs
        if case_ids and not include_all:
            data['case_ids'] = case_ids
        logger.info(f'Adding test run {name} for project {project_id} and suite {suite_id}')
        response = self.client.send_post(url, data=data)
        logger.info(response)
        return response

    def update_run(self, run_id, **kwargs):
        url = f'update_run/{run_id}'
        response = self.client.send_post(url, data=kwargs)
        logger.info(response)
        return response

    def close_run(self, run_id):
        url = f'close_run/{run_id}'
        #logger.info(f'Adding attachment file {filepath} to run {run_id}')
        response = self.client.send_post(url, data={})
        logger.info(response)
        return response

    # def delete_run(self, run_id):
    #     url = f'delete_run/{run_id}'
    #     #logger.info(f'Adding attachment file {filepath} to run {run_id}')
    #     response = self.client.send_post(url, data={})
    #     return response

    # RESULTS
    def get_results(self, test_id, **kwargs):
        url = f'get_results/{test_id}'
        return self.__get_with_offset(url, "results", **kwargs) 

    def get_results_for_case(self, run_id, case_id, **kwargs):
        url = f'get_results_for_case/{run_id}/{case_id}'
        return self.__get_with_offset(url, "results", **kwargs)

    def get_results_for_run(self, run_id, **kwargs):
        url = f'get_results_for_run/{run_id}'
        return self.__get_with_offset(url, 'results', **kwargs)

    def add_result_for_case(self, run_id, case_id, status_id=2, comment=None, elapsed=''):
        case = self.get_case(case_id)
        if elapsed == '0s':
            elapsed = ''
        if not case:
            raise AssertionError(f'Case {case_id} does not exist')
        logger.info(f'Adding status {status_id} to run/test {run_id}/{case_id} ({case.get("name")})')
        url = f'add_result_for_case/{run_id}/{case_id}'
        data = {
            "status_id": status_id,
            "comment": comment,
            "elapsed": elapsed
        }
        response = self.client.send_post(url, data=data)
        logger.info(response)
        return response
    
    def add_result(self):
        # TODO
        pass

    # ATTACHMENTS
    def add_attachment_to_test_run(self, run_id, filepath):
        url = f'add_attachment_to_run/{run_id}'
        logger.info(f'Adding attachment file {filepath} to run {run_id}')
        response = self.client.send_post(url, data=filepath)
        logger.info(response)
        return response

    def get_attachments_for_run(self, run_id:int, **kwargs):
        logger.info(f'Getting attachments for run {run_id}')
        url = f'get_attachments_for_run/{run_id}'
        return self.__get_with_offset(url, "attachments", **kwargs)
        
    def delete_attachment(self, attachment:dict):
        attachment_id = attachment.get('id')
        attachment_name = attachment.get('name')
        attachment_created_timestamp = attachment.get('created_on')
        attachment_created_date = datetime.datetime.fromtimestamp(attachment_created_timestamp)
        logger.info(
            f'Deleting from testrail attachment {attachment_id}:{attachment_name} created on {attachment_created_date}')
        return self.delete_attachment_by_id(attachment_id)

    def delete_attachment_by_id(self, attachment_id):
        url = f'delete_attachment/{attachment_id}'
        response = self.client.send_post(url, data=None)
        logger.info(response)
        return response

    def get_statuses(self):
        """
        """
        url = f'get_statuses/'
        response = self.client.send_get(url)
        logger.info(response)
        return response

    def set_status_on_test_run(self, status_id, **kwargs):
        """
        """
        statuses = self.get_statuses()
        status_ids = list(map(lambda x: x.get("id"), statuses))
        if str(status_id).lower() in ('pass', 'passed'):
            status_id = TEST_STATUS_PASSED
        elif str(status_id).lower() in ('fail', 'failed'):
            status_id = TEST_STATUS_FAILED
        elif str(status_id).isdigit() and int(status_id) == TEST_STATUS_UNTESTED:
            logger.error(f'Setting status to Untested is not supported')
            return {}
        else:
            if not (str(status_id).isdigit() and int(status_id) in status_ids):
                raise Exception(f'{status_id} is not a valid status id.' 
                f'Should be any of {status_ids} or one of the following strings (case insensitive):'  
                'pass, passed, fail, failed') 
        kwargs['status_id'] = status_id
        self.set_test_case_result(**kwargs)
        suite_info = self.test_case_result.suite_id or self.test_case_result.suite_name
        test_case_info = self.test_case_result.test_id or self.test_case_result.test_name
        section_info = self.test_case_result.section_id or self.test_case_result.section_name
        run_info = self.test_case_result.run_id or self.test_case_result.run_name
        if not self.test_case_result.project_id or not suite_info or not test_case_info or not section_info or not run_info:
            if not self.test_case_result.project_id:
                logger.error('Testrail project id missing!')
            elif not run_info:
                logger.error(f'Test run info is missing, you must provide either a run name or a run id')
            elif not suite_info:
                logger.error(f'Suite info is missing, you must provide either a suite name or a suite id')
            elif not section_info:
                logger.error(f'Section info is missing, you must provide either a section name or a section id')
            elif not test_case_info:
                logger.error(f'Test case info is missing, you must provide either a test name or a test id')
            else:
                logger.error(f'Unexpected error for {self.test_case_result.project_id}')
            return {}
        if self.test_case_result.suite_name:
            suite = self.add_suite(project_id=self.test_case_result.project_id,
                                           suite_name=self.test_case_result.suite_name,
                                           description=self.test_case_result.description)
            if not suite:
                return {}
            self.test_case_result.suite_id = suite.get("id")
        if self.test_case_result.section_name:
            section = self.add_section(name=self.test_case_result.section_name, 
                                                   project_id=self.test_case_result.project_id,
                                                   suite_id=self.test_case_result.suite_id,
                                                   description=self.test_case_result.description
                                                   )
            if not section:
                return {}
            self.test_case_result.section_id = section.get("id")
            self.test_case_result.section_name = section.get("name")
        if self.test_case_result.test_name:
            test = self.add_case(section_name=self.test_case_result.section_name,
                                 section_id=self.test_case_result.section_id,
                                                  project_id=self.test_case_result.project_id,
                                                  suite_id=self.test_case_result.suite_id,
                                                  title=self.test_case_result.test_name)
            if not test:
                return {}
            self.test_case_result.test_id = test.get("id")

        if self.test_case_result.run_name:
            run = self.add_run(project_id=self.test_case_result.project_id,
                                                suite_id=self.test_case_result.suite_id,
                                                name=self.test_case_result.run_name,
                                                description=self.test_case_result.description,
                                                include_all=self.test_case_result.include_all)
            if not run:
                return {}
            self.test_case_result.run_id = run.get("id")
        response = self.add_result_for_case(run_id=self.test_case_result.run_id,
                                            case_id=self.test_case_result.test_id,
                                            elapsed=self.test_case_result.elapsed,
                                            status_id=self.test_case_result.status_id,
                                            comment=self.test_case_result.comment
        )
        logger.info(response)
        return response
    
    def upload_robot_to_testrail(self, outputdir, run_id, extension="html", type="log"):
        """
        Keyword used for uploading robot framework report files to Testrail. 

        """        
        files = os.listdir(outputdir)
        html_files = list(filter(lambda x: x.endswith(f'.{extension}') and x.startswith(type), files))
        for log_file in html_files:
            log_path = Path(outputdir) / log_file
            print(f'Adding file {log_path} to run {run_id}')
            response = self.add_attachment_to_test_run(run_id, log_path)
            if response:
                logger.info(f'Successfully uploaded file {log_path} to test run {run_id}: {response}')
            else:
                logger.error(f'Error: {response}')
            return response
              
    def delete_attachments_cleanup(self, run_id, max_to_keep=7):
        attachments = self.get_attachments_for_run(run_id)
        attachments_sorted = sorted(attachments, key=lambda x: x.get("created_on"))
        deleted = []
        if len(attachments_sorted) > max_to_keep:
            to_delete = attachments_sorted[0:len(attachments) - max_to_keep]
            
            for attachment in to_delete:
                #print(f'Deleting attachment {attachment["name"]} from run {run_id}')
                logger.info(f'Deleting attachment {attachment["name"]} from run {run_id}')
                try:
                    deleted_response = self.delete_attachment(attachment)
                    deleted.append(deleted_response)
                except Exception as e:
                    logger.error(e)  
        logger.info(deleted)      
        return deleted


class DuplicateException(BaseException):
    pass