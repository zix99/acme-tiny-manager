
# Certificate manager

Manages certificates in /etc/certs and stores keys and challenges locally.

Requires that nginx be setup according to the acme_tiny readme, with the challenges directory being in this subdirectory.

Keep user.key super private.  Will be generated if not founds in `keys` folder.

Requires root permissions.

## Dependencies

* Python 2.x
* openssl
* wget

