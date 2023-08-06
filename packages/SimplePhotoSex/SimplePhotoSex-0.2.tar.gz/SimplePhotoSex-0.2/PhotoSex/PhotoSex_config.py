from configparser import ConfigParser
import os
import numpy as np
import pandas as pd
import pathlib
import pdb
import ast

class PhotoSex_config(object):
    '''read or write configuration file for PhotoSex'''
    
    def __init__(self,path_config_file='./',name_config_file='PhotoSex_config.ini'):
        self.cfile=path_config_file+'/'+name_config_file
        config_object = ConfigParser()
        self.config_object=config_object
        self.homedir=str(pathlib.Path.home())+'/'
        self.workdir_default=path_config_file
    
    def create_config_file(self):
        self.config_object['BASIC']={
            'show_computer_info':True
        }
        
        self.config_object['PATHS']={
            'workdir':self.workdir_default,
            'sexdir':self.homedir+'Science/data/models/sextractor/',
        }
        
        self.config_object['PHOTOMETRY']={
            'apertures':[0.5,1.,1.5,2.,3.,4.,5.,6.,7.,8.,12.,18]
        }
        
        self.config_object['APERTURE_CORRECTION']={
            'apc_polyorder':0,
            'apc_radius_total_flux':100,
            'apc_checkplot_curveofgrowth':False
        }
        
        self.config_object['CHECK_PHOT_PROCESS']={
            'checkpro_check_fits_image':False,
            'checkpro_check_png_plot':False,
            'checkpro_checkpng_width':12.
        }
        
        self.config_object['CHECK_PHOT_RESULT']={
            'checkres_reference_flag_threshold':128,
            'checkres_zmagfit_outliers_method':0,
            'checkres_zmagfit_outliers_nsig_dbscan':1.5,
            'checkres_zmagfit_outliers_minfrac_dbscan':0.5,
            'checkres_zmagfit_outliers_nsig_sigmaclip':3.,
            'checkres_zmagfit_polyorder':0,
            'checkres_plot_rawimage_scalerange':[0.1,99.],
            'checkres_plot_zoominimage_width':60.,
            'checkres_plot_zoominimage_scalerange':[0.1,97],
            'checkres_keep_html_only':True
        }
        
        with open(self.cfile, 'w') as conf:
            self.config_object.write(conf)
        #pdb.set_trace()    
        return 1
    
    def read_config(self):
        self.config_object.read(self.cfile)
        photosex_info={'phot_show_env':self.config_object.getboolean('BASIC','show_computer_info'),
                       'workdir':self.config_object['PATHS']['workdir'],
                       'sexdir':self.config_object['PATHS']['sexdir'],
                       'order_apc':self.config_object.getint('APERTURE_CORRECTION','apc_polyorder'),
                       'apc_rad_tot':self.config_object.getfloat('APERTURE_CORRECTION','apc_radius_total_flux'),
                       'checkcog_apc':self.config_object.getboolean('APERTURE_CORRECTION',
                                                                    'apc_checkplot_curveofgrowth'),
                       'checkimg':self.config_object.getboolean('CHECK_PHOT_PROCESS','checkpro_check_fits_image'),
                       'checkplot':self.config_object.getboolean('CHECK_PHOT_PROCESS','checkpro_check_png_plot'),
                       'checkfig_width':self.config_object.getfloat('CHECK_PHOT_PROCESS','checkpro_checkpng_width'),
                       'checkphot_zmag_order':self.config_object.getint('CHECK_PHOT_RESULT','checkres_zmagfit_polyorder'),
                       'checkphot_flag_ref_threshold':self.config_object.getfloat('CHECK_PHOT_RESULT',
                                                                                  'checkres_reference_flag_threshold'),
                       'checkphot_if_cali_outliers_detection_method':self.config_object.getint('CHECK_PHOT_RESULT',
                                                                                               'checkres_zmagfit_outliers_method'),
                       'checkphot_imgraw_interval':ast.literal_eval(self.config_object.get('CHECK_PHOT_RESULT',
                                                                                           'checkres_plot_rawimage_scalerange')),
                       'checkphot_imgzoom_interval':ast.literal_eval(self.config_object.get('CHECK_PHOT_RESULT',
                                                                                            'checkres_plot_zoominimage_scalerange')),
                       'checkphot_nsig_dbscan':self.config_object.getfloat('CHECK_PHOT_RESULT',
                                                                           'checkres_zmagfit_outliers_nsig_dbscan'),
                       'checkphot_minfrac_dbscan':self.config_object.getfloat('CHECK_PHOT_RESULT',
                                                                              'checkres_zmagfit_outliers_minfrac_dbscan'),
                       'checkphot_nsig_sigmaclip':self.config_object.getfloat('CHECK_PHOT_RESULT',
                                                                              'checkres_zmagfit_outliers_nsig_sigmaclip'),
                       'checkphot_keep_html_only':self.config_object.getboolean('CHECK_PHOT_RESULT',
                                                                                'checkres_keep_html_only'),
                       'apers':ast.literal_eval(self.config_object.get('PHOTOMETRY','apertures')),
                       'checkphot_zoom_width':self.config_object.getfloat('CHECK_PHOT_RESULT',
                                                                          'checkres_plot_zoominimage_width')}
        
        return photosex_info
    
    def setconfig(self):
        if os.path.isfile(self.cfile) == False:
            self.create_config_file()
            photosex_info=self.read_config()
        else:
            photosex_info=self.read_config()
        return photosex_info
