import http

import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course
from django_testing import settings


@pytest.fixture
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


# - проверка получения первого курса (retrieve-логика):
@pytest.mark.django_db
def test_get_course(client, course_factory):
    # Arrange
    #   - создаем курс через фабрику;
    courses = course_factory(_quantity=2)

    # Act
    #   - строим урл и делаем запрос через тестовый клиент;
    response = client.get('/api/v1/courses/%d/' % courses[0].id)

    # Assert
    #   - проверяем, что вернулся именно тот курс, который запрашивали;
    assert response.status_code == http.HTTPStatus.OK

    data = response.json()
    assert data['name'] == courses[0].name


# - проверка получения списка курсов (list-логика):
#   - аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат;
@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == http.HTTPStatus.OK

    data = response.json()
    assert len(data) == len(courses)

    for i, с in enumerate(data):
        assert с['name'] == courses[i].name


# - проверка фильтрации списка курсов по `id`:
#   - создаем курсы через фабрику, передать ID одного курса в фильтр, проверить результат запроса с фильтром;
@pytest.mark.django_db
def test_get_course_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/', {'id': courses[0].id})

    assert response.status_code == http.HTTPStatus.OK

    data = response.json()
    assert len(data) == 1

    for i, с in enumerate(data):
        assert с['name'] == courses[i].name


# - проверка фильтрации списка курсов по `name`;
@pytest.mark.django_db
def test_get_course_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/', {'name': courses[0].name})

    assert response.status_code == http.HTTPStatus.OK

    data = response.json()
    assert len(data) >= 1

    for i, с in enumerate(data):
        assert с['name'] == courses[i].name


# - тест успешного создания курса:
#   - здесь фабрика не нужна, готовим JSON-данные и создаём курс;
@pytest.mark.django_db
def test_create_course(client, course_factory):
    course_name = 'test_create_course'
    data = {'name': course_name}

    response = client.post('/api/v1/courses/', data=data)

    assert response.status_code == http.HTTPStatus.CREATED

    data = response.json()
    assert data['name'] == course_name


# - тест успешного обновления курса:
#   - сначала через фабрику создаём, потом обновляем JSON-данными;
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)[0]
    course.save()

    course_name = 'test_create_course'
    data = {'name': course_name}

    response = client.patch('/api/v1/courses/%d/' % course.id, data=data)

    assert response.status_code == http.HTTPStatus.OK

    data = response.json()
    assert data['name'] == course_name


# - тест успешного удаления курса.
@pytest.mark.django_db
def test_create_course(client, course_factory):
    course = course_factory(_quantity=1)[0]
    course.save()

    response = client.delete('/api/v1/courses/%d/' % course.id)

    assert response.status_code == http.HTTPStatus.NO_CONTENT


TEST_MAX_STUDENTS_PER_COURSE = 2


# Добавьте валидацию на максимальное число студентов на курсе — 20
@pytest.mark.parametrize(
    ["student_count", "expected_status"],
    (
            (TEST_MAX_STUDENTS_PER_COURSE, http.HTTPStatus.CREATED),
            (TEST_MAX_STUDENTS_PER_COURSE + 1, http.HTTPStatus.BAD_REQUEST),
    )
)
@pytest.mark.django_db
def test_create_course_with_students(client, student_factory, student_count, expected_status):
    # фикстура settings не работает константа в serializers.CourseSerializer.validate не меняется
    save_max_students_per_course = settings.MAX_STUDENTS_PER_COURSE
    settings.MAX_STUDENTS_PER_COURSE = TEST_MAX_STUDENTS_PER_COURSE

    students = student_factory(_quantity=student_count)
    students_id = [s.id for s in students]

    course_name = f'test_create_course_with_students_{student_count}'
    data = {'name': course_name, 'students': students_id}

    response = client.post('/api/v1/courses/', data=data)

    if student_count > TEST_MAX_STUDENTS_PER_COURSE:
        assert response.status_code == expected_status
    else:
        assert response.status_code == expected_status
        data = response.json()
        assert data['name'] == course_name

    settings.MAX_STUDENTS_PER_COURSE = save_max_students_per_course
