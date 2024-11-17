from rest_framework.test import APIClient
import pytest as pytest
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture  # Фикстура клиента
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client,
                          ):
    pass

