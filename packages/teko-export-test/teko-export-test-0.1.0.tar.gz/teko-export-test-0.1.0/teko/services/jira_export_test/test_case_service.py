import re
import copy
from teko.models.jira_export_test.storage import Storage
from teko.models.jira_export_test.test_case import TestCase
from teko.models.jira_export_test.test_step import TestStep

__author__ = 'Dungntc'


class TestCaseService:

    @classmethod
    def create_test_case(cls, **kwargs):
        test_case = TestCase(**kwargs)
        Storage.list_test_case.append(test_case)
        return test_case

    @classmethod
    def find_test_case(cls, test_id, test_index=None):
        for test_case in Storage.list_test_case:
            if test_case.test_id == test_id:
                new_test_case = copy.copy(test_case)
                if test_index == None:
                    return test_case

                if isinstance(new_test_case.test_name, list) and test_index < len(new_test_case.test_name):
                    new_test_case.test_name = new_test_case.test_name[test_index]
                elif isinstance(new_test_case.test_name, list) and test_index >= len(new_test_case.test_name):
                    return None

                if isinstance(new_test_case.objective, list) and test_index < len(new_test_case.objective):
                    new_test_case.objective = new_test_case.objective[test_index]
                elif isinstance(new_test_case.objective, list) and test_index >= len(new_test_case.objective):
                    return None

                if isinstance(new_test_case.precondition, list) and test_index < len(new_test_case.precondition):
                    new_test_case.precondition = new_test_case.precondition[test_index]
                elif isinstance(new_test_case.precondition, list) and test_index >= len(new_test_case.precondition):
                    return None

                Storage.list_test_case.append(new_test_case)
                return new_test_case
        return None

    @classmethod
    def create_test_case_from_docstring(cls, docstring, function_name, test_id, test_index=None):
        MAX_NAME_LENGTH = 255
        if len(function_name) > MAX_NAME_LENGTH:
            function_name = function_name.substring(0, MAX_NAME_LENGTH)
        docstring = docstring + '::END_JIRA'
        scripts = []
        m_scripts_text = TestCaseService.parse_string(docstring, 'scripts:')
        if m_scripts_text:
            for test_step_text in m_scripts_text.split('description:'):
                if 'expectedResult:' and 'testData:' in test_step_text:
                    test_step = TestStep(
                        description=test_step_text[:test_step_text.index('expectedResult:')].strip(),
                        expected_result=test_step_text[test_step_text.index('expectedResult:') + 15
                                                       :test_step_text.index('testData:')].strip(),
                        test_data=test_step_text[test_step_text.index('testData:') + 9:].strip()
                    )
                    scripts.append(test_step)

        try:
            test_case = TestCase(
                test_id=test_id,
                test_name=TestCaseService.parse_string(docstring, 'name:', function_name, test_index),
                issue_links=TestCaseService.parse_array(docstring, 'issueLinks:'),
                objective=TestCaseService.parse_string(docstring, 'objective:', test_index=test_index),
                precondition=TestCaseService.parse_string(docstring, 'precondition:', test_index=test_index),
                priority=TestCaseService.parse_string(docstring, 'priority:', 'Normal'),
                folder=TestCaseService.parse_string(docstring, 'folder:'),
                web_links=TestCaseService.parse_array(docstring, 'webLinks:'),
                confluence_links=TestCaseService.parse_array(docstring, 'confluenceLinks:'),
                plan=TestCaseService.parse_string(docstring, 'plan:'),
                scripts=scripts
            )
            Storage.list_test_case.append(test_case)
            return test_case
        except Exception as e:
            return None

    @classmethod
    def parse_string(cls, docstring, key, default='', test_index=None):
        base_regex = '(?s:(.*?)(issueLinks:|objective:|precondition:|priority:' \
                     '|folder:|confluenceLinks:|webLinks:|plan:|scripts:|::END_JIRA))'
        m_key = re.search(rf'{key}{base_regex}', docstring, re.MULTILINE)
        if m_key:
            m_value = m_key.group(1).strip()
            if test_index != None:
                try:
                    m_value = list(eval(m_value))
                    return m_value[test_index].strip()
                except IndexError as ie:
                    raise ie
                except Exception as e:
                    return m_value

            return m_value
        else:
            return default

    @classmethod
    def parse_array(cls, docstring, key, default=[]):
        base_regex = '(?s:(.*?)(issueLinks:|objective:|precondition:|priority:' \
                     '|folder:|confluenceLinks:|webLinks:|plan:|scripts:|::END_JIRA))'
        m_key = re.search(rf'{key}{base_regex}', docstring, re.IGNORECASE)
        if m_key:
            return [k.strip() for k in m_key.group(1).split(',')]
        else:
            return default
