import functools
import re
import time
from collections import defaultdict

from django.db import connection


class QueryDebug:
    """
    A class for analyzing and optimizing code blocks from the point
    of view of the number of queries to the database.

    You can use it as a decorator:

        @QueryDebug()
        def f():
            ...

    You can use it as a context manager:

        with QueryDebug("code_block_name"):
            ...
    """

    def __init__(self, code_block_name='', file_name=None):
        self.name = code_block_name
        self.old_queries = set()
        self.new_queries = set()
        self.from_counter = defaultdict(int)
        self.command_count = defaultdict(int)
        self.from_command_count = defaultdict(int)
        self.start_time = 0
        self.end_time = 0
        self.file_name = file_name

    def __enter__(self):
        self.old_queries = {query['sql'] for query in connection.queries}
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.new_queries = {
            query['sql'] for query in connection.queries
        } - self.old_queries
        self.end_time = time.time()
        self.check_tables()
        self.print_result()

    def check_tables(self):
        """Change the pattern when using a DBMS other than MS SQL."""

        pattern = re.compile(r'\b(FROM|JOIN)\s+\[?(\w+)\].\[?(\w+)\]', re.IGNORECASE)
        for query in self.new_queries:
            from_clauses = pattern.findall(query)
            command = query.split()[0].upper()
            self.command_count[command] += 1
            if from_clauses:
                for fc in from_clauses:
                    fc = ".".join(fc)
                    self.from_counter[fc] += 1
                    self.from_command_count[f'{command}_{fc}'] += 1

    def __call__(self, func):
        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            self.start_time = time.time()
            self.old_queries = {query['sql'] for query in connection.queries}
            result = func(*args, **kwargs)
            self.new_queries = {
                query['sql'] for query in connection.queries
            } - self.old_queries
            self.end_time = time.time()
            self.name = f'function:{func.__name__}'
            self.check_tables()
            self.print_result()
            return result

        return inner_func

    def print_result(self):
        # log = f'''
        # BLOCK: {self.name}
        # TIME: {self.end_time - self.start_time} sec
        # QUERIES COUNT: {len(self.new_queries)}
        # TABLES: {dict(self.from_counter)}
        # COMMANDS: {dict(self.command_count)}
        # INFO: {dict(self.from_command_count)}
        # '''
        log = f"BLOCK: {self.name}\nTIME: {self.end_time - self.start_time} sec\nQUERIES COUNT: {len(self.new_queries)}\nTABLES: {dict(self.from_counter)}\nCOMMANDS: {dict(self.command_count)}\nINFO: {dict(self.from_command_count)}\n"
        # print(log, file=self.file_name)
        with open(self.file_name, "a") as data:
            delimiter = "=" * 100
            data.write(f"{log}\n{delimiter}\n")
