# Makefile

CC = gcc
CFLAGS = -Wall -Wextra -g
ifeq ($(shell uname -s),Linux)
    LDFLAGS = -lseccomp
else
    LDFLAGS =
endif

# List of source files
SRCS = util.c crunner.c

# List of object files
OBJS = $(SRCS:.c=.o)

# Output executable
TARGET = crunner

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) $(CFLAGS) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
