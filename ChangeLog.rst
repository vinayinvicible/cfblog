cfblog ChangeLog
================
0.1.9 - 20-Oct-2015
-------------------

* fixed issues #12, #13 and #14

* scripts and templates install in package folder.

* replaced `request.path` usage with `request.path_info`.

* added catchall url to fix the `csrf_token` being loaded as `NOTPROVIDED`.

* `process_response` now catches all the exceptions similar to flatpage middleware and return the original response.

* rewrote ContentManager to support chaining custom methods.

* added proper post notification on post failure.

0.1.8 - 15-Oct-2015
-------------------

* bug fix for `__getitem__` on CacheObject

0.1.7 - 14-Oct-2015
-------------------

* added view on site option at admin list_display.
* added MANIFEST template to include static and templates in the package.
* pre loading localStorage value in the editor if exists.
* bug fixes while publishing content.

0.1.6 - 9-Oct-2015
------------------

* not escaping html elements while parsing through markdown
* added tests for this change

0.1.5 - 9-Oct-2015
------------------

* changed requirement from `django-jsonfield` to `jsonfield`

0.1.4 - 9-Oct-2015
------------------

* restricted static page category deletion from admin page instead of `AssertionError`

0.1.3 - 9-Oct-2015
------------------

* middleware is now called `cfblog.Middleware` [Backward Incompatible]

0.1.2 - 8-Oct-2015
------------------

* added `blank=True` for auth_data and public_data fields

0.1.1 - 8-Oct-2015
------------------

* fixed a typo in readme

0.1.0 - 8-Oct-2015
------------------

* first release

