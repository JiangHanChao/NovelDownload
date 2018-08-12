# -*- coding: utf-8 -*-
#!/usr/bin/python3
#utils tools 
import urllib

def PrintObj(obj):
	print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

def Che2ULC(cn_string):
	u_str =  urllib.request.quote(cn_string)
	return u_str