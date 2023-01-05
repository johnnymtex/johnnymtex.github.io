import sqlite3
from typing import Dict, List, Set

import pandas as pd
from dataload import EUProjectData
import json
import numpy as np
import matplotlib.pyplot as plt
import os
def create_path_tree(unique_paths_str:Set[str]):


    unique_paths_lst = list(map(lambda x: x if x[0].strip() != "" else x[1:], map(lambda x:x.split("/"),unique_paths_str)))
    # unique_names = set(sum(unique_paths_lst,[]))
    # unique_words = set(sum(map(lambda x:x.strip().split(),sum(map(lambda x:x.split(","),unique_names ),[])),[] ))


    def fill_dict(base,path):
        if(len(path) > 1):
            next_level = path[0]
            rest_path = path[1:]
            base[next_level] = fill_dict(base.get(next_level,{}),rest_path)
            return base
        elif(len(path) == 1):
            if(path[0] not in base.keys()):
                return base | {path[0]:{}}
            return base
        else:
            raise Exception(path)
    path_dict = {}
    for path in unique_paths_lst:
        path_dict = fill_dict(path_dict,path)
    return path_dict

def path_search_recursive(current_node,current_path=[]):
    level_paths = [current_path + [key] for key in current_node.keys()]
    lower_level_paths = sum([path_search_recursive(current_node[key],current_path + [key]) for key in current_node.keys()],[])
    return level_paths + lower_level_paths
def topic_path_dict(all_paths):
        path_dict = {}
        for path in all_paths:
            if path[-1] in path_dict.keys():
                raise Exception("dup last path")
            path_dict[path[-1]] = path
        return path_dict
    
def distance(topic_a,topic_b,path_lookup,sensitivity = -1,start_distance = 1):
    path_a = path_lookup[topic_a]
    path_b = path_lookup[topic_b]
    distance = start_distance
    search_length = max(len(path_a),len(path_b)) 
    if(sensitivity != -1):
        search_length = max(sensitivity,search_length)
    for i in range( max(len(path_a),len(path_b)) ):
        if(i<len(path_a) and i<len(path_b) and path_a[i] != path_b[i]):
            distance += start_distance/(2**i)
        elif(i>=len(path_a) or i>=len(path_b)):
            distance += start_distance/(2**(i-1))/3
            return distance
    return distance

def distance_dict(topic_list,path_lookup,sensitivity = -1,start_distance = 1):
    d_dict = {}
    for i,topic_a in enumerate(topic_list):
        for ii,topic_b in enumerate(topic_list):
            d_dict[ (topic_a,topic_b)] = distance(topic_a,topic_b,path_lookup,sensitivity=sensitivity,start_distance = start_distance)
    return d_dict

def truncate_path(topic,path_lookup,sensitivity = -1):
    path = path_lookup[topic]
    new_length = len(path) if sensitivity == -1 else min(sensitivity,len(path))

    return "/".join(path[:new_length])


def update_sql_paths(db_con):
    df = pd.read_sql(
    '''SELECT DISTINCT euroSciVocCode,euroSciVocPath,euroSciVocTitle
        FROM euroSciVoc
        ORDER by euroSciVocTitle
    ''',db_con)
    path_dict = create_path_tree(set(df["euroSciVocPath"]))
    all_paths = path_search_recursive(path_dict)
    topic_path = topic_path_dict(all_paths)
    create_clean_topics(db_con,topic_path)

def create_clean_topics(db_con,topic_path_table):
    
    for path_segment in range(7):
        cur = db_con.cursor()
        cur.execute(f'ALTER TABLE euroSciVoc\n ADD COLUMN path{path_segment} TEXT')
        
        db_con.commit()
        case_string = "CASE\n"
        for key,item in topic_path_table.items():
            if(path_segment<len(item)):
                case_string += f'\tWHEN euroSciVocTitle = "{key}" THEN "{item[path_segment]}"\n'
                # print(key,item[path_segment])
        case_string += "ELSE NULL \n END"
        
        update_sql = "UPDATE euroSciVoc\n" +\
        f"SET path{path_segment} = " + case_string
        # print(update_sql)
        cur = db_con.cursor()
        cur.execute(update_sql)
        db_con.commit()



if __name__ == "__main__":
    data = EUProjectData()
    df = data.table_from_query(
    '''SELECT DISTINCT euroSciVocCode,euroSciVocPath,euroSciVocTitle
        FROM euroSciVoc
        ORDER by euroSciVocTitle
    ''')
    path_dict = create_path_tree(set(df["euroSciVocPath"]))
    all_paths = path_search_recursive(path_dict)
    topic_path = topic_path_dict(all_paths)
    distance_lookup = distance_dict(list(set(df["euroSciVocTitle"])),topic_path)

    #how many distinct topics/titles
    print("total topics:",len(set(df["euroSciVocTitle"])))
    #max depth of tree
    print("tree depth:",max(map(lambda x:len(x),all_paths)))

    #display tree part
    print("tree:")
    for top_level,second_level_dict in path_dict.items():
        print(top_level)
        for second_level,third_level_dict in second_level_dict.items():
            print(">",second_level)

    #top level groups
    all_table = data.table_from_query(
    '''SELECT projectID,euroSciVocTitle
        FROM euroSciVoc
        ORDER by euroSciVocTitle
    '''
    )
    top_level_table = all_table.copy()
    top_level_table["trunk_path"] = top_level_table["euroSciVocTitle"].apply(lambda x:truncate_path(x,topic_path,1))
    top_level_table = top_level_table[["trunk_path","projectID"]]
    top_level_table = top_level_table.drop_duplicates()
    top_level_table = top_level_table.groupby(["trunk_path"]).count()
    # all_tables = all_tables.loc[all_tables["projectID"] > 1000]
    plt.title("distribution of project in top level topics")
    plt.pie(top_level_table["projectID"],labels=top_level_table.index)
    plt.savefig(os.path.join("graphs","project_top_level_topics.png"))
    plt.clf()

    biggest_topics = all_table.copy()
    biggest_topics = biggest_topics.groupby(["euroSciVocTitle"]).count()
    biggest_topics = biggest_topics.loc[biggest_topics["projectID"] > 1500]
    
    plt.title("most common base level tags")
    plt.bar(biggest_topics.index,biggest_topics["projectID"])
    plt.xticks(rotation=30)
    plt.savefig(os.path.join("graphs","project_base_level_topics.png"))
    plt.clf()


    engineering = all_table.copy()
    engineering[f"group_a"] = engineering["euroSciVocTitle"].apply(lambda x:truncate_path(x,topic_path,2))
    engineering=engineering.loc[engineering["group_a"] == "engineering and technology/civil engineering"]
    engineering = engineering[["projectID","euroSciVocTitle"]]
    engineering[f"trunk_path"] = engineering["euroSciVocTitle"].apply(lambda x:truncate_path(x,topic_path,7))
    engineering = engineering[["trunk_path","projectID"]]
    engineering = engineering.drop_duplicates()
    engineering = engineering.groupby(["trunk_path"]).count()
    engineering = engineering.reset_index()
    engineering = engineering.sort_values(["projectID"],ascending=False)
    engineering["trunk_path"] = engineering["trunk_path"].apply(lambda x:x.split("/")[-1])
    
    
    
    big_topics = data.table_from_query(
        '''SELECT path0,path1,path2,round(sum(ecMaxContribution))
            FROM euroSciVoc 
            INNER JOIN project on euroSciVoc.projectID = project.id
            GROUP BY path0,path1,path2
            ORDER BY sum(ecMaxContribution) DESC
        ''')
    print("top projects by funding")
    print(big_topics.head(10))
    
    
