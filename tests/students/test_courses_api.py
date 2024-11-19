from rest_framework.test import APIClient
import pytest as pytest
from model_bakery import baker
from students.models import Course, Student


# Фикстура клиента
@pytest.fixture
def client():
    return APIClient()


# Фикстура создания фабрики студентов
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# Фикстура создания фабрики студентов
@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# 1. Проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_first_course(client,
                          course_factory, ):
    course = course_factory(name='Python', )
    response = client.get(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 200
    assert response.data['name'] == 'Python'


# 2. Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_course_list(client,
                         course_factory, ):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/')

    assert response.status_code == 200
    assert len(response.json()) == len(courses)


# 3. Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_courses_id(client,
                           course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[0].id

    response = client.get(f'/api/v1/courses/?id={course_id}')

    # Проверяем, что статус ответа — 200(ОК)
    assert response.status_code == 200

    # Проверяем, что в ответе содержится только один курс с заданным ID
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == course_id


# 4. Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_courses_name(client,
                             course_factory):
    courses = course_factory(_quantity=10)
    course_name = courses[0].name

    response = client.get(f'/api/v1/courses/?name={course_name}')

    # Проверяем, что статус ответа — 200(ОК)
    assert response.status_code == 200

    # Проверяем, что в ответе содержится только один курс с заданным именем
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['name'] == course_name


# Тест успешного создания курса
@pytest.mark.django_db
def test_success_post_course(client):
    data = {
        'name': 'Course_test',
    }
    response = client.post('/api/v1/courses/', data=data)

    assert response.status_code == 201


# 6. Тест успешного обновления курса
@pytest.mark.django_db
def test_success_put_course(client,
                            course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    data = {
        'name': 'Python-разработчик'
    }
    response = client.put(f'/api/v1/courses/{course_id}/',
                          data)

    # Проверяем, что статус ответа — 200(ОК)
    assert response.status_code == 200

    # Обновляем курс из базы данных
    courses[0].refresh_from_db()

    # Проверяем, что имя курса было обновлено
    assert courses[0].name == data['name']


# 7. Тест успешного удаления курса.
@pytest.mark.django_db
def test_success_delete_course(client,
                               course_factory):

    course = course_factory(_quantity=10)
    course_id = course[0].id

    response = client.delete(f'/api/v1/courses/{course_id}/')

    # Проверяем, что статус ответа — 204 (No Content)
    assert response.status_code == 204

    # Проверяем, что курс удалён из базы данных
    assert course_id not in course



