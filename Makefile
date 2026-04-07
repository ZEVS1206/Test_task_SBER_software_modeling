COMPILE_CONFIGS  = research_different_configs.py
PARALLEL_EXECUTE = parallel_execute.py
PARSE_LOGS       = parse_logs.py
GET_GRAPHICS     = get_graphics.py
CLEAN_SCRIPT     = clean.sh

CC = python3

.PHONY: all, clean, configurate, execution, parsing, get_info, run
all: configurate

get_info: parsing
	$(CC) $(GET_GRAPHICS)

parsing:
	$(CC) $(PARSE_LOGS)

execution: configurate
	$(CC) $(PARALLEL_EXECUTE)

configurate:
	$(CC) $(COMPILE_CONFIGS)

run: configurate
	$(CC) $(PARALLEL_EXECUTE)
	$(CC) $(PARSE_LOGS)
	$(CC) $(GET_GRAPHICS)

clean:
	./$(CLEAN_SCRIPT)
