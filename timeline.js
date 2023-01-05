function timeline(input_event_data,fill_artical,hide_artical,item_count=5,y_pos=500){
    // console.log("input_event_data")
    // console.log(input_event_data)
    event_data = input_event_data.map(
        elm=>{
            elm["Date"] = new Date(elm["Date"])
            return elm
        }
    )

// event_data = [
//     {
//         "name":"event a",
//         "date":new Date("1-1-2016"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
//         "link":"www.google.com"
//     },
//     {
//         "name":"event B long",
//         "date":new Date("4-4-2018"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vehicula ipsum a arcu cursus vitae. Tempor commodo ullamcorper a lacus vestibulum sed arcu non odio. Odio eu feugiat pretium nibh ipsum consequat nisl vel. Dui ut ornare lectus sit amet est placerat. Gravida cum sociis natoque penatibus et magnis dis parturient montes. Sit amet nulla facilisi morbi tempus iaculis urna. Enim eu turpis egestas pretium aenean pharetra magna ac. Nulla pharetra diam sit amet nisl. Id neque aliquam vestibulum morbi. Feugiat in ante metus dictum at tempor commodo ullamcorper a. Mattis molestie a iaculis at erat pellentesque adipiscing commodo. Euismod elementum nisi quis eleifend quam adipiscing vitae proin sagittis. Sollicitudin aliquam ultrices sagittis orci. Tortor at auctor urna nunc id cursus. Metus aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices. Nisl nisi scelerisque eu ultrices vitae auctor eu.\nId faucibus nisl tincidunt eget nullam non. Dignissim cras tincidunt lobortis feugiat vivamus at. Id donec ultrices tincidunt arcu non sodales neque sodales ut. Scelerisque eleifend donec pretium vulputate sapien. Elementum facilisis leo vel fringilla est. Integer quis auctor elit sed vulputate mi sit. Pharetra magna ac placerat vestibulum lectus mauris ultrices eros in. Dolor sit amet consectetur adipiscing elit duis tristique sollicitudin nibh. Viverra ipsum nunc aliquet bibendum enim facilisis gravida. Diam vel quam elementum pulvinar etiam non quam. Sit amet luctus venenatis lectus magna fringilla urna porttitor rhoncus. Duis tristique sollicitudin nibh sit amet commodo nulla facilisi nullam. Donec ac odio tempor orci dapibus ultrices in. Dignissim diam quis enim lobortis. Ut lectus arcu bibendum at varius. Leo vel orci porta non pulvinar neque laoreet suspendisse interdum. Purus in massa tempor nec feugiat nisl pretium.\nA scelerisque purus semper eget duis. Sit amet porttitor eget dolor morbi non arcu risus quis. Mi proin sed libero enim sed faucibus turpis in. Nunc sed id semper risus in hendrerit gravida rutrum. Eu turpis egestas pretium aenean pharetra magna. Pulvinar etiam non quam lacus. Sapien eget mi proin sed libero enim sed. Sed felis eget velit aliquet sagittis. Quam vulputate dignissim suspendisse in est ante in nibh mauris. Nec tincidunt praesent semper feugiat nibh sed. Enim facilisis gravida neque convallis a cras semper auctor neque. Id cursus metus aliquam eleifend mi in. Molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed. Interdum varius sit amet mattis vulputate. Imperdiet proin fermentum leo vel orci porta non pulvinar. Ac tortor vitae purus faucibus ornare suspendisse. Amet purus gravida quis blandit turpis cursus in hac habitasse. Bibendum est ultricies integer quis auctor elit sed vulputate. Euismod nisi porta lorem mollis aliquam. Vehicula ipsum a arcu cursus vitae congue.\nUrna neque viverra justo nec ultrices dui sapien. Suspendisse interdum consectetur libero id. Vel fringilla est ullamcorper eget. Dolor morbi non arcu risus quis varius quam quisque. Ut morbi tincidunt augue interdum velit euismod in pellentesque. Facilisis gravida neque convallis a cras semper. Commodo ullamcorper a lacus vestibulum sed arcu non. Elit sed vulputate mi sit. Purus faucibus ornare suspendisse sed. Diam sit amet nisl suscipit adipiscing bibendum. Feugiat sed lectus vestibulum mattis ullamcorper velit sed. Lacinia at quis risus sed. Commodo elit at imperdiet dui accumsan sit amet. Facilisis leo vel fringilla est ullamcorper eget nulla facilisi etiam. Duis ultricies lacus sed turpis tincidunt id. Lacus suspendisse faucibus interdum posuere lorem ipsum dolor. Tellus cras adipiscing enim eu turpis egestas pretium aenean.\nSit amet luctus venenatis lectus magna fringilla. Dignissim enim sit amet venenatis urna cursus. Scelerisque purus semper eget duis at. Egestas fringilla phasellus faucibus scelerisque eleifend donec. Velit egestas dui id ornare arcu odio. Blandit libero volutpat sed cras ornare arcu dui. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada. Tellus mauris a diam maecenas sed enim. Tempor commodo ullamcorper a lacus vestibulum sed arcu non. Viverra mauris in aliquam sem fringilla ut morbi tincidunt augue. Morbi blandit cursus risus at ultrices mi tempus imperdiet. Porta nibh venenatis cras sed felis eget velit aliquet sagittis.",
//         "link":"www.google.com"
//     },
//     {
//         "name":"event C",
//         "date":new Date("1-1-2007"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
//         "link":"www.google.com"
//     },

//     {
//         "name":"event d1",
//         "date":new Date("4-4-2012"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Odio tempor orci dapibus ultrices in iaculis nunc. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Tincidunt ornare massa eget egestas. Lacus laoreet non curabitur gravida arcu. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Ultrices neque ornare aenean euismod elementum nisi quis. Dictum fusce ut placerat orci nulla pellentesque. A condimentum vitae sapien pellentesque. Facilisis sed odio morbi quis commodo odio. Pharetra pharetra massa massa ultricies. Mauris a diam maecenas sed enim ut sem viverra. Ornare suspendisse sed nisi lacus sed viverra tellus in. Tincidunt ornare massa eget egestas purus. Ut sem nulla pharetra diam. Risus nec feugiat in fermentum posuere. Aliquet eget sit amet tellus cras adipiscing.\nInteger eget aliquet nibh praesent tristique magna sit. Tortor aliquam nulla facilisi cras fermentum odio eu. Ac ut consequat semper viverra nam libero justo laoreet. Dignissim suspendisse in est ante. Augue lacus viverra vitae congue eu. Aenean vel elit scelerisque mauris pellentesque pulvinar pellentesque habitant. Amet tellus cras adipiscing enim eu turpis egestas. Orci nulla pellentesque dignissim enim sit amet. Hendrerit gravida rutrum quisque non tellus. Pharetra pharetra massa massa ultricies mi quis hendrerit dolor. Quisque sagittis purus sit amet volutpat consequat mauris nunc congue. Ac auctor augue mauris augue neque gravida in fermentum. Vestibulum lectus mauris ultrices eros in cursus. Pharetra convallis posuere morbi leo urna molestie at. Cras fermentum odio eu feugiat pretium nibh ipsum consequat.\nTincidunt ornare massa eget egestas purus viverra accumsan. Quam elementum pulvinar etiam non quam lacus suspendisse faucibus. In eu mi bibendum neque egestas congue. Porta non pulvinar neque laoreet. Ultrices in iaculis nunc sed augue lacus viverra vitae congue. Pellentesque massa placerat duis ultricies lacus sed turpis tincidunt. Ultrices in iaculis nunc sed augue lacus. Consectetur lorem donec massa sapien faucibus et molestie. Lacus sed viverra tellus in hac habitasse platea dictumst. Rhoncus mattis rhoncus urna neque.",
//         "link":"www.google.com"
//     },

//     {
//         "name":"event d2",
//         "date":new Date("8-8-2012"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
//         "link":"www.google.com"
//     },

//     {
//         "name":"event d3",
//         "date":new Date("6-6-2012"),
//         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
//         "link":"www.google.com"
//     },
// ]


let event_line_group = d3.select("#funding_graph").append("g").attr("class","event_lines")
let svg = document.querySelector("#funding_graph")
let label_group = document.createElementNS("http://www.w3.org/2000/svg","g")
label_group.classList = ["label_group"]

let project_label_group = document.createElementNS("http://www.w3.org/2000/svg","g")
project_label_group.classList = ["label_group","project_label_group"]
svg.appendChild(label_group)
svg.appendChild(project_label_group)
function zoom_update_call_back(local_x_scale,start,end){
    // console.log("zoom")
    // console.log(local_x_scale)
    
    mid_point = new Date(Math.ceil((end.getTime()+start.getTime())/2))

    
    on_screen = event_data.filter(elm=>elm["Type"]=="news").filter(elm=> elm["Date"].getTime() < end.getTime() && elm["Date"].getTime()>start.getTime())
    // console.log(on_screen)
    
    on_screen.sort((a,b)=>Math.abs(mid_point.getTime()-a["Date"].getTime())-Math.abs(mid_point.getTime()-b["Date"].getTime()))
    
    event_line_group.select(".main_event_lines").remove()
    main_event_lines = event_line_group.append("g").attr("class","main_event_lines")
    let graph_area = document.querySelector("#funding_graph .graph_area")
    
    
    label_group.replaceChildren()
    
    // on_screen.slice(item_count,on_screen.length).forEach(elm=>{
    //     loc_x = local_x_scale(elm["Date"]) + 50
    //     path = "M"+Math.round(loc_x)+" 0 L"+Math.round(loc_x) + " "+ (svg.getBoundingClientRect().height-150)
    //     main_event_lines.append("path").attr("d",path)
    // })
    
    on_screen.forEach(elm=>
    {

        let r = graph_area.getBoundingClientRect()
        loc_x = local_x_scale(elm["Date"]) + 50
        path = "M"+Math.round(loc_x)+" 0 L"+Math.round(loc_x) + " "+ (svg.getBoundingClientRect().height)
        
        
        //.text(elm["Acronym"])
        main_event_lines.append("circle").attr("cx",Math.round(loc_x)).attr("cy",y_pos).attr("class","event_label " + elm["Acronym"].replaceAll(" ","_").replaceAll(":","_"))
  
        let cur = document.querySelector("#funding_graph ."+elm["Acronym"].replaceAll(" ","_").replaceAll(":","_"))
        var cur_rect = cur.getBoundingClientRect()
        fine=false
        direction = null
        index = 0
        while(!fine && index < 2){
        index += 1
        fine = true
        document.querySelectorAll("#funding_graph .main_event_lines .event_label").forEach(
            elm=>{
                if(elm != cur){
                    other_rect = elm.getBoundingClientRect()
                    if(intersectRect(cur_rect,other_rect)){
                        // console.log("intersection")
                        if ((cur_rect.x + cur_rect.width/2 > other_rect.x + other_rect.width/2 && direction == null) || direction == "right" ){
                            cur.setAttribute("x",parseInt(cur.getAttribute("x")) - (cur_rect.x-(other_rect.x + other_rect.width)) + 10)
                            direction = "right"
                        }else{
                            cur.setAttribute("x",parseInt(cur.getAttribute("x")) - (cur_rect.x-(other_rect.x - cur_rect.width)) - 10)
                            direction = "left"
                        }
                        cur_rect = cur.getBoundingClientRect()
                        fine=false
                    }
                }
            }
        )
        }
         
        // path += "L"+(parseInt(cur.getAttribute("x")) + cur_rect.width/2) + " " + parseInt(cur.getAttribute("y")-20)

        main_event_lines.append("path").attr("d",path)
        
        cur.addEventListener("mouseover", fill_artical(elm["Name"],elm["Date"],elm["Notes"],elm["Link"]))
        cur.addEventListener("mouseout", ()=>{hide_artical()});
       
        
        return true
    })
    
    if(false){
        project_label_group.replaceChildren()


        on_screen_projects = event_data.filter(elm=>elm["Type"]=="projects").filter(elm=> elm["Date"].getTime() < end.getTime() && elm["Date"].getTime()>start.getTime())
        on_screen_projects.sort((a,b)=>Math.abs(mid_point.getTime()-a["Date"].getTime())-Math.abs(mid_point.getTime()-b["Date"].getTime()))

        // console.log(on_screen_projects)

        event_line_group.select(".project_event_lines").remove()
        project_event_lines = event_line_group.append("g").attr("class","project_event_lines")

        on_screen_projects.slice(10,100).forEach(elm=>{
            loc_x = local_x_scale(elm["Date"]) + 50
            path = "M"+Math.round(loc_x)+" 0 L"+Math.round(loc_x) + " "+ (svg.getBoundingClientRect().height-150)
            project_event_lines.append("path").attr("d",path)
        })
        on_screen_projects.slice(0,10).forEach(elm=>{
            let r = graph_area.getBoundingClientRect()
            loc_x = local_x_scale(elm["Date"]) + 50
            path = "M"+Math.round(loc_x)+" 0 L"+Math.round(loc_x) + " "+ (svg.getBoundingClientRect().height-150)
            
            
            
            project_event_lines.append("text").attr("x",Math.round(loc_x)).attr("y","550").text(elm["Acronym"]).attr("class","event_label " + "evt_"+elm["Acronym"].replaceAll("-","").replaceAll(" ","_").replaceAll(":","_"))

            let cur = document.querySelector("#funding_graph .project_event_lines ."+"evt_"+elm["Acronym"].replaceAll(" ","_").replaceAll(":","_").replaceAll("-",""))
            if(cur != null){
                var cur_rect = cur.getBoundingClientRect()
                fine=false
                direction = null
                index = 0
                while(!fine && index < 2){
                index += 1
                fine = true
                document.querySelectorAll("#funding_graph .project_event_lines .event_label").forEach(
                    elm=>{
                        if(elm != cur){
                            other_rect = elm.getBoundingClientRect()
                            if(intersectRect(cur_rect,other_rect)){
                                // console.log("intersection")
                                if ((cur_rect.x + cur_rect.width/2 > other_rect.x + other_rect.width/2 && direction == null) || direction == "right" ){
                                    cur.setAttribute("x",parseInt(cur.getAttribute("x")) - (cur_rect.x-(other_rect.x + other_rect.width)) + 10)
                                    direction = "right"
                                }else{
                                    cur.setAttribute("x",parseInt(cur.getAttribute("x")) - (cur_rect.x-(other_rect.x - cur_rect.width)) - 10)
                                    direction = "left"
                                }
                                cur_rect = cur.getBoundingClientRect()
                                fine=false
                            }
                        }
                    }
                )
                }
                
                path += "L"+(parseInt(cur.getAttribute("x")) + cur_rect.width/2) + " " + parseInt(cur.getAttribute("y")-20)

                main_event_lines.append("path").attr("d",path)
                
                cur.addEventListener("mouseover", fill_artical(elm["Name"],elm["Date"],elm["Notes"],elm["Link"]))
                cur.addEventListener("mouseout", ()=>{artical_popup.style.display=null});
            }else{
                console.log("found null")
                console.log(elm["Acronym"])
            }
        
    
            return true
        })
    }
}

return zoom_update_call_back
}
