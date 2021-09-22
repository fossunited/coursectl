# Introduction

The `coursectl` is a CLI tool for managing courses on instances of [community app][]. Currently, this is used for authoring courses on [Mon School][].

[community app]: https://github.com/fossunited/community
[Mon School]: https://mon.school/

This allows the course creators to:

- write the course material in markdown using their favorite editor
- preview it locally using mkdocs for material
- push the changes to the server using `coursectl`

This also allows the course creators to push the course to multiple sites. For example, keep pushing to a staging website to show the preview with a small group and push to the main site after it is ready.

## Installation

Install coursectl using:

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
anand@fossunited.org
```

