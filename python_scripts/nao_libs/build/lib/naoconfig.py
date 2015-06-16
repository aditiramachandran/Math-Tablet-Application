#
# Small config for me and visitors, be my guest...
#
# (c) Aldebaran-robotics 2008
# Author Alexandre Mazel
#

# constantes

LANG_EN = 0;
LANG_FR = 1;
LANG_SP = 2;
LANG_IT = 3;
LANG_GE = 4;
LANG_CH = 5;
LANG_PO = 6;

LOC_JAP = "Japan";
LOC_THA = "Thailand";
LOC_IND = "India";
LOC_CHI = "China";
LOC_WES = "West";
LOC_FRA = "France";
LOC_USA = "USA";

#
# global settings
#

# choose here the default language of Nao
#nNumLang = LANG_EN; 
nStrLoc = LOC_CHI;
nSpeakVolume = 140;
nSpeakPitch 	= 100;
nSpeakSpeed 	= 85;
nSpeakSpeedUI 	= 160;

bPrecomputeText = True; # activate it to precompute text in LocalizedText and various speech

# Debug mode add extra print in various modules
bDebugMode = False;

# This option change the creation of the proxy, move it to False to cut/paste code from choregraphe box directly in a python shell
bInChoregraphe = True; # default True

# Defaut adress when bInChoregraphe is False (to test it from outside choregraphe)
strIP = "10.0.252.135";
nPort = 9559;
