
https://luarocks.org -- package manager

https://github.com/cloudflare/lua-aho-corasick -- Aho-Corasick efficient string matching algorithm

https://github.com/mpeterv/luacheck -- linting and static analysis

https://github.com/Olivine-Labs/busted -- elegant unit testing


-- Main features/idioms -> cf. http://tylerneylon.com/a/learn-lua/
- has garbage collection
- global vars by default
- functions are first-class
- multiple results & multiple assignments
- ranges: i = 1,100 !! indices start at 1 !!
- named args & varargs
- closures & iterators
- error / pcall
- require
- coroutines
- tables : main datastructures, hash-lookup dicts that can also be used as lists
- unpack
- metatables & classes...

-- Used in Apache HTTP Server, Kong, MediaWiki, Nginx, Redis, VLC


-- Demo:

    luarocks install redis-lua
    luarocks install --server=http://luarocks.org luasec OPENSSL_LIBDIR=/usr/lib/x86_64-linux-gnu/
    luarocks install --server=http://luarocks.org luarepl
    eval $(luarocks path --bin)
    rep.lua  # use rlwrap

-- https://www.redisgreen.net/blog/intro-to-lua-for-redis-programmers/
-- https://www.compose.com/articles/a-quick-guide-to-redis-lua-scripting/

    redis-cli --eval hello.lua
