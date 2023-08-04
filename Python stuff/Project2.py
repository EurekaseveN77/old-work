#James Carton
#April 16th, 2023
import argparse
import os
import mysql.connector
import getpass
import datetime



def main():
    import csv
    parser = argparse.ArgumentParser(description='Process Baselight and Xytech files.')
    parser.add_argument('--baselight_files', nargs='+', help='List of Baselight files', required=True)
    parser.add_argument('--xytech', help='Xytech file', required=True)
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output')
    parser.add_argument('--csv', action='store_true', help='Print results to a CSV file')
    #parser.add_argument('--db', action='store_true', help='Print results to the database')
    
    
    args = parser.parse_args()
    xytech_file_location = os.path.join('/Users', 'jmscr', 'OneDrive', 'Desktop', 'import_files', args.xytech)
    xytech_folders = []
    with open(xytech_file_location, 'r') as read_xytech_file:
        for line in read_xytech_file:
            if "/" in line:
                xytech_folders.append(line.strip())
    mydb = mysql.connector.connect(
        host="localhost",
        user="sqluser",
        password="93021",
        database="mydatabase"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS frames (name VARCHAR(255), date VARCHAR(255), folder VARCHAR(255), frame_range VARCHAR(255))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS user_info (user VARCHAR(255), machine VARCHAR(255), name VARCHAR(255), date VARCHAR(255), submitted_date VARCHAR(255))")
    user = getpass.getuser()
    machine = os.environ['COMPUTERNAME'][1]
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    


    
    for baselight_file in args.baselight_files:
        baselight_file_location = os.path.join('/Users', 'jmscr', 'OneDrive', 'Desktop', 'import_files', baselight_file)
        with open(baselight_file_location, 'r') as read_baselight_file:
            for line in read_baselight_file:
                line_parse = line.split(" ")
                folder_location = line_parse.pop(0)  
                if folder_location == ("/net/flame-archive"):
                    folder_location = line_parse.pop(0)
                sub_folder = folder_location.replace("/images1/Avatar", "")
                sub_folder = sub_folder.replace("Avatar", "")
                new_location = ""
                for xytech_line in xytech_folders:
                    if sub_folder in xytech_line:
                        new_location = xytech_line
                frame_ranges = []
                first = ""
                last = ""
                for numeral in line_parse:
                    if not numeral.strip().isnumeric():
                        continue
                    if first == "":
                        first = int(numeral)
                        last = int(numeral)
                        continue
                    if int(numeral) == (last+1):
                        last = int(numeral)
                    else:
                        if first == last:
                            frame_ranges.append(str(first))
                        else:
                            frame_ranges.append(str(first) + "-" + str(last))
                        first = int(numeral)
                        last = int(numeral)
                if first != "":
                    if first == last:
                        frame_ranges.append(str(first))
                    else:
                        frame_ranges.append(str(first) + "-" + str(last))
                if frame_ranges:
                    for frame_range in frame_ranges:
                        txt_file_parts = os.path.splitext(os.path.basename(baselight_file_location))[0].split("_")
                        machine = txt_file_parts[0]
                        name = txt_file_parts[1]
                        date = txt_file_parts[2]
                        folder = new_location.split()[-1] if new_location else folder_location
                        row = (name, date, folder, frame_range)
                        mycursor.execute("INSERT INTO frames (name, date, folder, frame_range) VALUES (%s, %s, %s, %s)", row)
                        mydb.commit()
                        
                       
                        user = os.getlogin()  
                        submitted_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                        row2 = (user, machine, name, date, submitted_date)
                        mycursor.execute("INSERT INTO user_info (user, machine, name, date, submitted_date) VALUES (%s, %s, %s, %s, %s)", row2)
                        mydb.commit()
        if args.verbose:
            print(f'Finished processing files {baselight_file_location}')

    #mycursor.close()
    #mydb.close()

    if args.csv:
        import csv
        with open('output.csv', mode='w') as output_file:
            writer = csv.writer(output_file)

            with open(xytech_file_location, 'r') as f:
                xytech_lines = f.readlines()
                producer = None
                operator = None
                job = None
                notes = None
                
                for line in xytech_lines:
                    if "Producer:" in line:
                        producer = line.split(":")[-1].strip()
                    elif "Operator:" in line:
                        operator = line.split(":")[-1].strip()
                    elif "Job:" in line:
                        job = line.split(":")[-1].strip()
                    elif "Notes:" in line:
                        notes = xytech_lines[xytech_lines.index(line)+1].strip()
                        
                output_string = f"Producer:{producer} / Operator:{operator} / Job:{job} / Notes:{notes} /"
                writer.writerow([output_string])
            
            output_file.write('\n\n') 
            mycursor = mydb.cursor()
            mycursor.execute("SELECT folder, frame_range FROM frames")
            rows = mycursor.fetchall()
            for row in rows:
                folder = row[0]
                frame_range = row[1]
                output_str = f"{folder} / {frame_range}"
                writer.writerow([output_str])
            mycursor.close()

    mycursor.close()
    mydb.close()
if __name__ == '__main__':
    main()

