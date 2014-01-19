CXX			:= g++
LUA_INCLUDE	:= -I/usr/include/lua5.1
LUA_LIB    	:= /usr/lib/liblua5.1.so
CFLAGS		:= $(LUA_INCLUDE) -Wall -Wextra -pedantic-errors -Wfloat-equal -Wshadow
LDFLAGS		:= $(LUA_LIB)

all: fact.so

.PRECIOUS: %_wrap.cxx
%_wrap.cxx: %.i
	swig -c++ -lua $<

%.so: %.cpp %_wrap.cxx
	$(CXX) -shared $(LDFLAGS) $(CFLAGS) $^ -o $@

clean:
	@$(RM) -f *.so *_wrap.cxx
