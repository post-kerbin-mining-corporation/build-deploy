
def pytest_addoption(parser):
    parser.addoption("--testpath", action="append", default=[],
        help="path to run tests against")

def pytest_generate_tests(metafunc):
    if 'testpath' in metafunc.fixturenames:
        metafunc.parametrize("testpath",
                             metafunc.config.getoption('testpath'))
