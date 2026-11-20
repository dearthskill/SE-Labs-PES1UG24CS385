import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# membership_cost: every decision taken both ways

def test_plan_not_in_price_list_raises():
    with pytest.raises(ValueError):
        membership_cost("daily", 25, False, False)


def test_age_below_14_raises():
    with pytest.raises(ValueError):
        membership_cost("monthly", 10, False, False)


def test_age_exactly_14_allowed():
    assert membership_cost("quarterly", 14, False, False) == 4000


def test_every_plan_price():
    assert membership_cost("monthly", 30, False, False) == 1500
    assert membership_cost("quarterly", 30, False, False) == 4000
    assert membership_cost("yearly", 30, False, False) == 12000


def test_senior_at_60_gets_discount():
    assert membership_cost("yearly", 60, False, False) == 9000


def test_age_59_is_not_senior():
    assert membership_cost("yearly", 59, False, False) == 12000


def test_student_not_senior_gets_student_discount():
    assert membership_cost("quarterly", 20, True, False) == 3600


def test_senior_and_student_gets_only_senior_discount():
    assert membership_cost("quarterly", 70, True, False) == 3000


def test_no_discount_no_trainer():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_trainer_on_monthly():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_on_quarterly():
    assert membership_cost("quarterly", 30, False, True) == 6000


def test_trainer_on_yearly_has_reduction():
    assert membership_cost("yearly", 30, False, True) == 13500


# can_enter

def test_plan_inactive():
    assert can_enter(12, False, False, "F") is False


def test_hour_below_5():
    assert can_enter(4, True, False, "M") is False


def test_hour_above_22():
    assert can_enter(23, True, False, "M") is False


def test_hour_5_allowed():
    assert can_enter(5, True, False, "M") is True


def test_hour_22_allowed():
    assert can_enter(22, True, False, "M") is True


def test_women_only_slot_with_female():
    assert can_enter(18, True, True, "F") is True


def test_women_only_slot_with_non_female():
    assert can_enter(18, True, True, "M") is False


def test_regular_slot():
    assert can_enter(18, True, False, "F") is True


# bmi_category

def test_height_zero_raises():
    with pytest.raises(ValueError):
        bmi_category(60, 0)


def test_height_negative_raises():
    with pytest.raises(ValueError):
        bmi_category(60, -1.5)


def test_underweight_bmi():
    assert bmi_category(45, 1.7) == "underweight"


def test_normal_bmi():
    assert bmi_category(65, 1.7) == "normal"


def test_overweight_bmi():
    assert bmi_category(80, 1.7) == "overweight"


def test_obese_bmi():
    assert bmi_category(100, 1.7) == "obese"


def test_boundary_18_5_is_normal():
    assert bmi_category(18.5, 1) == "normal"


def test_boundary_25_is_overweight():
    assert bmi_category(25, 1) == "overweight"


def test_boundary_30_is_obese():
    assert bmi_category(30, 1) == "obese"
