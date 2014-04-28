#!/usr/bin/lua

--~ ADAPTED FROM: http://stackoverflow.com/questions/3077236/swig-support-for-inheritance-of-static-member-functions

require("libtest")

b = libtest.B()
d = libtest.D()
b:nonstat()
d:nonstat()
libtest.B_stat()
libtest.D_stat()
