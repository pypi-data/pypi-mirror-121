import random
import string

STATUS_VALUES = ["passes", "blocked", "untested", "retest", "failed", "custom_6"]
GET_STATUSES = [{"id": i+1, "name": STATUS_VALUES[i]} for i in range(len(STATUS_VALUES))]

def get_sentence(count):
    text = ''
    for i in range(count):
        text = f'{text} {get_random_string(random.randint(4, 10))}'  
    return text

def get_random_string(count=8):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(count))

class BaseResponse:

    def __init__(self, path, size=250, offset=0, limit=250) -> None:
        self.offset = offset
        self.limit = limit
        self.size = min(size, limit)
        self._links = {
            "next": f"/api/v2/{path}&limit={size}&offset={offset+size}",
            "prev": None if offset==0 else f"/api/v2/{path}&limit={limit}&offset={offset}"
        }
    
    @property
    def get(self):
        return vars(self)

class ProjectsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_projects", size=size, offset=offset, limit=limit)
        self.projects = [
                    {"id": i+offset+1, "name": f"Project {i+offset+1}", 
                    "announcement": f"This is a demo project ", 
                    "show_announcement": False, 
                    "is_completed": False, 
                    "completed_on": None, 
                    "suite_mode": 3, 
                    "url": f"https://example.testrail.net/index.php?/projects/overview/{i+offset+1}"
                    } 
                    for i in range(min(size, limit))
                    ]

class SuitesResponse(BaseResponse):
    def __init__(self, size=250, offset=0, limit=250):
        self.suites = [
            {"id": i+100, "name": f"Suite {i+100}"} for i in range(min(size, limit))
                    ]

class SectionsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_sections", size=size, offset=offset, limit=limit)
        self.sections = [
                    {"id": i+1000, "name": f"Section {i+1000}"} for i in range(min(size, limit))
                    ]

class RunsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_runs", size=size, offset=offset, limit=limit)
        self.runs = [
	            { "id": i+offset+1, "name": f"Test run {i+offset+1}", 'test_id': i+offset+1001, 
                'status_id': random.randint(1, 5), 'created_on': random.randint(16700000, 16800000), 'assignedto_id': None, 
                'comment': get_sentence(random.randint(3, 6)), 'version': None, 'elapsed': f'{random.randint(1, 120)}s', 'defects': None, 
                'created_by': random.randint(35, 40), 'custom_step_results': None, 
                'custom_environment': None, 'attachment_ids': []
                } for i in range(min(size, limit))]
                
class ResultsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_results", size=size, offset=offset, limit=limit)
        self.results = [{"id": i+5000, "test_id": i+1000, 
                        "status_id": random.randint(1, 5),
                        "comment": get_sentence(random.randint(3, 6))} for i in range(min(size, limit))
                        ]
        
class CasesResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_cases", size=size, offset=offset, limit=limit)
        self.cases = [{"id": i+offset+1, "title": f'Case {i+offset+1}', 
            "section_id": 1000} for i in range(min(size, limit))]

class TestsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_tests", size=size, offset=offset, limit=limit)
        self.tests = [{"id": i+offset+1, "title": f'Test Case {i+offset+1}', 
            "status_id": random.randint(1, 5)} for i in range(min(size, limit))]

class AttachmentsResponse(BaseResponse):

    def __init__(self, size=250, offset=0, limit=250) -> None:
        super().__init__("get_tests", size=size, offset=offset, limit=limit)
        self.attachments = [{ "id": i+offset+1, "name": f"Image_{i+offset+1}.jpg", 
                      "size": random.randint(500, 2500), "created_on": random.randint(1578900, 1600000),
                     "project_id": 17, "case_id": random.randint(5000, 5030), 
                     "user_id": random.randint(1, 5), 
                     "result_id": None} 
                     for i in range(min(size, limit))]