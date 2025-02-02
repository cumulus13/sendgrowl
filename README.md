# sendgrowl
Send notification to growl with multiple host and port

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
$ pip install sendgrowl
```

## Example

```python
>>> from sendgrowl import Growl
>>> Growl().send("TEST", "test", "test title", "test message", host = ['127.0.0.1', '192.168.43.236'], icon = icon)
```

run on terminal/cmd

```bash
$ usage: sendgrowl [-h] [-H [HOST ...]] [-P PORT] [-t TIMEOUT] [-i ICON] [-s] [-p PRIORITY] [-c CALLBACK] [-gc GNTP_CALLBACK] [-x CUSTOM_HEADERS] [-ax APP_HEADERS] [-gC GNTP_CLIENT_CLASS] [-id ID] [-cd COALESCING_ID] [-v] APP_NAME EVENT_NAME TITLE TEXT

positional arguments:
  APP_NAME              App name as registered/registering
  EVENT_NAME            Event name
  TITLE                 Title name
  TEXT                  Message/Text to be sending

options:
  -h, --help            show this help message and exit
  -H [HOST ...], --host [HOST ...]
                        host growl server
  -P PORT, --port PORT  port growl server
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout message display default: 20
  -i ICON, --icon ICON  Image icon path, default growl icon
  -s, --sticky          Sticky notification
  -p PRIORITY, --priority PRIORITY
                        Priority number, default 0
  -c CALLBACK, --callback CALLBACK
                        Call back function
  -gc GNTP_CALLBACK, --gntp-callback GNTP_CALLBACK
                        GNTP Call back function
  -x CUSTOM_HEADERS, --custom-headers CUSTOM_HEADERS
                        Custom Headers
  -ax APP_HEADERS, --app-headers APP_HEADERS
                        Custom Headers for app
  -gC GNTP_CLIENT_CLASS, --gntp-client-class GNTP_CLIENT_CLASS
                        GNTP client Class
  -id ID, --id ID       ID
  -cd COALESCING_ID, --coalescing-id COALESCING_ID
                        Coalescing Id
  -v, --verbose         Verbose
```

## Support

- Python 3.x

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)


