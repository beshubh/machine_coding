def can_accept_v0(
    registry: list[list[tuple[str, str]]],
    call_args: list[str],
) -> bool:
    def matches(signature):

        def dfs(i: int, j: int):

            if i >= len(signature):
                return j >= len(call_args)
            dtype, kind = signature[i]
            if kind == "required":
                ans = j < len(call_args) and call_args[j] == dtype and dfs(i + 1, j + 1)
            elif kind == "optional":
                # skip it
                ans = dfs(i + 1, j)
                # consume current if type matches
                if not ans and j < len(call_args) and call_args[j] == dtype:
                    ans = dfs(i + 1, j + 1)
            else:
                ans = all(arg == dtype for arg in call_args[j:])
            return ans

        return dfs(0, 0)

    return any(matches(signature) for signature in registry)


def can_accept(registry, call_args):
    def inner(signature):
        def go(i: int, j: int):
            if i >= len(signature):
                return j >= len(call_args)

            dtype, kind = signature[i]
            if kind == "required":
                ans = j < len(call_args) and dtype == call_args[j] and go(i + 1, j + 1)
            elif kind == "optional":
                # skip
                ans = go(i + 1, j)

                # take if datatypes match
                if not ans and j < len(call_args) and dtype == call_args[j]:
                    ans = go(i + 1, j + 1)
            else:
                ans = all(c == dtype for c in call_args[j:])
            return ans

        return go(0, 0)

    return any(inner(m) for m in registry)


def test_example_1():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("bool", "required"),
        ]
    ]
    call_args = ["int", "bool"]

    assert can_accept(registry, call_args) is True


def test_example_2():
    registry = [
        [
            ("int", "required"),
            ("str", "variadic"),
        ],
        [
            ("int", "required"),
            ("bool", "required"),
        ],
    ]
    call_args = ["int", "str", "str"]

    assert can_accept(registry, call_args) is True


def test_exact_required_match():
    registry = [
        [
            ("int", "required"),
            ("str", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "str"]) is True


def test_required_type_mismatch():
    registry = [
        [
            ("int", "required"),
            ("str", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "bool"]) is False


def test_missing_required_arg():
    registry = [
        [
            ("int", "required"),
            ("str", "required"),
        ]
    ]

    assert can_accept(registry, ["int"]) is False


def test_extra_arg_without_variadic():
    registry = [
        [
            ("int", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "int"]) is False


def test_optional_present():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("bool", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "str", "bool"]) is True


def test_optional_skipped():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("bool", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "bool"]) is True


def test_multiple_optionals_skipped():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("float", "optional"),
            ("bool", "required"),
        ]
    ]

    assert can_accept(registry, ["int", "bool"]) is True


def test_skip_first_optional_take_second():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("float", "optional"),
            ("bool", "required"),
        ]
    ]

    assert (
        can_accept(
            registry,
            ["int", "float", "bool"],
        )
        is True
    )


def test_optional_ambiguity():
    registry = [
        [
            ("int", "optional"),
            ("int", "required"),
        ]
    ]

    assert can_accept(registry, ["int"]) is True


def test_variadic_zero_args():
    registry = [
        [
            ("int", "required"),
            ("str", "variadic"),
        ]
    ]

    assert can_accept(registry, ["int"]) is True


def test_variadic_one_arg():
    registry = [
        [
            ("int", "required"),
            ("str", "variadic"),
        ]
    ]

    assert can_accept(registry, ["int", "str"]) is True


def test_variadic_many_args():
    registry = [
        [
            ("int", "required"),
            ("str", "variadic"),
        ]
    ]

    assert (
        can_accept(
            registry,
            ["int", "str", "str", "str"],
        )
        is True
    )


def test_variadic_wrong_type():
    registry = [
        [
            ("int", "required"),
            ("str", "variadic"),
        ]
    ]

    assert (
        can_accept(
            registry,
            ["int", "str", "bool"],
        )
        is False
    )


def test_optional_before_variadic_optional_skipped():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("bool", "variadic"),
        ]
    ]

    assert (
        can_accept(
            registry,
            ["int", "bool", "bool"],
        )
        is True
    )


def test_optional_before_variadic_optional_used():
    registry = [
        [
            ("int", "required"),
            ("str", "optional"),
            ("bool", "variadic"),
        ]
    ]

    assert (
        can_accept(
            registry,
            ["int", "str", "bool", "bool"],
        )
        is True
    )


def test_only_variadic():
    registry = [
        [
            ("int", "variadic"),
        ]
    ]

    assert can_accept(registry, []) is True
    assert can_accept(registry, ["int"]) is True
    assert can_accept(registry, ["int", "int", "int"]) is True
    assert can_accept(registry, ["str"]) is False


def test_empty_function():
    registry = [[]]

    assert can_accept(registry, []) is True
    assert can_accept(registry, ["int"]) is False


def test_empty_registry():
    assert can_accept([], []) is False
    assert can_accept([], ["int"]) is False


def test_any_registered_function_can_match():
    registry = [
        [
            ("str", "required"),
            ("bool", "required"),
        ],
        [
            ("int", "required"),
            ("float", "optional"),
        ],
    ]

    assert can_accept(registry, ["int"]) is True


def test_no_registered_function_matches():
    registry = [
        [
            ("str", "required"),
        ],
        [
            ("bool", "required"),
        ],
    ]

    assert can_accept(registry, ["int"]) is False
