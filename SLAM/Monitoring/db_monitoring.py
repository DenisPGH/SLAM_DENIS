import sqlite3

import paramiko

class DBInfoROBO:
    def __init__(self):
        self.robo_database= "/home/nanorobo/Desktop/Robo/map.db"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect("192.168.1.118", 22, username='nanorobo', password='D_12-K9', timeout=4)
        self.sftp = self.ssh.open_sftp()

    def all_nodes_names_r(self):
        """
        :return: the list with all nodes names
        get remotly the all names of nodes
        :return: list with all names of the all nodes
        """
        ssh_stdin, ssh_stdout, ssh_stderr = \
            self.ssh.exec_command(f"sqlite3 {self.robo_database} 'select id_node from node'")
        stdout = ssh_stdout.readlines()
        stdout=[x.strip('\n') for x in stdout]
        return stdout

    def return_all_coord_for_a_node_r(self, node_id):
        """
        :param node_id: node_id
        :return: list with tuple(x,y), all coordinates for this node
        """
        ssh_stdin, ssh_stdout, ssh_stderr = \
            self.ssh.exec_command(f"sqlite3 {self.robo_database} 'select x,y from coordinates where id={node_id}'")
        stdout = ssh_stdout.readlines() # strip \n
        stdout=[(float(x.split('|')[0]),float(x.split('|')[1].strip('\n'))) for x in stdout]
        return stdout

    def return_own_coord_of_node_r(self, node_id):
        """
        :param node_id: name node
        :return: tuple(x,y) of the node
        """
        result = (0, 0)
        ssh_stdin, ssh_stdout, ssh_stderr = \
            self.ssh.exec_command(f"sqlite3 {self.robo_database} 'select x,y from node where id_node={node_id}'")
        stdout = ssh_stdout.readlines()  # strip \n
        stdout = [(float(x.split('|')[0]), float(x.split('|')[1].strip('\n'))) for x in stdout]
        return stdout










