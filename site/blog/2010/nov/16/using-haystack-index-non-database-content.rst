.. post:: 2010-11-16 21:01:00

Using Haystack to index non-database content
============================================

Over on ReadTheDocs, I wanted to build
`search <http://readthedocs.org/search/?q=crawler>`_ around the
documentation that we're hosting. I chose
`Haystack <http://haystacksearch.org/>`_ and
`Solr <http://lucene.apache.org/solr/>`_ for this, because it's the
best way to do search in Django these days. However, I've only ever
used Haystack to index content that is in the database. I thought
about trying to add all the rendered HTML from the documentation
into the database, but that was a non-starter.

I ended up adding a ImportedFile model to the database, which would
contain the metadata for the HTML file:

::

    #!python
    class ImportedFile(models.Model):
        project = models.ForeignKey(Project, related_name='imported_files')
        name = models.CharField(max_length=255)
        slug = models.SlugField()
        path = models.CharField(max_length=255)
        md5 = models.CharField(max_length=255)

This allows me to link the SearchIndex in haystack to a model. Then
the interesting part is in the Haystack SearchIndex, where I
override the prepare\_text method, allowing me to read the data in
from the filesystem instead of from the database.

::

    #!python
    class ImportedFileIndex(SearchIndex):
        text = CharField(document=True)
        author = CharField(model_attr='project__user')
        project = CharField(model_attr='project__name')
        title = CharField(model_attr='name')
    
        def prepare_text(self, obj):
            full_path = obj.project.full_html_path
            to_read = os.path.join(full_path, obj.path.lstrip('/'))
            try:
                content = codecs.open(to_read, encoding="utf-8", mode='r').read()
                return content
            except IOError:
                print "%s not found" % full_path
    
    site.register(ImportedFile, ImportedFileIndex)

This means that I don't have to bloat my database with all my
rendered HTML, but have the full HTML stored in Solr which works
for querying.


