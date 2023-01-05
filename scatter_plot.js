function make_scatters(data, svg_func=(svg)=>{return [500,650]},graph_dims_func = (svg_size)=>{return [400,400,50]},showPopup,hidePopup,per_graph=true ){
        
       

    svg_size = svg_func(document.querySelector("#scatter_plot"))
    graph_dims =graph_dims_func(svg_size)
    let svg = d3.select("#scatter_plot")

    controls = document.getElementById("scatter_plot_selectors")
    controls2 = document.getElementById("percentage_selector")

    topic_names = ["biofuels","solar energy", "nuclear energy", "wind power", "fossil energy", "hydroelectricity"]
    opti = ["Percentage [%]", "Absolute [M€]"]
    let power_types = data.map(elm=>elm["power_type"]).filter(onlyUnique).filter(elm => elm != "total" && elm!="geothermal energy" && elm!="coal" && elm!="petroleum" && elm!="natural gas")
    let fund_use = ["funding percent","usage percent","funding raw","usage raw","usage total","funding total"]

    svg.attr("height",svg_size[1]).attr("width",svg_size[0])
    let graph_area = svg.append("g").attr("class","graph_area").attr("transform","translate(50,35)")
    graph_area.append("g").attr("class","y_axis")
    graph_area.append("g").attr("class","x_axis")

    options = {
        "":"None"
    }

    power_types.forEach(elm=>{
        fund_use.forEach(elm_2=>{
            options[elm+"-"+elm_2.replace(" ","_")] = elm+"-"+elm_2
        })
    })

    let sel = document.createElement("select")
    sel.id = "energy_scatter"
    sel.name = "energy_scatter"
    let lab = document.createElement("label")
    lab.for = "energy_scatter"

    items(power_types).forEach(elm=>{
        let opt = document.createElement("option")
        opt.value = elm[0]
        opt.text = elm[1]
        sel.appendChild(opt)
    })

    let csg = document.createElement("div")
    csg.className = "scatter_selectors"
    csg.appendChild(sel)
    csg.appendChild(lab)
    controls.appendChild(csg)

    opti.forEach(elm=>{
        let box = document.createElement("input")
        box.type = "radio"
        box.id = elm + "_scatter"
        box.name =  elm
        box.className = "test"
        let lab2 = document.createElement("label")
        lab2.for = box.id
        lab2.innerText = elm

        let csg2 = document.createElement("div")
        csg2.classList = ["percentage_selectors"]
        csg2.appendChild(box)
        csg2.appendChild(lab2)
        controls2.appendChild(csg2)
    })

    boxes = document.querySelectorAll(".percentage_selectors input[type=radio]")
    boxes[0].checked = true
    update_plot([power_types[0] + "-usage_percent",power_types[0] + "-funding_percent",power_types[0] + "-usage_total"])
    
    document.querySelectorAll(".scatter_selectors select").forEach(elm=>elm.onchange=update_plot_with_check_box)
    document.querySelectorAll(".percentage_selectors input[type=radio]").forEach(elm=>elm.onchange=update_plot_percentages)

    function update_plot_with_check_box(event){
        selector = document.querySelectorAll(".scatter_selectors select")
        selector.forEach(elm=>index = elm.value)

        boxes = document.querySelectorAll(".percentage_selectors input[type=radio]")

        if (boxes[0].checked==true)
        {
            update_plot([power_types[index] + "-usage_percent",power_types[index] + "-funding_percent",power_types[index] + "-usage_total"])
        }
        else
        {
            update_plot([power_types[index] + "-usage_percent",power_types[index] + "-funding_raw",power_types[index] + "-usage_total"])
        }
    }

    svg.attr("percentages", document.querySelectorAll(".percentage_selectors input[type=radio]")[0].checked)

    function update_plot_percentages(event){
        boxes = document.querySelectorAll(".percentage_selectors input[type=radio]")
        for(let i = 0; i<boxes.length; ++i){
            boxes[i].checked=false
        }

        event.target.checked = true

        selector = document.querySelectorAll(".scatter_selectors select")
        selector.forEach(elm=>index = elm.value)

        if (event.target.name == "Percentage [%]")
        {
            update_plot([power_types[index] + "-usage_percent",power_types[index] + "-funding_percent",power_types[index] + "-usage_total"])
        }
        else
        {
            update_plot([power_types[index] + "-usage_percent",power_types[index] + "-funding_raw",power_types[index] + "-usage_total"])
        }

        svg.attr("percentages", document.querySelectorAll(".percentage_selectors input[type=radio]")[0].checked)
    }

    /* let axis = ["X_axis","Y_axis","Z_axis"]
    axis.forEach(elm=>{
            let sel = document.createElement("select")
            sel.id = elm
            sel.name =  elm
            let lab = document.createElement("label")
            lab.for = elm
            lab.innerText = elm
            items(options).forEach(elm=>{
                let opt = document.createElement("option")
                opt.value = elm[0]
                opt.text = elm[1]
                sel.appendChild(opt)
            })
            let csg = document.createElement("div")
            csg.classList = ["scatter_plot_selector"]
            csg.appendChild(sel)
            csg.appendChild(lab)
            controls.appendChild(csg)
        }
    ) */

    //controls.querySelectorAll("select").forEach(elm=>elm.onchange=()=>update_plot([controls.querySelector("#X_axis").value,controls.querySelector("#Y_axis").value,controls.querySelector("#Z_axis").value]))

    let popup = document.getElementById("scatter_graph_popup")
    
    function update_plot(values) {
        console.log(values)
        

        if(values[0]=='' || values[1] == ''){
            return
        }
        if(values[2] == ''){
            values = [values[0],values[1]]
        }

        values = values.map(elm=>elm.split("-"))
        console.log(values)
        data_rows = values.map(elm=>data.filter(dr => dr["power_type"]==elm[0]))


        data_series = data_rows.map(series=>{
            data_hash = {}
            series.forEach(row=>{
                data_hash[row["country"]] = row
            })
            return data_hash
        })

        function convert_country_names(elm, number = 1){
            if (elm[1] == "AL") {elm[1] = "Albania";}
            else if (elm[1] == "AT") {elm[1] = "Austria";}
            else if (elm[1] == "BA") {elm[1] = "Bosnia and Herzegovina";}
            else if (elm[1] == "BE") {elm[1] = "Belgium";}
            else if (elm[1] == "BG") {elm[1] = "Bulgaria";}
            else if (elm[1] == "CY") {elm[1] = "Cyprus";}
            else if (elm[1] == "CZ") {elm[1] = "Czechia";}
            else if (elm[1] == "DE") {elm[1] = "Germany";}
            else if (elm[1] == "DK") {elm[1] = "Denmark";}
            else if (elm[1] == "EE") {elm[1] = "Estonia";}
            else if (elm[1] == "EL") {elm[1] = "Greece";}
            else if (elm[1] == "ES") {elm[1] = "Spain";}
            else if (elm[1] == "FI") {elm[1] = "Finland";}
            else if (elm[1] == "FR") {elm[1] = "France";}
            else if (elm[1] == "GE") {elm[1] = "Georgia";}
            else if (elm[1] == "HR") {elm[1] = "Croatia";}
            else if (elm[1] == "HU") {elm[1] = "Hungary";}
            else if (elm[1] == "IE") {elm[1] = "Ireland";}
            else if (elm[1] == "IS") {elm[1] = "Iceland";}
            else if (elm[1] == "IT") {elm[1] = "Italy";}
            else if (elm[1] == "LT") {elm[1] = "Lithuania";}
            else if (elm[1] == "LU") {elm[1] = "Luxembourg";}
            else if (elm[1] == "LV") {elm[1] = "Latvia";}
            else if (elm[1] == "MD") {elm[1] = "Moldova";}
            else if (elm[1] == "ME") {elm[1] = "Montenegro";}
            else if (elm[1] == "MK") {elm[1] = "North Macedonia";}
            else if (elm[1] == "MT") {elm[1] = "Malta";}
            else if (elm[1] == "NL") {elm[1] = "Netherlands";}
            else if (elm[1] == "NO") {elm[1] = "Norway";}
            else if (elm[1] == "PL") {elm[1] = "Poland";}
            else if (elm[1] == "PT") {elm[1] = "Portugal";}
            else if (elm[1] == "RO") {elm[1] = "Romania";}
            else if (elm[1] == "RS") {elm[1] = "Serbia";}
            else if (elm[1] == "SE") {elm[1] = "Sweden";}
            else if (elm[1] == "SI") {elm[1] = "Slovenia";}
            else if (elm[1] == "SK") {elm[1] = "Slovakia";}
            else if (elm[1] == "TR") {elm[1] = "Turkey";}
            else if (elm[1] == "UA") {elm[1] = "Ukraine";}
            else if (elm[1] == "XK") {elm[1] = "Kosovo";}
            else if (elm[1] == "EU27_2020") {elm[1] = "EU";}
            else if (elm[1] == "None") {elm[1] = "Country " + number;}
            else {elm[1] = "NA";}
    
            return elm[1];
        }

        keys = data_series.map(c_to_row=>Object.keys(c_to_row))

        accepted_countries = []
        data_points = intersection(keys[0],keys[1]).map(key=>{

            point = zip(values.map(x=>x[1]),data_series).map(axis=>{
                
                ["funding percent","usage percent","funding raw","usage raw","usage total","funding total"]

                if(axis[0]=="funding_percent"){
                    let v = axis[1][key]["funding"]/axis[1][key]["total_funding"]*100
                    if(isNaN(v)){
                        return 0;
                    }
                    return v;
                }else if (axis[0]=="usage_percent"){
                    let v = axis[1][key]["usage"]/axis[1][key]["total_usage"]*100
                    if( isNaN(v) ){
                        return 0;
                    }
                    return v;
                }
                else if(axis[0]=="funding_raw"){
                    return axis[1][key]["funding"]/1e6
                }else if (axis[0]=="usage_raw"){
                    return axis[1][key]["usage"]
                }
                else if(axis[0]=="funding_total"){
                    return axis[1][key]["total_funding"]
                }else if (axis[0]=="usage_total"){
                    return axis[1][key]["total_usage"]
                }

            })
            
            list = ["", key]
            key_aux = convert_country_names(list)
            
            return [key_aux,point]
        })
        // console.log(data_points)

        data_points.sort((a,b)=>a[0]-b[0])

        
        

        

        function select_axis_domain(axis_number,power_type,variable_type,data_point_min,data_point_max){
            console.log("set axis dims: "+ axis_number +","+ power_type +","+ variable_type)
            /* if(axis_number == 0){
                return [0,100]
            } */
            if(axis_number == 1){
                return [data_point_max+data_point_max/10,data_point_min]
            }else{
                return [data_point_min,data_point_max+5]
            }

        }



        var x_domain = select_axis_domain(0,values[0][0],values[0][1],Math.min(...data_points.map(x=>x[1][0])),Math.max(...data_points.map(x=>x[1][0])))
        var y_domain = select_axis_domain(1,values[1][0],values[1][1],Math.min(...data_points.map(x=>x[1][1])),Math.max(...data_points.map(x=>x[1][1])))
        var z_domain = select_axis_domain(2,values[2][0],values[2][1],Math.min(...data_points.map(x=>x[1][2])),Math.max(...data_points.map(x=>x[1][2])))
        
        // var z_domain = [0,200000]
        // if(per_graph){
        //     x_domain = [Math.min(...data_points.map(x=>x[1][0])),Math.max(...data_points.map(x=>x[1][0]))]
        //     y_domain = [Math.max(...data_points.map(x=>x[1][1])),Math.min(...data_points.map(x=>x[1][1]))]
        // }

        // if(["funding_percent","usage_percent"].indexOf(values[0][1])!=-1){
        //     x_domain = [0,100]
        // }
        // if(["funding_percent","usage_percent"].indexOf(values[1][1])!=-1){
        //     y_domain = [0,100]
        // }

        let x_scale = d3.scaleLinear().domain(x_domain).range([0,graph_dims[0]+150])
        let y_scale = d3.scaleLinear().domain(y_domain).range([0,graph_dims[1]])

        var z_scale = null
        if(values.length == 3){
            
            // if(per_graph){
            //     z_domain = [Math.max(...data_points.map(x=>x[1][2])),Math.min(...data_points.map(x=>x[1][2]))]
            // }
            // if(["funding_percent","usage_percent"].indexOf(values[2][1])!=-1){
            //     z_domain = [0,100]
            // }
            z_scale = d3.scaleLinear().domain(z_domain).range([5,graph_dims[2]])
        }
        
        graph_area.select(".y_axis").call(d3.axisRight().scale(y_scale))
        
        graph_area.select(".x_axis").attr("transform", "translate(0,"+graph_dims[0]+")").call(d3.axisBottom().scale(x_scale))
        document.querySelectorAll(".percentage_selectors input[type=radio]")[0].checked
        
        data_points.forEach(point=>{
            let data_point = [
                ["name"]
            ]
            var cur = document.querySelector("#scatter_plot .graph_area circle."+ point[0].split(" ")[0])
            var text = document.querySelector("#scatter_plot .graph_area text."+point[0])
            
            if(cur==null){
                cur = document.createElementNS("http://www.w3.org/2000/svg","circle")
                cur.setAttribute("class",point[0])
                document.querySelector("#scatter_plot .graph_area").appendChild(cur)
                
                cur.addEventListener("mouseover", showPopup);
                cur.addEventListener("mouseout", hidePopup);
            }
            
            
            if(text==null){
                text = document.createElementNS("http://www.w3.org/2000/svg","text")
                text.setAttribute("class",point[0])
                document.querySelector("#scatter_plot .graph_area").appendChild(text)
            }
            cur.setAttribute("transform","translate("+x_scale(point[1][0])+","+y_scale(point[1][1])+")")
            //text.setAttribute("transform","translate("+x_scale(point[1][0])+","+y_scale(point[1][1])+")")
            cur.setAttribute("data",point)
            text.innerHTML = point[0]


            
            if(values.length == 3){
                cur.style.r = ""+z_scale(point[1][2])
            }
        }
        )
        
        

        // if(values[2] != ''){domain}
        // Math.max(data_points.map(x=>x[1]))

        // dim_scales = [  d3.scaleLinear().domain(money_domain).range(money_range),
        //     d3.scaleLinear().domain([domains[1][0],domains[1][1]]).range([0,dims[1]])]

        // dim_axis = [    d3.axisRight().scale(dim_scales[0]),
        //         d3.axisBottom().scale(dim_scales[1])]

        





    }


    console.log(data)
    console.log(power_types)


}