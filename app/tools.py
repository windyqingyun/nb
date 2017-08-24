import hashlib
import uuid
import datetime
def get_md5(md_str):
    md = hashlib.md5()
    md.update(md_str)
    return md.hexdigest()

def get_uuid():
    return unicode(uuid.uuid4()) 

def get_current_time():
    return datetime.datetime.now()

def cut_string(s,lens):
    slen = len(s)
    if slen <= lens:
        return s
    else :
        return s[0:lens]+"..."

