# Modules we need
import subprocess
import types
import io
import re, urllib.request, getopt, sys
import time, random
import html.entities
import os, os.path, pickle
import http.cookiejar
import mimetypes, random
import gzip

# globals
iprtv_channellist = 'http://w.zt6.nl/tvmenu/index.xhtml.gz'
iprtv_channellist_xhtml = '/data/tvserver/index1.xhtml'
iprtv_channellisttv_m3u = '/data/media/index.m3u'
iprtv_channellisttv_m3u_udpxy = '/data/media/iptv.m3u'
url_udpxy = 'http://192.168.0.2:4022'
iprtv_channellistradio_m3u = '/data/media/radio.m3u'

hdpakket = 0
hdmediabox = 0
eredivisiepakket = 0
pluspakket = 0
talenpakket = 0
geenerotiek = 0
startv = 0
universetv = 0

v = "ghm"

q = 1
demo = 0

def evaluatecondition(expression):
    stmnt = expression
    stmnt = stmnt.replace('if', '')
    stmnt = stmnt.replace('{', '')
    stmnt = stmnt.replace('i.', '')
    stmnt = stmnt.replace('l.', '')
    stmnt = stmnt.replace('j.', '')
    stmnt = stmnt.replace('&&', ' and ')
    stmnt = stmnt.replace('||', ' or ')
    stmnt = stmnt.replace('!', ' not ')
    stmnt = stmnt.replace('h.', ' ')

    stmnt = stmnt.replace('"wba"', '1')
    stmnt = stmnt.replace('$.hd', 'hdmediabox')

    hello_mod = types.ModuleType("testmodule")

    stmnt= "y = " + stmnt
    #print (stmnt)
    codeObject = compile(stmnt, '<Summink>', 'exec')
    #tel = {'vodafone':0,'arabisch':0,'universetv':0, 'u':0, 'q':1, 'startv': 0, 'y': False, 'p': 1, 'wba': 0, 'hd': 0, 'hdmediabox': 0, 'demo': 0, 'ecv': 0, 'plus': 0, 'talen': 0, 'geenerotiek': 0}
    tel = {'vodafone':0,'arabtv':0,'universetv':universetv, 'u':s, 'q':q, 'startv': startv, 'y': False, 'p': 1, 'v': v, 'hd': hdpakket, 'hdmediabox': hdmediabox, 'demo': demo, 'ecv': eredivisiepakket, 'plus': pluspakket, 'talen': talenpakket, 'geenerotiek': geenerotiek}

    hello_mod.say_hell = types.FunctionType(codeObject, tel)
    hello_mod.say_hell()

			
    if (tel['y']):
        return 1

    return 0
	
def decompress(data):
    """Decompress a gzip compressed string in one shot.
    Return the decompressed string.
    """
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as f:
        return f.read()

def main():

    tvchannels = {}
    radiochannels = {}
	
    # Read the channel stuff
    req = urllib.request.Request(iprtv_channellist)
    fd = urllib.request.urlopen(req)

    decompresseddata = decompress(fd.read())

    lastmodified = fd.info().get('Last-Modified')

    print ('Grabbing channellist from url: %s\nLast modified on %s' % (iprtv_channellist, lastmodified))

    try:
        blah = decompresseddata.decode('utf-8', 'ignore')
        # f = open(iprtv_channellist_xhtml, 'w')
        # f.write(blah)
        # f.close()
    except:
        sys.stderr.write('Cannot decompress data from url: %s\n' % iprtv_channellist)
        sys.exit(1)
        
    blah = blah.replace('\r','')
    blah = blah.replace('\n','')

    # some useful regexps
    nameregex = '[^"]*'
    ipregex = '[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]'

    count = 0 
    
    #                       1                    2         3       4            5      6        7            8        9       10    11
    getrow = re.compile('(c\.push\("[ A-z0-9-]*)("\);)(if\(.*?)\{b=([0-9]*);if(.*?),[bc]:{".*?":"(%s)"},[kl]:{".*?":"(%s)"},[gf]:"(%s)",[ij]:"(%s)",n:"(%s)"(.*?)(\[c\.pop\(\))' % (nameregex, nameregex, nameregex, nameregex, nameregex))

    allrows = getrow.finditer(blah)

    temp = list(allrows)
    result = len(temp)
	
    print ("result=%d" % result)
#    sys.exit(1090)
	
    allrows = getrow.finditer(blah)

    for item in allrows:
        if (evaluatecondition(item.group(3))):

            channelnumber = item.group(4)
            if len(channelnumber) == 1:
                channelnumber = '00' + channelnumber
            if len(channelnumber) == 2:
                channelnumber = '0' + channelnumber

            channelascii = item.group(6).replace('\\u00e2', 'â')
            channelascii = channelascii.replace('\\u00e9', 'é')
            channelascii = channelascii.replace('\\u00fc', 'ü')
            channelascii = channelascii.replace('\\u00dc', 'Ü')
            channelascii = channelascii.replace('\\u00ef', 'ï')

            channelurl = ''
            category = 'other'
            isTV = 0
            isRadio = 0

            print ('channel: %s,%s' % (item.group(4), channelascii))

            #                     1         2             3    4    
            getsubrow = re.compile('for\([IJKL]\.tv_(.*?)\.a\.push')
            allsubrows = getsubrow.finditer(item.group(11))

            for subitem in allsubrows:
                isTV = 1
                category = subitem.group(1)

            getsubrow = re.compile('for\([IJKL]\.radio_(.*?)\.a\.push')
            allsubrows = getsubrow.finditer(item.group(11))

            for subitem in allsubrows:
                isRadio = 1
                category = subitem.group(1)
            #                     1         2             3    4        5              6
            getrow = re.compile('(if\(.*?){(.*?)"igmp://(%s):([0-9]*)(;rtpskip=yes)?"(.*?)\.push' % (ipregex))
            allsubrows = getrow.finditer(item.group(11))
	    
            for subitem in allsubrows:
                
                print ('   sub: %s,%s' % (item.group(4), subitem.group(1)))
                if(evaluatecondition(subitem.group(1))):
                    if (subitem.group(5) == ";rtpskip=yes"):
                        channelurl = ('rtp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                    else:
                        channelurl = ('udp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                    break
                    
            if channelurl != '':
                if (isTV):
                    tvchannels[channelnumber] = '#EXTINF:%s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl)
                    print ('#TV: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl))
#                    print ('new rec_%s broadcast enabled input "%s" output "#std{access=file,mux=ts,dst=/data/media/test_%s.ts} option sout-all"' % (item.group(4),channelurl ,item.group(4) ))
                else:
                    if (isRadio):
                        radiochannels[channelnumber] = '#EXTINF:%s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl)
                        print ('#RADIO: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl))
                    else: 
                        print ('#UNKNOWN: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, item.group(10)))
            else:
                 print ('#NO URL??  channel: %s,%s %s' % (item.group(4), channelnumber, channelascii))
				#           1                        2    3       4       5     6     7    8    9     10   11    12    13   14
    
    print ("result tvchannels=%d" % len(tvchannels))
    print ("result radiochannels=%d" % len(radiochannels))

    #c.push("ned1");b=1;if(e)F[a].h=b;else{e=1;f=b}F[b]={g:b,b:{"default":"Nederland 1"},k:{"default":"Nederland 1"},f:"ned1",i:"ned1",n:"ned1.png",o:"ned1.png",m:"ned1.png",j:a,c:[]};
    #                    1                          2    3       4               5     6               7     8       9    10        11    12   13   14
    getrow = re.compile('(c\.push\("[ A-z0-9-]*)"\)(;b=)([0-9]*)(.*?),[bc]:{".*?":"(%s)"}(,[kl]:){".*?":"(%s)"}(,[gf]:)"(%s)"(,[ij]:)"(%s)"(,n:)"(%s)"(.*?)(\[c\.pop\(\))' % (nameregex, nameregex, nameregex, nameregex, nameregex), re.DOTALL)

    allrows = getrow.finditer(blah)

    temp = list(allrows)
    result = len(temp)
    print ("result=%d" % result)
#	
    allrows = getrow.finditer(blah)

    for item in allrows:
        channelnumber = item.group(3)
        if len(channelnumber) == 1:
            channelnumber = '00' + channelnumber
        if len(channelnumber) == 2:
            channelnumber = '0' + channelnumber

        channelascii = item.group(5).replace('\\u00e2', 'â')
        channelascii = channelascii.replace('\\u00e9', 'é')
        channelascii = channelascii.replace('\\u00fc', 'ü')
        channelascii = channelascii.replace('\\u00dc', 'Ü')
        channelascii = channelascii.replace('\\u00ef', 'ï')

        channelurl = ''
        category = 'other'
        isTV = 0
        isRadio = 0
    
        getsubrow = re.compile('for\([IJKL]\.tv_(.*?)\.a\.push')
        allsubrows = getsubrow.finditer(item.group(14))

        for subitem in allsubrows:
            isTV = 1
            category = subitem.group(1)
            
        getsubrow = re.compile('for\([IJKL]\.radio_(.*?)\.a\.push')
        allsubrows = getsubrow.finditer(item.group(14))

        for subitem in allsubrows:
            isRadio = 1
            category = subitem.group(1)

        print ('channel: %s,%s' % (item.group(3), channelascii))
		#                     1         2             3    4    
        getrow = re.compile('(if\(.*?){(.*?)"igmp://(%s):([0-9]*)(;rtpskip=yes)?"(.*?)\.push' % (ipregex))

        allsubrows = getrow.finditer(item.group(14))

        for subitem in allsubrows:
            print ('   sub: %s,%s' % (item.group(3), subitem.group(1)))
            if(evaluatecondition(subitem.group(1))):

                if (subitem.group(5) == ";rtpskip=yes"):
                    channelurl = ('rtp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                else:
                    channelurl = ('udp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                break

        if channelurl != '':
            if (isTV):
                tvchannels[channelnumber] = '#EXTINF:%s,%s %s\n%s\n' % (item.group(3), channelnumber, channelascii, channelurl)
                print ('#TV: %s,%s %s\n%s\n' % (item.group(3), channelnumber, channelascii, channelurl))
            else:
                if (isRadio):
                    radiochannels[channelnumber] = '#EXTINF:%s,%s %s\n%s\n' % (item.group(3), channelnumber, channelascii, channelurl)
                    print ('#RADIO: %s,%s %s\n%s\n' % (item.group(3), channelnumber, channelascii, channelurl))
                else: 
                    print ('#UNKNOWN: %s,%s %s\n%s\n' % (item.group(3), channelnumber, channelascii, item.group(14)))
        else:
             print ('#NO URL??  channel: %s,%s %s' % (item.group(3), channelnumber, channelascii))
                    
    f = open(iprtv_channellisttv_m3u, 'w')
    f.write('#EXTM3U\n')

    u = open(iprtv_channellisttv_m3u_udpxy, 'w')
    u.write('#EXTM3U\n')

    print ('total %s tvchannels found\n' % len(tvchannels) )
    
    sortedchannels = sorted(tvchannels)
    for channel in sortedchannels:
        f.write(tvchannels[channel])
        s = tvchannels[channel].replace('udp://@', '%s/udp/' % url_udpxy)
        s = s.replace('rtp://@', '%s/rtp/' % url_udpxy)
        s = s.replace('\n%s' % url_udpxy, '\n%s' % url_udpxy)
        u.write(s)
    u.close()
    f.close()

    f = open(iprtv_channellistradio_m3u, 'w')
    f.write('#EXTM3U\n')

    print ('total %s radiochannels found\n' % len(radiochannels) )
    
    sortedchannels = sorted(radiochannels)
    for channel in sortedchannels:
        f.write(radiochannels[channel])
    f.close()


    # and return success
    sys.exit(0)

# allow this to be a module
if __name__ == '__main__':
    main()
