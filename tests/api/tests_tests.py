import random

import pytest
from faker import Faker


@pytest.mark.api
@pytest.mark.smoke
def test_get_tests_for_project(tests_controller, project_controller):
    """Get tests list (not empty) and validate pydantic model."""

    project = project_controller.random_project(with_tests=True)

    tests_list = tests_controller.get_tests_for_project_id(project.id)

    # Note: API may return None for suites without tests, normalize to 0 for comparison
    assert len(tests_list) == (project.attributes.tests_count or 0)


@pytest.mark.api
@pytest.mark.smoke
def test_get_tests_for_suite(tests_controller, project_controller, suite_controller):
    """Get a tests list (not empty) for specified suite and validate pydantic model."""

    # Pick a project with tests
    project = project_controller.random_project(with_tests=True)

    # Find a suite in the project with tests
    suite_controller.get_suites_for_project_id(project.id)
    random.shuffle(suite_controller.suites)
    for suite in suite_controller.suites:
        if suite.attributes.test_count > 0:
            break

    tests_list = tests_controller.get_tests_for_suite(project.id, suite.id)

    # Note: API may return None for suites without tests, normalize to 0 for comparison
    assert len(tests_list) == (suite.attributes.test_count or 0)


@pytest.mark.api
@pytest.mark.smoke
def test_get_test_by_id(tests_controller, project_controller):
    """Get a test by id and validate pydantic model."""
    project = project_controller.random_project(with_tests=True)
    tests_list = tests_controller.get_tests_for_project_id(project.id)

    random_test = random.choice(tests_list)

    test = tests_controller.get_by_id_for_project_id(project.id, random_test.id)

    assert test.attributes.title == random_test.attributes.title
    assert test.attributes.suite_id == random_test.attributes.suite_id


@pytest.mark.api
@pytest.mark.smoke
def test_add_test(tests_controller, suite_controller, project_controller):
    """Create a test with valid attributes."""

    # Find a random project that has suites
    if len(project_controller.projects) == 0:
        project_controller.get_all()
    random.shuffle(project_controller.projects)

    for project in project_controller.projects:
        if len(suite_controller.get_suites_for_project_id(project.id)) > 0:
            break

    suite = suite_controller.random_suite(project.id, folder_type=False)

    test_title = Faker().sentence()
    test_description = Faker().paragraph(nb_sentences=3)

    test = tests_controller.add_test(project.id, suite.id, test_title, test_description)

    assert test.attributes.title == test_title
    tests = tests_controller.get_tests_for_project_id(project.id)
    assert test.id in (test.id for test in tests)

    # Clean up
    tests_controller.delete_by_id_for_project_id(project.id, test.id)


@pytest.mark.api
@pytest.mark.smoke
def test_delete_test(tests_controller, suite_controller, project_controller):
    """Delete a test."""

    # Create a test
    project = project_controller.random_project(with_tests=True)
    suite_controller.get_suites_for_project_id(project.id)
    suite = suite_controller.random_suite(project.id, folder_type=False)
    test = tests_controller.add_test(project.id, suite.id, title=Faker().sentence())

    # Delete the suite
    tests_controller.delete_by_id_for_project_id(project.id, test.id)

    assert test.id not in (
        test.id for test in tests_controller.get_tests_for_project_id(project.id)
    )


@pytest.mark.api
@pytest.mark.regression
def test_update_test_title(tests_controller, suite_controller, project_controller):
    """Update a test's title, validate pydantic model, check other attributes haven't changed"""

    # Create a test
    project = project_controller.random_project(with_tests=True)
    suite_controller.get_suites_for_project_id(project.id)
    suite = suite_controller.random_suite(project.id, folder_type=False)
    test = tests_controller.add_test(project.id, suite.id, title=Faker().sentence())

    # Update the test
    upd_title = f"{suite.attributes.title} updated"
    updated_test = tests_controller.update_test(
        project.id,
        test.id,
        title=upd_title,
    )

    # Check id hasn't changed
    assert updated_test.id == test.id

    # Get updated test by id
    get_upd_test = tests_controller.get_by_id_for_project_id(project.id, test.id)
    assert get_upd_test.attributes.title == upd_title
    assert get_upd_test.attributes.suite_id == test.attributes.suite_id

    # Clean up
    tests_controller.delete_by_id_for_project_id(project.id, test.id)
