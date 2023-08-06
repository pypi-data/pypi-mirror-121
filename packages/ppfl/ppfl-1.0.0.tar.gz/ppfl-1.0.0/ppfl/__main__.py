import re
import requests
import sys

PROJ_BASE = "https://pypi.org/pypi/{}/json"
URL_RE = re.compile(r"(https?|s?ftp)://(\S+)", re.I)

def get_license(req):
    license = req["license"] or "UNKNOWN"
    for c in req["classifiers"]:
        if "License" in c:
            license = c.split("::")[-1].strip()
            break
    if license == "UNKNOWN":
        license = license.capitalize()
    if len(license) > 100:
        return "License name contains too many characters to display here."
    return license

def get_requires_python(req):
    pyr = req["requires_python"]
    if not pyr:
        return
    name = "Python Version Requirement"
    if len(pyr.split(",")) > 1:
        name += "s"
    return " | ".join(pyr.split(","))

def get_project_urls(req):
    links = req["project_urls"]
    if not links:
        return
    filtered_links = filter(lambda x: re.match(URL_RE, x[1]), list(links.items()))
    return "\n" + "\n".join(f"- {n}: {l}" for n, l in filtered_links)

def get_classifiers(req):
    classifiers = req["classifiers"]
    if not classifiers:
        return
    sort = sorted(classifiers, key=lambda x: len(x.split("::")[0]))
    return "\n" + "\n".join(f"- {x}" for x in sort)

def main():
    if not sys.argv[1:]:
        print("Please provide a project.")
        return
    proj = sys.argv[1]
    req = requests.get(PROJ_BASE.format(proj))
    if req.status_code != 200:
        print("Error: No project found with the name '%s'" % proj)
        return
    req = req.json()["info"]
    title = f"{req['name']} | {req['version']}"
    print()
    print(title)
    print("~" * len(title))
    print(req["summary"] or "No description was provided for this project.")
    print()
    if req["author"] == " ":
        print("Author", "Unknown", sep=": ")
    else:
        print("Author", req["author"], sep=": ")
    if maintainer_email := req["maintainer_email"]:
        print("Maintainer Email", maintainer_email, sep=": ")
    print("License", get_license(req), sep=": ")
    if requires_python := get_requires_python(req):
        print("Python Requirements", requires_python, sep=": ")
    print("Project URL", req["package_url"], sep=": ")
    if project_urls := get_project_urls(req):
        print()
        print("Project URLs", project_urls, sep=": ")
    if classifiers := get_classifiers(req):
        print()
        print("Classifiers", classifiers, sep=": ")

if __name__ == "__main__":
    main()
