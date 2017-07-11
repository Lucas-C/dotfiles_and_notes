/*    FROM: http://www.lua.org/pil */
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

/* Renamed to avoid confusion with the one from standard error.h */
void my_error_func (lua_State *L, const char *fmt, ...) {
    va_list argp;
    va_start(argp, fmt);
    vprintf(fmt, argp);
    va_end(argp);
    lua_close(L);
    exit(EXIT_FAILURE);
}

void load (char *filename, int *width, int *height) {
    lua_State *L = luaL_newstate();
    luaL_openlibs(L);

    if (luaL_loadfile(L, filename) || lua_pcall(L, 0, 0, 0))
        my_error_func(L, "cannot run configuration file: %s\n", lua_tostring(L, -1));

    lua_getglobal(L, "width");
    if (!lua_isnumber(L, -1))
        my_error_func(L, "`width' should be a number\n");
    lua_getglobal(L, "height");
    if (!lua_isnumber(L, -1))
        my_error_func(L, "`height' should be a number\n");

    *width = (int)lua_tonumber(L, -2);
    *height = (int)lua_tonumber(L, -1);

    lua_close(L);
}

int main (void) {

    int w = 0, h = 0;

    load("pp.lua", &w, &h);

    printf("w = %i, h = %i\n", w, h);

    return 0;
}
