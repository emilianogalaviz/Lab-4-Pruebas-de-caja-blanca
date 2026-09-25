import process_grades 
import pytest 


@pytest.mark.parametrize(
    "student,expected",
    [({"name": "Ana", "grades": [80, 80, 80]}, ["Ana"])]
)
@pytest.mark.system
def test_process_grade_pass(student, expected):
    result = process_grades.process_grades([student])
    assert result["passed"] == expected


@pytest.mark.parametrize(
    "students, expected",
    [([{"name": "Ana", "grades": [55, 55, 55]}], [])]
)
@pytest.mark.system
def test_process_recovery(students, expected, capsys):
    result = process_grades.process_grades(students)
    captured = capsys.readouterr()
    assert result["passed"] == expected
    assert "Ana is in recovery" in captured.out


@pytest.mark.parametrize(
    "student,expected",
    [({"name": "Ana", "grades": [40, 40, 40]}, ["Ana"])]
)
@pytest.mark.wip
def test_process_grade_fail(student, expected):
    result = process_grades.process_grades([student])
    assert result["failed"] == expected