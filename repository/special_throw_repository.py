
class SpecialThrowRepository:

    @staticmethod
    def getSpecialThrow(cursor, throw_type):
        cursor.execute("SELECT * FROM SPECIAL_THROW "
                           "WHERE SPECIAL_THROW=%s", (throw_type,))
        result = cursor.fetchone()
        return result

    @staticmethod
    def getAllSpecialThrows(cursor):
        cursor.execute("SELECT * FROM SPECIAL_THROW ")
        result = cursor.fetchall()
        return result
