import pytest
from dataclasses import dataclass

from attrs import define

from parsnip import Field, fields, fields_dict


# Define a dummy class and instance for testing
@dataclass
class TestDataClass:
    a: int
    b: str


@define
class TestAttrsClass:
    a: int
    b: str


def test_fields_dict_dataclass():
    result = fields_dict(TestDataClass)
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "a" in result
    assert isinstance(result["a"], Field)
    assert result["a"].name == "a"
    assert result["a"].type == int
    assert "b" in result
    assert isinstance(result["b"], Field)
    assert result["b"].name == "b"
    assert result["b"].type == str


def test_fields_dict_attrs():
    result = fields_dict(TestAttrsClass)
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "a" in result
    assert isinstance(result["a"], Field)
    assert result["a"].name == "a"
    assert result["a"].type == int
    assert "b" in result
    assert isinstance(result["b"], Field)
    assert result["b"].name == "b"
    assert result["b"].type == str


def test_fields_dataclass():
    result = fields(TestDataClass)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(field, Field) for field in result)


def test_fields_attrs():
    result = fields(TestAttrsClass)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(field, Field) for field in result)


def test_fields_unknown_type():
    with pytest.raises(TypeError):
        fields(int)


if __name__ == '__main__':
    test_fields_unknown_type()
