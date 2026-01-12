from setuptools import setup
import torch
from torch.utils.cpp_extension import CUDAExtension, CppExtension, BuildExtension
import os
from pathlib import Path

# Path to openfst
openfst_path = Path("openfst")

if "OPENFST_PATH" in os.environ:
    openfst_path = Path(os.environ["OPENFST_PATH"])

if not (openfst_path / "lib" / "libfst.so").exists():
    raise SystemExit(
        "Could not find libfst.so in {}.\n"
        "Install openfst and set OPENFST_PATH to the openfst "
        "root directory".format(openfst_path)
    )

openfst_lib = openfst_path / "lib"
torch_lib = Path(os.path.dirname(torch.__file__)) / "lib"

setup(
    name="pychain",
    version="0.1.0",
    description="PyTorch wrapper for implementation of LFMMI",
    packages=["pychain"],
    ext_modules=[
        CppExtension(
            "simplefst",
            ["openfst_binding/src/fstext.cc"],
            include_dirs=["openfst_binding/src", str(openfst_path / "include")],
            library_dirs=[str(openfst_path / "lib")],
            libraries=["fst", "fstscript"],
        ),
        CUDAExtension(
            "pychain_C",
            [
                "pytorch_binding/src/pychain.cc",
                "pytorch_binding/src/base.cc",
                "pytorch_binding/src/chain-kernels.cu",
                "pytorch_binding/src/chain-log-domain-kernels.cu",
                "pytorch_binding/src/chain-computation.cc",
                "pytorch_binding/src/chain-log-domain-computation.cc",
            ],
            include_dirs=["pytorch_binding/src"],
        )
    ],
    extra_link_args=[
        f"-Wl,-rpath,{openfst_lib}",
        f"-Wl,-rpath,{torch_lib}",
    ],
    cmdclass={"build_ext": BuildExtension},
    install_requires=[
        "torch",
        "numpy",
    ],
)