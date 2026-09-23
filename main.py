import base64
import requests

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
GITHUB_TOKEN = "your_github_personal_access_token"
REPO_OWNER = "your_github_username"
REPO_NAME = "your_repository_name"
BRANCH = "main"

# ---------------------------------------------------------------------------
# FILE CONTENTS
# ---------------------------------------------------------------------------
files_to_push = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KASS Enrollment Form</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h2>KASS Enrollment Form</h2>
        <form id="kassForm">
            <label for="empName">Employee Name (Capital Letters):</label>
            <input type="text" id="empName" required>
            <label for="kgidNumber">KGID Number:</label>
            <input type="text" id="kgidNumber" required>
            <label for="aadhaar">Aadhaar Number:</label>
            <input type="text" id="aadhaar" required>
            <button type="submit">Save Details</button>
        </form>
    </div>
    <script src="script.js"></script>
</body>
</html>""",

    "style.css": """body { font-family: Arial, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; padding: 40px; }
.container { background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
h2 { color: #333; font-size: 1.2rem; margin-bottom: 20px; }
label { display: block; margin-top: 15px; font-weight: bold; font-size: 0.9rem; color: #555; }
input { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
button { margin-top: 25px; width: 100%; padding: 12px; background: #0056b3; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }
button:hover { background: #004494; }""",

    "script.js": """document.getElementById('kassForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = {
        name: document.getElementById('empName').value,
        kgid: document.getElementById('kgidNumber').value,
        aadhaar: document.getElementById('aadhaar').value
    };
    console.log("KASS Form Data Captured:", formData);
    alert("Form submitted successfully! Check console for data.");
});"""
}

# ---------------------------------------------------------------------------
# PUSH LOGIC
# ---------------------------------------------------------------------------
def push_to_github(file_path, content, token, owner, repo, branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Check if the file already exists to get its SHA
    sha = None
    get_response = requests.get(url, headers=headers, params={"ref": branch})
    if get_response.status_code == 200:
        sha = get_response.json().get("sha")

    # Encode content to Base64
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    # Prepare payload
    data = {
        "message": f"Add or update {file_path}",
        "content": encoded_content,
        "branch": branch
    }
    if sha:
        data["sha"] = sha 

    # Upload
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✅ Successfully pushed: {file_path}")
    else:
        print(f"❌ Failed to push {file_path}: {response.json().get('message')}")

if __name__ == "__main__":
    for file_name, file_content in files_to_push.items():
        push_to_github(
            file_path=file_name,
            content=file_content,
            token=GITHUB_TOKEN,
            owner=REPO_OWNER,
            repo=REPO_NAME,
            branch=BRANCH
        )
