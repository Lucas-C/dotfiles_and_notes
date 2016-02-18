%module fact
// FROM: http://www.swig.org/Doc1.3/Lua.html#Lua_nn7

%typemap(in) int {
    $1 = (int) lua_tonumber(L,$input);
    printf("Received an integer : %d\n",$1);
}
%inline %{
extern int fact(int n);
%}
