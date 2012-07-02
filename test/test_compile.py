


def test_compile():
    try:
        import tiddlywebplugins.status
        assert True
    except ImportError, exc:
        assert False, exc
