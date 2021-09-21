from coursectl.api import Lesson
from textwrap import dedent

class TestLesson:
    def test_attrs(self, tmp_path):
        path = tmp_path / "test-chapter" / "test-lesson.md"
        path.parent.mkdir()
        path.write_text("# Test Lesson\n\n")
        lesson = Lesson.from_file(path)

        assert lesson.name == "test-lesson"
        assert lesson.chapter == "test-chapter"
        assert lesson.title == "Test Lesson"
        assert lesson.include_in_preview == False

    def test_metatags(self, tmp_path):
        path = tmp_path / "test-chapter" / "test-lesson.md"
        body = """
        ---
        include_in_preview: True
        chapter: getting-started
        ---
        # Test Lesson

        hello, world!
        """
        path.parent.mkdir()
        path.write_text(dedent(body))
        lesson = Lesson.from_file(path)

        assert lesson.name == "test-lesson"
        assert lesson.chapter == "getting-started"
        assert lesson.title == "Test Lesson"
        assert lesson.include_in_preview == True
