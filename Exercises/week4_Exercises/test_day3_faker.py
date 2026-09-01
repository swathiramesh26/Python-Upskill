def test_dynamic_todos(dynamic_todos):
    print("\nDynamic todos:", dynamic_todos)
    assert len(dynamic_todos) == 5

def test_static_todos(static_todos):
    print("\nStatic todos:", static_todos)
    assert len(static_todos) == 5
    assert "Shopping" in static_todos