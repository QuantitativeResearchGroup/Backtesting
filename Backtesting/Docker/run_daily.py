import subprocess
# run at end of the day
# this pulls daily price from latest entry in SQL table
subprocess.run(["python", "pullDailyPrice.py"])


# run whenever needed
# this pulls daily price from latest entry in SQL table
subprocess.run(["python", "pullIntradayPrice.py"])

