from database.DB_connect import DBConnect
from model.attori import Attori


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def allObjectDD():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ select distinct genre
                         from genre g """
        cursor.execute(query)
        for row in cursor:
            result.append(row["genre"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allNodes(genere):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT distinct n.id , n.name ,n.height , n.date_of_birth , n.known_for_movies 
                    from names n 
                    join role_mapping rm on rm.name_id = n.id 
                    join movie m on m.id = rm.movie_id 
                    join genre g on m.id =g.movie_id 
                    where g.genre = %s """
        cursor.execute(query, (genere,))
        for row in cursor:
            result.append(Attori(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def allPossibleEdges():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """ SELECT v1.name_id as idAttore1, v2.name_id as idAttore2, count(*) as peso
                    from (SELECT rm.name_id , m.id 
                            FROM movie m 
                            join role_mapping rm on m.id =rm.movie_id ) v1
                    join (SELECT rm2.name_id , m2.id 
                            FROM movie m2 
                            join role_mapping rm2 on m2.id =rm2.movie_id ) v2
                    on v1.id= v2.id
                    where v1.name_id<v2.name_id
                    GROUP BY idAttore1, idAttore2"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["idAttore1"], row["idAttore2"], row["peso"]))
        cursor.close()
        conn.close()
        return result