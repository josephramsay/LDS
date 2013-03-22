'''
v.0.0.1

LDSReplicate -  LDSUtilities

Copyright 2011 Crown copyright (c)
Land Information New Zealand and the New Zealand Government.
All rights reserved

This program is released under the terms of the new BSD license. See the 
LICENSE file for more information.

Simple LDS specific utilities class

Created on 9/08/2012

@author: jramsay
'''
# for windows lxml binary from here http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

import re
import os
import logging
import ast
import string

from urllib2 import urlopen
from StringIO import StringIO
from lxml import etree

ldslog = logging.getLogger('LDS')

class LDSUtilities(object):
    '''Does the LDS related stuff not specifically part of the datastore''' 
    
    LDS_TN_PREFIX = 'v:x'
    LDS_TN_VXPATH = '/'+LDS_TN_PREFIX.replace(':','/')
    
    @staticmethod
    def splitLayerName(layername):
        '''Splits a layer name typically in the format v:x### into /v/x### for URI inclusion'''
        return "/"+layername.split(":")[0]+"/"+layername.split(":")[1]
    
    @staticmethod
    def cropChangeset(layername):
        '''Removes changeset identifier from layer name'''
        return layername.rstrip("-changeset")
    
    @staticmethod
    def checkDateFormat(xdate):
        '''Checks a date parameter conforms to yyyy-MM-ddThh:mm:ss format'''        
        if type(xdate) is str:
            if re.search('^\d{4}\-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$',xdate):
                return xdate
            elif re.search('^\d{4}\-\d{2}-\d{2}$',xdate):
                return xdate+"T00:00:00"
        return None

    # 772 time test string
    # http://wfs.data.linz.govt.nz/ldskey/v/x772-changeset/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=v:x772-changeset&viewparams=from:2012-09-29T07:00:00;to:2012-09-29T07:30:00&outputFormat=GML2
    
    @staticmethod
    def checkLayerName(lconf,lname):
        '''Makes sure a layer name conforms to v:x format'''
        if type(lname) is str:
            if re.search('^'+LDSUtilities.LDS_TN_PREFIX+'\d+$',lname):
                return lname if lname in lconf.getLayerNames() else None
            else:
                return lconf.findLayerIdByName(lname)
        return None
         
    
    @staticmethod
    def getLayerNameFromURL(url):
        from DataStore import MalformedConnectionString
        l1 = re.search(LDSUtilities.LDS_TN_VXPATH+'(\d+)',url,flags=re.IGNORECASE)
        l2 = re.search('typeName='+LDSUtilities.LDS_TN_PREFIX+'(\d+)',url,flags=re.IGNORECASE)
        if l1 is None or l2 is None:
            raise MalformedConnectionString('Cannot extract correctly formatted layer strings from URI')
        else:
            l1 = l1.group(1)
            l2 = l2.group(1)
            if l1!=l2:
                raise MalformedConnectionString('Layer specifications in URI differ; '+str(l1)+'!='+str(l2))
        return LDSUtilities.LDS_TN_PREFIX+str(l1)
        
    @staticmethod
    def checkHasChangesetIdentifier(url):
        '''Parse a selected date string from a user supplied URL. Can return none as that would indicate non incremental'''
        #yeah thats right, F or T
        c1 = re.search(LDSUtilities.LDS_TN_VXPATH+'\d+-changeset',url,flags=re.IGNORECASE)
        c2 = re.search('typeName='+LDSUtilities.LDS_TN_PREFIX+'\d+-changeset',url,flags=re.IGNORECASE)
        return c1 is not None and c2 is not None
    
    @staticmethod
    def getDateStringFromURL(fort,url):
        '''Parse a selected date string from a user supplied URL. Can return none as that would indicate non incremental'''
        #yeah thats right, F or T
        udate = re.search(fort+':(\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})*)',url)
        return udate


    @staticmethod
    def xmlEscape(url):
        '''Simple XML escaping regex used to properly format WFS URLS (though it doesn't seem to be needed)'''
        #first 4, simple replace: "=&quot; '=&apos; <=&lt; >=&gt; &=&amp;
        url = re.sub('"','&quot;',url)
        url = re.sub('\'','&apos;',url)
        url = re.sub('<','&lt;',url)
        url = re.sub('>','&gt;',url)
        #them match & but not anything that has already been escaped
        #the original string could also contain escaped chars so we have to do skip escapes anyway 
        return re.sub('&(?!amp;|apos;|quot;|lt;|gt;)','&amp;',url)    
    
    
    @staticmethod
    def percentEncode(url):
        '''Simple http bracket/comma escaping regex used to properly format WFS URLS'''
        #!     #     $     &     '     (     )     *     +     ,     /     :     ;     =     ?     @     [     ]
        #%21   %23   %24   %26   %27   %28   %29   %2A   %2B   %2C   %2F   %3A   %3B   %3D   %3F   %40   %5B   %5D
        url = re.sub('\(','%28',url)
        url = re.sub('\)','%29',url)
        url = re.sub(',','%2C',url)
        url = re.sub(' ','%20',url)
        return url

    @staticmethod
    def checkCQL(cql):
        '''Since CQL commands are freeform strings we need to try and validate at least the most basic errors. This is very simple
        RE matcher that just looks for valid predicates... for now
        
        <predicate> ::= <comparison predicate> | <text predicate> | <null predicate> | <temporal predicate> | <classification predicate> | <existence_predicate> | <between predicate> | <include exclude predicate>
        
        LDS expects the following;
        Was expecting one of:
            "not" ...
            "include" ...
            "exclude" ...
            "(" ...
            "[" ...
            "id" ...
            "in" ...
            <IDENTIFIER> ...
            "-" ...
            <INTEGER_LITERAL> ...
            <FLOATING_LITERAL> ...
            <STRING_LITERAL> ...
            <STRING_LITERAL> "*" ...
            <STRING_LITERAL> "/" ...
            <STRING_LITERAL> "+" ...
            <STRING_LITERAL> "-" ...
            <STRING_LITERAL> "not" ...
            <STRING_LITERAL> "like" ...
            <STRING_LITERAL> "exists" ...
            <STRING_LITERAL> "does-not-exist" ...
            <STRING_LITERAL> "is" ...
            <STRING_LITERAL> "between" ...
            <STRING_LITERAL> "before" ...
            <STRING_LITERAL> "after" ...
            <STRING_LITERAL> "during" ...
            <STRING_LITERAL> "=" ...
            <STRING_LITERAL> ">" ...
            <STRING_LITERAL> "<" ...
            <STRING_LITERAL> ">=" ...
            <STRING_LITERAL> "<=" ...
            <STRING_LITERAL> "<>"
        '''
        v = 0
        
        #comp pred
        if re.match('.*(?:!=|=|<|>|<=|>=)',cql):
            v+=1
        #text pred
        if re.match('.*(?:not\s*)?like.*',cql,re.IGNORECASE):
            v+=2
        #null pred
        if re.match('.*is\s*(?:not\s*)?null.*',cql,re.IGNORECASE):
            v+=4
        #time pred
        if re.match('.*(?:before|during|after)',cql,re.IGNORECASE):
            v+=8
        #clsf pred, not defined
        #exst pred
        if re.match('.*(?:does-not-)?exist',cql,re.IGNORECASE):
            v+=32
        #btwn pred
        if re.match('.*(?:not\s*)?between',cql,re.IGNORECASE):
            v+=64
        #incl pred
        if re.match('.*(?:include|exclude)',cql,re.IGNORECASE):
            v+=128
        #geo predicates just for good measure, returns v=16 overriding classification pred
        if re.match('.*(?:equals|disjoint|intersects|touches|crosses|within|contains|overlaps|bbox|dwithin|beyond|relate)',cql,re.IGNORECASE):
            v+=16
            
        ldslog.debug("CQL check:"+cql+":"+str(v))
        if v>0:
            return cql
        else:
            return ""
        
    @staticmethod    
    def precedence(cmdline_arg,config_arg,layer_arg):
        '''Decide which CQL filter to apply based on scope and availability'''
        '''Currently we have; CommandLine > Config-File > Layer-Properties but maybe its better for individual layers to override a global setting... '''
        if LDSUtilities.mightAsWellBeNone(cmdline_arg) is not None:
            return cmdline_arg
        elif LDSUtilities.mightAsWellBeNone(config_arg) is not None:
            return config_arg
        elif LDSUtilities.mightAsWellBeNone(layer_arg) is not None:
            return layer_arg
        return None
    
    @staticmethod
    def extractFields(feat):
        '''Extracts named fields from a layer config feature'''
        '''Not strictly independent but common and potentially used by a number of other classes'''
        
        try:
            pkey =  feat.GetField('PKEY')
        except:
            ldslog.debug("LayerSchema: No Primary Key Column defined, default to 'ID'")
            pkey = 'ID'
            
        '''names are/can-be stored so we can reverse search by layer name'''
        try:
            name = feat.GetField('NAME')
        except:
            ldslog.debug("LayerSchema: No Name saved in config for this layer, returning ID")
            name = None
            
        '''names are/can-be stored so we can reverse search by layer name'''
        try:
            group = feat.GetField('CATEGORY')
        except:
            ldslog.debug("Group List: No Groups defined for this layer")
            group = None
                  
        try:
            gcol = feat.GetField('GEOCOLUMN')
        except:
            ldslog.debug("LayerSchema: No Geo Column defined, default to 'SHAPE'")
            gcol = 'SHAPE'
            
        try:
            index = feat.GetField('INDEX')
        except:
            ldslog.debug("LayerSchema: No Index Column/Specification defined, default to None")
            index = None
            
        try:
            epsg = feat.GetField('EPSG')
        except:
            #print "No Projection Transformation defined"#don't really need to state the default occurance
            epsg = None
            
        try:
            lmod = feat.GetField('LASTMODIFIED')
        except:
            ldslog.debug("LayerSchema: No Last-Modified date recorded, successful update will write current time here")
            lmod = None
            
        try:
            disc = feat.GetField('DISCARD')
        except:
            disc = None 
            
        try:
            cql = feat.GetField('CQL')
        except:
            cql = None
            
        
        return LayerConfEntry(pkey,name,group,gcol,index,epsg,lmod,disc,cql)
    
    @staticmethod
    def readDocument(url):
        '''Non-Driver method for fetching LDS DS as a document'''
        ldslog.debug("LDs URL "+url)
        lds = urlopen(url)
        data = lds.read()
        lds.close()
        return data
    
    @staticmethod
    def mightAsWellBeNone(nstr):
        if nstr == None or nstr=='None' or all(i in string.whitespace for i in nstr):
            return None
        return nstr
    
    @staticmethod
    def setupLogging():
        log = logging.getLogger('LDS')
        log.setLevel(logging.DEBUG)
        
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../log/"))
        if not os.path.exists(path):
            os.mkdir(path)
        df = os.path.join(path,"debug.log")
        
        fh = logging.FileHandler(df,'w')
        fh.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s %(lineno)d - %(message)s')
        fh.setFormatter(formatter)
        log.addHandler(fh)
        
        return ldslog

class ConfigInitialiser(object):
    '''Initialises configuration, for use at first run'''

    @staticmethod
    def buildConfiguration(xml, fileid):
        '''Given a destination DS use this to select an XSL transform object and generate an output document that will initialise a new config file/table'''
        xslt = etree.parse(os.path.join(os.path.dirname(__file__), '../conf/getcapabilities.'+fileid+'.xsl'))
        transform = etree.XSLT(xslt)
        doc = etree.parse(StringIO(xml))
        res = transform(doc)
        hackpk = {'file':ConfigInitialiser._hackPrimaryKeyFieldCP,'json':ConfigInitialiser._hackPrimaryKeyFieldJSON}.get(fileid)
        return hackpk(str(res))
 
    @staticmethod
    def _hackPrimaryKeyFieldCP(cpdoc,csvfile=os.path.join(os.path.dirname(__file__),'../conf/ldspk.csv')):
        '''temporary hack method to rewrite the layerconf primary key field for ConfigParser file types'''
        import csv,io
        from ConfigParser import ConfigParser, NoSectionError
        cp = ConfigParser()
        cp.readfp(io.BytesIO(str(cpdoc)))
        with open(csvfile, 'rb') as csvtext:
            reader = csv.reader(csvtext, delimiter=',', quotechar='"')
            reader.next()
            for line in reader:
                try:
                    cp.set(str(LDSUtilities.LDS_TN_PREFIX+line[0]),'pkey',line[2].replace('"','').lstrip())
                except NoSectionError as nse:
                    ldslog.warn('PK hack CP: '+str(nse))

        #CP doesn't have a simple non-file write method?!?
        cps = "# LDS Layer Properties Initialiser - File\n"
        for section in cp.sections():
            cps += "\n["+str(section)+"]\n"
            for option in cp.options(section):
                cps += str(option)+": "+str(cp.get(section, option))+"\n"

        return cps
    
    @staticmethod
    def _hackPrimaryKeyFieldJSON(jtext,csvfile=os.path.join(os.path.dirname(__file__),'../conf/ldspk.csv')):
        '''temporary hack method to rewrite the layerconf primary key field in JSON responses'''
        import json
        import csv

        jdata = json.loads(jtext)
        with open(csvfile, 'rb') as csvtext:
            reader = csv.reader(csvtext, delimiter=',', quotechar='"')
            reader.next()
            for line in reader:
                for jline in jdata:
                    if LDSUtilities.LDS_TN_PREFIX+line[0] == str(jline[0]):
                        jline[1] = line[2].replace('"','').lstrip()
                        
        return json.dumps(jdata)
    
class SUFIExtractor(object):
    '''XSL parser to read big int columns returning a dict of id<->col matches'''
    @staticmethod
    def readURI(xml,colname):
        converter = open(os.path.join(os.path.dirname(__file__), '../conf/sufiselector.xsl'),'r').read()

        xslt = etree.XML(converter.replace('#REPLACE',colname))
        transform = etree.XSLT(xslt)
        
        doc = etree.parse(StringIO(xml))
        res = transform(doc)
        
        sufi = ast.literal_eval(str(res))
        #ldslog.debug(sufi)
        
        return sufi
        
class LayerConfEntry(object):
    '''Storage class for layer config info'''
    def __init__(self,pkey,name,group,gcol,index,epsg,lmod,disc,cql):
        self.pkey = pkey
        self.name = name
        self.group = group
        self.gcol = gcol
        self.index = index
        self.epsg = epsg
        self.lmod = lmod
        self.disc = disc
        self.cql = cql
    
        