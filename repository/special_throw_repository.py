

class SpecialThrowRepository:

    @staticmethod
    def getSpecialThrow(cursor, throw_type):
        query = cursor.execute("SELECT * FROM SPECIAL_THROW"
                               "WHERE SPECIAL_THROW = ?", throw_type)
        result = query.fetchone()
        return result

    @staticmethod
    def getAllSpecialThrows(cursor, throw_type):
        query = cursor.execute("SELECT * FROM SPECIAL_THROW", throw_type)
        result = query.fetchall()
        return result
