:Date: 2010-02-14 08:48:20

Django Inspect: A generic introspection API for Django models
=============================================================

Django itself has shipped with a "semi-private" introspection API,
``_meta``, for a long time. I have created a drop-dead simple
wrapper on top of this.

The value of introspection keeps growing on me as I realize how it
makes making truly reusable applications possible. It is an
interesting intersection of duck-typing and interfaces. Basically,
you can create functionality that will work with
**any Django model**, as long as it has the correct values on
them.

However, I present this as a very useful proof of concept, and I
think a lot can be done with these ideas to improve on them. I
recommend you just pull down the code and play with it. The ideas
are very simple, but the power it gives you is vast.

The code is on
`Github <http://github.com/ericholscher/django_inspect>`_ with a
very simple test suite showing usage.

What does it do?
~~~~~~~~~~~~~~~~

The API is very simple. You pass in a instance of a Django model,
and you can get off the values that you care about.

::

    from django_inspect import base
    intro = base.Inspecter(comment)
    self.assertEqual(intro.content.field, 'comment')
    self.assertEqual(intro.content.value, 'First here, too!')

This example is using a Django comment, as you can see. When you
get a comment object, you want to see what the actual "content" of
it is. Normally, this requires special casing in your code, or
somewhere else. However, here we see it's just
``intro.content.value``, to get the value, or ``.field`` to get the
name of the content field.

The idea is that you have pluggable "parsers" that have names,
which then map to fields on the model. By default, the name of the
parser is checked, and any mappings you have passed in. Then it
will go ahead and execute any custom logic that is associated with
that parser.

So for this example, the "content parser" knows about comments, so
it knows to check for the "comment" field for it's main content.
This lets this mapping of content to fields to live inside the
parser, and lets the user of the Inspecter to just say "I want the
content".

Again, it's just easier if you
`read the code <http://github.com/ericholscher/django_inspect/blob/master/django_inspect/base.py#L42>`_,
it's really pretty simple.

Handling third party apps
~~~~~~~~~~~~~~~~~~~~~~~~~

Django Inspect also has the concept of mapping models to fields. So
you can create a simple dictionary and pass it into your
Introspection class, and it will map those keys to the
corresponding fields. An example is worth a thousand words:

::

        DEFAULT_MAPPINGS = {
        'comments.comment': {
            'content': 'comment',
            'pub_date': 'submit_date',
             }
        }

I call this the "Mingus use case". For example, if
`Mingus <http://github.com/montylounge/django-mingus>`_ wanted to
be able to introspect any of it's reusable apps for what it's
"pub\_date" or "content" fields were, it could ship with a mapping
for all of the reusable app models, and then you would be able to
write generic code that would work across all of those apps.

This is partially inspired by South's support for
`app migration directories <http://south.aeracode.org/wiki/Settings#SOUTH_MIGRATION_MODULES0.7andhigher>`_

A complex example
~~~~~~~~~~~~~~~~~

Say I am using Nathan Borror's Fantastic
`Basic Blog <http://github.com/nathanborror/django-basic-apps/blob/master/basic/blog/models.py#L33>`_.
It has it's Blog Post model defined as such:

::

    class Post(models.Model):
        STATUS_CHOICES = (
            (1, _('Draft')),
            (2, _('Public')),
        )
        title = models.CharField(_('title'), max_length=200)
        slug = models.SlugField(_('slug'), unique_for_date='publish')
        author = models.ForeignKey(User, blank=True, null=True)
        body = models.TextField(_('body'), )
        tease = models.TextField(_('tease'), blank=True, help_text=_('Concise text suggested. Does not appear in RSS feed.'))
        status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
        allow_comments = models.BooleanField(_('allow comments'), default=True)
        publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
        created = models.DateTimeField(_('created'), auto_now_add=True)
        modified = models.DateTimeField(_('modified'), auto_now=True)
        categories = models.ManyToManyField(Category, blank=True)
        tags = TagField()
        objects = PublicManager()

When I go ahead and create an inspecter class for this, I will be
able to define what fields I want to map onto what. So for example,
here the 'content' field of the blog post is actually called
"body". I could create a simple mapping for this model, or I could
modify the default parser to make the "content" field look for
"body" models.

::

        BLOG_MAPPING = {
        'blog.post': {
            'content': 'body',
            'pub_date': 'publish',
             }
        }
    
        from django_inspect import base
        ins = base.Inspecter(post, BLOG_MAPPING)

Now the following fields should have the following values:

::

        ins.content.field: 'body'
        ins.content.value: <Whatever my blog post is about>
        ins.pub_date.field: 'publish'
        ins.pub_date.value: <When my blog post was published>

Lots of room for improvement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a lot of interesting API niceities that could be added in
on top of this code. I want to keep it really simple, however there
is room for improvement. A couple that I have thought of:


-  Expose this as a Proxy Model, where you would get a proxy model
   of your model with the introspection bits attached onto it.
-  Make a descriptor so that you can have a pass through values do
   magical things on the Parsers
-  Allow for complex parsers by having the parsers know about each
   other
-  Make the Inspecter class know more about the parsers and be able
   to do more interesting things there
-  Ship it with a default set of mapping that work for most
   reusable apps out there. Also have a "standard" way for apps to
   define mappings.
-  Lots more

The whole idea of releasing this is to get feedback on what the
actual API should look like. I think it's pretty awesome currently
for the simple case, but for more advanced use, it's going to need
to grow some features.

Conclusion
~~~~~~~~~~

The whole idea behind this is that if your code is named or modeled
sanely, it should "Just Work". However, if you have a crazy data
model, or have to depend on wonky third party apps outside your
control, it is incredibly simple to map and introspect those models
as well.

The other powerful idea is the application of semantics to models.
I can query your model for the "content" or "tease" field, and be
able to define exactly what that is. This lets me build interfaces
and applications that "know" more about their data, even when that
data is unknown at the time of writing.

This gives the application developer the power to write truly
generic applications that will work with any suitable model. At
least I hope so :). I have some other ideas that fall out from the
implications of this introspection code that I will be talking
about at Pycon, and probably doing a lightning talk. So feel free
to find me and I probably won't shut up about it.


