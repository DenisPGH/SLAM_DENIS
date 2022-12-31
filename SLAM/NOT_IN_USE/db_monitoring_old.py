
import sqlite3

from SLAM.Monitoring.db_monitoring import DBInfoROBO


class DBMonitoring:
    def __init__(self):
        self.robo_db=DBInfoROBO()
        #self.con = sqlite3.connect(f'{self.robo_db.DB()}')
        self.con = sqlite3.connect('../Monitoring/map.db')
        self.cur = self.con.cursor()

    def return_all_coord_for_a_node(self, node_id):
        """
        :param node_id: node_id
        :return: list with tuple(x,y), all coordinates for this node
        """
        result = ''
        self.cur.execute(f"select x,y from coordinates where id={node_id}")
        result = self.cur.fetchall()
        # self.con.close()
        return result

    def all_nodes_names(self):
        """
        :return: the list with all nodes names
        """
        self.cur.execute(f"select id_node from node")
        res = self.cur.fetchall()
        res=[x[0] for x in res]
        return res

    def close(self):
        """
        close connection to the DB IMPORTANT
        """
        self.con.close()

    def return_own_coord_of_node(self, node_id):
        """
        :param node_id: name node
        :return: tuple(x,y) of the node
        """
        result = (0, 0)
        self.cur.execute(f"select x,y from node where id_node={node_id}")
        self.con.commit()
        result = self.cur.fetchall()
        return result















