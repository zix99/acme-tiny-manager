
# ACME-Tiny Certificate manager

This certificate manager wraps the [acme-tiny](https://github.com/diafygi/acme-tiny/) script to manage keys in `/etc/certs` and provide
the tooling to keep the keys up to date.

Much like the acme-tiny script, this one requires **root permissions**.


## Dependencies

* Python 2.x
* openssl
* wget

## Use

Keep user.key super private.  Will be generated if not founds in `keys` folder.

### First Time Setup

Run the script `create_or_renew.py` with the argument of the domain you
own on the server that is setup to use the domain.

It will generate your user key, domain key, and domain csr in the `keys` folder.

When asked to setup, create a route on your server to server files for `/.well-known/acme-challenge/` to
`/chalenges/*your domain*`.

eg, for nginx, your config might look like this:
```
# Normal HTTP redirect to SSL
server {
        listen 80;
        server_name example.com;

        # This is where it'll read the challenges from
        location /.well-known/acme-challenge/ {
                alias /path/to/challenges/example.com/;
                try_files $uri =404;
        }
        # Redirect to https
        location / {
                return 301 https://example.com;
        }
}


# The SSLd site
server {
        listen 443 ssl;
        server_name example.com;

        ssl_certificate /etc/certs/example.com.pem;
        ssl_certificate_key /etc/certs/example.com.pem;

        # Replace below with your normal config
        root /path/to/content;
        index index.html;
}
```

Continue the script.  Validation will occur, and you will get a crt.  The key, the crt, and the intermediate file
will be joined and output to `/etc/certs/*domain*.pem`

### Renewals

Set up a cron job to run `renew_all.py` monthly.

This script goes through each key-folder in `keys/`, and will call `renew` on them, outputting a new
key to `/etc/certs` if successful.

Make sure to reload your web server after the renewal script completes successfully.

eg, your crontab might look like this:
```
0 0 1 * * /path/to/renew_all.py && service nginx reload
```

# License

**The MIT License (MIT)**
Copyright (c) 2016 Christopher LaPointe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
