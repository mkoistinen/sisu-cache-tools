# sisu-cache-tools

Basic cache management tools for djangoCMS projects.

Implements a relatively automatic cache-invalidation capability and a
'precache' management command.

This is useful for sites that have largely static content and are using
memcached.

## Installation

```` shell
pip install sisu-cache-tools
````

Then, add `cache_tools` to your project's INSTALLED_APPS in settings.
Sisu Cache Tools does not use an database models, so no migration is
necessary, but it must be added to INSTALLED_APPS, or the management commands
will not be found and the signal handlers will not "see" any signals.


## Automated Cache invalidation

To get the automated cache-invalidation, add 'taints_cache = True' as a class-
attribute on any models that contain objects that will change the way pages
appear. Using signals, this module will detect changes to those model objects
and invalidate the (entire) cache.

The cache can also be cleared with:

```` shell
python manage.py clearcache
````

## Automated Varnish Cache Invalidation (via BAN)

**New from version 0.1.0**

Assuming there are one or more Varnish cache servers with a VCL that includes something like:

```` vcl
acl purge {
    "appserver1.your_domain.xyz",
    "appserver2.your_domain.xyz",
    "appserver3.your_domain.xyz",
}

sub vcl_recv {

	...

    if (req.request == "DELETE" && req.http.X-Ban-Host) {
        if ( !client.ip ~purge ) {
            error 405 "Not allowed";
        }
        ban("obj.http.x-host ~ " + req.http.X-Ban-Host);
        error 200 "Banned";
    }

	...
}
````

and you have configured a list of these servers in settings.CACHE_SERVERS:

```` python
CACHE_SERVERS = [
	10.0.0.1,
	10.0.0.2,
]
````

and you have django.contrib.sites in use in your settings:

```` python
INSTALLED_APPS = (
    ....
    'django.contrib.sites',
    ....
)

...

SITE_ID = 1
````

Sisu Cache Tools will then send a DELETE request with the header X-Ban-Host to your Varnish cache servers so that even your remote caches are "cleared" too.



## Pre-emptive Caching

When the operator is done with all of their changes, the might consider using:

```` shell
python manage.py precache
````

to make HTTP requests to every page found in the sitemaps defined in the
ROOT_URLCONF. This will essentially preemptively load the pages into the cache
so your visitors will get speedy access, even if they're the first one to
'hit' a given page.

Also, to simply review all of the URLs, the operator can use:

```` shell
python manage.py listurls
````

And it will print all of the known URLs to stdout.
