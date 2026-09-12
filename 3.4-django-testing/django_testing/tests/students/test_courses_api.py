import pytest
from students.models import Student


# ============ RETRIEVE (получение одного курса) ============

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса (retrieve-логика)."""
    # Arrange
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


# ============ LIST (получение списка курсов) ============

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list-логика)."""
    # Arrange
    courses = course_factory(_quantity=5)
    url = '/api/v1/courses/'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 5
    returned_ids = {course['id'] for course in response.data}
    expected_ids = {course.id for course in courses}
    assert returned_ids == expected_ids


# ============ FILTER BY ID ============

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id."""
    # Arrange
    courses = course_factory(_quantity=3)
    target_course = courses[0]
    url = '/api/v1/courses/'

    # Act
    response = api_client.get(url, data={'id': target_course.id})

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id


# ============ FILTER BY NAME ============

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name."""
    # Arrange
    course_factory(name='Python')
    course_factory(name='Django')
    course_factory(name='JavaScript')
    url = '/api/v1/courses/'

    # Act
    response = api_client.get(url, data={'name': 'Python'})

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Python'


# ============ CREATE ============

@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    # Arrange
    url = '/api/v1/courses/'
    data = {'name': 'Новый курс'}

    # Act
    response = api_client.post(url, data=data)

    # Assert
    assert response.status_code == 201
    assert response.data['name'] == 'Новый курс'
    assert 'id' in response.data


# ============ UPDATE ============

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса."""
    # Arrange
    course = course_factory(name='Старое название')
    url = f'/api/v1/courses/{course.id}/'
    data = {'name': 'Новое название'}

    # Act
    response = api_client.patch(url, data=data)

    # Assert
    assert response.status_code == 200
    assert response.data['name'] == 'Новое название'

    # Проверяем, что изменения сохранились в БД
    course.refresh_from_db()
    assert course.name == 'Новое название'


# ============ DELETE ============

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса."""
    # Arrange
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response = api_client.delete(url)

    # Assert
    assert response.status_code == 204

    # Проверяем, что курс удален из БД
    from students.models import Course
    assert not Course.objects.filter(id=course.id).exists()

@pytest.mark.django_db
def test_max_students_per_course_validation(api_client, course_factory, student_factory, settings):
    """Тест: превышение максимального количества студентов на курсе."""
    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 3

    course = course_factory()
    students = student_factory(_quantity=4)  # 4 студента > 3
    student_ids = [s.id for s in students]

    url = f'/api/v1/courses/{course.id}/'
    data = {'students': student_ids}

    # Act
    response = api_client.patch(url, data=data)

    # Assert
    assert response.status_code == 400
    assert 'students' in response.data


@pytest.mark.django_db
def test_max_students_per_course_success(api_client, course_factory, student_factory, settings):
    """Тест: успешное добавление студентов в пределах лимита."""
    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 3

    course = course_factory()
    students = student_factory(_quantity=2)  # 2 студента < 3
    student_ids = [s.id for s in students]

    url = f'/api/v1/courses/{course.id}/'
    data = {'students': student_ids}

    # Act
    response = api_client.patch(url, data=data)

    # Assert
    assert response.status_code == 200
    assert len(response.data['students']) == 2


@pytest.mark.parametrize('count_students, expected_status', [
    (2, 200),   # Успех: меньше лимита
    (3, 200),   # Успех: ровно лимит
    (4, 400),   # Ошибка: больше лимита
    (5, 400),   # Ошибка: сильно больше лимита
])
@pytest.mark.django_db
def test_max_students_per_course_parametrize(
    api_client, course_factory, student_factory, settings,
    count_students, expected_status
):
    """Параметризованный тест: проверка границы MAX_STUDENTS_PER_COURSE."""
    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = 3

    course = course_factory()
    students = student_factory(_quantity=count_students)
    student_ids = [s.id for s in students]

    url = f'/api/v1/courses/{course.id}/'
    data = {'students': student_ids}

    # Act
    response = api_client.patch(url, data=data)

    # Assert
    assert response.status_code == expected_status
    