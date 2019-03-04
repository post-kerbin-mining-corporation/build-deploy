# Tests for packaging items
import os

def test_no_tgas(testpath):
    """Test that no tga files are left when packaging"""
    tgas = []
    for path, subdirs, files in os.walk(testpath):
        for name in files:
            if '.tga' in name:
                tgas.append(os.path.join(path, name))
    print(tgas)
    assert len(tgas) == 0

def test_no_intermediates(testpath):
    """Test that no intermediate workflow files are left when packaging"""
    intermediate_files = []
    for path, subdirs, files in os.walk(testpath):
        for name in files:
            if '-b.dds' in name:
                intermediate_files.append(os.path.join(path, name))
    print(intermediate_files)
    assert len(intermediate_files) == 0
