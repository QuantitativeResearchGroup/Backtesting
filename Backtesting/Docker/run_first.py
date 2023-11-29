import subprocess

# Ensure connection is correct
subprocess.run(["python", "Methods.py"])

# Extraction process
subprocess.run(["python", "pulldata.py"])

# Execute SP500wiki.py
subprocess.run(["python", "SP500wiki.py"])

# Execute CreateTable.py
subprocess.run(["python", "CreateTable.py"])
