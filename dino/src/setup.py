import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="dino",
    options={
        "build_exe": {"packages": ["pygame"], "include_files": ["images", "audios"]}
    },
    executables=executables,
)
