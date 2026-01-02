from setuptools import setup
import torch
from torch.utils.cpp_extension import CppExtension, BuildExtension
import os

openfst_path = "../openfst"

if "OPENFST_PATH" in os.environ:
    openfst_path = os.environ["OPENFST_PATH"]

if not os.path.exists(os.path.join(openfst_path, "lib", "libfst.so")):
    raise SystemExit(
        "Could not find libfst.so in {}.\n"
        "Install openfst and set OPENFST_PATH to the openfst "
        "root directory".format(openfst_path)
    )

openfst_lib = os.path.join(openfst_path, "lib")
torch_lib = os.path.join(os.path.dirname(torch.__file__), "lib")

setup(
    name="simplefst",
    ext_modules=[
        CppExtension(
            "simplefst",
            ["src/fstext.cc"],
            include_dirs=["src", os.path.join(openfst_path, "include")],
            library_dirs=[os.path.join(openfst_path, "lib")],
            libraries=["fst", "fstscript"],
        )
    ],
    extra_link_args=[
        f"-Wl,-rpath,{openfst_lib}",
        f"-Wl,-rpath,{torch_lib}",
    ],
    cmdclass={"build_ext": BuildExtension},
)