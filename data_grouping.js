//data for the grouping structure is here
var group_data;

//makes the tree recursively
// function recursive_list_display(root_path,data){
//     data_arr = items(data);
//     d3.select(root_path).selectAll("li").data(data_arr).text(elm=>elm[0]).attr("class",elm=>elm[0].replaceAll(" ","_")).enter().append("li").text(elm=>elm[0]).attr("class",elm=>elm[0].replaceAll(" ","_"))
//     data_arr.forEach(function(e,i,a) {
//         if(e[1]){
//             document.querySelector(root_path + "> ."+e[0].replaceAll(" ","_")).appendChild(document.createElement("ul"));
//             recursive_list_display(root_path + "> ."+e[0].replaceAll(" ","_")+"> ul",e[1]);
//         }
//     });
// }
// //top level for above recursion
// function display_grouping(){
//     recursive_list_display("#groups",group_data);  
// }

//form the group names get a list of all topics
function recursive_group_collect(remain){
    end = [] 
    items(remain).forEach( (v,i,a)=>{
        end.push(v[0])
        if(v[1]){end = end.concat(recursive_group_collect(v[1]))}
    }
    )
    return end
}








