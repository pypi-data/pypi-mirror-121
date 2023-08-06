import unittest
import random
from unittest.mock import patch
from unittest.mock import Mock
from TestrailLibrary.TestrailLibrary import TestrailLibrary as TR, DuplicateException
from .mock_responses import *


class BasicTests(unittest.TestCase):     

    def setUp(self) -> None:
        self.tr = TR("dummy")
        return super().setUp()

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_project(self, mock_get):
        projects = ProjectsResponse(5)
        project = projects.projects[0]
        mock_get.return_value = project
        res = self.tr.get_project(project.get("id"))
        self.assertTrue(res)
        self.assertEqual(res.get("id"), project.get("id"))
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_projects(self, mock_get):
        projects = ProjectsResponse(5)
        mock_get.return_value = projects.get
        res = self.tr.get_projects()
        self.assertTrue(res)
        self.assertTrue(len(res)==5)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=[]))
    def test_get_project_when_empty_projects(self):
        res = self.tr.get_project(1)
        self.assertFalse(res)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_project_by_name(self, mock_get):
        projects = ProjectsResponse(5)
        project = projects.projects[0]
        mock_get.return_value = projects.get
        project_name = project.get("name")
        res = self.tr.get_project_by_name(project_name)
        self.assertTrue(res)
        self.assertEqual(res.get('id'), project.get("id"))
        self.assertEqual(res.get('name'), project_name)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=ProjectsResponse(10).get))
    def test_get_project_by_name_when_name_no_exists(self):
        res = self.tr.get_project_by_name("some project")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=[]))
    def test_get_project_by_name_when_empty_projects(self):
        res = self.tr.get_project_by_name("some project")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={"message": "Error"}))
    def test_get_project_by_name_when_error_response(self):
        res = self.tr.get_project_by_name("some project")
        self.assertFalse(res)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suite(self, mock_get):
        suites = SuitesResponse(10).suites
        mock_get.return_value = suites[0]
        res = self.tr.get_suite(suites[0].get("id"))
        self.assertTrue(res)
        self.assertEqual(res.get('id'), suites[0].get('id'))

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suite_by_name(self, mock_get):
        suites = SuitesResponse(2).suites
        mock_get.return_value = suites
        res = self.tr.get_suites_by_name(17, suites[0].get("name"))
        self.assertTrue(res)
        self.assertEqual(res[0].get('id'), suites[0].get('id'))
        self.assertEqual(res[0].get('name'), suites[0].get("name"))

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suite_by_name_when_no_exists(self, mock_get):
        suites = SuitesResponse(10).suites
        mock_get.return_value = suites
        res = self.tr.get_suites_by_name(17, "some suite")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=[]))
    def test_get_suite_by_name_when_empty(self):
        res = self.tr.get_suites_by_name(17, "some suite")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={"message":"error"}))
    def test_get_suite_by_name_when_error(self):
        res = self.tr.get_suites_by_name(17, "some suite")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suite_by_name_when_duplicates(self, mock_get):
        suites = SuitesResponse(10).suites
        suites.append(suites[0])
        mock_get.return_value = suites
        with self.assertRaises(DuplicateException): 
            res = self.tr.get_suites_by_name(17, suites[0].get("name"))
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suite_by_name_when_duplicates_and_expect(self, mock_get):
        suites = SuitesResponse(10).suites
        suites.append(suites[0])
        mock_get.return_value = suites
        self.tr.set_expect_duplicates(True)
        res = self.tr.get_suites_by_name(17, suites[0].get("name"))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].get("name"), res[1].get("name"))
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_suites_in_project(self, mock_get):
        suites = SuitesResponse(10).suites
        mock_get.return_value = suites
        res = self.tr.get_suites_in_project(17)
        self.assertTrue(res)
        self.assertEqual(res, suites)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_run(self, mock_get):
        runs = RunsResponse(10)
        mock_get.return_value = runs.runs[0]
        res = self.tr.get_run(1)
        self.assertTrue(res)
        self.assertEqual(res.get('id'), 1) 

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_run_by_name(self, mock_get):
        runs = RunsResponse(10)
        mock_get.return_value = runs.get
        run = runs.runs[random.randint(0, len(runs.runs)-1)]
        run_name = run.get('name') 
        res = self.tr.get_runs_by_name(17, run_name)
        self.assertTrue(res)
        self.assertEqual(res[0].get('name'), run_name) 
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(10).get))
    def test_get_run_by_name_when_not_exists(self):
        res = self.tr.get_runs_by_name(17, "test")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(0).get))
    def test_get_run_by_name_when_empty(self):
        res = self.tr.get_runs_by_name(17, "test")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={"message":"error"}))
    def test_get_run_by_name_when_error(self):
        res = self.tr.get_runs_by_name(17, "test")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_run_by_name_when_duplicates(self, mock_get):
        runs = RunsResponse(10)
        runs.runs.append(runs.runs[0])
        mock_get.return_value = runs.get
        with self.assertRaises(DuplicateException): 
            res = self.tr.get_runs_by_name(17, runs.runs[0].get("name"))
        
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(side_effect=[RunsResponse().get, 
                                                 RunsResponse(10, 250).get])) 
    def test_get_runs(self):
        res = self.tr.get_runs(17)
        self.assertTrue(res)
        self.assertTrue(len(res)==260)
        
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(50).get))
    def test_get_runs_with_size_and_no_limit(self):
        res = self.tr.get_runs(17)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(10, limit=50).get)) 
    def test_get_runs_with_size_smaller_than_limit(self):
        res = self.tr.get_runs(17, limit=50)
        self.assertTrue(res)
        self.assertTrue(len(res)==10)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(50, limit=50).get)) 
    def test_get_runs_with_size_equal_to_limit(self):
        res = self.tr.get_runs(17, limit=50)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(60, limit=50).get)) 
    def test_get_runs_with_size_greater_than_limit(self):
        res = self.tr.get_runs(17, limit=50)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(1).get)) 
    def test_get_runs_with_size_one(self):
        res = self.tr.get_runs(17)
        self.assertTrue(res)
        self.assertTrue(len(res)==1)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(1, limit=1).get)) 
    def test_get_runs_with_size_one_and_limit_one(self):
        res = self.tr.get_runs(17, limit=1)
        self.assertTrue(res)
        self.assertTrue(len(res)==1)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(50, offset=5).get)) 
    def test_get_runs_with_offset(self):
        res = self.tr.get_runs(17, offset=5)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)
        self.assertEqual(res[0].get('id'), 6)
        self.assertEqual(res[4].get('id'), 10)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(50, offset=5, limit=2).get)) 
    def test_get_runs_with_offset_and_limit(self):
        res = self.tr.get_runs(17, offset=5, limit=2)
        self.assertTrue(res)
        self.assertTrue(len(res)==2)
        self.assertEqual(res[0].get('id'), 6)
        self.assertEqual(res[1].get('id'), 7)
    
    

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_case_by_name(self, mock_get):
        cases_1 = CasesResponse()
        cases_2 = CasesResponse(10, 250)
        mock_get.side_effect=[cases_1.get, cases_2.get]
        res = self.tr.get_cases_by_name(17, 1000, 1000, cases_1.cases[0].get("title"))
        self.assertTrue(res)
        self.assertEqual(res[0].get('title'), cases_1.cases[0].get("title")) 
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(20).get))
    def test_get_case_by_name_when_no_exists(self):
        res = self.tr.get_cases_by_name(17, 1000, 1000, "Case 500")
        self.assertFalse(res)  
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(0).get))
    def test_get_case_by_name_when_empty(self):
        res = self.tr.get_cases_by_name(17, 1000, 1000, "Case 500")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={"message":"error"}))
    def test_get_case_by_name_when_error(self):
        res = self.tr.get_cases_by_name(17, 1000, 1000, "Case 500")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_case_by_name_when_duplicates(self, mock_get):
        cases = CasesResponse(10)
        new_cases = CasesResponse(1)
        cases.cases.append(new_cases.cases[0])
        mock_get.return_value = cases.get
        with self.assertRaises(DuplicateException): 
            res = self.tr.get_cases_by_name(17, 1000, 1000, cases.cases[0].get("title"))

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_case_by_name_when_duplicates_and_expect(self, mock_get):
        cases = CasesResponse(10)
        new_cases = CasesResponse(1)
        cases.cases.append(new_cases.cases[0])
        mock_get.return_value = cases.get
        self.tr.set_expect_duplicates(True)
        res = self.tr.get_cases_by_name(17, 1000, 1000, cases.cases[0].get("title"))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].get("name"), res[1].get("name"))
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(side_effect=[CasesResponse().get, 
                                                CasesResponse(10, offset=250).get]))
    def test_get_cases(self):
        res = self.tr.get_cases(17, 1000)
        self.assertTrue(res)
        self.assertTrue(len(res)==260)
        
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(20).get))
    def test_get_cases_with_size_and_no_limit(self): 
        res = self.tr.get_cases(17, 1000)
        self.assertTrue(res)
        self.assertTrue(len(res)==20)
        self.assertEqual(res[0].get("id"), 1)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(20, limit=5).get))
    def test_get_cases_with_size_and_limit(self): 
        res = self.tr.get_cases(17, 1000, limit=5)
        self.assertTrue(res)
        self.assertTrue(len(res)==5)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(5, limit=10).get))
    def test_get_cases_with_size_smaller_than_limit(self): 
        res = self.tr.get_cases(17, 1000, limit=10)
        self.assertTrue(res)
        self.assertTrue(len(res)==5)
        self.assertEqual(res[0].get("id"), 1)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(5, limit=5).get))
    def test_get_cases_with_size_equal_to_limit(self): 
        res = self.tr.get_cases(17, 1000, limit=5)
        self.assertTrue(res)
        self.assertTrue(len(res)==5)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(20, limit=10).get))
    def test_get_cases_with_size_greater_than_limit(self): 
        res = self.tr.get_cases(17, 1000, limit=10)
        self.assertTrue(res)
        self.assertTrue(len(res)==10)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(1).get))
    def test_get_cases_with_size_one(self): 
        res = self.tr.get_cases(17, 1000)
        self.assertTrue(res)
        self.assertTrue(len(res)==1)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(1, limit=1).get))
    def test_get_cases_with_size_one_and_limit_one(self): 
        res = self.tr.get_cases(17, 1000, limit=1)
        self.assertTrue(res)
        self.assertTrue(len(res)==1)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(50, offset=5).get)) 
    def test_get_cases_with_offset(self):
        res = self.tr.get_cases(17, 1000, offset=5)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)
        self.assertEqual(res[0].get('id'), 6)
        self.assertEqual(res[4].get('id'), 10)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=CasesResponse(50, offset=5, limit=2).get)) 
    def test_get_cases_with_offset_and_limit(self):
        res = self.tr.get_cases(17, 1000, offset=5, limit=2)
        self.assertTrue(res)
        self.assertTrue(len(res)==2)
        self.assertEqual(res[0].get('id'), 6)
        self.assertEqual(res[1].get('id'), 7)


    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(50).get))
    @patch('TestrailLibrary.apiclient.Apiclient.send_post', Mock(return_value=RunsResponse(1, offset=1000).runs[0]))
    def test_add_run(self):
        res = self.tr.add_run(17, 1000, name="Test run 1001", description="")
        self.assertTrue(res)
        self.assertEqual(res.get("name"), "Test run 1001")

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=RunsResponse(10).get))
    def test_add_run_when_exists(self):
        res = self.tr.add_run(17, 1000, name="Test run 1", description="")
        self.assertTrue(res)
        self.assertEqual(res.get('name'), "Test run 1") 

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_add_run_when_duplicates(self, mock_get):
        runs = RunsResponse(10)
        runs.runs.append(runs.runs[0])
        mock_get.return_value = runs.get
        with self.assertRaises(DuplicateException): 
            res = self.tr.add_run(17, 1000, name=runs.runs[0].get("name"), description="")
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_add_run_when_duplicates_and_expected(self, mock_get):
        runs = RunsResponse(10)
        runs.runs.append(runs.runs[0])
        mock_get.return_value = runs.get
        self.tr.set_expect_duplicates(True)
        res = self.tr.add_run(17, 1000, name=runs.runs[0].get("name"), description="")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_add_case(self, mock_get, mock_post):
        suites = SuitesResponse(2)
        cases = CasesResponse(10)
        sections = SectionsResponse(2)
        section_name = sections.sections[0].get("name")
        mock_post.return_value = suites.suites[0]
        mock_get.side_effect = [
            suites.suites[0], sections.get, cases.get
        ]
        suite_id = suites.suites[0].get('id')
        res = self.tr.add_case(17, suite_id, "New Case", section_name=section_name)
        self.assertTrue(res)
        self.assertEqual(res.get('id'), suites.suites[0].get('id')) 
        self.assertEqual(res.get('title'), suites.suites[0].get('title')) 
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')  
    def test_add_case_when_exists(self, mock_get):
        cases = CasesResponse(10)
        suites = SuitesResponse(1)
        title = cases.cases[0].get("title")
        sections = SectionsResponse(2)
        section_name = sections.sections[0].get("name")
        case_id = cases.cases[0].get("id")
        mock_get.side_effect = [
            suites.suites[0], sections.get, cases.get
        ]
        res = self.tr.add_case(17, suites.suites[0].get("id"), title, section_name=section_name)
        self.assertTrue(res)
        self.assertEqual(res.get("id"), case_id)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')  
    def test_add_case_when_duplicates(self, mock_get):
        cases = CasesResponse(10)
        suites = SuitesResponse(1)
        new_cases = CasesResponse(1)
        new_case = new_cases.cases[0]
        new_case["id"] = 11
        cases.cases.append(new_case)
        title = cases.cases[0].get("title")
        sections = SectionsResponse(2)
        section_name = sections.sections[0].get("name")
        mock_get.side_effect = [
            suites.suites[0], sections.get, cases.get
        ]
        with self.assertRaises(DuplicateException):
            res = self.tr.add_case(17, suites.suites[0].get("id"), title, section_name=section_name)
    

    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=ResultsResponse(50).get)) 
    def test_get_results_for_case(self):
        res = self.tr.get_results_for_case(1, 1)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=ResultsResponse(0).get)) 
    def test_get_results_for_case_when_zero(self):
        res = self.tr.get_results_for_case(1, 1)
        self.assertFalse(res)
        self.assertTrue(len(res)==0)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={})) 
    def test_get_results_for_case_when_empty(self):
        res = self.tr.get_results_for_case(1, 1)
        self.assertFalse(res)
        self.assertTrue(len(res)==0)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=ResultsResponse(50).get)) 
    def test_get_results_for_run(self):
        res = self.tr.get_results_for_run(1)
        self.assertTrue(res)
        self.assertTrue(len(res)==50)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value=ResultsResponse(0).get)) 
    def test_get_results_for_run_when_empty(self):
        res = self.tr.get_results_for_run(1)
        self.assertFalse(res)
        self.assertTrue(len(res)==0)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get', Mock(return_value={"message": "error"}))
    def test_get_results_for_run_when_error(self):
        res = self.tr.get_results_for_run(1)
        self.assertFalse(res)
        self.assertTrue(len(res)==0)

    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_add_result_to_test(self, mock_get, mock_post):
        cases = CasesResponse(10)
        results = ResultsResponse(1)
        result = results.results[0]
        mock_get.return_value = cases.cases[0]
        mock_post.return_value = result
        res = self.tr.add_result_for_case(1000, 5000, 1, comment=result.get("comment"))
        self.assertTrue(res)
        self.assertEqual(res, result)
       
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run(self, mock_get, mock_post):
        results = ResultsResponse(1)
        result = results.results[0]
        mock_post.return_value = result
        mock_get.side_effect = [GET_STATUSES, CasesResponse(10).get]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_id=1, section_id=1000,
            test_id=5000, run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_suite_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(1)
        result = results.results[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, suites.suites, CasesResponse(10).get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_name=suites.suites[0].get("name"), 
            section_id=1000, test_id=5000, run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_suite_and_section_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        sections = SectionsResponse(10)
        section = sections.sections[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, suites.suites, sections.get, CasesResponse(10).get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_name=suites.suites[0].get("name"), 
            section_name=section.get("name"), test_id=5000, run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_suite_and_section_and_test_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        sections = SectionsResponse(10)
        section = sections.sections[0]
        cases = CasesResponse(10)
        case = cases.cases[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, suites.suites, sections.get, cases.get, 
                                 sections.get, cases.get, cases.get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_name=suites.suites[0].get("name"), 
            section_name=section.get("name"), test_name=case.get("title"), run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_all_names(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        sections = SectionsResponse(10)
        section = sections.sections[0]
        cases = CasesResponse(10)
        case = cases.cases[0]
        runs = RunsResponse(5)
        run = runs.runs[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, suites.suites, sections.get, cases.get, 
                                 sections.get, cases.get, runs.get, cases.get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_name=suites.suites[0].get("name"), 
            section_name=section.get("name"), test_name=case.get("title"), run_name=run.get("name") )
        self.assertTrue(res)
        self.assertEqual(res, result)

    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_section_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        sections = SectionsResponse(10)
        section = sections.sections[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, sections.get, CasesResponse(10).get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_id=suites.suites[0].get("id"), 
            section_name=section.get("name"), test_id=5000, run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_test_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        cases = CasesResponse(10)
        case = cases.cases[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, cases.get, SectionsResponse(10).get, cases.get, cases.get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_id=suites.suites[0].get("id"), 
            section_id=1000, test_name=case.get("title"), run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_run_name(self, mock_get, mock_post):
        results = ResultsResponse(1)
        suites = SuitesResponse(2)
        result = results.results[0]
        cases = CasesResponse(10)
        runs = RunsResponse(5)
        run = runs.runs[0]
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, runs.get, cases.get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_id=suites.suites[0].get("id"), 
            section_id=1000, test_id=5000, run_name=run.get("name") )
        self.assertTrue(res)
        self.assertEqual(res, result)

    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_test_name_when_duplicate(self, mock_get, mock_post):
        results = ResultsResponse(1)
        result = results.results[0]
        cases = CasesResponse(10)
        case = cases.cases[0]
        new_cases = CasesResponse(1, 10)
        new_case = new_cases.cases[0]
        new_case["title"] = case.get("title")
        cases.cases.append(new_case)
        mock_post.return_value = result
        mock_get.side_effect = [ GET_STATUSES, SectionsResponse(10).get, cases.get, cases.get ]
        res = self.tr.set_status_on_test_run(1, project_id=17, suite_id=100, 
            section_id=1000, test_name=case.get("title"), run_id=1 )
        self.assertTrue(res)
        self.assertEqual(res, result)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get') 
    def test_set_status_on_test_run_using_wrong_status_id(self, mock_get): 
        mock_get.return_value = GET_STATUSES
        with self.assertRaises(Exception):
            res = self.tr.set_status_on_test_run(8, project_id=17, suite_id=100, 
                section_id=1000, test_id=1, run_id=1 )
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    def test_update_run(self, mock_post):
        run = RunsResponse(1).runs[0]
        mock_post.return_value = run
        res = self.tr.update_run(1, description="New description")
        self.assertEqual(res, run)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_test(self, mock_get):
        test = CasesResponse(1).cases[0]
        mock_get.return_value = test
        res = self.tr.get_test(1)
        self.assertEqual(res, test)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_tests(self, mock_get):
        mock_get.return_value = TestsResponse(10).get
        res = self.tr.get_tests(1)
        self.assertEqual(len(res), 10)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_tests_by_case_name(self, mock_get):
        tests = TestsResponse(10)
        test = tests.tests[0]
        mock_get.return_value = tests.get
        res = self.tr.get_tests_by_case_name(1, test.get("title"))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], test)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_tests_by_case_name_when_not_found(self, mock_get):
        tests = TestsResponse(10)
        test = tests.tests[0]
        mock_get.return_value = tests.get
        res = self.tr.get_tests_by_case_name(1, "New Test")
        self.assertFalse(res)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    def test_add_attachment_to_test_run(self, mock_post):
        run = RunsResponse(1).runs[0]
        mock_post.return_value = {"attachment_id": 12345}
        res = self.tr.add_attachment_to_test_run(run_id=run.get("id"), filepath="filepath")
        self.assertTrue(res)
        self.assertEqual(res.get("attachment_id"), 12345)

    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_attachments_for_run(self, mock_get):
        run = RunsResponse(1).runs[0]
        mock_get.return_value = AttachmentsResponse(10).get
        res = self.tr.get_attachments_for_run(run_id=run.get("id"))
        self.assertEqual(len(res), 10)
    
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_get_attachments_for_run_when_not_found(self, mock_get):
        run = RunsResponse(1).runs[0]
        mock_get.return_value = AttachmentsResponse(0).get
        res = self.tr.get_attachments_for_run(run_id=run.get("id"))
        self.assertEqual(len(res), 0)
    
    @patch('os.listdir')
    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    def test_upload_robot_to_testrail(self, mock_post, mock_listdir):
        info = {"run_id": 1, "project_id": 17}
        #text = io.BytesIO(str(info).encode('utf8'))
        files = ["log.html", "report.html", "output.xml"]
        mock_listdir.return_value = files 
        run = RunsResponse(1).runs[0]
        mock_post.return_value = {"attachment_id": 12345}
        res = self.tr.upload_robot_to_testrail("", run.get("id"))
        self.assertEqual(res.get("attachment_id"), 12345)


    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    def test_delete_attachment(self, mock_post):
        attachment = AttachmentsResponse(1).attachments[0]
        mock_post.return_value = {"attachment_id": attachment.get("id")}
        res = self.tr.delete_attachment(attachment)
        self.assertEqual(res.get("attachment_id"), attachment.get("id"))

    @patch('TestrailLibrary.apiclient.Apiclient.send_post')
    @patch('TestrailLibrary.apiclient.Apiclient.send_get')
    def test_delete_attachments_cleanup(self, mock_get, mock_post):
        
        run = RunsResponse(1).runs[0]
        attachments = AttachmentsResponse(10)
        mock_get.return_value = attachments.get 
        deleted_response = [{"attachment_id": attachments.attachments[i].get("id")} 
                        for i in range(len(attachments.attachments[:-7]))]
        mock_post.side_effect = deleted_response
        res = self.tr.delete_attachments_cleanup(run.get("id"))
        self.assertEqual(res, deleted_response)

if __name__ == "__main__":
    unittest.main()
        

