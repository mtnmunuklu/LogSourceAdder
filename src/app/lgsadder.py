from src.config import Config
import logging
from src.app.logger import Logger
import mysql.connector
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

class LGSAdder:
    """
    Adds log sources based on reference log sources.
    """

    def __init__(self):
        """
        Constructer function.
        Gets some information from config file.
        :return: None.
        """
        self.database_server_ip = Config.DATABASE_SERVER_IP
        self.database_name = Config.DATABASE_NAME
        self.database_username = Config.DATABASE_USERNAME
        self.database_password = Config.DATABASE_PASSWORD
        self.log_sources = Config.LOG_SOURCES
        self.logger = Logger('LGSAdder')

    def add_lgses(self):
        """
        Adds new log sources.
        :return: None. 
        """
        lgses = self.read_lgses_from_file()
        connection = self.connect_to_database()
        last_lgsid = int(self.get_last_lgsid(connection)) + 1
        for lgs in lgses:
            rf_lgs = self.get_lgs_data(connection, lgs[5])
            tree = ET.fromstring(rf_lgs.encode('utf-8'))
            root = tree.getchildren()
            for childies in root:
                if (childies.tag == "LSource"):
                    for child in childies:
                        if (child.tag == "LogSource"):
                            child.attrib['ID'] = str(last_lgsid) # Log Source ID
                            child.attrib['OldID'] = str(last_lgsid) # Log Source ID
                            child.attrib['Name'] = lgs[0] # Log Source Name
                            child.attrib['Path'] = lgs[2] # File Path
                            child.attrib['FileName'] = lgs[3] # File Name
                            child.attrib['FileNameFormat'] = lgs[4] # File Name Format
                            for subchildies in child:
                                if (subchildies.tag == "SSHConfig"):
                                    subchildies.attrib['Host'] = lgs[1] # SSH Host
                elif (childies.tag == "PList"):
                    for child in childies:
                        if (child.tag == "Plugin"):
                            child.attrib['ID'] = str(last_lgsid) # Plugin ID
                            child.attrib['LogSourceID'] = str(last_lgsid) # Log Source ID
                            child.set('RefPluginID', lgs[6]) # Reference Plugin ID
                            child.set('RefPluginName', str(child.attrib['Name']))# Reference Plugin Name
                            child.attrib['Name'] = lgs[0] # Log Source Name
                            for subchildies in child:
                              if (subchildies.tag == "Expressions"):
                                subchildies.clear() 
           
            data = ET.tostring(tree, encoding='utf8', method='xml').decode().replace("\'","\"").replace("utf8","utf-8")
            self.add_lgs_to_database(connection, data, last_lgsid)
            last_lgsid+=1
        connection.close()
        # Convert xml tree to string

    def read_lgses_from_file(self):
        """
        Reads information about log sources from csv file.
        :return: All lines in the csv file. 
        """
        try:
            rows = []
            with open(self.log_sources, mode ='r') as file:
                # Reading the CSV file
                reader = csv.reader(file)
                # Displaying the contents of the CSV file
                next(reader)
                for row in reader:
                    rows.append(row)
            return rows
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while reading from file")
            self.logger.log(logging.ERROR, e)

    def connect_to_database(self):
        """
        Connects to database.
        :return: Database connection.
        """
        try:
            connection = mysql.connector.connect(host=self.database_server_ip, 
                                                database=self.database_name,
                                                user=self.database_username, 
                                                password=self.database_password)
            if connection.is_connected():
                self.logger.log(logging.INFO, "Connected to MySQL Server")
                return connection
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while connecting to MySQL")
            self.logger.log(logging.ERROR, e)

    def get_lgs_data(self, connection, lgs_id):
        """
        Gets log source xml data from database.
        :param connection: Database connection.
        :param lgs_id: Log source id
        :return: XML data.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cc_store WHERE NAME = '"+ lgs_id +"' AND STORETYPE='CONF_PLG_LGS'")
            record = cursor.fetchone()
            cursor.close()
            return record[4]
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while getting reference log source")
            self.logger.log(logging.ERROR, e)

    def get_last_lgsid(self, connection):
        """
        Gets last log source id from database.
        :param connection: Database connection.
        :return: Last log source id.
        """
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cc_store where NAME = 'MAIN' AND STORETYPE = 'CONF_PLG_MAIN'")
            record = cursor.fetchone()
            last_lgsid = self.get_attribute_from_xml(record[4], "LastID")
            cursor.close()
            return last_lgsid
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while getting last lgsid")
            self.logger.log(logging.ERROR, e)

    def get_attribute_from_xml(self, xml, attribute):
        """
        Gets attribute value from xml tree.
        :param xml: XML tree.
        :param attribute: Attribute name in xml tree.
        :return: XML attribute value.
        """
        try:
            tree = ET.fromstring(xml)
            return tree.attrib[attribute]
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while getting attribute from XML")
            self.logger.log(logging.ERROR, e)

    def add_lgs_to_database(self, connection, data, name):
        """
        Adds log source to database.
        :param connection: Database connection.
        :param data: Log source xml data.
        :param name: Log source id.
        :return: None.
        """
        try:
            enterdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = connection.cursor()
            sql_query = """INSERT INTO cc_store (NAME, STORETYPE, ISSYSTEM, DATA, ENTERDATE, DESCRIPTION, VIEWRIGHT, EDITRIGHT, ISDELETED) 
                           VALUES 
                           ({}, 'CONF_PLG_LGS', 0, '{}', '{}', NULL, NULL, NULL, NULL)""".format(name, data, enterdate)
            cursor.execute(sql_query)
            connection.commit()
            cursor.close()
        except Exception as e:
            self.logger.log(logging.WARNING, "Error while adding log source to database")
            self.logger.log(logging.ERROR, e)