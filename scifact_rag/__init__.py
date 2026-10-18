"""SciFact retrieval-augmented generation service and evaluation."""
import os

# The macOS arm64 wheels of torch and faiss-cpu each bundle their own libomp.dylib;
# loading both aborts with "OMP: Error #15". We allow the duplicate runtime and pin
# OpenMP to one thread. Because Intel/LLVM call this workaround unsupported, the
# retrieval reproduction script checks every FAISS top-10 against an exact NumPy
# ranking and fails on any difference (see README, "Limits").
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")
