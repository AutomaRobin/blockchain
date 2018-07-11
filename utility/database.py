import sqlite3


class Database:

    def __init__(self, db_path=None):
        """
         The constructor of the Database class.

         Arguments:
        :db_path: The path to the database which should be connected to.
        """
        self.conn = None
        self.cursor = None

        if db_path:
            self.open(db_path)

    def open(self, database):
        """
            Opens a new database connection.

            Arguments:
                :database: The database to which will be connected
        """
        try:
            self.conn = sqlite3.connect(database)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            return e

    def close(self):
        """ Function to close a database connection. """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()

    def get(self, table, columns, limit=None):
        """Function to fetch/query data from a database.

            Arguments:
                :table: Table The name of the database's table to query from.
                :columns: The string of columns, comma-separated, to fetch.
                :limit: Optionally, a limit of items to fetch.
        """
        query = "SELECT {0} from {1}".format(columns, table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows) - limit if limit else 0:]

    def get_last(self, table, columns):
        """Utility function to get the last row of data from a database.

            Arguments:
                :table: The database's table from which to query.
                :columns: The columns which to query.
        """
        return self.get(table, columns, limit=1)[0]

    @staticmethod
    def to_csv(data, fname="output.csv"):
        """Utility function that converts a dataset into CSV format.

            Arguments:
                :data: The data, retrieved from the get() function.
                :fname: The file name to store the data in.
        """
        with open(fname, 'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))

    def write(self, table, columns, data):
        """Function to write data to the database.

            Arguments:
                :table: The name of the database's table to write to.
                :columns: The columns to insert into, as a comma-separated string.
                :data: The new data to insert, as a comma-separated string.
        """
        query = "INSERT INTO {0} ({1}) VALUES (?);".format(table, columns)

        self.cursor.execute(query, (data,))

    def query(self, sql):
        """Function to query any other SQL statement.

            Arguments:
                :sql: A valid SQL statement in string format.
        """
        self.cursor.execute(sql)

    @staticmethod
    def summary(rows):
        """Utility function that summarizes a dataset.

            Arguments:
                :rows: The retrieved data.
        """
        # split the rows into columns
        cols = [[r[c] for r in rows] for c in range(len(rows[0]))]

        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        t = lambda col: "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c) / len(rows)

            ret.append(((hi, hi_t), (lo, lo_t), avg))

        return ret


