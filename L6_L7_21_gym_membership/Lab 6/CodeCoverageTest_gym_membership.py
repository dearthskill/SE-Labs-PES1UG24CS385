import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# membership_cost

def test_unknown_plan_raises():
    with pytest.raises(ValueError):
        membership_cost("weekly", 30, False, False)


def test_too_young_raises():
    with pytest.raises(ValueError):
        membership_cost("monthly", 13, False, False)


def test_age_14_is_valid():
    assert membership_cost("monthly", 14, False, False) == 1500


def test_plan_prices():
    assert membership_cost("monthly", 30, False, False) == 1500
    assert membership_cost("quarterly", 30, False, False) == 4000
    assert membership_cost("yearly", 30, False, False) == 12000


def test_senior_discount_at_60():
    assert membership_cost("monthly", 60, False, False) == 1125


def test_no_senior_discount_at_59():
    assert membership_cost("monthly", 59, False, False) == 1500


def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_senior_student_gets_only_senior_discount():
    assert membership_cost("monthly", 65, True, False) == 1125


def test_trainer_monthly():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_quarterly():
    assert membership_cost("quarterly", 30, False, True) == 6000


def test_trainer_yearly_reduction():
    assert membership_cost("yearly", 30, False, True) == 13500


# can_enter

def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False


def test_hour_too_early():
    assert can_enter(4, True, False, "M") is False


def test_hour_too_late():
    assert can_enter(23, True, False, "M") is False


def test_boundary_hours():
    assert can_enter(5, True, False, "M") is True
    assert can_enter(22, True, False, "M") is True


def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


def test_women_only_slot_male():
    assert can_enter(10, True, True, "M") is False


def test_normal_slot():
    assert can_enter(10, True, False, "M") is True


# bmi_category

def test_zero_height_raises():
    with pytest.raises(ValueError):
        bmi_category(70, 0)


def test_negative_height_raises():
    with pytest.raises(ValueError):
        bmi_category(70, -1.7)


def test_underweight():
    assert bmi_category(50, 1.8) == "underweight"


def test_normal():
    assert bmi_category(70, 1.8) == "normal"


def test_overweight():
    assert bmi_category(85, 1.8) == "overweight"


def test_obese():
    assert bmi_category(110, 1.8) == "obese"


def test_bmi_boundaries():
    assert bmi_category(18.5, 1) == "normal"
    assert bmi_category(25, 1) == "overweight"
    assert bmi_category(30, 1) == "obese"
