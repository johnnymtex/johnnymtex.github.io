import pandas as pd
import wget
from zipfile import ZipFile
from io import BytesIO
import os
import sqlite3
from tqdm import tqdm
import json
import gzip
import re
import xml.etree.ElementTree as ET

# URL = "https://cordis.europa.eu/data/cordis-fp7projects-csv.zip"
# response = wget.download(URL,"cordis-fp7projects-csv.zip")
data_source_urls_csv = ["https://cordis.europa.eu/data/cordis-fp7projects-csv.zip",
                    "https://cordis.europa.eu/data/cordis-h2020projects-csv.zip",
                    "https://cordis.europa.eu/data/cordis-HORIZONprojects-csv.zip"]
data_source_urls_xml = [
    "https://cordis.europa.eu/data/cordis-fp7projects-xml.zip",
    "https://cordis.europa.eu/data/cordis-h2020projects-xml.zip",
    "https://cordis.europa.eu/data/cordis-HORIZONprojectDeliverables-xml.zip"
]
data_source_other_stats = {
    "gdp.csv.gz":"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/TEC00001/A.B1GQ.CP_EUR_HAB.EU27_2020+EU28+EA+EA19+BE+BG+CZ+DK+DE+EE+IE+EL+ES+FR+HR+IT+CY+LV+LT+LU+HU+MT+NL+AT+PL+PT+RO+SI+SK+FI+SE+IS+LI+NO+CH+UK+ME+MK+AL+RS+TR+BA+XK/?format=SDMX-CSV&compressed=true&startPeriod=2010&endPeriod=2021",
    "population.csv.gz":"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/TPS00005/A.POPSHARE_EU27_2020.EU27_2020+BE+BG+CZ+DK+DE+EE+IE+EL+ES+FR+HR+IT+CY+LV+LT+LU+HU+MT+NL+AT+PL+PT+RO+SI+SK+FI+SE/?format=SDMX-CSV&compressed=true&startPeriod=2011&endPeriod=2022"
}

data_root = "data"

if not os.path.exists(data_root):
    os.mkdir(data_root)
data_sources_file_names = list(map(os.path.basename,data_source_urls_csv)) 

def download_data():
    new = False
    for url in data_source_urls_csv+data_source_urls_xml:
        file_name = os.path.basename(url)
        if not os.path.exists(os.path.join(data_root,file_name)):
            wget.download(url,os.path.join(data_root,file_name))
            new = True
    #pop_stats
    for stat_name,url in data_source_other_stats.items():
        if not os.path.exists(os.path.join(data_root,stat_name)):
            wget.download(url,os.path.join(data_root,stat_name))
    return new

def clean_up():
    for url in data_source_urls_csv:
        file_name = os.path.basename(url)
        if os.path.exists(os.path.join(data_root,file_name)):
            os.remove(os.path.join(data_root,file_name))
    for stat_name,url in data_source_other_stats.items():
        if os.path.exists(os.path.join(data_root,stat_name)):
            os.remove(os.path.join(data_root,stat_name))

csv_table_cache = None
def csv_table():
    global csv_table_cache
    if(csv_table_cache == None):
        zip_file_contents = {}
        for file_name_zip in data_sources_file_names:
            with ZipFile(os.path.join(data_root,file_name_zip),'r') as f:
                for file_name in f.filelist:

                    df = pd.read_csv(BytesIO(f.read(file_name)),sep=";",low_memory=False)

                    zip_file_contents[(file_name_zip,file_name.filename)] = list(df.columns)
        csv_table_cache = zip_file_contents
    return csv_table_cache

def check_csv():
    zip_file_contents = csv_table()
    #file mismatch
    print("check file mismatch")
    file_mis_match = False
    for i,((zip_fileA,csv_fileA),itemA) in enumerate(zip_file_contents.items()):
        for ii,((zip_fileB,csv_fileB),itemB) in enumerate(zip_file_contents.items()):
            if(i > ii):
                if(zip_fileA!=zip_fileB):
                    if(csv_fileA == csv_fileB):
                        if(set(itemA) != set(itemB)):
                            print(set(itemA).difference(set(itemB)),set(itemB).difference(set(itemA)))
                            file_mis_match = True
    print(f"complete csv check: {'fail' if file_mis_match else 'pass' }")
    folder_mis_match = False
    for i,file_name_zipA in enumerate(data_sources_file_names):
        for ii,file_name_zipB in enumerate(data_sources_file_names):
            if(i > ii):
                a_file_list = set(map(lambda x:x[1],filter(lambda x:x[0] == file_name_zipA,zip_file_contents.keys())))
                b_file_list = set(map(lambda x:x[1],filter(lambda x:x[0] == file_name_zipB,zip_file_contents.keys())))
                if(a_file_list != b_file_list):
                    print(file_name_zipA,file_name_zipB,b_file_list.difference(a_file_list),a_file_list.difference(b_file_list))
                    folder_mis_match = True
    print(f"complete folder check: {'fail' if folder_mis_match else 'pass' }")


def clean_table_name(name):
    return name.replace("csv/","").replace(".csv","").replace(".gz","")
def save_data_table(con,df:pd.DataFrame,table_name): #set up primary key stuff for sql
    key = []
    column_information = json.load(open("column_description.json",'r'))
    for column_name,column_info in column_information[table_name].items():
        if column_info and column_info.find("KEY")>=0:
            key.append(column_name)
    if len(key):
        try:
            df = df.set_index(key,verify_integrity=True)
        except Exception as E: #dump data for debugging
            dups = df[df.duplicated(key,keep=False)]
            if(len(dups.index)):
                dups.to_csv("debug.csv")
                print(table_name)
                print(dups)
                print(len(df.index),len(dups.index))
            raise E
    df.to_sql(clean_table_name(table_name),con)
def load_csv_semi_colon_from_zip(zip_name,file_path): #load via as zip file 
    with ZipFile(zip_name) as z:
        return pd.read_csv(BytesIO(z.read(file_path)),sep=";",low_memory=False)

def load_csv_from_gz(gz_path):
    with gzip.open(gz_path) as g: 
        return pd.read_csv(BytesIO(g.read()))



def load_table(name):
    table_data = csv_table()
    if name in ["csv/webLink_2.csv","csv/webLink.csv"]:
        return load_special_web_link_table()

    if name in set(map(lambda x:x[1],table_data.keys())):
        return load_merge_table(name)
    
    return load_simple_table(name)

def load_special_web_link_table():
    
    merge_targets = []
    for table_name in ["csv/webLink_2.csv","csv/webLink.csv"]: #both files into a single table
        for project_group in set(map(lambda x:x[0],csv_table().keys())):
            try:
                df = load_csv_semi_colon_from_zip(os.path.join("data",project_group),table_name)
                df["data_source"] = f"{project_group}/{table_name}"
                merge_targets.append(df)
            except KeyError:
                pass
    return pd.concat(merge_targets)

def load_merge_table(table_name): 


    merge_targets = []
    for project_group in set(map(lambda x:x[0],csv_table().keys())):
        try:
                df = load_csv_semi_colon_from_zip(os.path.join("data",project_group),table_name)
                df["data_source"] = f"{project_group}/{table_name}"
                merge_targets.append(df)
        except KeyError:
            pass
    return pd.concat(merge_targets)



def auto_clean(df:pd.DataFrame,table_name):
    column_information = json.load(open("column_description.json",'r'))
    df= df.drop_duplicates()
    to_keep = list(df.columns)
    for column_name,column_info in  column_information[table_name].items():
        try:
            if(column_info):
                if(column_info.find(",->.")>= 0):
                    df[column_name] = df[column_name].str.replace(",",".")
                if(column_info.find("DATE") >= 0):
                    df[column_name] = pd.to_datetime(df[column_name])
                if(column_info.find("FLOAT") >= 0):
                    df[column_name] = pd.to_numeric(df[column_name],errors='coerce')
                if(column_info.find("INT") >= 0):
                    df[column_name] = df[column_name].astype("Int64")
                if(column_info.find("BOOL") >= 0):
                    df[column_name] = df[column_name].astype(bool)
                if(column_info.find("DROP") >= 0):
                    to_keep.remove(column_name)
        except Exception as E:
            print("failed",column_name,column_info)
    df = df[to_keep]
    return df

def load_simple_table(name):
    df = load_csv_from_gz(os.path.join(data_root,name))
    df["data_source"] = os.path.join(data_root,name)
    return df

def xml_hash():
    xml_hash_file_to_zip = {}
    for url in data_source_urls_xml:
        path = os.path.join(data_root,os.path.basename(url))
        with ZipFile(path) as z:
            for c_file in z.filelist:
                xml_hash_file_to_zip[c_file.filename] = os.path.basename(url)
    return xml_hash_file_to_zip

class EUProjectData:

    

    def __init__(self) -> None:
        self.con = sqlite3.connect(os.path.join("data","all_data.db"))
        self.xml_hash_table = xml_hash()


    def table_from_query(self,sql):
        return pd.read_sql_query(sql,self.con)
    
    def table_from_table(self,table_name):
        return pd.read_sql_query(f"select * from {table_name}",self.con)
        
    def xml_from_many_rnc(self,rcns,functions = [lambda x:x]):
        rcn_lookup = re.compile(f".*({'|'.join(rcns)}).*") #danger unchecked
        file_names = list(filter(lambda x:x != None,map(lambda x:rcn_lookup.match(x),self.xml_hash_table.keys())))
        num_to_name = {}
        for file_name in file_names:
            num_to_name[file_name.group(1)] = file_name.group(0)
        end = [[] for _ in functions]
        for rcn in rcns:
            try:
                file_name = num_to_name[rcn]
                zip_name = self.xml_hash_table[file_name]
                with ZipFile(os.path.join(data_root,zip_name)) as z:
                    tree = ET.parse(BytesIO(z.read(file_name)))
                    for i,fun in enumerate(functions):
                        try:
                            end[i].append(fun(tree))
                        except Exception as E:
                            end[i].append(str(E))
            except KeyError as E:
                for i,fun in enumerate(functions):
                    end[i].append(None)
        return end


    def xml_from_rcn(self,rcn):
        rcn_lookup = re.compile(f".*{rcn}.*") #danger unchecked
        file_names = list(filter(lambda x:x != None,map(lambda x:rcn_lookup.match(x),self.xml_hash_table.keys())))

        if(len(file_names) != 1):
            raise Exception("multiple files returned")
        with ZipFile(os.path.join(data_root,self.xml_hash_table[file_names[0].group(0)])) as z:
            return ET.parse(BytesIO(z.read(file_names[0].group(0))))


    
    def close(self):
        self.con.close()

if __name__ == "__main__":
    from topicVariation import update_sql_paths
    if(not os.path.exists(os.path.join(data_root,"all_data.db"))):
        if(download_data()):
            check_csv()
        con = sqlite3.connect(os.path.join("data","all_data.db"))

        all_tables = list(filter(lambda x:x!="csv/webLink_2.csv",set(map(lambda x: x[1],csv_table().keys())))) + list(set(data_source_other_stats.keys()))

    
        for table_name in tqdm(all_tables,desc="loading & cleaning tables"):
            df = load_table(table_name)
            df = auto_clean(df,table_name)

            if(table_name == "csv/organization.csv"): #remove one bad entry?
                df = df.loc[~(df["rcn"] == "xxxxxxx")]

            save_data_table(con,df,table_name)

        cur = con.cursor() #some indexes to improve performance
        cur.execute('''CREATE INDEX "euroSciVocPid" ON "euroSciVoc" ("projectID");''')
        cur.execute('''CREATE INDEX "projectPid" ON "project" ("id");''')
        cur.execute('''CREATE INDEX "organizationPid" ON "organization" ("projectID");''')
        cur.execute('''CREATE INDEX "organizationid" ON "organization" ("organisationID");''')


        con.commit()
        #euroSciVoc split path data
        update_sql_paths(con)

        #update project status to normalize across data files
        cur.execute(
        '''UPDATE project
            set status = CASE 
                WHEN status = "ONG" THEN "SIGNED"
                WHEN status = "CLO" THEN "CLOSED"
                WHEN status = "CAN" THEN "TERMINATED"
            END
            WHERE status in ("ONG","CAN","CLO")
        ''')
        con.commit()

        #group funding table
        #inclusive sum of sub groups
        #uses all projects including incomplete and terminated
        #shows max ec contribution
        cur.execute(
            '''CREATE VIEW group_funding as 
                WITH project_topic as(
                select path0,path1,path2,path3,path4,path5,project.ecMaxContribution,project.status
                FROM euroSciVoc
                INNER JOIN project ON euroSciVoc.projectID=project.id
                )
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,"" as "path1","" as "path2","" as "path3","" as "path4","" as "path5"
                FROM project_topic
                GROUP BY path0,status
                UNION
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,path1,"" as "path2","" as "path3","" as "path4","" as "path5"
                FROM project_topic
                WHERE path1 IS NOT NULL
                GROUP BY path0,path1,status
                UNION
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,path1,path2,"" as "path3","" as "path4","" as "path5"
                FROM project_topic
                WHERE path1 IS NOT NULL AND path2 IS NOT NULL
                GROUP BY path0,path1,path2,status
                UNION
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,path1,path2,path3,"" as "path4","" as "path5"
                FROM project_topic
                WHERE path1 IS NOT NULL AND path2 IS NOT NULL AND path3 IS NOT NULL
                GROUP BY path0,path1,path2,path3,status
                UNION
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,path1,path2,path3,path4,"" as "path5"
                FROM project_topic
                WHERE path1 IS NOT NULL AND path2 IS NOT NULL AND path3 IS NOT NULL AND path4 IS NOT NULL
                GROUP BY path0,path1,path2,path3,path4,status
                UNION
                SELECT SUM(project_topic.ecMaxContribution) as max_contribution,status,path0,path1,path2,path3,path4,path5
                FROM project_topic
                WHERE path1 IS NOT NULL AND path2 IS NOT NULL AND path3 IS NOT NULL AND path4 IS NOT NULL  AND path5 IS NOT NULL
                GROUP BY path0,path1,path2,path3,path4,path5,status
            ''')
        con.commit()
        #create a table of monthly time periods for over time grouping
        #periods are numbered from with an period and a start and end date inclusive on one end along with a day count
        cur.execute(
        '''CREATE VIEW TIME_PERIODS as 
            WITH DATE_PERIOD_EDGES as(
                SELECT row_number() over (order by '') as i, 
                    DATE("20"||CASE WHEN year_num < 10 THEN "0"||year_num ELSE year_num END ||"-"||
                    CASE WHEN month_num < 10 THEN ("0"||month_num) ELSE month_num END||"-01") as date_str
                FROM (
                    WITH RECURSIVE Numbers as (
                        SELECT 0 as Number
                        UNION ALL
                        SELECT Number + 1
                        FROM Numbers
                        WHERE Number < 30
                    )
                    SELECT month_num.Number as month_num, year_num.Number as year_num
                    FROM Numbers as month_num
                    CROSS JOIN Numbers as year_num
                    WHERE year_num >= 6 AND year_num < 30 AND month_num > 0 and month_num <= 12
                    ORDER BY year_num,month_num
                )
            )
            select start_date.i as period,start_date.date_str as start_date,end_date.date_str as end_date, julianday(end_date.date_str)-julianday(start_date.date_str) as days
            FROM DATE_PERIOD_EDGES as start_date
            INNER JOIN DATE_PERIOD_EDGES as end_date ON start_date.i+1 == end_date.i
        ''')
        con.commit()

        #this is a over time funding table
        #calculates 
        cur.execute(
            '''CREATE VIEW monthly_group_funding AS
                SELECT period,SUM(daily_contribution*overlap_days) as "contribution",status,path0,path1,path2,path3,path4,path5,path6
                FROM (
                    SELECT time_periods.period,time_periods.start_date,time_periods.end_date,project.id,project.status,project.title,project.startDate,project.endDate,project.ecMaxContribution,project.ecMaxContribution/(julianday(project.endDate)-julianday(project.startDate)) as "daily_contribution",project_codes.*,
                    CASE 
                        WHEN project.startDate < time_periods.start_date AND project.endDate > time_periods.end_date THEN time_periods.days
                        WHEN project.startDate > time_periods.start_date AND project.endDate > time_periods.end_date THEN julianday(time_periods.end_date) - julianday(project.startDate)
                        WHEN project.startDate < time_periods.start_date AND project.endDate < time_periods.end_date THEN julianday(project.endDate) - julianday(time_periods.start_date)
                        WHEN project.startDate > time_periods.start_date AND project.endDate < time_periods.end_date THEN julianday(project.endDate) - julianday(project.startDate)
                    END as "overlap_days"
                    FROM project
                    INNER JOIN (
                        SELECT projectID,path0,path1,path2,path3,path4,path5,path6
                        FROM euroSciVoc
                        ) 
                    as project_codes on project_codes.projectID = project.id
                    INNER JOIN (
                        SELECT * 
                        FROM TIME_PERIODS) 
                    as "time_periods" ON NOT (time_periods.start_date > project.endDate OR time_periods.end_date < project.startDate)
                )
                GROUP BY period,status,path0,path1,path2,path3,path4,path5,path6
        ''')
        con.commit()
        cur.execute(
        '''CREATE TABLE monthly_group_funding_cache(
            period INTEGER,
            contribution NUMERIC,
            status TEXT,
            path0 TEXT,
            path1 TEXT,
            path2 TEXT,
            path3 TEXT,
            path4 TEXT,
            path5 TEXT,
            path6 TEXT
            );
        ''')
        cur.execute(
        '''
            INSERT INTO monthly_group_funding_cache
            SELECT *
            FROM monthly_group_funding
            ''')
        con.commit()

        con.close()
        # if True:
        #     clean_up()

    
    #simple management class
    eu = EUProjectData()

    #from a query
    df = eu.table_from_query('''select * from "project" where nature NOT NULL''')
    print(df.head())
    #just the whole table
    df = eu.table_from_table("project")
    print(df.head())

    #fetching xml trees in bulk
    print(eu.xml_from_many_rnc(["872135","872135","872df5"],[lambda x:x.find("title").text]))
    print(eu.xml_from_rcn(str(872135)).find("title").text)

    #sql queries examples

    #what projects have what sci codes (204115 rows)
    #each row is a project->code relation 
    df = eu.table_from_query(
    '''SELECT *
        FROM project
        INNER JOIN euroSciVoc ON euroSciVoc.projectID = project.id
        ORDER BY project.id
    ''')
    print(df.head())

    #what organizations are involved with what projects (344226 rows)
    #each row is a project->organizations relation 
    df = eu.table_from_query(
    '''SELECT *
        FROM project
        INNER JOIN organization ON organization.projectID = project.id
        ORDER BY project.id
    ''')
    print(df.head())


    #what organizations are involved with what topics/codes (1029609 rows)
    #each row is a organizations->codes relation 
    df = eu.table_from_query(
    '''SELECT *
        FROM organization
        INNER JOIN euroSciVoc ON euroSciVoc.projectID = organization.projectID
        ORDER BY organization.organisationID NULLS LAST
    ''')
    print(df.head())

    #what organizations are involved with what topics(second table)(65840 rows)
    #each row is a organizations->codes relation 
    df = eu.table_from_query(
    '''SELECT * 
        FROM project
        INNER JOIN topics ON topics.projectID = project.id
        ORDER BY topics.topic
    ''')
    print(df.head())
    

