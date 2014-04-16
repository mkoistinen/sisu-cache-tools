sisu-cache-tools
================

Basic cache management tools for djangoCMS projects.

Implements a relatively automatic cache-invalidation capability and a 'precache' management command.

This is useful for sites that have largely static content and are using memcached.


Automated Cache invalidation
----------------------------

To get the automated cache-invalidation, add 'taints_cache = True' as a class-attribute on any models that contain objects that will change the way pages appear. Using signals, this module will detect changes to those model objects and invalidate the (entire) cache.

The cache can also be cleared with::

```` shell
python manage.py clearcache
````

Pre-emptive Caching
-------------------

When the operator is done with all of their changes, the might consider using::

```` shell
python manage.py precache
````

to make HTTP requests to every page found in the sitemaps defined in the ROOT_URLCONF. This will essentially preemptively load the pages into the cache so your visitors will get speedy access, even if they're the first one to 'hit' a given page.
