class InMemDb(object):
    """ Functions:
        SET [name] [value] - Sets the name in the database to the given value
        GET [name] - Prints the value for the given name. If the value is not in the database, prints N​ ULL
        DELETE [name] - Deletes the value from the database
        COUNT [value] -Returns the number of names that have the given value assigned to them. If that value is not
              assigned anywhere, prints ​0
        END - Exits the database
        The database must also support transactions:
        BEGIN - Begins a new transaction
        ROLLBACK - Rolls back the most recent transaction. If there is no transaction to rollback,
            prints T​RANSACTION NOT FOUND
        COMMIT -Commits a​ll​ of the open transactions
"""

    def __init__(self):
        """ Initialize db instance. """
        self.__db = {}
        self.__values_counts = {}
        self.__transaction_values = []  # Stores previous values to allow rollback
        self.transactions = []
        self.__rollbackstate = False

    def get_transaction_state(self):
        return len(self.transactions) > 0

    def set(self, key, value):
        """ Sets value of name to value. Inserts name into database if it doesn't already exist. """
        current_value = self.__db[key] if key in self.__db else None

        # caught and edge case on tests, if we are replaying commands in rollback, do not save the prev value
        if self.get_transaction_state() and not self.__rollbackstate:
            if current_value is not None:
                self.transactions[-1].insert(0, ['set', key, current_value])
            else:
                self.transactions[-1].insert(0, ['delete', key])

        if current_value == value:
            return

        # keeping track of count to comply with Big(O) preformance requirements
        if current_value in self.__values_counts:
            self.__values_counts[current_value] -= 1

        if value in self.__values_counts:
            self.__values_counts[value] += 1
        else:
            self.__values_counts[value] = 1

        self.__db[key] = value

    def get(self, key):
        """ Returns value of key if it exists in the database, otherwise returns 'NULL'. """
        return self.__db[key] if key in self.__db else 'NULL'

    def get_count(self, value):
        """ Returns number of entries in the database that have the specified value. """
        return self.__values_counts[value] if value in self.__values_counts else 0

    def delete(self, key):
        """ Removes name from database if it's present. """
        current_value = self.__db.pop(key, None)
        if current_value is None:
            return

        self.__values_counts[current_value] -= 1

        if self.get_transaction_state() and not self.__rollbackstate:
            self.transactions[-1].insert(0, ['set', key, current_value])

    def begin(self):
        """ Opens transaction block. """
        # TODO: this is probably easier to track, but no necessary, refactor
        transaction_values = []
        self.transactions.append(transaction_values)

    def rollback(self):

        """
        Rolls back the most recent transaction.
        If there is no transaction to rollback, prints T​RANSACTION NOT FOUND
        """
        self.__rollbackstate = True
        if not self.get_transaction_state():
            return "T​RANSACTION NOT FOUND"

        # replay the commands
        currentTansactionActions = self.transactions.pop()
        print("rolling back recent transaction:", currentTansactionActions)

        for cmd in currentTansactionActions:
            if len(cmd) > 2:
                self.set(cmd[1], cmd[2])

            else:
                self.delete(cmd[1])

        currentTansactionActions = []
        self.__rollbackstate = False
        return True

    def commit(self):
        """
        Commits all transactions to database. Returns True on success,
        """
        if not self.transactions:
            return False
        self.transactions = []
        return True


def display(value, default=None):
    """
    Prints value to stdout. If value is None and a default value is
    specified (and not None), then the default value is printed instead. Otherwise
    the None value is printed.
    """
    if value is None and default is not None:
        value = default
    print(value)


COMMANDS = {
    'SET': (3, lambda db, key, value: db.set(key, value)),
    'GET': (2, lambda db, key: display(db.get(key), "NULL")),
    'DELETE': (2, lambda db, key: db.delete(key)),
    'COUNT': (2, lambda db, value: display(db.get_count(value))),
    'END': (1, lambda db: False),
    'BEGIN': (1, lambda db: db.begin()),
    'ROLLBACK': (1, lambda db: db.rollback() or display("NO TRANSACTION")),
    'COMMIT': (1, lambda db: db.commit())
}


def process_command(simpleDb, command):
    """
    Parses string commands and applies them to the database.
    Returning False indicates that no more commands should be passed in.
    """
    command = command.split()
    opcode = command.pop(0).upper() if len(command) > 0 else None
    if opcode is None or opcode not in COMMANDS or len(command) != (COMMANDS[opcode][0] - 1):
        print("INVALID COMMAND")
    elif 'END' == opcode:
        return False
    else:
        COMMANDS[opcode][1](simpleDb, *command)
    return True


def run():
    """ Reads database command from the command line and passes it through for processing. """
    simpleDb = InMemDb()
    print("Initialized successfully")
    print("Supported commends are: SET, GET, COUNT, BEGIN, COMMIT, ROLLBACK and END")
    while process_command(simpleDb, input()):
        pass
    print("Exiting")

if __name__ == '__main__':
    run()
