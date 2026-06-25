from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query =  """select *
                    from genre g """

        cursor.execute(query )

        for row in cursor:
            results.append(row["Name"])

        cursor.close()
        conn.close()
        return results
