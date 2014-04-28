C_EXEC		:= pp

CC			:= gcc
CFLAGS		:= -I/usr/include/lua5.1 -Wall -Wextra -pedantic -DLUA_USE_APICHECK
LDFLAGS		:= /usr/lib/liblua5.1.so


all: $(C_EXEC)


$(C_EXEC): %: %.c
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@


clean:
	@$(RM) $(C_EXEC)
