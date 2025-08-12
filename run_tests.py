import subprocess
import datetime
import os

# Create a timestamped log filename
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = os.path.join("test_logs", f"test_result_{now}.log")

# Run pytest and write output to log
with open(log_path, "w") as f:
    subprocess.run(["pytest", "--alluredir=allure-results"], stdout=f, stderr=subprocess.STDOUT)

# Optional: Check if any test failed
with open(log_path, "r") as f:
    content = f.read()
    if "FAILED" in content:
        print("⚠️ Some tests failed. Check log:", log_path)
    else:
        print("✅ All tests passed.")
