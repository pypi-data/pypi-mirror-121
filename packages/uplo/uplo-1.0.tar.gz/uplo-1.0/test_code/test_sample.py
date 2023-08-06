def name(first_name,last_name):
    full_name = first_name + ' ' +last_name
    return full_name.title()


def test_name():
    assert name("hello","world") == "Hello World"