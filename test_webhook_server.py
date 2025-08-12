# webhook_trigger.py

from flask import Flask, request, jsonify
import subprocess, requests, base64, os, re, glob, json
from PIL import Image, ImageEnhance
import numpy as np
from sklearn.cluster import DBSCAN
from dotenv import load_dotenv
from threading import Thread
from concurrent.futures import ProcessPoolExecutor, as_completed


load_dotenv()
app = Flask(__name__)

BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME")
# BITBUCKET_API_TOKEN = os.getenv("BITBUCKET_API_TOKEN")
BITBUCKET_APP_PASSWORD = os.getenv("BITBUCKET_APP_PASSWORD")
BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")

POSTMARK_API_TOKEN = "4872bc90-08b9-47c2-9cac-e5d8bd83c72c"
FROM_EMAIL = "sanjai@webnexs.in"
TO_EMAIL = "kowsalya@webnexs.in"
# CC_EMAILS = ["manoj@webnexs.com", "david@webnexs.com", "dbl0207@gmail.com"]

STATUS_FILE = "/home/automationflickn/vodwebsite/test_status.json"

MODULE_SOURCES = {
    "Modules-Admin": [
        # "Advertiser_Management", "All_Slider", "App_setting", "AudioManagement",
        # "Cast", "Cms_page", "Contact_Request", "homepage_settings",
        # "Language&Translation", "Library", "LiveStream","Login_Signup",
        # "Logs_last_module", "Main_settings", "Menus", "OurPlans", "Partner",
        # "Payment", "Playersetting", "Registration_Menu", "Role_Management ",
        # "Seo_meta", "Series_Episodes", "Storefront_Settings", "User_Management",
          "Video_management",
    ],
    # "Frontend-Modules": [
    #     "Choose-Profile", "Forgetpassword", "HomePage", "LIVE", "Login",
    #     "Movies", "music", "myprofile", "SERIES", "Sing-up", "Videos",
    #     "WatchLater", "Wishlater"
    # ],
    # "Advertisements":["AddAdverser", "Login", "Signup"]
}

def load_branch_status():
    return json.load(open(STATUS_FILE)) if os.path.exists(STATUS_FILE) else {}

def save_branch_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def update_bitbucket_status(commit_hash, state, description, url):
    endpoint = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_REPO_SLUG}/commit/{commit_hash}/statuses/build"
    payload = {
        "state": state,
        "key": "automation-tests",
        "name": "Automation Test Result",
        "url": url,
        "description": description
    }
    # response = requests.post(endpoint, json=payload, auth=(BITBUCKET_USERNAME, BITBUCKET_API_TOKEN))
    response = requests.post(endpoint, json=payload, auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))

    print("✅ Status update" if response.ok else f"❌ Status error: {response.text}")

def comment_on_pr(pr_id, message):
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/comments"
    response = requests.post(url, json={"content": {"raw": message}}, auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    print("💬 PR commented" if response.status_code == 201 else f"❌ Comment failed: {response.text}")

def send_postmark_email(subject, html_body, attachment_paths=None):
    headers = {
        "Accept": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "From": FROM_EMAIL,
        "To": TO_EMAIL,
        # "Cc": ",".join(CC_EMAILS),
        "Subject": subject,
        "HtmlBody": html_body,
        "MessageStream": "broadcast"
    }
    if attachment_paths:
        failed_images = [p for p in attachment_paths if screenshot_contains_red_error(p)]
        payload["Attachments"] = [ {
            "Name": os.path.basename(p),
            "Content": base64.b64encode(open(p, "rb").read()).decode(),
            "ContentType": "image/png"
        } for p in failed_images if os.path.exists(p) ]
    r = requests.post("https://api.postmarkapp.com/email", json=payload, headers=headers)
    print("✅ Email sent" if r.status_code == 200 else f"❌ Email error: {r.text}")

def collect_all_screenshots(folder):
    return glob.glob(os.path.join(folder, "**", "*.png"), recursive=True)

def screenshot_contains_red_error(path):
    try:
        img = Image.open(path).convert("RGB")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        np_img = np.array(img)

        orange_mask = (
            (np_img[:, :, 0] >= 200) & (np_img[:, :, 0] <= 255) &
            (np_img[:, :, 1] >= 90) & (np_img[:, :, 1] <= 180) &
            (np_img[:, :, 2] >= 0) & (np_img[:, :, 2] <= 80)
        )

        red_mask = (
            (np_img[:, :, 0] >= 180) &
            (np_img[:, :, 1] <= 100) &
            (np_img[:, :, 2] <= 100) &
            (~orange_mask)
        )

        red_pixels = np.argwhere(red_mask)
        if len(red_pixels) == 0:
            return False

        clustering = DBSCAN(eps=10, min_samples=20).fit(red_pixels)
        for label in set(clustering.labels_):
            if label == -1:
                continue
            region = red_pixels[clustering.labels_ == label]
            if (region[:, 1].ptp() >= 10) and (region[:, 0].ptp() >= 10):
                return True
        return False
    except Exception as e:
        print(f"⚠️ Red check error: {e}")
        return False

def run_group(group):
    print(f"🚀 Running group: {group}")
    passed = failed = skipped = 0
    test_file_status = {}

    process = subprocess.Popen(["python3", "order.py", group], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in iter(process.stdout.readline, ""):
        line = line.strip()
        if not line:
            continue
        print(f"[{group}] {line}")  # print everything live tagged

        # Detect test file starting
        match_start = re.search(r"collected.*?items.*?\n=+.*?(\w+\.py)", line)
        if match_start:
            current_test = match_start.group(1)
            print(f"🟡 RUNNING — {current_test}")
            test_file_status[current_test] = "RUNNING"

        # Detect result status
        if "PASSED" in line and ".py" in line:
            filename = re.search(r"(\w+\.py)", line)
            if filename:
                print(f"✅ PASSED — {filename.group(1)}")
                test_file_status[filename.group(1)] = "PASSED"
                passed += 1

        elif "FAILED" in line and ".py" in line:
            filename = re.search(r"(\w+\.py)", line)
            if filename:
                print(f"❌ FAILED — {filename.group(1)}")
                test_file_status[filename.group(1)] = "FAILED"
                failed += 1

        elif "SKIPPED" in line and ".py" in line:
            filename = re.search(r"(\w+\.py)", line)
            if filename:
                print(f"⏭️ SKIPPED — {filename.group(1)}")
                test_file_status[filename.group(1)] = "SKIPPED"
                skipped += 1

    process.stdout.close()
    process.wait()

    total = passed + failed + skipped
    print("📊 Final Summary:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️ Skipped: {skipped}")
    print(f"📂 Total Tests: {total}")

    status = "Failed" if failed else "Passed" if passed else "Skipped"
    return group, status, passed, failed, skipped


def run_test_groups(groups):
    results = []
    batch_size = 3  # ⛔ reduced for lower memory use
    batches = [groups[i:i + batch_size] for i in range(0, len(groups), batch_size)]

    for batch_index, batch in enumerate(batches):
        print(f"🧪 Batch {batch_index+1}/{len(batches)} — Groups: {batch}")
        with ProcessPoolExecutor(max_workers=min(len(batch), 2)) as executor:  # ⛔ limit parallelism
            futures = [executor.submit(run_group, g) for g in batch]
            for future in as_completed(futures):
                results.append(future.result())

    p = sum(x[2] for x in results)
    f = sum(x[3] for x in results)
    s = sum(x[4] for x in results)
    return p, f, s, results

def run_and_email(branch, commit, pr_id):
    groups = MODULE_SOURCES["Modules-Admin"]
    # + MODULE_SOURCES["Frontend-Modules"]
    print("🗂️ Running modules from:")
    for module, g_list in MODULE_SOURCES.items():
        print(f"  📁 {module}: {len(g_list)} groups")

    passed, failed, skipped, test_results = run_test_groups(groups)

    screenshots = collect_all_screenshots("/home/automationflickn/vodwebsite/reports")
    visual_fails = sum(1 for s in screenshots if screenshot_contains_red_error(s))
    failed += visual_fails
    passed = max(0, passed - visual_fails)

    test_result = "passed" if failed == 0 else "failed"
    status_data = load_branch_status()
    status_data[branch] = test_result
    save_branch_status(status_data)

    status_table = "".join(
        f"<tr><td><b>{b}</b></td><td style='color:{'green' if r == 'passed' else 'red'}'>{r.upper()}</td></tr>"
        for b, r in status_data.items()
    )

    result_table = "".join(
        f"<tr><td>{name}</td><td>{res}</td><td>{p}</td><td>{f}</td><td>{s}</td></tr>"
        for name, res, p, f, s in test_results
    )

    module_list_html = "".join(
        f"<li><b>{mod}</b>: {len(grps)} test groups</li>" for mod, grps in MODULE_SOURCES.items()
    )

    html_body = f"""
        <h2>🧪 Test Report – <b>{branch}</b></h2>
        <h3>📌 Branch Test Status</h3>
        <table border='1' cellpadding='6' style='border-collapse:collapse; font-size:15px;'>
            <tr><th>Branch</th><th>Status</th></tr>
            {status_table}
        </table>
        <h3>📂 Module Sources</h3>
        <ul>{module_list_html}</ul>
        <h3>📋 Individual Test Results</h3>
        <table border='1' cellpadding='6'>
            <tr><th>Test Group</th><th>Status</th><th>Passed</th><th>Failed</th><th>Skipped</th></tr>
            {result_table}
        </table>
    """

    subject = f"Test Results – {branch}: ✅ {passed} ❌ {failed}"
    send_postmark_email(subject, html_body, screenshots)
    update_bitbucket_status(commit, "SUCCESSFUL" if test_result == "passed" else "FAILED", f"{test_result.upper()} – {branch}", "https://webnexs.com")

    if pr_id and test_result == "failed":
        comment_on_pr(pr_id, f"❌ Tests failed in {branch}. Please fix before merging.")

@app.route("/", methods=["GET"])
def index():
    return "✅ Webhook server is running", 200

@app.route("/bitbucket-webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload"}), 400

    if "push" not in data or "changes" not in data["push"]:
        print("⚠️ Ignored non-push event")
        return jsonify({"status": "ignored - not a push event"}), 200

    try:
        branch = data["push"]["changes"][0]["new"]["name"]
        commit = data["push"]["changes"][0]["new"]["target"]["hash"]
        pr_id = data.get("pullrequest", {}).get("id")
    except (IndexError, KeyError, TypeError) as e:
        print(f"❌ Error extracting branch/commit info: {e}")
        return jsonify({"error": "Malformed payload"}), 400

    print(f"🚀 Branch pushed: {branch} | Commit: {commit}")

    branch_flow = ["node-staging", "node-master", "node-version1"]
    if branch not in branch_flow:
        return jsonify({"skip": True, "reason": f"Branch {branch} not in flow"}), 200

    status_data = load_branch_status()
    prev_index = branch_flow.index(branch) - 1
    if prev_index >= 0:
        prev_branch = branch_flow[prev_index]
        if status_data.get(prev_branch) != "passed":
            reason = f"❌ Merge blocked: Previous stage '{prev_branch}' has failing test cases."
            print(reason)
            if pr_id:
                comment_on_pr(pr_id, reason)
            return jsonify({"blocked": True, "reason": reason}), 403

    Thread(target=run_and_email, args=(branch, commit, pr_id)).start()
    return jsonify({"message": f"🧪 Running tests for {branch}..."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
