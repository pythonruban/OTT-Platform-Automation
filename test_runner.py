from ai_analyzer import get_ai_suggestion
import traceback

def run_test_with_ai(test_function, test_name):
    try:
        test_function()
    except Exception as e:
        error = traceback.format_exc()
        print(f"❌ {test_name} Failed\n\n{error}")
        
        prompt = f"""My Selenium/Pytest script for test case '{test_name}' failed. Here's the error log:
{error}

Please suggest:
1. The reason for failure
2. The code correction (if needed)
3. How to fix it in the webpage or test script
"""
        ai_response = get_ai_suggestion(prompt)

        with open(f"Reports/{test_name}_failure_report.txt", "w", encoding="utf-8") as report_file:
            report_file.write("ERROR:\n" + error)
            report_file.write("\n\nSUGGESTION FROM AI:\n" + ai_response)

        print("✅ AI report generated at:", f"Reports/{test_name}_failure_report.txt")