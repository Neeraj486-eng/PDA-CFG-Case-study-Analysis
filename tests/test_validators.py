import pytest
from pda_cfg.validators import (validate_arithmetic, validate_program, validate_brackets,
    validate_palindrome, validate_marked_palindrome, validate_password, ParseError)

@pytest.mark.parametrize("s", ["a+b*c", "(x+12)/y", "42", "a*(b-c)"])
def test_arithmetic_accept(s): assert validate_arithmetic(s)
@pytest.mark.parametrize("s", ["a+*b", "(x+2", "a b", "+a"])
def test_arithmetic_reject(s):
    with pytest.raises(ParseError): validate_arithmetic(s)
@pytest.mark.parametrize("s", ["let total = price * 2", "x=3; y=x+4", "let avg=(a+b)/2"])
def test_program_accept(s): assert validate_program(s)
@pytest.mark.parametrize("s", ["let = 3", "x 3", "x=; y=2", "x=1;"])
def test_program_reject(s):
    with pytest.raises(ParseError): validate_program(s)
@pytest.mark.parametrize("s", ["()", "([]{})", "f(a[2], {b})"])
def test_brackets_accept(s): assert validate_brackets(s)
@pytest.mark.parametrize("s", ["(", ")(", "([)]", "{[}"])
def test_brackets_reject(s): assert not validate_brackets(s)
@pytest.mark.parametrize("s", ["", "a", "abba", "baab", "babab"])
def test_palindrome_accept(s): assert validate_palindrome(s)
@pytest.mark.parametrize("s", ["ab", "aab", "abb"])
def test_palindrome_reject(s): assert not validate_palindrome(s)
def test_marked_palindrome():
    assert validate_marked_palindrome("ab#ba")
    assert not validate_marked_palindrome("ab#ab")
@pytest.mark.parametrize("s", ["Formal123!", "Pda_Cfg9", "Study#2026"])
def test_password_accept(s): assert validate_password(s)
@pytest.mark.parametrize("s", ["password", "PASSWORD1!", "Pass123", "Pass word9!"])
def test_password_reject(s): assert not validate_password(s)
