##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PdfPeek Event Handlers
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from zope.interface import alsoProvides, noLongerProvides
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable

from collective.pdfpeek.transforms import convertPDFToPNG
from collective.pdfpeek.interfaces import IPDF

def pdf_changed(pdf, event):
    """
    This event handler is fired when ATFile objects are initialized or edited
    and calls the appropriate functions to convert the pdf to png thumbnails
    and store the list of thumbnails annotated on the file object.
    """
    if pdf.getContentType() == 'application/pdf':
        """Mark the object with the IPDF marker interface."""
        alsoProvides(pdf, IPDF)
        image_converter = convertPDFToPNG()
        images = image_converter.generate_thumbnails(pdf)
        alsoProvides(pdf, IAttributeAnnotatable)
        annotations = IAnnotations(pdf)
        annotations['pdfpeek'] = {}
        annotations['pdfpeek']['image_thumbnails'] = images
        
        if IPDF.providedBy(pdf):
            print "IPDF Marker Interface Applied to %s." % pdf
    else:
        noLongerProvides(pdf, IPDF)
        print "Marker Interface Removed from %s." % pdf
    
    return None
