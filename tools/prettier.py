"""
The MIT License (MIT)

Copyright (c) 2023-present shiüo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import os
import subprocess


def code_format(path):
    try:
        # Create a list to store target files for code formatting
        target_files = []

        # Traverse the directory tree rooted at path
        for root, dirs, files in os.walk(path):
            for file in files:
                # Check if the file is a Python file and not inside a "venv" directory
                if file.endswith(".py") and root.find("venv") == -1:
                    target_files.append(os.path.join(root, file))

        # Iterate over the target files and apply code formatting using Black
        for file in target_files:
            command = f"black {file}"
            print(command)
            subprocess.run(command, shell=True)

        print("code_format done")
    except Exception as e:
        print(e)
