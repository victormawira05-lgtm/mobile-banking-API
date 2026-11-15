import pathlib
p = pathlib.Path("app/main.py")
text = p.read_text()
if "CORSMiddleware" not in text:
    text = text.replace(
        "from fastapi import FastAPI",
        "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware"
    )
    text = text.replace(
        "app = FastAPI(",
        "app = FastAPI("
    )
    # Insert middleware right after app = FastAPI(...)
    lines = text.splitlines()
    new_lines = []
    added = False
    for line in lines:
        new_lines.append(line)
        if "app = FastAPI" in line and not added:
            # find closing )
            # add after next few lines - simple: add after app definition
            pass
    # Better: insert after first app = block
    text = text.replace(
        "app = FastAPI(title=",
        "app = FastAPI(title="
    )
    # Simple patch: add middleware after app creation
    if "app.add_middleware" not in text:
        text = text.replace(
            "app =",
            "from fastapi.middleware.cors import CORSMiddleware\napp =",
            1
        ) if "CORSMiddleware" not in text else text

print("Current main.py:")
print(text[:1000])
