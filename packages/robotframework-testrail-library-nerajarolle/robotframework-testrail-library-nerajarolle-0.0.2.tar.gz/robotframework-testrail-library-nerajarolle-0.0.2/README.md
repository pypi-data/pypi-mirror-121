# robotframework-testrail-library

This is a robot framework library to be used with Testrail API.


Installation:
```
pip install robotframework-testrail-library-nerajarolle
```

Example Usage:
```
*** Settings ***
Library   TestrailLibrary   ${SERVER}
Suite Setup    set testrail credentials  
...   ${TESTRAIL_USERNAME}   ${TESTRAIL_KEY}

*** Test Cases ***
Test Get Project
    [Tags]   project
    ${id}  get Project id   TA Test Project  
    IF  ${id}
        Log To Console  ${id}
    ELSE
        Log To Console  Not found  
    END
```

