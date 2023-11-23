# Makefile

CC = clang
CFLAGS = -Wall -Wextra -g

# List of source files
SRCS = util.c crunner.c

# List of object files
OBJS = $(SRCS:.c=.o)

# Output executable
TARGET = crunner

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
