import pytest
from faker import Faker


@pytest.mark.api
@pytest.mark.smoke
def test_get_suites_for_project(suite_controller, project_controller):
    """Get suites list (not empty) and validate pydantic model."""

    # Pick a random project with suites
    while len(suite_controller.suites) == 0:
        project = project_controller.random_project()
        suites_list = suite_controller.get_suites_for_project_id(project.id)

    # Count the sum of "test-count" attributes for all suites in suites_list
    suites_test_count = sum(suite.attributes.test_count for suite in suites_list)
    assert project.attributes.tests_count == suites_test_count


@pytest.mark.api
@pytest.mark.smoke
def test_get_suite_by_id_for_a_project(suite_controller, project_controller):
    """Get a suite by id and validate pydantic model."""
    project = project_controller.random_project()
    rand_suite = suite_controller.random_suite(project.id)
    while rand_suite is None:
        project = project_controller.random_project()
        rand_suite = suite_controller.random_suite(project.id)

    suite = suite_controller.get_by_id_for_project_id(project.id, rand_suite.id)

    assert suite.attributes.title == rand_suite.attributes.title
    assert suite.attributes.public_title == rand_suite.attributes.public_title
    assert suite.attributes.test_count == rand_suite.attributes.test_count


@pytest.mark.api
@pytest.mark.smoke
def test_add_suite(suite_controller, project_controller):
    """Create a suite with valid attributes."""
    project = project_controller.random_project()

    suite_title = Faker().sentence()
    suite = suite_controller.add_suite(project.id, title=suite_title)

    assert suite.attributes.title == suite_title
    suites = suite_controller.get_suites_for_project_id(project.id)
    assert suite.id in (suite.id for suite in suites)

    # Clean up
    suite_controller.delete_by_id_for_project_id(project.id, suite.id)


@pytest.mark.api
@pytest.mark.smoke
def test_delete_suite(suite_controller, project_controller):
    """Delete a suite."""

    # Create a suite
    project = project_controller.random_project()
    suite_title = Faker().sentence()
    suite = suite_controller.add_suite(project.id, title=suite_title)

    # Delete the suite
    suite_controller.delete_by_id_for_project_id(project.id, suite.id)

    assert suite.id not in (
        suite.id for suite in suite_controller.get_suites_for_project_id(project.id)
    )
