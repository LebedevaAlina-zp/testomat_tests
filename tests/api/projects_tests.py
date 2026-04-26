import pytest


@pytest.mark.smoke
@pytest.mark.api
def test_get_projects(project_controller):
    """Get a projects list and validate pydantic model."""
    projects_list = project_controller.get_all()
    assert len(projects_list) > 0


@pytest.mark.smoke
@pytest.mark.api
def test_get_project_by_id(project_controller):
    """Get a project by id and validate pydantic model."""
    rand_project = project_controller.random_project()

    project = project_controller.get_by_id(rand_project.id)
    assert project.id == rand_project.id
    assert project.attributes.title == rand_project.attributes.title
    assert project.attributes.tests_count == rand_project.attributes.tests_count
