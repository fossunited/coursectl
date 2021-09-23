# Getting Started

## Installation

To install `coursectl`, install the following command from command-line:

```
$ pip install https://github.com/fossunited/coursectl/zipball/main
```

## Configuration

Using `coursectl` requires api key and api secret. Please ask the admin of the platform to create api key and secret for you.

Once you have the api key and secret, use the following command to configure `coursectl`.

```
$ coursectl configure
frappe_site_url: https://mon.school/
frappe_api_key: XXXXX
frappe_api_secret: YYYYY
```

Once you configure `coursectl` you can verify it using the `whoami` command.

```
$ coursectl whoami
foo@bar.com
```

TODO: explain about using multiple profiles

## Clone Your Course

The first step after you configure your environment is to clone your course.

```
$ coursectl clone the-joy-of-programming
...
```

This command will clone the specified course, all its chapters, lessons and exercises and saves them to the current directory.

The directory strucutre will be in the following structure:

```
.
├── course.yml
├── getting-started-jp
│   ├── hello-joy-jp.md
│   └── hello-python-jp.md
├── drawing-shapes-jp
│   ├── drawing-circles-jp.md
│   ├── lines-and-polygons-jp.md
├── exercises
│   ├── circle-jp.yml
│   ├── concentric-circles-x3-jp.yml
│   ├── draw-rectangle-jp.yml
│   ├── six-circles-in-a-line-jp.yml
```

The `course.yml` file will contain the information about the course and all the chapters.

There will be one directory for each chapter and each lesson in that chapter will be stored as a markdown file.

All the exercisies are placed in the `exercises/` diirectory as YAML files.

## Editing Course and Chapters

The course and chapter info is stored in the `course.yml` file.

This file must be edited to update the following:

- title of the course
- short intro of the course
- description of the course
- title of a chapter
- description of a chapter
- lessons that are part of a chapter

Let's understand the format of the `course.yml` file.

```
name: the-joy-of-programming
is_published: 1
title: The Joy of Programming
short_introduction: 'Start your journey into the magical world of programming, by
  writing programs to create amusing patterns. '
description: |
  Programming is fun. How about learning programming by writing programs to make the computer draw interesting shapes?

  In this course, you'll write programs to draw simple shapes and move on to draw more and more complex shapes by applying different ideas of programming introduced gradually through out the course.
chapters:
- name: getting-started-jp
  title: Getting Started
  description: A gentle introduction to programming.
  lessons:
  - getting-started-jp/hello-joy-jp.md
  - getting-started-jp/hello-python-jp.md
- name: drawing-shapes-jp
  title: Drawing Shapes
  description: ' Write small programs to draw simple shapes. '
  lessons:
  - drawing-shapes-jp/drawing-circles-jp.md
  - drawing-shapes-jp/lines-and-polygons-jp.md
```

Most of it is self explanatory.

One thing that you have noticed is that all chapter, lesson and exercise names have a `-jp` suffix. We use a two-letter short code for course and use that as a suffix for all names used for the course to avoid conflicts with names used for some other courses.

Please note that the name field is the course is the unique name that identifies that course in the system. For a lesson or an exercise, the name will be the filename sans the extension.

Whenever you make changes to the `course.yml`, you just need to run:

```
$ coursectl push-course
```

That will push the course to the server and you should see the course updated on the site.

## Editing a lesson

Let's first look at the strucure of a lesson.

```
---
include_in_preview: true
---

# Hello, Python!

In this lesson, we'll learn how to write simple Python programs.
```

The file has three parts. The first one is YAML frontmatter, as used with Jekyll.

The line after that starting with `#` is the title of the lesson.

Everything after that is the contents of the lesson.

The `include_in_preview` decides whether or not a preview is shown to the users who have not joined the course. Typically, the preview is made available for the lessons in the first few chapters.

Once you make changes to a lesson, you can push it to the server using:

```
$ coursectl push getting-started-jp/hello-python-jp.md
...
```

It is also possible to push multiple lessons at once:

```
$ coursectl push getting-started-jp/*.md
...
```

## Adding a new lesson

To add a new lesson, we need to create a new file in that directory corresponding to the chapter where want to add this lesson and also include it in the `course.yml` file under the lessons of that chapter.

Once these changes are done, we need to push the lesson and then push the course.


```
$ coursectl push-lesson getting-started-jp/new-lesson-jp.md
...

$ coursectl push-course
...
```

# Adding/editing an exercise

Exercises are stored in `exercise/*.yml`.

You can make changes to an existing exercise or create a new one. Once your exercise is ready, you need to push the exercise.

```
$ coursectl push-exercise exercises/circle-jp.yml
...
```

You an push all exercises at once using:

```
$ coursectl push-exercise exercises/*.yml
```

The `coursectl` will first test if there are any modifications and update only the ones that have been modified.

To include an exercise in a lesson, use the following markup.

```
{{ Exercise("circle-jp") }}
```
