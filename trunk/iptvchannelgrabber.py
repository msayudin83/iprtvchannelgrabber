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
import json

# globals
iprtv_channellist = 'http://w.zt6.nl/tvmenu/index.xhtml.gz'
iprtv_channellist_js = '/data/tvserver/code.js'
iprtv_channellisttv_m3u = '/data/media/index.m3u'
iprtv_channellisttv_m3u_udpxy = '/data/media/iptv.m3u'
url_udpxy = 'http://192.168.0.2:4022'
iprtv_channellistradio_m3u = '/data/media/radio.m3u'

hdpakket = 0
hdmediabox = 0
eredivisiepakket = 0
pluspakket = 0
talenpakket = 0
geenerotiek = 1
startv = 0
universetv = 0

dordrecht = 1
almen = 0
barchem = 0
enter = 0
gorssel = 0
laren = 0
lochem = 0
notter = 0
wierden = 0
ruurlo = 0
arnhem = 0
amersfoort = 0
hoogland = 0
hooglanderveen = 0
houten = 0
leusden = 0
maarssen = 0
maarssenbroek = 0
nieuwegein = 0
soest = 0
soesterberg = 0
stoutenburg = 0
utrecht = 0
veenendaal = 0
woudenberg = 0
rijssen = 0
aarlerixtel = 0
beekendonk = 0
haarlem = 0
hillegom = 0
leiden = 0
lieshout = 0
achterveld = 0
amersfoort = 0
hoogland = 0
hooglanderveen = 0
leusden = 0
stoutenburg = 0
houten = 0
steenenkamer = 0
twello = 0
wilp = 0
amsterdam = 0
hoevelaken = 0
nijkerk = 0
nijkerkerveen = 0
winterswijk = 0
elburg = 0
doornspijk = 0
haaksbergen = 0
goutum = 0
hempens = 0
leeuwarden = 0
enschede = 0
boekelo = 0
bleiswijk = 0
berkelenrodenrijs = 0
bergschenhoek = 0
alphenadrijn = 0
utrecht = 0
bussum = 0
hilversum = 0
naarden = 0
hooglanderveen = 0
hoogland = 0
amersfoort = 0
zeewolde = 0
volkel = 0
veghel = 0
uden = 0
son = 0
odiliapeel = 0
mierlo = 0
geldrop = 0
erp = 0
breugel = 0
sintoedenrode = 0
schijndel = 0
veldhoven = 0
best = 0
valkenswaard = 0
handel = 0
helmond = 0
lieshout = 0
mariahout = 0
milheeze = 0
nuenen = 0
aarlerixtel = 0
bakel = 0
beekendonk = 0
demortel = 0
eindhoven = 0
gemert = 0
meppel = 0
almere = 0
balgoij = 0
batenburg = 0
bergharen = 0
hernen = 0
ntrik = 0
nijmegen = 0
wijchen = 0
schalkhaar = 0
diepenveen = 0
deventer = 0
colmschate = 0
bathmen = 0
v = "ghm"
#v = "wba"
demo = 0
j = 1

def evaluatecondition(expression, hdbox):
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
    stmnt = stmnt.replace('n.', '')
    stmnt = stmnt.replace('c.', '')
    stmnt = stmnt.replace('d.', '')
    stmnt = stmnt.replace('o.', '')
    stmnt = stmnt.replace('Z.', '')
    
    
    #stmnt = stmnt.replace('"wba"', '1')
    stmnt = stmnt.replace('$.hd', 'hdmediabox')

    hello_mod = types.ModuleType("testmodule")

    stmnt= "y = " + stmnt
    #print (stmnt)
    codeObject = compile(stmnt, '<Summink>', 'exec')
    #tel = {'vodafone':0,'arabisch':0,'universetv':0, 'u':0, 'q':1, 'startv': 0, 'y': False, 'p': 1, 'wba': 0, 'hd': 0, 'hdmediabox': 0, 'demo': 0, 'ecv': 0, 'plus': 0, 'talen': 0, 'geenerotiek': 0}
    tel = {'i':1,'epse':0,'almen':0,'barchem':0,'eefde':0,'enter':0,'gorssel':0,'laren':0,'lochem':0,'notter':0,'wierden':0,'ruurlo':0,'almen':almen,'barchem':barchem,'enter':0,'gorssel':0,'laren':0,'lochem':0,'notter':0,'wierden':0,'ruurlo':0,'arnhem':0,'amersfoort':0,'hoogland':0,'hooglanderveen':0,'houten':0,'leusden':0,'maarssen':0,'maarssenbroek':0,'nieuwegein':0,'soest':0,'soesterberg':0,'stoutenburg':0,'utrecht':0,'veenendaal':0,'woudenberg':0,'rijssen':0,'aarlerixtel':0,'beekendonk':0,'haarlem':0,'hillegom':0,'leiden':0,'lieshout':0,'achterveld':0,'amersfoort':0,'hoogland':0,'hooglanderveen':0,'leusden':0,'stoutenburg':0,'houten':0,'steenenkamer':0,'twello':0,'wilp':0,'amsterdam':0,'hoevelaken':0,'nijkerk':0,'nijkerkerveen':0,'winterswijk':0,'elburg':0,'doornspijk':0,'haaksbergen':0,'goutum':0,'hempens':0,'leeuwarden':0,'enschede':0,'boekelo':0,'bleiswijk':0,'berkelenrodenrijs':0,'bergschenhoek':0,'alphenadrijn':alphenadrijn,'dordrecht':dordrecht,'utrecht':utrecht,'bussum':0,'hilversum':0,'naarden':0,'hooglanderveen':0,'hoogland':0,'amersfoort':0,'zeewolde':0,'volkel':0,'veghel':0,'uden':0,'son':0,'odiliapeel':0,'mierlo':0,'geldrop':0,'erp':0,'breugel':0,'sintoedenrode':0,'schijndel':0,'veldhoven':0,'best':0,'valkenswaard':0,'handel':0,'helmond':0,'lieshout':0,'mariahout':0,'milheeze':0,'nuenen':0,'aarlerixtel':0,'bakel':0,'beekendonk':0,'demortel':0,'eindhoven':0,'gemert':0,'meppel':0,'almere':0,'balgoij':0,'batenburg':0,'bergharen':0,'hernen':0,'ntrik':0,'nijmegen':0,'wijchen':0,'schalkhaar':0,'diepenveen':0,'deventer':0,'colmschate':0,'bathmen':0,'solcon':0,'vodafone':0,'arabtv':0,'universetv':universetv, 'v':v, 'w':v, 'q':1, 'startv': startv, 'y': False, 'wba': 0, 'j': 1, 'hd': hdpakket, 'hdmediabox': hdbox, 'demo': demo, 'ecv': eredivisiepakket, 'plus': pluspakket, 'talen': talenpakket, 'geenerotiek': geenerotiek}

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
        # f = open(iprtv_channellist_js, 'w')
        # f.write(blah)
        # f.close()
    except:
        sys.stderr.write('Cannot decompress data from url: %s\n' % iprtv_channellist)
        sys.exit(1)
        
    blah = blah.replace('\r','')
    blah = blah.replace('\n','')

    getrow = re.compile("src=\'code\.js\.gz\?([0-9]*)\'")
    allrows = getrow.finditer(blah)
    
    scripturl = 'http://w.zt6.nl/tvmenu/code.js.gz?'

    for item in allrows:
        scripturl += item.group(1)
    
    print ('scripturl = ', scripturl)
    
    # Read the channel stuff
    req = urllib.request.Request(scripturl)
    fd = urllib.request.urlopen(req)

    # continue?
    lastmodified = fd.info().get('Last-Modified')
    print (lastmodified)

    #try:
    decompresseddata = decompress(fd.read())

    try:
        blah = decompresseddata.decode('utf-8', 'ignore')
        #f = open(iprtv_channellist_js, 'w')
        #f.write(blah)
        #f.close()
    except:
        if not quiet:
            sys.stderr.write('Cannot decompresseddata from url: %s\n' % scripturl)
        sys.exit(1)
    
    blah = blah.replace('\r','')
    blah = blah.replace('\n','')

    # some useful regexps
    nameregex = '[^"]*'
    ipregex = '[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]'

    count = 0 
    
    #                       1                    2         3       4            5      6        7            8        9       10    11
    getrow = re.compile('([cde]\.push\("[ A-z0-9-]*)("\);)(if\(.*?)\{b=([0-9]*);if(.*?),[bc]:{".*?":"(%s)"},[klm]:{".*?":"(%s)"},[gf]:"(%s)",[ij]:"(%s)",[np]:"(%s)"(.*?)(\[[cde]\.pop\(\))' % (nameregex, nameregex, nameregex, nameregex, nameregex))

    allrows = getrow.finditer(blah)

    temp = list(allrows)
    result = len(temp)
	
    print ("result=%d" % result)
#    sys.exit(1090)
	
    allrows = getrow.finditer(blah)

    for item in allrows:
        #print (item.group(3))
        if (evaluatecondition(item.group(3), hdmediabox)):
            
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
            getsubrow = re.compile(';[IJK]\.tv_(.*?)\.[ab]\.push')
            allsubrows = getsubrow.finditer(item.group(11))

            for subitem in allsubrows:
                isTV = 1
                category = subitem.group(1)

            getsubrow = re.compile(';[IJK]\.radio_(.*?)\.[ab]\.push')
            allsubrows = getsubrow.finditer(item.group(11))

            for subitem in allsubrows:
                isRadio = 1
                category = subitem.group(1)
            #                     1         2             3    4        5              6
            getrow = re.compile('(if\(.*?){(.*?)"igmp://(%s):([0-9]*)(;rtpskip=yes)?"(.*?)\.push' % (ipregex))
            allsubrows = getrow.finditer(item.group(11))
            
            isHD = ''
            
            for subitem in allsubrows:
                
                print ('   sub: %s,%s' % (item.group(4), subitem.group(1)))
                if(evaluatecondition(subitem.group(1), hdmediabox)):
                    if hdmediabox == 1:
                        if (evaluatecondition(subitem.group(1), 0) == False):
                            isHD = ' HD'
                    
                    if (subitem.group(5) == ";rtpskip=yes"):
                        channelurl = ('rtp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                    else:
                        channelurl = ('udp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                    break
                    
            if channelurl != '':
                if (isTV):
                    tvchannels[channelnumber] = '#EXTINF:%s,%s %s%s\n%s\n' % (item.group(4), channelnumber, channelascii, isHD, channelurl)
                    print ('#TV: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl))
#                    print ('new rec_%s broadcast enabled input "%s" output "#std{access=file,mux=ts,dst=/data/media/test_%s.ts} option sout-all"' % (item.group(4),channelurl ,item.group(4) ))
                else:
                    if (isRadio):
                        radiochannels[channelnumber] = '#EXTINF:%s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl)
                        print ('#RADIO: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, channelurl))
                    else: 
                        print ('#UNKNOWN: %s,%s %s\n%s\n' % (item.group(4), channelnumber, channelascii, item.group(11)))
            else:
                 print ('#NO URL??  channel: %s,%s %s\n%s' % (item.group(4), channelnumber, channelascii, item.group(11)))
				#           1                        2    3       4       5     6     7    8    9     10   11    12    13   14
            count += 1
    
    print ("result tvchannels=%d" % len(tvchannels))
    print ("result radiochannels=%d" % len(radiochannels))

    #c.push("ned1");b=1;if(e)F[a].h=b;else{e=1;f=b}F[b]={g:b,b:{"default":"Nederland 1"},k:{"default":"Nederland 1"},f:"ned1",i:"ned1",n:"ned1.png",o:"ned1.png",m:"ned1.png",j:a,c:[]};
    #                    1                          2       3       4               5     6               7     8       9    10        11    12   13   14
     getrow = re.compile('([cde]\.push\("[ A-z0-9-]*)"\)(;b=)([0-9]*)(.*?),[bc]:{".*?":"(%s)"}(,[klm]:){".*?":"(%s)"}(,[gf]:)"(%s)"(,[ij]:)"(%s)"(,[np]:)"(%s)"(.*?)(\[[cde]\.pop\(\))' % (nameregex, nameregex, nameregex, nameregex, nameregex), re.DOTALL)

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
    
        getsubrow = re.compile(';[IJKL]\.tv_(.*?)\.[ab]\.push')
        allsubrows = getsubrow.finditer(item.group(14))

        for subitem in allsubrows:
            isTV = 1
            category = subitem.group(1)
            
        getsubrow = re.compile(';[IJKL]\.radio_(.*?)\.[ab]\.push')
        allsubrows = getsubrow.finditer(item.group(14))

        for subitem in allsubrows:
            isRadio = 1
            category = subitem.group(1)

        print ('channel: %s,%s' % (item.group(3), channelascii))
		#                     1         2             3    4    
        getrow = re.compile('(if\(.*?){(.*?)"igmp://(%s):([0-9]*)(;rtpskip=yes)?"(.*?)\.push' % (ipregex))

        allsubrows = getrow.finditer(item.group(14))

        isHD = ''

        for subitem in allsubrows:
            print ('   sub: %s,%s' % (item.group(3), subitem.group(1)))
            if(evaluatecondition(subitem.group(1), hdmediabox)):

                if hdmediabox == 1:
                    if (evaluatecondition(subitem.group(1), 0) == False):
                        isHD = ' HD'

                if (subitem.group(5) == ";rtpskip=yes"):
                    channelurl = ('rtp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                else:
                    channelurl = ('udp://@%s:%s' % (subitem.group(3), subitem.group(4)))
                break

        if channelurl != '':
            if (isTV):
                tvchannels[channelnumber] = '#EXTINF:%s,%s %s%s\n%s\n' % (item.group(3), channelnumber, channelascii, isHD, channelurl)
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
