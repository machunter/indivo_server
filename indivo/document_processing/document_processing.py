"""
IDP - Indivo Document Processing
"""

import os
import sys
import hashlib
import re
import logging

from StringIO import StringIO
from lxml import etree

from indivo.models import DocumentSchema, Fact
from django.conf import settings
from django.core.files.base import ContentFile

from indivo.lib.utils import LazyProperty
from indivo.lib.simpledatamodel import SDMXData, SDMJData
from . import REGISTERED_SCHEMAS

DEFAULT_PREFIX= "http://indivo.org/vocab/xml/documents#"
ETREE_NS_RE = re.compile(r'{(?P<ns>.*?)}')

# Mimetypes that we shouldn't treat as binary
# Only covering the most common cases here--expand as needed
TEXT_MIMETYPES = [
  'application/xml',
  'text/xml',
  'text/plain', 
  'application/json',
  'text/html',
]

# Mimetypes that represent XML
# We can validate XML Syntax for these types
XML_MIMETYPES = [
  'application/xml',
  'text/xml',
]

# subclass of utils.LazyProperty which returns None if the object is binary
class NonBinaryLazyProperty(LazyProperty):
  def __get__(self, obj, _=None):
    if obj and obj.is_binary:
      setattr(obj, self._calculate.func_name, None)
      return None
    return super(NonBinaryLazyProperty, self).__get__(obj)

class DocumentProcessing(object):

  @classmethod
  def expand_schema(cls, schema):
    """
    go from Allergy to http://indivo.org/vocab/xml/documents#Allergy
    """
    if schema is None:
      return None

    if schema.find(':') > -1 or schema.find('/') > -1:
      return schema
    else:
      return "%s%s" % (DEFAULT_PREFIX, schema)

  def __init__(self, content, mime_type):
    logging.info("Document Processing __init__")
    # if mime_type is null, we assume it's XML
    self.is_binary = (mime_type and mime_type not in TEXT_MIMETYPES)
    self.is_xml = mime_type in XML_MIMETYPES
    self.content = content
    self.processed_facts = []

    # Validate basic XML Syntax, if required
    if self.is_xml and settings.VALIDATE_XML_SYNTAX:
      self.validate_xml_syntax() 

  def process(self):
    logging.info("Document Processing process")
    # Validate the XML, if necessary
    if self.validate_p:
      self.validate_xml()

    # Process the doc into Fact objects, if necessary
    if self.process_p:
      self.processed_facts = self._process()

  @property # Not a NonBinaryLazyProperty, as it depends on the value of settings.VALIDATE_XML
  def validate_p(self):
    """ Whether or not this doc needs validation.

    Right now:
    * is it non-binary?
    * Can it be validated?
    * Are we configured to validate XML?

    """
    logging.info("Document Processing validate_p")

    return settings.VALIDATE_XML and self.validation_func

  @NonBinaryLazyProperty
  def process_p(self):
    """ Whether or not this doc needs processing. 

    Right now:

    * Can it be transformed?

    """
    logging.info("Document Processing process_p")
    return self.transform_func

  def _process(self):
    """ Process the incoming doc """
    logging.info("Document Processing _process")

    ret = []

    # Run the transform
    output = self.transformed_doc

    # If the output of the transform was a Fact object, we're done
    if isinstance(output, Fact):
      ret.append(output)

    # If the output of the transform was a list of Fact objects,
    # just return the list
    elif isinstance(output, list):
      
      # But they have to all be Fact objects
      for fact in output:
        if not isinstance(fact, Fact):
          raise ValueError("Transform outputted a list of fact objects, but not all list elements were facts.")
        ret.append(fact)
    
    return ret

  @NonBinaryLazyProperty
  def content_etree(self):
    logging.info("Document Processing content_etree")
    try:
      return etree.parse(StringIO(self.content))
    except Exception, e:
      return None # Don't raise an error, so processing can still 'work' if validation is turned off

  @NonBinaryLazyProperty
  def basename(self):
    logging.info("Document Processing basename")
    if self.content_etree is not None:
      return ETREE_NS_RE.sub('', self.content_etree.getroot().tag)
    return None

  @NonBinaryLazyProperty
  def fqn(self):
    logging.info("Document Processing fqn")
    if self.content_etree is not None:
      return ETREE_NS_RE.sub('\g<ns>', self.content_etree.getroot().tag)
    return None

  @NonBinaryLazyProperty
  def validation_func(self):
    logging.info("Document Processing validation_func")
    if self.fqn and REGISTERED_SCHEMAS.has_key(self.fqn):
      logging.info('validation_func:'+self.fqn)
      return REGISTERED_SCHEMAS[self.fqn][0]
    return None

  @NonBinaryLazyProperty
  def transform_func(self):
    logging.info("Document Processing transform_func")
    if self.fqn and REGISTERED_SCHEMAS.has_key(self.fqn):
      logging.info('transform_func:'+self.fqn)
      return REGISTERED_SCHEMAS[self.fqn][1]
    return None

  @LazyProperty
  def digest(self):
    logging.info("Document Processing digest")
    if self.is_binary:
      return hashlib.sha1(self.content).hexdigest()
    else:
      md = hashlib.sha256()
      md.update(self.content)
      return md.hexdigest()

  @LazyProperty
  def size(self):
    logging.info("Document Processing size")
    if self.is_binary:
      file = ContentFile(self.content)
      return file.size
    else:
      return len(self.content)

  @NonBinaryLazyProperty
  def transformed_doc(self):
    logging.info("Document Processing transformed_doc")
    try:
      if self.transform_func:
        logging.info('transformed_doc')
        return self.transform_func(self.content_etree)
      else:
        logging.info('not transformed_doc')
    except ValueError:
      raise
    except Exception:
      pass
    
    # return None if we don't have a transform func,
    # or if the transform didn't work
    return None

  def validate_xml_syntax(self):
    """ Make sure that the incoming document is properly formatted XML, regardless of content. """
    logging.info("Document Processing validate_xml_syntax")
    try:
      xml_etree = etree.XML(self.content)
    except Exception as e:
      raise ValueError("Input document didn't parse as XML, error was: %s"%(str(e)))

  def validate_xml(self):
    """ Validate our doc against its XSD. """
    logging.info('validating xml')
    try:
      if self.validation_func:
        self.validation_func(self.content_etree)
    except etree.DocumentInvalid as e:
      raise ValueError("Input document didn't validate, error was: %s"%(str(e)))
