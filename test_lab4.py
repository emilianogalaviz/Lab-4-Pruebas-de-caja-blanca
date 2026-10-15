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




@pytest.mark.statement
@pytest.mark.parametrize(
    "students, exp_passed, exp_failed, exp_output",
    [
        # grades == None  -> sentencia print + continue
        ([{"name": "Ana", "grades": None}], [], [], "Student Ana has no grades"),
        # promedio > 70   -> passed.append
        ([{"name": "Luis", "grades": [80, 90, 85]}], ["Luis"], [], ""),
        # 50 <= promedio <= 70 -> print recovery
        ([{"name": "Jorge", "grades": [60, 60, 60]}], [], [], "Jorge is in recovery"),
        # promedio < 50   -> failed.append
        ([{"name": "Marta", "grades": [40, 45, 50]}], [], ["Marta"], ""),
    ],
)
def test_statement_coverage(students, exp_passed, exp_failed, exp_output, capsys):
    result = process_grades.process_grades(students)
    out = capsys.readouterr().out
    assert result["passed"] == exp_passed
    assert result["failed"] == exp_failed
    assert exp_output in out


@pytest.mark.branch
@pytest.mark.parametrize(
    "students, exp_passed, exp_failed",
    [
        ([], [], []),                                       # for: no entra al ciclo
        ([{"name": "Ana", "grades": None}], [], []),        # grades == None -> True
        ([{"name": "Luis", "grades": [71, 71, 71]}], ["Luis"], []),  # > 70 -> True
        ([{"name": "Jorge", "grades": [70, 70, 70]}], [], []),       # > 70 False, >= 50 True (limite)
        ([{"name": "Sofi", "grades": [50, 50, 50]}], [], []),        # >= 50 True (limite inferior)
        ([{"name": "Marta", "grades": [49, 49, 49]}], [], ["Marta"]),  # >= 50 -> False
    ],
)
def test_branch_coverage(students, exp_passed, exp_failed):
    result = process_grades.process_grades(students)
    assert result["passed"] == exp_passed
    assert result["failed"] == exp_failed
    assert result["overall_average"] == 0  # counter siempre es 0



@pytest.mark.path
@pytest.mark.parametrize(
    "students, exp_passed, exp_failed, exp_output",
    [
        ([], [], [], ""),                                                        # P1
        ([{"name": "Ana", "grades": None}], [], [], "Student Ana has no grades"),  # P2
        ([{"name": "Luis", "grades": [90, 95, 100]}], ["Luis"], [], ""),         # P3
        ([{"name": "Jorge", "grades": [65, 60, 55]}], [], [], "Jorge is in recovery"),  # P4
        ([{"name": "Marta", "grades": [10, 20, 30]}], [], ["Marta"], ""),        # P5
        (                                                                        # P6
            [
                {"name": "Ana", "grades": None},
                {"name": "Luis", "grades": [90, 95, 100]},
                {"name": "Jorge", "grades": [65, 60, 55]},
                {"name": "Marta", "grades": [10, 20, 30]},
            ],
            ["Luis"],
            ["Marta"],
            "Jorge is in recovery",
        ),
    ],
)
def test_path_coverage(students, exp_passed, exp_failed, exp_output, capsys):
    result = process_grades.process_grades(students)
    out = capsys.readouterr().out
    assert result["passed"] == exp_passed
    assert result["failed"] == exp_failed
    assert exp_output in out
    assert result["overall_average"] == 0


@pytest.mark.path
@pytest.mark.parametrize("students", [[{"name": "Pedro", "grades": []}]])
def test_path_coverage_empty_grades(students):                                  # P7
    with pytest.raises(ZeroDivisionError):
        process_grades.process_grades(students)