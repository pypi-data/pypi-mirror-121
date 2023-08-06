# robotframework-testrail-library

This is a robot framework library to be used with Testrail API.


Installation:
```
pip install robotframework-testrail-library-nerajarolle
```

Example Usage:
```
*** Settings ***
Library   TestrailLibrary  
Suite Setup    connect to testrail    ${SERVER}   
...                 ${TESTRAIL_USERNAME}   ${TESTRAIL_KEY}

*** Test Cases ***
Test Get Project
    [Tags]   project   id
    ${project}   Get Project     1 
    IF  ${project}
        Log To Console  ${project}
    ELSE
        Log To Console    Project id 1 Not found  
    END

Test Get Project by Name
    [Tags]   project  name
    ${project}   Get Project by Name    TA Test Project  
    IF  ${project}
        Log To Console  ${project}
    ELSE
        Log To Console   TA Test Project Not found  
    END

Test Update Run Status 
    [Tags]   update_status
    ${params}   Create Dictionary    project_id=${PROJECT_ID}   run_name=Run number 1  
    ...   suite_name=${SUITE_NAME}   test_name=${TEST_NAME}   section_name=${SUITE_NAME}
    ...   elapsed=20s   comment=a comment   
    ${response}  set status on test run   status_id=1   &{params}  
    IF  ${response}
        log To Console    ${response}
    ELSE 
        log to console    Failed to update run ${response}
    END  

```

