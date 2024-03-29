import re
import os

def get_version():
	with open("setup.py", "r") as setupfile:
		contents = setupfile.read()
		regex = r"version=('(\d*)\.(\d*)\.(\d*)')"
		result = re.search(regex, contents)
		whole = result.group(1)
		major = result.group(2)
		minor = result.group(3)
		patch = result.group(4)
		return whole, major, minor, patch


def delete_and_publish(tag):
	# returns true regardless of tag being deleted or not
        # allows for situations where tag doesn't exist
	os.system(f"git tag -d {tag} || true")
	os.system(f"git push origin :refs/tags/{tag}")
	os.system(f"git tag {tag}")
	os.system(f"git push origin {tag}")

def main():
	whole, major, minor, patch = get_version()
	delete_and_publish(whole)
	delete_and_publish(f"{major}.x")

if __name__ == "__main__":
	main()
