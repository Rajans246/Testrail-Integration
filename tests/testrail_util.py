import os
from tests.testrail import *
from tests.testrail import APIClient

class TestRailUtil:
    testrail = None
    project = None
    suite = "TestDem"
    section = None
    testCase = None
    run = None

    str_testcaseID = None
    scenario_status = None

    @staticmethod
    def create_testrail_instance(url, username, password):
        try:
            TestRailUtil.testrail = APIClient(url)
            TestRailUtil.testrail.user = username
            TestRailUtil.testrail.password = password
            print("Testrail Instance Created")
        except Exception as e:
            print("Error:", str(e))

    # @staticmethod
    # def create_testrail_project(project_name):
    #     try:
    #         TestRailUtil.project = TestRailUtil.testrail.send_post(
    #             'add_project',
    #             {'name': project_name}
    #         )
    #         print("TestRail Project Added Successfully")
    #     except Exception as e:
    #         print("Error:", str(e))
    @staticmethod
    def create_testrail_project(project_name):
        try:
            # Get the list of projects

            projects_response = TestRailUtil.testrail.send_get('get_projects')
            projects = projects_response.get('projects', []) 
            # print("projectsss")
            # print(projects)

            # Check if a project with the given name already exists
            existing_project = next((project for project in projects if project['name'] == project_name), None)
            # print("exist    projectttttt")
            # print(existing_project)

            if existing_project:
                # Project with the given name already exists, use its ID
                # print("check existing")
                TestRailUtil.project = existing_project
                print(f"TestRail Project '{project_name}' Already Exists (ID: {existing_project['id']})")
                return existing_project['id']
            else:
                # Project with the given name does not exist, create a new project
                TestRailUtil.project = TestRailUtil.testrail.send_post(
                    'add_project',
                    {'name': project_name}
                )
                print(f"TestRail Project '{project_name}' Added Successfully (ID: {TestRailUtil.project['id']})")
                return TestRailUtil.project['id']
        except Exception as e:
            print("Error:", str(e))
        



    @staticmethod
    def create_testrail_suite_test(project_id, suite_name):
        try:
            # print("before start")
            existing_suite_id = TestRailUtil.get_suite_id_by_name(project_id, suite_name)

            # print("exissssst suite id was")
            # print("exissssst suite id was 1")
            # print("exissssst suite id was 2")
            # print(existing_suite_id)
            if existing_suite_id:
                print(f"TestRail Suite '{suite_name}' Already Exists (ID: {existing_suite_id})")
                return existing_suite_id
            
            # if project_id:
            else:
                suite_data = {'name': suite_name}
                # print("in the if before suite data")
                suite_data['project_id'] = str(project_id)  # Convert project_id to string
                # print(suite_data)
                # print(suite_name)
                # Add the suite using send_post
                TestRailUtil.suite = TestRailUtil.testrail.send_post(f'add_suite/{project_id}', suite_data)
                print("TestRail Suite added successfully")
                suites = TestRailUtil.testrail.send_get(f'get_suites/{project_id}')
                print("Suites after adding a new suite:")
                print(suites)
                if suites:
                    new_suite = next((s for s in suites if s['name'] == suite_name), None)
                    if new_suite:
                        suite_id = new_suite['id']
                        print(f"Suite ID after adding a new suite: {suite_id}")
                return suite_id
                


        except Exception as e:
                print("failed in the test suite adding")
                print("Error:", str(e))
        


    @staticmethod
    def create_testrail_section(project_id, suite_id, section_name):
        try:
            # print("Started in the section")
            print(f"Project ID: {project_id}, Suite ID: {suite_id}, Section Name: {section_name}")
            # Check if a section with the same name already exists
            existing_section = TestRailUtil.get_existing_section(project_id, suite_id, section_name)

            if existing_section:
                print(f"Section '{section_name}' already exists. Section ID: {existing_section['id']}")
                return existing_section['id']
            else:
        
                # print("started in the section")
                # print(project_id)
                # print(type(project_id))
                # print("section_name")
                # print(section_name)
                # print("uou yahs")
                section_data = {'name': section_name}
                # print(suite_id)
                if suite_id:
                    section_data['suite_id'] = int(suite_id)
                # print("tet section")
                # print(section_data)
                print("project id ", project_id)
                if project_id:
                    section_data['project_id'] = int(project_id)
                    print(section_data)
                TestRailUtil.section = TestRailUtil.testrail.send_post(f'add_section/{project_id}',section_data)
                
                print("TestRail Section Added Successfully")
                sections_id = TestRailUtil.get_sections(project_id, suite_id)
                # print("secsss_id")
                # print(sections_id)
                # print(type(sections_id))
                my_id = sections_id['id']
                # print(my_id)
                # print(type(my_id))
                myIdInt = int(my_id)
                # print(type(int(my_id)))
                return myIdInt
        except Exception as e:
            print("testrail section failed")
            print("Error:", str(e))

    @staticmethod
    def create_testrail_testcases( project_id, suite_id,section_id, test_case_title):
        try:
            # custom_case_fields = TestRailUtil.testrail.send_get('get_case_fields')
            existing_test_case = TestRailUtil.get_existing_test_case(project_id, suite_id, test_case_title)

            # print("existingggg test casess")
            
            # print(existing_test_case)
            if existing_test_case:
                print(f"Test case '{test_case_title}' already exists in Section ID: {section_id}. Case ID: {existing_test_case['id']}")
                return existing_test_case['id']
            else:
    
                case_data = {'title': test_case_title}
                if section_id:
                    case_data['section_id'] = int(section_id)
                TestRailUtil.testCase = TestRailUtil.testrail.send_post(f'add_case/{section_id}',case_data)
                print("TestRail Testcase Added Successfully")
        except Exception as e:
            print("Error:", str(e))

    @staticmethod
    def create_testrail_run(project_id, suite_id, test_run_name):
        try:
            # Check if a run with the same name already exists
            
           # projects_response = TestRailUtil.testrail.send_get('get_projects')
            existing_runs_response = TestRailUtil.testrail.send_get(f'get_runs/{project_id}&suite_id={suite_id}')
            # print("exis runs")
            new_existing = TestRailUtil.testrail.send_get(f'get_variables/{project_id}')
            # print("new existing____")
            # print(new_existing)
            # print(existing_runs_response)
            
            if 'runs' in existing_runs_response:
                existing_runs = existing_runs_response['runs']
                existing_run = next((run for run in existing_runs if run['name'] == test_run_name), None)
                # projects = projects_response.get('projects', []) 

                if existing_run:
                    # Run with the same name already exists, return its ID
                    existing_run_id = existing_run['id']
                    print(f"TestRail test Run with name '{test_run_name}' already exists. Run ID: {existing_run_id}")
                    return existing_run_id
                else:
                    # Run does not exist, create a new run
                    run_data = {'name': test_run_name, 'suite_id': int(suite_id)}
                    if project_id:
                        run_data['project_id'] = int(project_id)
                    TestRailUtil.run = TestRailUtil.testrail.send_post(f'add_run/{project_id}', run_data)
                    new_run_id = TestRailUtil.run['id']
                    print("TestRail test Run Added Successfully. New Run ID:", new_run_id)
                    result_data = os.path.join(os.path.dirname(__file__), 'testdata.json')
                    with open(result_data, 'r') as json_file:
                        data = json.load(json_file)

                    # Update the value of str_testrunID
                    data['str_testrunID'] = new_run_id

                    # Save the updated JSON data back to the file
                    with open('your_json_file.json', 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                    
                    return new_run_id

            else:
                print("Error: 'runs' key not found in the response.")
                return None

        except Exception as e:
                print("Error:", str(e))
                return None
        

    #     try:
    #         run_data = {'name': test_run_name, 'suite_id': int(suite_id)}
    #         if project_id:
    #             run_data['project_id'] = int(project_id)
    #         TestRailUtil.run = TestRailUtil.testrail.send_post(f'add_run/{project_id}',run_data)
    #         print("TestRail test Run Added Successfully")
    #     except Exception as e:
    #         print("Error:", str(e))

    @staticmethod
    def add_test_result(test_run_id):
        # try:
        #     # if str(test_case_id) == str(TestRailUtil.str_testcaseID):
        #     if str(test_case_id) == test_case_id:
        #         print("test case_ id")
        #         print(test_case_id)
        #         custom_result_fields = TestRailUtil.testrail.send_get('get_result_fields')
        #         status_id = 1 if TestRailUtil.scenario_status == "PASSED" else 5
        #         result_data = {'status_id': status_id, 'custom_result_fields': custom_result_fields}
        #         print("result data")
        #         print("run id ")                
        #         print("#@!")
        #         print(test_run_id)
        #         run_id = test_run_id
        #         run_id = int(run_id)
        #         result_data['run_id'] = run_id
        #         print(run_id)
        #         TestRailUtil.testrail.send_post(f'add_result_for_case/{run_id}/{test_case_id}', result_data)
        #         print("Testrail Run id:", run_id)
        #         print("Test Result Added to Testrail")
        # except Exception as e:
        #     print("Error:", str(e))
        try:
            # Check if the test run exists
            run_info = TestRailUtil.testrail.send_get(f'get_run/{test_run_id}')
            if 'error' in run_info:
                print(f"Error: Test run with ID {test_run_id} not found.")
                return
            
            # status_id = 1 if TestRailUtil.scenario_status == "PASSED" else 5
            result_data = os.path.join(os.path.dirname(__file__), 'result.json')
            with open(result_data, "r") as json_file:
                data = json.load(json_file)

            print("your data's are")
            print(data)
            dd = {'results': [{'case_id': 18, 'status_id': 1}]}
            # Add the result for the specified test run and test case
            TestRailUtil.testrail.send_post(f'add_results_for_cases/{test_run_id}',data)
            
            print("Test Result Added to TestRail")
        except Exception as e:
            print("Error:", str(e))


    @staticmethod
    def get_sections(project_id, suite_id):
        try:
            # print("get sec lat")
            # Send GET request to get sections
            sections_data = TestRailUtil.testrail.send_get(f'get_sections/{project_id}&suite_id={suite_id}')
            sections = sections_data.get('sections', [])
            # print("get lat section")
            # print(sections)
            

            if sections:
                # Filter sections based on suite_id
                # print("entered if secs")
                filtered_sections = [section for section in sections if section['suite_id'] == int(suite_id)]
                if filtered_sections:
                    # Sort sections by ID in descending order to get the latest one
                    latest_section = max(filtered_sections, key=lambda x: x['id'])
                    print("Latest Section with Suite ID and Project ID:")
                    print(f"Section ID: {latest_section['id']}")
                    return latest_section
                else:
                    print("No sections found with the specified Suite ID and Project ID.")
                    return None
            else:
                print("No sections found for the specified Project ID.")
                return None
        except Exception as e:
            print("Failed to get sections")
            print("Error:", str(e))
            return None

    @staticmethod
    def get_suite_id_by_name(project_id, suite_name):
        try:
            # Get the list of suites for the project
            # print("get names proj, suitename")
            # print(project_id)
            # print(suite_name)
            suites_response = TestRailUtil.testrail.send_get(f'get_suites/{project_id}')
            # print("suites_response")
            # print(suites_response)
            if isinstance(suites_response, list):
                # Sort suites by some criteria (e.g., creation time) in descending order
                sorted_suites = sorted(suites_response, key=lambda x: x.get('created_on', 0), reverse=True)
                
                # Get the latest suite
                latest_suite = sorted_suites[0] if sorted_suites else None
                
                if latest_suite:
                    # Latest suite found, return its ID
                    print(f"Latest Suite ID: {latest_suite['id']}")
                    return latest_suite['id']
                else:
                    print("No suites found.")
                    return None
            else:
                print("Error: Response is not a list.")
                return None
            
        except Exception as e:
            print("Error:", str(e))

    @staticmethod
    def get_existing_section(project_id, suite_id, section_name):
        try:
            # Send GET request to get sections
            sections_data = TestRailUtil.testrail.send_get(f'get_sections/{project_id}&suite_id={suite_id}')
            sections = sections_data.get('sections', [])

            # Filter sections based on name
            existing_section = next((section for section in sections if section['name'] == section_name), None)
            return existing_section

        except Exception as e:
            print("Failed to get sections")
            print("Error:", str(e))
            return None
        
    
    @staticmethod
    def get_existing_test_case(project_id, suite_id, test_case_title):
        try:
            # Send GET request to get cases in the section
            print("get exisiting casesss")
            # cases_data = TestRailUtil.testrail.send_get(f'get_cases/{section_id}')
            cases_data = TestRailUtil.testrail.send_get(f'get_cases/{project_id}&suite_id={suite_id}')
            print("case_data_001")
            print(cases_data)
            cases = cases_data.get('cases', [])
            # print("scases")
            # print(cases)

            # Filter cases based on title
            existing_case = next((case for case in cases if case['title'] == test_case_title), None)
            return existing_case

        except Exception as e:
            print("Failed to get test cases in the section")
            print("Error:", str(e))
            return None

