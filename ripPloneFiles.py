# ripPloneFiles.py

"""
Exports all the files from a Plone site to a target directory.

Usage:

* put ripfiles.py in the buildout folder (same as buildout.cfg)
* Set and/or create the "rftargetpath" assignment

* Start a debug client and make sure you are in the
  appropriate context

* import and run

Personally, I use the whole ipzope stuff to debug,
etc. But, I'd imagine zopepy or client debug should work::

    $ ./bin/ipzope
    >>> import ripPloneFiles
    >>> ripPloneFiles.ripfiles()

After the thing is done running, check the output
in the rftargetpath dir.

"""

import os
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

rftargetpath = '/tmp' #make sure path exists and there is enuf disk space!

def ripfiles():
    site = getSite()
    catalog = getToolByName(site, 'portal_catalog')
    brains = catalog.search(query_request = {'portal_type':'File'})

    for b in brains:
        ob = b.getObject()
        obid = ob.id
        opath = ob.getPhysicalPath()
        filename = ob.getFilename()

        #write the path
        odir = '/'.join(opath[:-1])
        odir = rftargetpath + '/' + odir
        fp = odir + '/' + filename
        if not os.path.exists(odir):
            os.makedirs(odir)
        # assume now the path exists. Write the file
        print "Writing: %s" % fp
        f = open(fp, 'w')
        f.write(ob.data)
        f.close()
