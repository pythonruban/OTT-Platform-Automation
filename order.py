import glob
import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dotenv import load_dotenv
import multiprocessing
import psutil
from collections import defaultdict
import time

load_dotenv()

MODULE_DIRS = ["Modules-Admin"
               # "Frontend-Modules"
               ]
RUNNING_TESTS_FILE = "running_tests.txt"

def get_test_files(folder_keyword):
    all_tests = []
    for base_dir in MODULE_DIRS:
        pattern = os.path.join(base_dir, "**", folder_keyword, "**", "test_*.py")
        found = glob.glob(pattern, recursive=True)
        all_tests.extend(found)
    return all_tests

def run_single_test(file, log_folder):
    file_name = os.path.basename(file)
    print(f"\n🔄 Currently Running: {file} ...")
    
    with open(RUNNING_TESTS_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} STARTED {file}\n")

    log_file_path = os.path.join(log_folder, file_name.replace(".py", ".log"))
    passed = failed = skipped = 0

    with open(log_file_path, "w") as log_file:
        process = subprocess.Popen(
            ["pytest", "-v", "-s", "--disable-warnings", file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            log_file.write(line)
            line = line.strip()
            if "PASSED" in line:
                passed += 1
            elif "FAILED" in line:
                failed += 1
            elif "SKIPPED" in line:
                skipped += 1

        process.wait()

    with open(RUNNING_TESTS_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} FINISHED {file}\n")

    status_summary = f"✅ {passed} | ❌ {failed} | ⏭️ {skipped}"
    print(f"🧪 Completed: {file_name} — {status_summary}")

    module_name = file.split(os.sep)[1]  # Assumes Modules-Admin/module_name/...
    return module_name, passed, failed, skipped

def generate_allure_report():
    subprocess.Popen(["bash", os.path.abspath("run_allure_report.sh")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_safe_thread_limit():
    total_mem_gb = psutil.virtual_memory().total / (1024 ** 3)
    approx_mem_per_thread = 1.5
    max_threads = int(total_mem_gb // approx_mem_per_thread)
    return max(1, min(max_threads, multiprocessing.cpu_count()))

def clear_memory_cache():
    cmd = "echo 3 | sudo /usr/bin/tee /proc/sys/vm/drop_caches"
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No folder keywords provided.")
        sys.exit(1)

    open(RUNNING_TESTS_FILE, "w").close()
    all_test_files = []
    for folder_keyword in sys.argv[1:]:
        test_files = get_test_files(folder_keyword)
        all_test_files.extend(test_files)

    if not all_test_files:
        print("❌ No test cases to run.")
        sys.exit(0)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_folder = os.path.join("logs", timestamp)
    os.makedirs(log_folder, exist_ok=True)

    print(f"\n🧪 Total test files: {len(all_test_files)}")
    print(f"🧠 Parallel threads: {get_safe_thread_limit()}\n")

    batch_size = 2
    module_summary = defaultdict(lambda: {"passed": 0, "failed": 0, "skipped": 0})

    for i in range(0, len(all_test_files), batch_size):
        batch = all_test_files[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=len(batch)) as executor:
            futures = [executor.submit(run_single_test, file, log_folder) for file in batch]
            for future in as_completed(futures):
                module, passed, failed, skipped = future.result()
                module_summary[module]["passed"] += passed
                module_summary[module]["failed"] += failed
                module_summary[module]["skipped"] += skipped
        clear_memory_cache()
        time.sleep(3)

    # Final Summary
    print("\n📊 Module-wise Test Summary:")
    grand_total = {"passed": 0, "failed": 0, "skipped": 0}
    for module, results in module_summary.items():
        print(f"\n📁 Module: {module}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⏭️ Skipped: {results['skipped']}")
        total = sum(results.values())
        print(f"📦 Total: {total}")
        for key in grand_total:
            grand_total[key] += results[key]

    print("\n📋 Overall Test Summary:")
   
    print(f"✅ Passed: {grand_total['passed']}")
    print(f"❌ Failed: {grand_total['failed']}")
    print(f"⏭️ Skipped: {grand_total['skipped']}")
    print(f"📦 Total Tests: {sum(grand_total.values())}")
    print(f"🕔 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 Logs saved in: {log_folder}")

    generate_allure_report()
