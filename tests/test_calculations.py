import math
import pytest

from utils.calculations import (
    calculate_column_capacity,
    calculate_rectangular_column_capacity,
    calculate_beam_moment_capacity,
    calculate_shear_capacity,
    calculate_deflection_check,
)


def test_circular_column_capacity_reasonable():
    res = calculate_column_capacity(diameter=400, length=3000, concrete_grade="M25", steel_grade="Fe500", steel_area=2010)
    assert res["capacity"] > 0
    assert res["area"] == pytest.approx(math.pi * (400/2) ** 2)


def test_rectangular_column_capacity_reasonable():
    res = calculate_rectangular_column_capacity(width=300, depth=450, length=3000, concrete_grade="M25", steel_grade="Fe500", steel_area=2262)
    assert res["capacity"] > 0
    assert res["area"] == 300 * 450


def test_beam_capacity_monotonic_with_ast():
    res1 = calculate_beam_moment_capacity(300, 500, "M25", "Fe415", tension_steel=800)
    res2 = calculate_beam_moment_capacity(300, 500, "M25", "Fe415", tension_steel=1200)
    assert res2["moment_capacity"] >= res1["moment_capacity"]


def test_shear_capacity_increases_with_stirrups():
    no_stirrups = calculate_shear_capacity(300, 500, "M25", 8, stirrup_spacing=0)
    with_stirrups = calculate_shear_capacity(300, 500, "M25", 8, stirrup_spacing=150)
    assert with_stirrups["shear_capacity"] > no_stirrups["shear_capacity"]


def test_deflection_basic_ratio():
    res = calculate_deflection_check(span=6000, depth=300, loading_type='simply_supported')
    assert res["allowable_ratio"] == 20
    assert isinstance(res["deflection_ok"], bool)