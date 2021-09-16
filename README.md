# coursectl

The `coursectl` is a tool to author courses on web apps built using the [Community LMS][1].

[1]: https://github.com/fossunited/community

## How to install

The `coursectl` depends on [frappe-client][]. It is not availble on pypi, so you need install it manually.

```
$ pip install https://github.com/frappe/frappe/client/zipball/master/
```

Once that is done, install using `coursectl` using pip:

```
$ pip install https://github.com/fossunited/coursectl/zipball/master/"
```

[frappe-client]: https://github.com/frappe/frappe-client

### How to use

The Community LMS is built using the frappe framework and the `coursectl` command requires the api-key and api-secret to communite with the server. Please refer to [Frappe Documentation][2] to learn how to create them.

[2]: https://frappeframework.com/docs/user/en/guides/integration/how_to_set_up_token_based_auth


### Configure 

The first step is to provide the credentials to the tool. 

```
$ coursectl configure
FRAPPE_API_KEY: XXXXX
FRAPPE_API_SECRET: YYYY 
FRAPPE_SITE_URL: https://mon.school/

Updated configuration for profile default in /home/anand/.config/frappe/config.
```

This command saves the credentials in `~/.config/frappe/config` file.

It is possible to have multiple profiles and specify the profile when running a command. These are typically used to push the course to a dev server while developing the course and push to production after it is ready. The name of the default profile is `default`.

To configure a new profile, just pass `--profile` argument to configure.

```
$ coursectl configure --profile dev
...
```

### Pulling an existing course from a server

TODO: add documentation for every command