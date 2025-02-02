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
> usage: sendgrowl.py [-h] [-H [HOST ...]] [-P PORT] [-t TIMEOUT] [-i ICON] APP_NAME EVENT_NAME TITLE TEXT

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

```

## Support

- Python 3.x

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)


