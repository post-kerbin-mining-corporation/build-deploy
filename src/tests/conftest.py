
def pytest_addoption(parser):
    parser.addoption("--test_path", action="append", default=[],
        help="path to run tests against")

def pytest_generate_tests(metafunc):
    if 'test_path' in metafunc.fixturenames:
        metafunc.parametrize("test_path",
                             metafunc.config.getoption('test_path'))
