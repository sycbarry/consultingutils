import os
import sys
import oracledb
import os
import ibm_db
import cx_Oracle




"""
our base db object.
"""
class DB(object):

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

    def test_conn(): 
        return

    def testquery(self, query=None, isreturnable=True): 
        return 

    @property
    def get_user(self): 
        return self.user
    
    @property 
    def get_pw(self): 
        return self.pw


class DB2(DB): 

    def __init__(
        self, 
        pw = None, 
        user = None, 
        database = None, 
        port = None,
        hostname = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pw = pw
        self.user = user
        self.database = database
        self.port = port
        self.hostname = hostname


        self.dsn = f"DATABASE={self.database};HOSTNAME={self.hostname};PORT={self.port};PROTOCOL=TCPIP;UID={self.user};PWD={self.pw}"

    """

    This is just a function that tests queries for us. 
    We use this queyr to validate that a query actually runs 
    against the database.  
    
    """
    def testquery(self, query=None, isreturnable=False): 
        if query == None: 
            raise FileNotFoundError("no query provided")

        try: 
            connection = ibm_db.connect(self.dsn, '', '')
            try: 
                statement = ibm_db.exec_immediate(
                    connection, query)
                results = []
                rows = ibm_db.fetch_both(statement)
                while rows != False:
                    results.append(rows)
                    rows = (ibm_db.fetch_both(statement))
                return results
            except Exception as e: 
                print(e) 
                return Exception(e)
        except Exception as e: 
            print(e) 
            return Exception(e)


class Oracle(DB): 

    def __init__(
        self, pw=None, 
        user=None, dsn=None, 
        libdir=None, *args, **kwargs
    ): 
        super().__init__(*args, **kwargs)
        self.pw = pw
        self.user = user
        self.dsn = dsn
        self.libdir = libdir
    
        self.initdb()

    def initdb(self): 
        if self.libdir == None: 
            raise FileNotFoundError("Oracle Driver not specified.")
        try: 
            cx_Oracle.init_oracle_client(lib_dir=self.libdir)
        except BaseException as e: 
            raise FileNotFoundError(e)
        finally: 
            return


    """
    
    This is just a function that tests queries for us. 
    We use this queyr to validate that a query actually runs 
    against the database.  
    
    """
    #### TODO will have to adjust this sometime.
    def testquery(self, query="", isreturnable=False): 
        try: 
            connection = cx_Oracle.connect(
                user = self.user, 
                password = self.pw, 
                dsn = self.dsn
            )
            cursor = connection.cursor()
            try: 
                rows = []
                for row in cursor.execute(query): 
                    if isreturnable == True: 
                        # is_lob = lambda x: True if x.read() else False
                        # val = { x[0].read() if is_lob(x[0]) else x[0] : x[1] for x in row }
                        rows.append(
                            {"DESIGN": ''.join(row[0].read()), "REPORTNAME": row[1]}
                        )
                    else: 
                        if row is not None:
                            if row[0] is not None: 
                                cursor.close()
                                return rows
                        else: 
                            return None
                cursor.close()
                return rows
            except Exception as e: 
                print(e) 
                return Exception(e)
        except Exception as e: 
            print(e) 
            return Exception(e)