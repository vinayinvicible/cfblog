.. _syntax:

===================================
Creating your own editable template
===================================

There are two ways in which you can edit a html page using cfblog.

    * Edit the content of the tag.
    * Edit any attribute of the tag.


Attributes
==========

Syntax
------

To make any attribute of a tag editable, add an attribute ``data-cms-attr`` inside the tag.

Value of the ``data-cms-attr`` should be of the form ``name_of_the_attribute:key``.

If you wish to edit multiple tags you can insert all the values following the above syntax separated using ``|`` (pipe).

.. code-block:: html

    <title data-cms-attr="content:page_title" content="Page Title">
    <img data-cms-attr="src:footer_img_src|alt:footer_img_alt" src='path/to/img' alt="alt text" />


Content
=======

Syntax
------

To make the content of a tag editable, add an attribute ``data-cms-content`` inside the tag.

Value of the ``data-cms-content`` should be of the form ``md:key`` if you want the content to be parsed as
markdown content, else the value is just ``key``.

.. code-block:: html

    <p data-cms-content="md:main_body">
        Default main body content
    </p>

.. note::

    Editor that is used for all the editable fields is a markdown editor.
    Hence during editing, content can be previewed as markdown rendered
    even if the content field is not markdown supported

Namespace
=========

Since the key specified in the tag is used to store the corresponding data,
care should be taken that the keys are not repeated inside a template.

If the same key is to be used for multiple tags,
it can be achieved by wrapping the tags inside another tag which specifies the namespace

Syntax
------

To specify a namespace for a section ``data-cms-namespace`` attribute is to be added to the tag
with a value of ``namespace``.

.. code-block:: html

    <div data-cms-namespace="header">
        <img data-cms-attr="src:img_src|alt:img_alt" src='path/to/img' alt="alt text" />
    </div>
    <div data-cms-namespace="footer">
        <img data-cms-attr="src:img_src|alt:img_alt" src='path/to/img' alt="alt text" />
    </div>

.. note::

    * Value of the ``data-cms-content`` acts as a namespace for it's content
    * Inside the ``data-cms-content`` tags you can insert new html code with editing features and create new editable fields on the fly. This enables us to insert template snippets

Snippets
========

You can extend the content editing functionality to include html snippets inside the main template.

These snippets may or may not be editable.

Syntax
------

To include a template snippet inside the content tag, two attributes
``data-cms-include`` and ``data-cms-namespace`` are to be added to the tag.

Value of the ``data-cms-include`` should be the template path and ``data-cms-namespace`` should be the ``key``.

.. code-block:: html

    <div data-cms-include="path/to/default/template" data-cms-namespace="namespace">
        Default content
    </div>

Instead of two attributes you can only use ``data-cms-include`` and specify the value as ``namespace:path/to/template``.

It will later be converted to the above format

.. code-block:: html

    <div data-cms-include="namespace:path/to/default/template">
        Default content
    </div>
