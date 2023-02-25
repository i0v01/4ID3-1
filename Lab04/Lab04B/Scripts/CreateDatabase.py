import mysql.connector
from mysql.connector import Error
from Config import HOST_IP, USER, PASSWORD, GROUP_NAME, DEVICE_ID



try:
    connection = mysql.connector.connect(host=HOST_IP,
                                         user=USER,
                                         password=PASSWORD)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        try:
            cursor.execute(f"DROP DATABASE {GROUP_NAME}")
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
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{GROUP_NAME}` DEFAULT CHARACTER SET utf8;")
            cursor.close() 
            connection.commit()
            print("Created Database")
        except Error as e:
            print(e)


        connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=GROUP_NAME)
        
        print("Connected to database")

        #cursor.execute(f"USE `{DB_NAME}`;")
        try:
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`;")
            cursor.close() 
            print("Dropped table")
        except Error as e:
            print("Failed to drop table", e)

        try:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{GROUP_NAME}`.`{DEVICE_ID}`
                    (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT, 
                    `Timestamp` VARCHAR(45) NOT NULL,
                    `Sensor` VARCHAR(45) NOT NULL,
                    `Reading` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
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
                                            database=GROUP_NAME)

        try:  
            cursor = connection.cursor()  
            cursor.execute(f"""INSERT INTO `{GROUP_NAME}`.`{DEVICE_ID}` (`Timestamp`, `Sensor`, `Reading`) 
                    VALUES ('Test', 'Test', 'Test'); """)
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
                                            database=GROUP_NAME)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM `{GROUP_NAME}`.`{DEVICE_ID}`;")
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