/*    FROM: http://www.lua.org/pil */
#include <stdio.h>
#include <lua.h>
#include <lauxlib.h>

static void stackDump (lua_State *L) {
    int i;
    int top = lua_gettop(L);
    for (i = 1; i <= top; i++) {  /* repeat for each level */
        int t = lua_type(L, i);
        switch (t) {

          case LUA_TSTRING:  /* strings */
            printf("`%s'", lua_tostring(L, i));
            break;

          case LUA_TBOOLEAN:  /* booleans */
            printf(lua_toboolean(L, i) ? "true" : "false");
            break;

          case LUA_TNUMBER:  /* numbers */
            printf("%g", lua_tonumber(L, i));
            break;

          default:  /* other values */
            printf("%s", lua_typename(L, t));
            break;

        }
        printf("  ");  /* put a separator */
    }
    printf("\n");  /* end the listing */
}


int main (void) {
    lua_State *L = luaL_newstate();
    lua_pushboolean(L, 1); lua_pushnumber(L, 10);
    lua_pushnil(L); lua_pushstring(L, "hello");
    stackDump(L);
                       /* true  10  nil  `hello'  */

    lua_pushvalue(L, -4); stackDump(L);
                       /* true  10  nil  `hello'  true  */

    lua_replace(L, 3); stackDump(L);
                       /* true  10  true  `hello'  */

    lua_settop(L, 6); stackDump(L);
                       /* true  10  true  `hello'  nil  nil  */

    lua_remove(L, -3); stackDump(L);
                       /* true  10  true  nil  nil  */

    lua_settop(L, -5); stackDump(L);
                       /* true  */

    lua_close(L);
    return 0;
}
