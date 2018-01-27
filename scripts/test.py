#!/usr/bin/env python
import pycurl, cStringIO
response_buffer = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'https://www.ag8.com')
c.setopt(c.SSL_VERIFYPEER, 0)
c.setopt(c.SSL_VERIFYHOST, 0)
#c.setopt(c.FOLLOWLOCATION, True)
c.setopt(c.HEADER, True)
c.setopt(c.WRITEFUNCTION, response_buffer.write)
#c.setopt(c.SSL_CIPHER_LIST, 'TLSv1')
c.setopt(c.SSLVERSION, 2)
c.perform()
print c.getinfo(pycurl.HTTP_CODE)
c.close


