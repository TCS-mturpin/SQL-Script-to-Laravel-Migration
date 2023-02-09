import re
import tkinter as tk
from tkinter import filedialog
import os
import datetime
import chardet


def sql_to_laravel(sql_script):
    # Remove comments from the SQL script
    sql_script = re.sub(r"--.*\n", "", sql_script)
    # Split the script into individual lines
    lines = sql_script.split("\n")
    # Initialize variables to store the table name and columns
    table_name = ""
    columns = []
    # Loop through each line of the SQL script
    for line in lines:
        # If the line starts with "CREATE TABLE", extract the table name
        if line.startswith("CREATE TABLE"):
            table_name = line.split(" ")[2].strip("[]")
            table_name = table_name[:-1]
            table_name = table_name[:-1]

        # If the line starts with "[", extract the column name and type
        if line.startswith("	"):
            line.replace("	","")
            column_name = line.split("]")[0]
            column_name = column_name[1:]
            column_name = column_name[1:]
            column_type = line.split("]")[1][1:]
            column_type = column_type[1:]
            # Convert the column type to Laravel syntax
            if column_type == "int":
                column_type = "integer"
            elif column_type == "varchar":
                column_type = "string"
            elif column_type == "nvarchar":
                column_type = "string"
            elif column_type == "char":
                column_type = "string"
            elif column_type == "datetime2":
                column_type = "dateTime"
            elif column_type == "bigint":
                column_type = "bigInteger"
            elif column_type == "binary":
                column_type = "binary"
            elif column_type == "bit":
                column_type = "boolean"
            elif column_type == "char":
                column_type = "char"
            elif column_type == "datetime":
                column_type = "dateTime"
            elif column_type == "datetime2":
                column_type = "dateTime"
            elif column_type == "datetimeoffset":
                column_type = "dateTime"
            elif column_type == "decimal":
                column_type = "decimal"
            elif column_type == "float":
                column_type = "float"
            elif column_type == "int":
                column_type = "integer"
            elif column_type == "money":
                column_type = "decimal"
            elif column_type == "nchar":
                column_type = "char"
            elif column_type == "nvarchar":
                column_type = "string"
            elif column_type == "real":
                column_type = "float"
            elif column_type == "smallint":
                column_type = "smallInteger"
            elif column_type == "sql_variant":
                column_type = "text"
            elif column_type == "sysname":
                column_type = "string"
            elif column_type == "timestamp":
                column_type = "timestamp"
            elif column_type == "tinyint":
                column_type = "tinyInteger"
            elif column_type == "uniqueidentifier":
                column_type = "uuid"
            elif column_type == "varbinary":
                column_type = "binary"
            elif column_type == "varchar":
                column_type = "string"
            else:
                column_type = "unknown"
            # Add the column to the list of columns
            if column_type != "unknown":
                columns.append(f"\n\t\t\t\t\t$table->{column_type}('{column_name}');")
        # Generate the Laravel migration script
        laravel_script = f"""
        <?php
        use Illuminate\\Support\\Facades\\Schema;
        use Illuminate\\Database\\Schema\\Blueprint;
        use Illuminate\\Database\\Migrations\\Migration;

       return new class extends Migration
       {{
            public function up()
            {{
                Schema::create('{table_name}', function (Blueprint $table) {{
        {''.join(columns)}
                }});
            }}

            public function down()
            {{
                Schema::dropIfExists('{table_name}');
            }}
        }};
            """


        today = datetime.datetime.now()
        date_string = today.strftime("%Y_%m_%d_create_")

        current_path = os.getcwd()
        migrationName = date_string + table_name
        print(table_name)
    with open(current_path+"\\migrations\\"+migrationName+".php", "w") as new_file:
        new_file.write(laravel_script)
    return laravel_script


def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read())
    return result['encoding']


if __name__ == '__main__':
    # Example usage
    # prompt user file
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory()
    for filename in os.listdir(folder_path):

        print(folder_path+"/"+filename)
        encoding = detect_encoding(folder_path+"//"+filename)

        try:
            with open(folder_path+"/"+filename, "r", encoding=encoding) as file:
                contents = file.read()
        except FileNotFoundError:
            continue

        today = datetime.datetime.now()
        date_string = today.strftime("%Y_%m_%d_")
        contents = contents.replace("[dbo].", "")
        print(contents)
        laravel_script = sql_to_laravel(contents)




