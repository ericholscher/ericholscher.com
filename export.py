import psycopg2
import pdb
import os

conn = psycopg2.connect("dbname='ericholscher' user='postgres'")
cur = conn.cursor()
cur.execute("select title, slug, body, publish, tags from blog_posts where status=2;")
rows = cur.fetchall()
for row in rows:
	title, slug, body, date, tags = row
	print "Working on %s" % slug
	in_file = open('%s.md' % slug, 'w+')
	in_file.write(body)
	in_file.close()
	out_dir = 'blog/%s/%s/%s' % (date.year, date.strftime("%b").lower(), date.day)
	os.system('mkdir -p %s' % out_dir)
	os.system('pandoc --from=markdown --to=rst -o %s/%s.rst %s.md' % (out_dir, slug, slug))

cur = conn.cursor()
cur.execute("select title, slug, body, publish, tags from blog_posts where status=1;")
rows = cur.fetchall()
for row in rows:
	title, slug, body, date, tags = row
	print "Working on %s" % slug
	in_file = open('%s.md' % slug, 'w+')
	in_file.write(body)
	in_file.close()
	out_dir = 'unpublished/blog/%s/%s/%s' % (date.year, date.strftime("%b").lower(), date.day)
	os.system('mkdir -p %s' % out_dir)
	os.system('pandoc --from=markdown --to=rst -o %s/%s.rst %s.md' % (out_dir, slug, slug))
