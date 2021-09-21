from pathlib import Path
import re

import frontmatter
from frappeclient import FrappeClient

from . import config

class API:
    def __init__(self, profile):
        self.profile = profile
        self.config = config.read_config(profile)
        self.frappe = self.get_frappe()

    def get_frappe(self):
        # TODO: verify that config is valid
        url = self.config['frappe_site_url'].rstrip("/")
        api_key = self.config['frappe_api_key']
        api_secret = self.config['frappe_api_secret']

        frappe = FrappeClient(url)
        frappe.authenticate(api_key, api_secret)
        return frappe

    def save_document(self, doctype, name, doc):
        data = {
            "doctype": doctype,
            "name": name,
            "doc": doc
        }
        return invoke_method(self.frappe, "mon_school.api.save_document", data=data)

    def push_lesson(self, filename):
        print("{} -- pushing lesson {}".format(self.config['frappe_site_url'], filename))
        lesson = Lesson.from_file(filename)
        self.save_document("Lesson", lesson.name, lesson.dict())

    def pull_lesson(self, name):
        print("{} -- pulling lesson {} ...".format(self.config['frappe_site_url'], name))
        doc = self.frappe.get_doc("Lesson", name)
        lesson = Lesson(name, doc)
        lesson.save_file()

def invoke_method(frappe, method, data):
    url = frappe.url + "/api/method/" + method
    result = frappe.session.post(url, json=data).json()
    message = result['message']
    if message.get("ok"):
        return message
    else:
        raise Exception(message.get("error") or f"unknown error: {message}")

RE_TITLE = re.compile("# (.*)")

class Lesson:
    def __init__(self, name, doc):
        self.name = name
        self.chapter = doc.get("chapter", "no-chapter")
        self.title = doc.get("title", name)
        self.body = doc.get("body", "")
        self.include_in_preview = doc.get("include_in_preview") == True

    def _load_file(self, path: Path):
        text = path.read_text()
        data = frontmatter.loads(text)

        title_line, *lines = data.content.strip().splitlines()
        self.title = title_line.strip(" #")
        self.body = "\n".join(lines).strip()


        self.chapter = data.get("chapter") or path.parent.name
        self.include_in_preview = data.get("include_in_preview") == True

    def find_title(self):
        m = RE_TITLE.search(self.body)
        return m.group(1).strip() if m else self.name

    def save_file(self):
        """Saves this lesson as a file.
        """
        path = Path(f"{self.chapter}/{self.name}.md")
        path.parent.mkdir(exist_ok=True)

        text = LESSON_TEMPLATE.format(
            title=self.title,
            body=self.body,
            include_in_preview=str(self.include_in_preview).lower()
        )
        print("writing file", path)
        path.write_text(text)

    @classmethod
    def from_file(cls, filename):
        path = Path(filename).absolute()
        name = path.stem
        lesson = Lesson(name, {})
        lesson._load_file(path )
        return lesson

    def dict(self):
        return {
            "chapter": self.chapter,
            "include_in_preview": self.include_in_preview,
            "body": self.body
        }

LESSON_TEMPLATE = """
---
include_in_preview: {include_in_preview}
---

# {title}

{body}
"""