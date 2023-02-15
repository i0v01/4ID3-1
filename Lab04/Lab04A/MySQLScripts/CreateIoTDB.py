import mysql.connector
from mysql.connector import Error

HOST_IP = "localhost"
USER = "root"
PASSWORD = "9055259140"
DB_NAME = "iot"
TABLE_NAME = "data"


try:
    connection = mysql.connector.connect(host=HOST_IP,
                                         user=USER,
                                         password=PASSWORD)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        try:
            cursor.execute(f"DROP DATABASE {DB_NAME}")
            print("Database dropped successfully")
            cursor.close() 
                

        except Error as e:
            print(e)

        try:
            cursor = connection.cursor()

            cursor.execute("SHOW DATABASES;")
            for x in cursor:
                print(f"   -> {x}")

            cursor.close()
            
            cursor = connection.cursor()
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8;")
            cursor.close() 
            connection.commit()
            print("Created Database")
        except Error as e:
            print(e)


        connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DB_NAME)
        
        print("Connected to database")

        #cursor.execute(f"USE `{DB_NAME}`;")
        try:
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS `{DB_NAME}`.`{TABLE_NAME}`;")
            cursor.close() 
            print("Dropped table")
        except Error as e:
            print("Failed to drop table", e)

        try:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{DB_NAME}`.`{TABLE_NAME}`
                    (`iddata` INT UNSIGNED NOT NULL AUTO_INCREMENT, `DeviceName` VARCHAR(45) NOT NULL,
                    `SensorName` VARCHAR(45) NOT NULL,
                    `SensorValue` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`iddata`),
                    UNIQUE INDEX `iddata_UNIQUE` (`iddata` ASC) VISIBLE)
                    ENGINE = InnoDB;
                    SET SQL_MODE=@OLD_SQL_MODE;
                    SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
                    SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS; """)

            print("Created table")
            print(cursor.fetchall())
            cursor.close() 
            
            
        except Error as e:
            print("Failed to create table", e)

        connection.close()
        connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DB_NAME)

        try:  
            cursor = connection.cursor()  
            cursor.execute(f"""INSERT INTO `{TABLE_NAME}` (`DeviceName`, `SensorName`, `SensorValue`) 
                    VALUES ('TestDevice', 'TestSensor', '22.4'); """)
            print("Inserted into table")
            res = cursor.fetchall()
            print(res)
            cursor.close() 
            connection.commit()
            
        except:
            print("Failed to insert into table")


        try:
            connection.close()
            connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DB_NAME)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM `{DB_NAME}`.`{TABLE_NAME}`;")
            table = cursor.fetchall()
            for row in table:
                print(f" [ {row} ] \n")

            print("Selected data from table")
            cursor.close()
            connection.commit()

        except Error as e:
            print("Failed to read table", e)




except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")