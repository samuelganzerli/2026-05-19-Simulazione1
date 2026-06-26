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

    @staticmethod
    def getAllNodes(genre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId, a.Name  
                    from artist a, album al, track t, genre g  
                    where t.GenreId = g.GenreId  
                    and a.ArtistId=al.ArtistId 
                    and al.AlbumId = t.AlbumId 
                    and g.Name = %s """

        cursor.execute(query, (genre,))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarita(genre):
        conn = DBConnect.get_connection()
        results = {}
        cursor = conn.cursor(dictionary=True)
        query = """ select al.ArtistId, sum(il.Quantity) as popolarita
                    from album al, track t, invoiceline il, genre g
                    where al.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and t.GenreId = g.GenreId
                    and g.Name = %s
                    group by al.ArtistId """
        cursor.execute(query, (genre,))
        for row in cursor:
            results[row["ArtistId"]] = int(row["popolarita"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(genre):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct al1.ArtistId as artistaA, al2.ArtistId as artistaB
                    from invoice i1, invoiceline il1, track t1, album al1, genre g1,
                         invoice i2, invoiceline il2, track t2, album al2, genre g2
                    where i1.InvoiceId = il1.InvoiceId
                    and il1.TrackId = t1.TrackId
                    and t1.AlbumId = al1.AlbumId
                    and t1.GenreId = g1.GenreId
                    and g1.Name = %s
                    and i1.CustomerId = i2.CustomerId
                    and i2.InvoiceId = il2.InvoiceId
                    and il2.TrackId = t2.TrackId
                    and t2.AlbumId = al2.AlbumId
                    and t2.GenreId = g2.GenreId
                    and g2.Name = %s
                    and al1.ArtistId < al2.ArtistId """
        cursor.execute(query, (genre, genre))
        for row in cursor:
            results.append((row["artistaA"], row["artistaB"]))
        cursor.close()
        conn.close()
        return results

