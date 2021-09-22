# Reference

## `coursectl configure`

Prompts for site url and api credentials and saves them in `~/.config/frappe/config` file.

```
$ coursectl configure
frappe_site_url: https://mon.school/
frappe_api_key: XXXX
frappe_api_secret: YYYY
write config to /home/anand/.config/frappe/config
```

The `coursectl` command supports multiple profiles and by default, it uses a profile with name `default`. A different profile can be configured by passing global option `--profile`.

```
$ coursectl --profile local configure
frappe_site_url: http://mon.localhost:8000/
frappe_api_key: XXXX
frappe_api_secret: YYYY
write config to /home/anand/.config/frappe/config
```

## `coursectl pull-lesson`

Pulls a lesson from the server and saves it locally.

```
$ coursectl pull-lesson hello-python
http://mon.school/ -- pulling lesson hello-python ...
writing file getting-started/hello-python.md
```

The lesson will be saved as `$chapter/$lesson.md`

ARGUMENTS:

_name_: name of the lesson to pull

## `coursectl push-course`

Updates the course and chapters from course.yml file.

```
$ coursectl push-course
Chapter getting-started: updated
Chapter drawing-shapes: updated
```

This also updates the lessons linked to each chapter, but it doesn't update the content of the lessons.

## `coursectl push-lesson`

Pushes one or more lessons to the server.

```
$ coursectl push-lesson getting-started/hello-joy.md getting-started/hello-python.md
http://mon.school/ -- pushing lesson getting-started/hello-joy.md
http://mon.school/ -- pushing lesson getting-started/hello-python.md
```

ARGUMENTS:

_filenames_: paths to lesson files to be pushed

## `coursectl version`

Prints the version of the `coursectl` command.

```
$ coursectl version
0.1.0
```

## `coursectl whoami`

Prints the email of the user with the specified api key.

```
$ coursectl whoami
foo@bar.com
```
