'''
Created on 9/08/2012

@author: jramsay

:~$ ogrinfo --formats
Supported Formats:
  -> "ESRI Shapefile" (read/write)
  -> "MapInfo File" (read/write)
  -> "UK .NTF" (readonly)
  -> "SDTS" (readonly)
  -> "TIGER" (read/write)
  -> "S57" (read/write)
  -> "DGN" (read/write)
  -> "VRT" (readonly)
  -> "REC" (readonly)
  -> "Memory" (read/write)
  -> "BNA" (read/write)
  -> "CSV" (read/write)
  -> "NAS" (readonly)
  -> "GML" (read/write)
  -> "GPX" (read/write)
  -> "KML" (read/write)
  -> "GeoJSON" (read/write)
  -> "Interlis 1" (read/write)
  -> "Interlis 2" (read/write)
  -> "GMT" (read/write)
  -> "SQLite" (read/write)
  -> "DODS" (readonly)
  -> "ODBC" (read/write)
  -> "PGeo" (readonly)
  -> "MSSQLSpatial" (read/write)
  -> "OGDI" (readonly)
  -> "PostgreSQL" (read/write)
  -> "MySQL" (read/write)
  -> "PCIDSK" (read/write)
  -> "XPlane" (readonly)
  -> "AVCBin" (readonly)
  -> "AVCE00" (readonly)
  -> "DXF" (read/write)
  -> "Geoconcept" (read/write)
  -> "GeoRSS" (read/write)
  -> "GPSTrackMaker" (read/write)
  -> "VFK" (readonly)
  -> "PGDump" (read/write)
  -> "GPSBabel" (read/write)
  -> "SUA" (readonly)
  -> "OpenAir" (readonly)
  -> "PDS" (readonly)
  -> "WFS" (readonly)
  -> "HTF" (readonly)
  -> "AeronavFAA" (readonly)
  -> "Geomedia" (readonly)
  -> "EDIGEO" (readonly)
  -> "GFT" (read/write)
  -> "SVG" (readonly)
  -> "CouchDB" (read/write)
  -> "Idrisi" (readonly)
  -> "ARCGEN" (readonly)
  -> "SEGUKOOA" (readonly)
  -> "SEGY" (readonly)


'''

import sys, ogr, osr, re

from datetime import datetime, timedelta
from abc import ABCMeta, abstractmethod

from LDSUtilities import LDSUtilities
from MetaLayerInformation import MetaLayerReader
from ProjectionReference import Projection

#exceptions
class DSReaderException(Exception): pass
class LDSReaderException(DSReaderException): pass
class IncompleteWFSRequestException(LDSReaderException): pass
class CannotInitialiseDriverType(LDSReaderException): pass
class DatasourceCopyException(LDSReaderException): pass
class DatasourceCreateException(LDSReaderException): pass
class DatasourceOpenException(DSReaderException): pass
class InvalidLayerException(LDSReaderException): pass
class InvalidFeatureException(LDSReaderException): pass




class DataStore(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta



    def __init__(self,conn_str=None):
        '''
        cons init driver
        '''
        
        if conn_str is not None:
            self.conn_str = conn_str
            
            
        self.DATE_FORMAT='%Y-%m-%d'
        self.EARLIEST_INIT_DATE = '2000-01-01'

        #default clear the INCR flag
        self.setOverwrite()
        self.clearIncremental()
        
        '''set of <potential> columns not needed in final output. ogc_fid can be discarded if alternative PK is used'''
        self.optcols = set(['__change__','gml_id'])
        
        
    def getDriver(self,driver_name):

        self.driver = ogr.GetDriverByName(driver_name)
        if self.driver==None:
            raise CannotInitialiseDriverType, "Driver cannot be initialised for type "+driver_name
            sys.exit(1)


    #filter/cql (applicable for source type)
    def setFilter(self,cql):
        self.cql = cql
         
    def getFilter(self):
        return self.cql
    
    #incr flag
    def setIncremental(self):
        self.INCR = True
         
    def clearIncremental(self):
        self.INCR = False
         
    def getIncremental(self):
        return self.INCR
    
    #overwrite flag
    def setOverwrite(self):
        self.OVERWRITE = "YES"
         
    def clearOverwrite(self):
        self.OVERWRITE = "NO"
         
    def getOverwrite(self):
        return self.OVERWRITE      
    
    def getOptions(self):
        '''override this in subclasses as new options are required'''
        return ['OVERWRITE='+self.getOverwrite()]    
    
    
    @abstractmethod
    def sourceURI(self):
        raise NotImplementedError("Abstract method sourceURI not implemented")
    
    @abstractmethod
    def destinationURI(self):
        raise NotImplementedError("Abstract method destinationURI not implemented")

    #@abstractmethod
    #def buildExternalLayerDefinition(self,name,fdef_list):
    #    raise NotImplementedError("Abstract method buildExternalLayerDefinition not implemented")
    
    def read(self,dsn):
        '''main read method'''
        print "DS read",dsn.split(":")[0]
        self.ds = self.driver.Open(dsn)
    
    def write(self,src,dsn):
        '''Main write method attempts to open then create a datasource'''
        if src.getIncremental():#TODO. maybe consider this as the branch point for by-feature or driver copy
            pass
        
        print "DS write",dsn#.split(":")[0]
        try:
            self.ds = self.driver.Open(dsn, update = 1 if self.getOverwrite() else 0)
            if self.ds is None:
                raise DSReaderException("Error opening DS on Destination "+str(dsn)+", attempting DS Create")
        except DSReaderException as dsre1:
            print "DSReaderException",dsre1 
            try:
                self.ds = self.driver.CreateDataSource(dsn)
                if self.ds is None:
                    raise DSReaderException("Error creating DS on Destination "+str(dsn)+", quitting")
            except DSReaderException as dsre2:
                print "DSReaderException",dsre2
                raise
            
        if src.getIncremental():
            # change col in delete list and as change indicator
            self.copyDS(src.ds,self.ds,src.CHANGE_COL)
        else:
            # no cols to delete and no operational instructions
            self.cloneDS(src.ds,self.ds,None)
        
        self.ds.SyncToDisk()
        self.ds.Destroy()  

              
    def cloneDS(self,src_ds,dst_ds):
        '''Copy from source to destination using the driver copy and without manipulating data'''
        '''TODO. address problems with this approach if a user has changed a tablename, specified ignore columns etc'''
        dst_ds.Copy(src_ds)
    
    
    def copyDS(self,src_ds,dst_ds,changecol):
        #TDOD. decide whether C_C is better as an arg or a src.prop
        '''Data Store replication for incremental queries'''
        #build new layer by duplicating source layers  
            
        
        for li in range(0,src_ds.GetLayerCount()):

            src_layer = src_ds.GetLayer(li)
            src_layer_name = src_layer.GetName()
            src_layer_sref = src_layer.GetSpatialRef()
            src_layer_geom = src_layer.GetGeomType()
            src_layer_defn = src_layer.GetLayerDefn()
            
            #TODO. resolve conflict between lastmodified and fdate
            ref_layer_name = LDSUtilities.cropChangeset(src_layer_name)
            
            '''retrieve per-layer settings from props'''
            (ref_pkey,ref_name,ref_gcol,ref_epsg,ref_lmod,ref_disc,ref_cql) = self.mlr.readAllLayerParameters(ref_layer_name)
            
            dst_layer_name = self.schema+"."+self.sanitise(ref_name) if self.schema is not None else self.sanitise(ref_name)
            
            
            '''parse discard columns'''
            self.optcols |= set(ref_disc.strip('[]{}()').split(',') if ref_disc is not None else [])
            
            #check for user a defined projection
            self.transform = None
            dst_sref = src_layer_sref#not necessary but for clarity
            if ref_epsg is not None and ref_epsg != '':
                trans_sref = Projection.validateEPSG(ref_epsg)
                if trans_sref is not None:
                    self.transform = osr.CoordinateTransformation(src_layer_sref, trans_sref)
                    if self.transform is not None:
                        dst_sref = trans_sref
            
            #new_layer_flag = False # used if we del/ins features instead of setting them            
            
            #assuming output layer name will be the same... confusion if this isnt so
            dst_layer = dst_ds.GetLayer(dst_layer_name)
            if dst_layer is None:
                '''create a new layer if a similarly named existing layer can't be found on the dst'''
                print dst_layer_name+" does not exist. Creating new layer."
                #new_layer_flag = True
                
                #read defns of each field
                fdef_list = []
                for fi in range(0,src_layer_defn.GetFieldCount()):
                    fdef_list.append(src_layer_defn.GetFieldDefn(fi))
                
                #use the field defns to build a schema since this needs to be loaded as a create_layer option
                opts = self.getOptions(ref_layer_name)
                
                '''build layer replacing poly with multi and revert to def if that doesn't work'''
                if src_layer_geom is ogr.wkbPolygon:
                    dst_layer = dst_ds.CreateLayer(dst_layer_name,dst_sref,ogr.wkbMultiPolygon,opts)
                else:
                    dst_layer = dst_ds.CreateLayer(dst_layer_name,dst_sref,src_layer_geom,opts)
                    
                if dst_layer is None:
                    #overwrite the dst_sref if its causing trouble (ie GDAL general function errors)
                    dst_sref = Projection.getDefaultSpatialRef()
                    print "Warning. Could not initialise Layer with specified SRID {",src_layer_sref,"}.\n\nUsing Default {",dst_sref,"} instead"
                    if src_layer_geom is ogr.wkbPolygon:
                        dst_layer = dst_ds.CreateLayer(dst_layer_name,dst_sref,ogr.wkbMultiPolygon,opts)
                    else:
                        dst_layer = dst_ds.CreateLayer(dst_layer_name,dst_sref,src_layer_geom,opts)

                #dst_layer.SetFID("id")
            
                '''setup layer headers for new layer etc'''                
                for fdef in fdef_list:
                    #print "field:",fi
                    if fdef.GetName() not in self.optcols:# and fdef.GetName() in reqdcols:
                        dst_layer.CreateField(fdef)
                        #could check for any change tags and throw exception if none
            
            #add/copy features
            #src_layer.ResetReading()
            src_feat = src_layer.GetNextFeature()
            
            '''since the characteristics of each feature wont change between layers we only need to define a new feature definition once'''
            if src_feat is not None:
                new_feat_def = self.partialCloneFeatureDef(src_feat)
            
            while src_feat is not None:
                #print src_feat.GetFID()
                change =  src_feat.GetField(changecol) if changecol is not None and len(changecol)>0 else "INSERT"
                #src_fid = src_feat.GetFieldAsInteger(ref_pkey)

                #self._showFeatureData(new_feat)
                #print "CHANGE::",change
                
                try:
                    if change == "INSERT":
                        '''build new feature from defn and insert'''
                        new_feat = self.partialCloneFeature(src_feat,new_feat_def,ref_gcol)
                        err = dst_layer.CreateFeature(new_feat)
                        dst_fid = new_feat.GetFID()
                    elif change == "DELETE":
                        '''lookup and delete using fid matching ID of feature being deleted'''
                        #if not new_layer_flag: 
                        src_pkey = src_feat.GetFieldAsInteger(ref_pkey)
                        dst_fid = self._findMatchingFID(dst_layer, ref_pkey, src_pkey)
                        if dst_fid is not None:
                            err = dst_layer.DeleteFeature(dst_fid)
                        else:
                            raise InvalidFeatureException("No match for FID with ID="+str(src_pkey)+" on "+change)
                    elif change == "UPDATE":
                        '''build new feature, assign it the looked-up matching fid and overwrite on dst'''
                        #if not new_layer_flag: 
                        dst_fid = self._findMatchingFID(dst_layer, ref_pkey, src_feat.GetFieldAsInteger(ref_pkey))
                        new_feat = self.partialCloneFeature(src_feat,new_feat_def,ref_gcol)
                        if dst_fid is not None:
                            new_feat.SetFID(dst_fid)
                            err = dst_layer.SetFeature(new_feat)
                        else:
                            raise InvalidFeatureException("No match for FID with ID="+str(src_pkey)+" on "+change)
                        
                    if err!=0: 
                        raise InvalidFeatureException("Driver Error ["+str(err)+"] using FID="+str(dst_fid)+" on "+change)
                    
                except InvalidFeatureException as ife:
                    print "InvalidFeatureException",ife
                               
                src_feat = src_layer.GetNextFeature()

            #self._showLayerData(dst_layer)
            src_layer.ResetReading()
            dst_layer.ResetReading()
            #since we can't delete a field on the source try on the dest
            #dst_layer.DeleteField(dst_layer.GetLayerDefn().GetFieldIndex(CHANGE_COL))
            
            #self._showLayerData(dst_layer)
            
            '''notes. fid is not necessarily unique between calls to source so cant be used directly when doing deletes/updates, instead
           we must use the actual key (id in most cases) and use this as a reference to get the destination fid.'''


    def partialCloneFeature(self,fin,fout_def,ref_gcol):
        '''rebuilds a feature using a passed in feature def. must still ignore discarded columns since they will be in the source'''

        fout = ogr.Feature(fout_def)

        '''Set Geometry transforming if needed'''
        fin_geom = fin.GetGeometryRef()
        if self.transform is not None:
            #TODO check whether this fin_geom needs to be cloned first
            fin_geom.Transform(self.transform)
        fout.SetGeometry(fin_geom)

        #DataStore._showFeatureData(fin)
        #DataStore._showFeatureData(fout)
        
        '''populate feature'''
        fout_no = 0
        for fin_no in range(0,fin.GetFieldCount()):
            fin_field_name = fin.GetFieldDefnRef(fin_no).GetName()
            if fin_field_name not in self.optcols:
                copy_field = fin.GetField(fin_no)
                fout.SetField(fout_no, copy_field)
                fout_no += 1
            
        #DataStore._showFeatureData(fout)
        fout_geom = fout.GetGeometryRef()
   
        if fout_geom.ExportToWkt()[:7]=="POLYGON":
            fin.SetGeometryDirectly(ogr.ForceToMultiPolygon(fout_geom))
            
        return fout
    
    def partialCloneFeatureDef(self,fin):
        '''builds a feature definition ignoring the __change__ and discarded columns'''
        #create blank feat defn
        fout_def = ogr.FeatureDefn()
        #read input feat defn
        fin_feat_def = fin.GetDefnRef()
        
        #loop existing feature defn ignoring column X
        for fin_no in range(0,fin.GetFieldCount()):
            fin_field_def = fin.GetFieldDefnRef(fin_no)
            fin_field_name = fin_field_def.GetName()
            if fin_field_name not in self.optcols:
                fin_fld_def = fin_feat_def.GetFieldDefn(fin_no)
                #print "n={}, typ={}, wd={}, prc={}, tnm={}".format(fin_fld_def.GetName(),fin_fld_def.GetType(),fin_fld_def.GetWidth(),fin_fld_def.GetPrecision(),fin_fld_def.GetTypeName())
                fout_def.AddFieldDefn(fin_fld_def)
                
        return fout_def
    
    
    def _findMatchingFID(self,dst_layer,ref_pkey,key):
        '''find the FID matching a primary key value'''
        qry = ref_pkey+" = "+str(key)
        dst_layer.SetAttributeFilter(qry)
        found_feat = dst_layer.GetNextFeature()
        if found_feat is not None:
            return found_feat.GetFID()
        return None
            
    
    
    def getLastModified(self,layer):
        '''gets the last modification time of a layer to use for incremental "fromdate" calls'''
        '''this is intended to be run as a destination method ie dst.getLastModified'''
        lmd = self.mlr.readLastModified(layer)
        if lmd is None or lmd == '':
            lmd = self.EARLIEST_INIT_DATE
        return lmd
        #return lm.strftime(self.DATE_FORMAT)
        
    def setLastModified(self,layer,newdate):
        '''gets the last modification time of a layer to use for incremental "fromdate" calls'''
        '''this is intended to be run as a destination method ie dst.getLastModified'''
        self.mlr.writeLastModified(layer, newdate)    

    def getCurrent(self,offset):
        '''gets the current timestamp plus any required offset for incremental todate calls'''
        '''offset expected in dict form with {day=D, hour=H, minute=M}'''
        if offset is None:
            offset = {'day':0,'hour':0,'minute':0}
        dpo = datetime.now()+timedelta(days=offset['day'],hours=offset['hour'],minutes=offset['minute'])
        return dpo.strftime(self.DATE_FORMAT)
        
        
        
    #utility methods
    
    @classmethod
    def sanitise(self,name):
        '''manually subst potential table naming errors, generic function to retain naming convention across all outputs'''
        '''no guarantees this wont cause naming conflicts eg A-B-C -> a_b_c <- a::{b}::c'''
        #append _ to name beginning with a number
        if re.match('\A\d',name):
            name = "_"+name
        #replace unwanted chars with _ and compress multiple and remove trailing
        return re.sub('_+','_',re.sub('[ \-,.\\\\/:;{}()\[\]]','_',name.lower())).rstrip('_')
    

    @classmethod
    def parseStringList(self,st):
        '''flakey name type parse'''
        return st.rstrip(')]').lstrip('[(').split(',') if st.find(',')>-1 else st

    
    #debugging methods
    
    @classmethod
    def _showFeatureData(self,feature):
        '''prints feature/fid info. useful for debugging'''
        print "\nFeat:FID:",feature.GetFID()
        for field_no in range(0,feature.GetFieldCount()):
            print "fid={},fld_no={},fld_data={}".format(feature.GetFID(),field_no,feature.GetFieldAsString(field_no))
            
    @classmethod
    def _showLayerData(self,layer):
        '''prints layer and embedded feature data. useful for debugging'''
        print "\nLayer:Name:",layer.GetName()
        layer.ResetReading()
        feat = layer.GetNextFeature()
        while feat is not None:
            self._showFeatureData(feat)
            feat = layer.GetNextFeature()                
                

