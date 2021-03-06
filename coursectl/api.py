from pathlib import Path

import frontmatter
from frappeclient import FrappeClient
import yaml

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

    def push_lesson(self, filename):
        print("{} -- pushing lesson {}".format(self.config['frappe_site_url'], filename))
        lesson = Lesson.from_file(filename)
        self.save_document("Course Lesson", lesson.name, lesson.dict())

    def pull_lesson(self, name):
        print("{} -- pulling lesson {} ...".format(self.config['frappe_site_url'], name))
        doc = self.frappe.get_doc("Course Lesson", name)
        lesson = Lesson(name, doc)
        lesson.save_file()

    def push_exercise(self, filename):
        print("{} -- pushing exercise {}".format(self.config['frappe_site_url'], filename))
        exercise = Exercise.from_file(filename)
        exercise.push(api=self)

    def pull_exercise(self, name):
        print("{} -- pulling exercise {} ...".format(self.config['frappe_site_url'], name))
        exercise = Exercise.load(self, name)
        exercise.save_file()

    def pull_course(self, name):
        print("{} -- pulling course {} ...".format(self.config['frappe_site_url'], name))
        course = Course.load(self.frappe, name)
        course.save_file()
        return course

    def push_course(self, filename):
        course = Course.from_file(filename)
        course.push(self)

    def clone(self, course_name):
        course = self.pull_course(course_name)
        for c in course.chapters:
            for name in c.lessons:
                self.pull_lesson(name)

        for name in self.get_exercises(course_name):
            self.pull_exercise(name)

    def get_exercises(self, course_name):
        """Returns names of all exercises in a course.
        """
        filters = {"course": course_name}
        exercises = self.frappe.get_list("Exercise", fields=['name'], filters=filters)
        return [e['name'] for e in exercises]

    def whoami(self):
        url = self.frappe.url + "/api/method/" + "frappe.auth.get_logged_user"
        response = self.frappe.session.get(url).json()
        return response['message']

    def save_document(self, doctype, name, doc):
        data = {
            "doctype": doctype,
            "name": name,
            "doc": doc
        }
        return self.invoke_method("mon_school.api.save_document", data=data)

    def get_doc(self, doctype, name):
        return self.frappe.get_doc(doctype, name)

    def exists(self, doctype, name):
        return bool(self.get_doc(doctype, name))

    def invoke_method(self, method, data):
        url = self.frappe.url + "/api/method/" + method
        result = self.frappe.session.post(url, json=data).json()
        if "message" not in result:
            print("ERROR:", result)
            raise Exception(f"Failed to invoke method: {method}")

        message = result['message']
        if message.get("ok"):
            return message
        else:
            raise Exception(message.get("error") or f"unknown error: {message}")

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

        self.title = data.get("title") or path.stem.replace("-", " ").title()
        self.body = data.content

        self.chapter = data.get("chapter") or path.parent.name
        self.include_in_preview = data.get("include_in_preview") == True

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
            "title": self.title,
            "body": self.body or "-"
        }

class Course:
    def __init__(self, name, doc):
        self.name = name
        self.doc = doc
        self.chapters = self.doc['chapters']

    @property
    def title(self):
        return self.doc.get('title')

    def save_file(self, filename="course.yml"):
        print("writing file course.yml")
        with open("course.yml", "w") as f:
            data = self.dict()
            yaml.safe_dump(data, f, sort_keys=False)

    def dict(self):
        fields = ['name', 'is_published', 'title', 'short_introduction', 'description']
        data = {k: self.doc[k] for k in fields}
        data['chapters'] = [c.to_simple_dict() for c in self.chapters]
        return data

    @classmethod
    def load(cls, api, name):
        doc = api.get_doc("LMS Course", name)
        doc['chapters'] = [Chapter.load(api, row['chapter']) for row in doc['chapters']]
        return cls(name, doc)

    @classmethod
    def from_file(cls, filename="course.yml"):
        data = yaml.safe_load(open(filename))
        data['chapters'] = [Chapter.from_dict(data["name"], c) for c in data['chapters']]
        return cls(data['name'], data)

    def push(self, api):
        doc = api.get_doc("LMS Course", self.name) or {}
        is_new_course = not doc

        keys = ['name', 'is_published', 'title', 'short_introduction', 'description']
        doc.update({k: self.doc[k] for k in keys if k in self.doc})

        if is_new_course:
            api.save_document("LMS Course", self.name, doc)

        for c in self.chapters:
            c.push(api)

        doc['chapters'] = [{"chapter": c.name} for c in self.chapters]
        api.save_document("LMS Course", self.name, doc)
        print(f"Course {self.name}: updated")

class Chapter:
    def __init__(self, name, doc):
        self.name = name
        self.doc = doc
        self.lessons = [row['lesson'] for row in doc['lessons']]

    @property
    def course(self):
        return self.doc['course']

    @property
    def title(self):
        return self.doc['title']

    @property
    def description(self):
        return self.doc['description']

    def __eq__(self, other):
        return (
            isinstance(other, Chapter)
            and self.name == other.name
            and self.title == other.title
            and self.description == other.description
            and self.lessons == other.lessons)

    def to_simple_dict(self):
        return {
            "name": self.name,
            "title": self.doc['title'],
            "description": self.doc['description'],
            "lessons": [self.get_lesson_filename(name) for name in self.lessons]
        }

    def get_lesson_filename(self, lesson):
        return f"{self.name}/{lesson}.md"

    @classmethod
    def load(cls, frappe, name):
        doc = frappe.get_doc("Course Chapter", name)
        return cls(name, doc)

    @classmethod
    def from_dict(cls, course, data):
        """Creates a Course from dictionary as chapter is specified in the course.yml file.

        Expected format:

            name: getting-started
            title: Getting Started
            description: Getting Started with Python
            lessons:
                - getting-started/hello-world.md
        """
        doc = dict(data)
        doc['course'] = course
        doc['lessons'] = [{"lesson": cls.find_lesson_name(path)} for path in data['lessons'] or []]
        return cls(data['name'], doc)

    @classmethod
    def find_lesson_name(cls, filepath):
        return Path(filepath).stem

    def push(self, api):
        doc = api.get_doc("Course Chapter", self.name)
        if not doc:
            self.create(api)
            doc = api.get_doc("Course Chapter", self.name)

        c2 = Chapter(self.name, doc)
        if self == c2:
            print(f"Chapter {self.name}: no changes to update")
            return

        keys = ['course', 'title', 'description']
        for k in keys:
            doc[k] = self.doc[k]

        def lesson_exists(lesson):
            exists = api.exists("Course Lesson", lesson)
            if not exists:
                print("ignoring missing lesson:", lesson)
            return exists

        doc['lessons'] = [{"lesson": lesson} for lesson in self.lessons if lesson_exists(lesson)]
        api.save_document("Course Chapter", self.name, doc)
        print(f"Chapter {self.name}: updated")

    def create(self, api):
        doc = {"course": self.course, "title": self.title, "description": self.description}
        api.save_document("Course Chapter", self.name, doc)


class Exercise:
    FIELDS = ["title", "description", "code", "answer", "hints", "tests"]

    def __init__(self, name, doc):
        self.name = name
        self.doc = self.subdict(doc, self.FIELDS)

    def __eq__(self, other):
        return (
            isinstance(other, Exercise)
            and self.name == other.name
            and self.doc == other.doc)

    def subdict(self, d, keys):
        return {k: d[k] for k in keys if k in d}

    def push(self, api):
        e = self.load(api, self.name)
        if self == e:
            print(f"Exercise {self.name}: no changes to update")
            return
        else:
            api.save_document("Exercise", self.name, self.doc)
            print(f"Exercise {self.name}: updated")

    @classmethod
    def load(cls, api, name):
        doc = api.get_doc("Exercise", name)
        return cls(name, doc)

    @classmethod
    def from_file(cls, filename):
        path = Path(filename).absolute()
        name = path.stem
        doc = yaml.safe_load(path.open())
        return cls(name, doc)

    def save_file(self):
        filename = f"exercises/{self.name}.yml"
        path = Path(filename)
        path.parent.mkdir(exist_ok=True)
        with path.open("w") as f:
            yaml.safe_dump(self.doc, f, sort_keys=False)
        print("saved exercise to", path)

# Hack from Stackoverflow:
# https://stackoverflow.com/questions/45004464/yaml-dump-adding-unwanted-newlines-in-multiline-strings#45004775
yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)

yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

LESSON_TEMPLATE = """\
---
title: {title}
include_in_preview: {include_in_preview}
---

{body}
"""