#!/usr/bin/env python
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print('numpy not found in current python env', file=sys.stderr)
    print('install numpy using > pip install numpy', file=sys.stderr)
    sys.exit(1)
try:
    from rich.console import Console
except ImportError:
    Console = None

if len(sys.argv) != 2:
    print('argument must be an .npy file')
    sys.exit(1)

input_file = Path(sys.argv[1])

if not input_file.is_file():
    print(f'File {input_file} not found')
    sys.exit(1)

if input_file.suffix != ".npy":
    print(f"File {input_file} is not of type .npy")
    sys.exit(1)

data = np.load(str(input_file))

if Console:
    console = Console()
    console.print(data)
else:
    print(data)
