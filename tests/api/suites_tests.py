import random

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
    # Find a random project that has suites
    if len(project_controller.projects) == 0:
        project_controller.get_all()
    random.shuffle(project_controller.projects)

    for project in project_controller.projects:
        if len(suite_controller.get_suites_for_project_id(project.id)) > 0:
            rand_suite = suite_controller.random_suite(project.id)
            break

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
def test_add_suite_with_description(suite_controller, project_controller):
    """Create a suite with valid attributes."""
    project = project_controller.random_project()

    suite_title = Faker().sentence()
    description = Faker().paragraph(nb_sentences=3)
    suite = suite_controller.add_suite(
        project.id, title=suite_title, description=description
    )

    assert suite.attributes.title == suite_title
    assert suite.attributes.description == description
    # Get suites list to check whether created suite is in there
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


@pytest.mark.api
@pytest.mark.smoke
def test_update_suite_title(suite_controller, project_controller):
    """Update a suite title, validate pydantic model, check other attributes haven't changed"""
    # Create a suite for a random project
    project = project_controller.random_project()
    suite = suite_controller.add_suite(
        project.id, title=Faker().company(), description=Faker().sentence()
    )

    # Update the suite
    upd_title = f"{suite.attributes.title}_updated"
    updated_suite = suite_controller.update_suite(
        project.id,
        suite.id,
        title=upd_title,
    )

    # Check id hasn't changed
    assert updated_suite.id == suite.id
    # Get updated  suite by id
    get_upd_suite = suite_controller.get_by_id_for_project_id(project.id, suite.id)
    assert get_upd_suite.attributes.title == upd_title
    assert get_upd_suite.attributes.description == suite.attributes.description

    # Clean up
    suite_controller.delete_by_id_for_project_id(project.id, suite.id)


@pytest.mark.api
@pytest.mark.smoke
def test_update_suite_description(suite_controller, project_controller):
    """Update a suite description, validate pydantic model, check other attributes haven't changed"""
    # Create a suite for a random project
    project = project_controller.random_project()
    suite = suite_controller.add_suite(
        project.id, title=Faker().company(), description=Faker().sentence()
    )

    upd_description = Faker().sentence()
    upd_suite = suite_controller.update_suite(
        project.id,
        suite.id,
        description=upd_description,
    )

    # Check id hasn't changed
    assert upd_suite.id == suite.id

    # Get updated suite by id
    get_upd_suite = suite_controller.get_by_id_for_project_id(project.id, suite.id)
    assert get_upd_suite.attributes.title == suite.attributes.title
    assert get_upd_suite.attributes.description == upd_description

    # Clean up
    suite_controller.delete_by_id_for_project_id(project.id, suite.id)
