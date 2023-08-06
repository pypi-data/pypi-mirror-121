from ford.sourceform import FortranProgram, FortranContainer, FortranSourceFile
from ford.reader import FortranReader

from collections import defaultdict


def test_program(tmp_path):
    """Check that types can be read"""

    source = """\
    !> This is a program
    program prog_foo
    end program prog_foo
    """

    filename = tmp_path / "test.f90"
    with open(filename, "w") as f:
        f.write(source)

    settings = defaultdict(str)
    settings["predocmark"] = "!"
    settings["predocmark"] = ">"
    settings["encoding"] = "utf-8"

    fortran_prog = FortranSourceFile(str(filename), settings)

    assert len(fortran_prog.programs) == 1
    program = fortran_prog.programs[0]
    assert isinstance(program, FortranProgram)
    assert program.name == "prog_foo"
    # assert program.doc
