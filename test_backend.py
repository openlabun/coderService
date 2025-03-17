import requests

#API_URL = "http://localhost:8000/execute"
API_URL = "http://coderservice.openlab.uninorte.edu.co/execute"

# Define test cases for each language
test_cases = {
    "python": {
        "code": "print(\"Hello World\")",
        "expected_output": "Hello World\n"
    },
    "javascript": {
        "code": "console.log(\"Hello World\");",
        "expected_output": "Hello World\n"
    },
    "java": {
        "code": "public class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }",
        "expected_output": "Hello World\n"
    },
    "c": {
        "code": "#include <stdio.h>\nint main() { printf(\"Hello World\\n\"); return 0; }",
        "expected_output": "Hello World\n"
    },
    "cpp": {
        "code": "#include <iostream>\nint main() { std::cout << \"Hello World\" << std::endl; return 0; }",
        "expected_output": "Hello World\n"
    },
    "ruby": {
        "code": "puts \"Hello World\"",
        "expected_output": "Hello World\n"
    },
    "php": {
        "code": "<?php echo \"Hello World\\n\"; ?>",
        "expected_output": "Hello World\n"
    },
    "csharp": {
        "code": "using System; class Program { static void Main() { Console.WriteLine(\"Hello World\"); } }",
        "expected_output": "Hello World\n"
    },
    "go": {
        "code": "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello World\") }",
        "expected_output": "Hello World\n"
    },
    "r": {
        "code": "print(\"Hello World\")",
        "expected_output": "[1] \"Hello World\"\n"
    }
}

def test_execution():
    """Test code execution for all languages."""
    for language, data in test_cases.items():
        response = requests.post(API_URL, json={"language": language, "code": data["code"]})
        assert response.status_code == 200, f"Failed for {language}"
        response_json = response.json()
        assert "output" in response_json, f"Missing output for {language}"
        assert response_json["output"].strip() == data["expected_output"].strip(), f"Incorrect output for {language}"

if __name__ == "__main__":
    test_execution()
