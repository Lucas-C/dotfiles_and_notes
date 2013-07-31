TESTS_CXX	:= $(patsubst %.cpp, %, $(wildcard *.cpp))
TESTS_C		:= $(patsubst %.c, %, $(wildcard *.c))

all: $(TESTS_C) $(TESTS_CXX)

$(TESTS_C): %: %.c
	$(CC) $(CCFLAGS) $< -o $@

$(TESTS_CXX): %: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# Options de compilation générales
CXX			:= g++
CXXFLAGS	:= -O1 -Wall -Wextra -pedantic-errors -Wfloat-equal -Wconversion -Wshadow -Weffc++
CC			:= gcc
CCFLAGS		:= -O1 -Wall -Wextra -pedantic-errors -Wfloat-equal -Wconversion -Wshadow -std=c99

.PHONY: clean

clean:
	@$(RM) *.o $(TESTS_C) $(TESTS_CXX) *.aux *.log *.out *.log
