function hex_graph(data, svg_size_func = svg => { return [500, 500] }, radius = 200, sub_lines = 5, option_names = { "FR": "france" }, showPopup, hidePopup) {

    all_data = data
    options = {
        "": "None",
    }
    all_data.map(elm => elm["country"]).filter(onlyUnique).forEach(elm => {
        options[elm] = elm
        if (Object.keys(option_names).indexOf(elm) != -1) { options[elm] = option_names[elm] }
    })



    // topic_names = all_data.map(elm => elm["power_type"]).filter(onlyUnique).filter(elm => elm != "total" & elm != "geothermal energy")
    topic_names = ["biofuels","solar energy", "nuclear energy", "wind power", "fossil energy", "hydroelectricity"]
    mock_data = Object.keys(options).filter(elm => elm != "").map(key => {
        row = {
            "name": key
        }
        topic_names.forEach(elm => {
            row[elm] = 0
        })
        all_data.filter(elm => elm["country"] == key).forEach(elm => {
            row[elm["power_type"]] = elm["usage"] / elm["total_usage"]
        })
        return row
    })

    // console.log(mock_data)



    degree_data = range(0, topic_names.length - 1).map(elm => elm * 360/ topic_names.length)
    var max_values = topic_names.map(name => Math.max(...mock_data.map(mdr => mdr[name])))
        // console.log(mock_data.map(mdr=>mdr["wind power"]))
    point_data = {};
    zip(topic_names, zip(degree_data, max_values)).forEach(elm => {
        point_data[elm[0]] = { "point": radial_to_cart(radius, elm[1][0]) }
    })



    //stop
    let svg_size = svg_size_func(document.querySelector("#hex_graph"))





    var main_window = d3.select("#hex_graph")
    main_window.append("g").attr("class", "graph_area").attr("transform", "translate( 300 , 250 )")
    var graph_area = d3.select("#hex_graph .graph_area")
    var label_group = graph_area.append("g").attr("class","value_label")
    main_window.attr("height", svg_size[0]).attr("width", svg_size[1])

    //graph_area.append("g").attr("class", "base_points").selectAll("circle").data(items(point_data)).enter().append("circle")
        //.attr("cx", elm => elm[1]["point"][0]).attr("cy", elm => elm[1]["point"][1]).attr("class", elm => elm[0].replaceAll(" ", "_"))

    graph_area.append("g").attr("class", "base_lines").selectAll("line").data(items(point_data)).enter().append("line")
        .attr("x1", 0).attr("y1", 0).attr("x2", elm => elm[1]["point"][0]).attr("y2", elm => elm[1]["point"][1]).attr("class", elm => elm[0].replaceAll(" ", "_"))

    ring_lines_group = graph_area.append("g").attr("class", "ring_lines")

    for (let i = 1; i < sub_lines + 1; i++) {
        let new_r = radius * i / sub_lines
        ring_lines = []
        for (let a = 0; a < degree_data.length; a++) {
            ring_lines.push([
                [radial_to_cart(new_r, degree_data[a]), radial_to_cart(new_r, degree_data[(a + 1) % degree_data.length])],
                [topic_names[a], topic_names[(a + 1) % degree_data.length]]
            ])
        }
        ring_lines_group.append("g").attr("class", "i" + i).selectAll("line").data(ring_lines).enter().append("line")
            .attr("x1", elm => elm[0][0][0]).attr("y1", elm => elm[0][0][1]).attr("x2", elm => elm[0][1][0]).attr("y2", elm => elm[0][1][1]).attr("class", elm => elm[1][0].replaceAll(" ", "_") + " " + elm[1][1].replaceAll(" ", "_"))

    }

    graph_area.append("g").attr("class", "labels").selectAll("text").data(items(point_data)).enter().append("text")
        .attr("x", elm => elm[1]["point"][0] + elm[1]["point"][0]/4 - 45).attr("y", elm => elm[1]["point"][1] + elm[1]["point"][1]/9).attr("class",elm=>elm[0].replaceAll(" ", "_")).text(elm => titleCase(elm[0]))

    let shape_groups = graph_area.append("g").attr("class", "shape_groups")



    // console.log("mock data")
    // console.log(mock_data)
    controls = document.getElementById("hex_graph_selectors")

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

    selectors = ["1", "2", "3"]
    selectors.forEach(elm => {
        let sel = document.createElement("select")
        sel.id = "country_" + elm
        sel.name = "country_" + elm
        let lab = document.createElement("label")
        lab.for = "country_" + elm
        //lab.innerText = "   Country " + elm
        number = elm
        items(options).forEach(elm => {
            let opt = document.createElement("option")
            convert_country_names(elm, number)

            if(elm[1] != "NA"){
            opt.value = elm[0]
            opt.text = elm[1]
            sel.appendChild(opt)}
        })
        let csg = document.createElement("div")
        csg.classList = ["country_select_group"]
        csg.appendChild(sel)
        csg.appendChild(lab)
        controls.appendChild(csg)
    })



    function update_shape_display(event) {


        all_selector = document.querySelectorAll("#hex_graph_selectors select")

        var selected_values = []
        var html_class_source = []
        for (let i = 0; i < all_selector.length; i++) {
            selected_values.push(all_selector[i].value)
            html_class_source.push(all_selector[i].classList)
        }
        let current_rows = mock_data.filter(elm => selected_values.indexOf(elm["name"]) != -1)
        

        //max value option (pick any)
        max_values = topic_names.map(
            name => Math.max(...mock_data.map(mdr => isNaN(mdr[name])?0:mdr[name] ))) // overall max
        //max_values = topic_names.map(name => 0.7) // constant 1
        /* max_values = topic_names.map(name => { // pick per row
            if (name == "nuclear energy" ){
                return .5
            }else{
                return 1
            }
        }) */
        //max_values = topic_names.map(name => Math.max(...current_rows.map(mdr => mdr[name]))) // by current selection

        //post processes
        //max_values = max_values.map(x=>Math.ceil(Math.max(x,.01)*10)/10) // round to the nearest 
        // label_group.selectAll("text").remove()
        // label_group.selectAll("text").data(zip(degree_data, max_values)).enter().append("text")
        //     .attr("x", elm => radial_to_cart(radius, elm[0])[0]).attr("y", elm => radial_to_cart(radius, elm[0])[1] + 20).text(elm => Math.round(elm[1] * 100))

        console.log(max_values)

        i = 1

        all_selector.forEach(
            elm => {
                shape_groups.select("." + elm.name).remove()
                var data_row = mock_data.filter(mdr => mdr["name"] == elm.value)
                if (data_row.length > 0) {
                    points = zip(topic_names, zip(degree_data, max_values)).map(elm => {
                        if (elm[1][1] == 0) {
                            return radial_to_cart(0, elm[1][0])
                        }
                        return radial_to_cart(data_row[0][elm[0]] / elm[1][1] * radius, elm[1][0])

                    })

                    point_path = "M" + points[0][0] + " " + points[0][1] + " "
                    for (let i = 1; i < points.length; i++) {
                        point_path += "L" + points[i][0] + " " + points[i][1] + " "
                    }
                    point_path += "Z"


                    let shape_group = shape_groups.append("g").attr("class", elm.name + " " + elm.value)
                    shape_group.append("path").attr("d", point_path)

                    shape_group.selectAll("circle").data(zip(topic_names, points)).enter().append("circle")
                        .attr("cx", elm => elm[1][0]).attr("cy", elm => elm[1][1]).attr("class", elm => elm[0].replaceAll(" ", "_")).attr("data", elm => elm[0] + "," + data_row[0][elm[0]])

                    document.querySelectorAll("." + elm.name + " circle").forEach(
                        elm => {
                            elm.addEventListener("mouseover", showPopup);
                            elm.addEventListener("mouseout", hidePopup);
                        }
                    )
                }
                i+=1
            }
        )


        // label_data = zip(zip(topic_names,zip(,html_class_source)),zip(degree_data,max_values)).map(elm=>{
        //     return{ "name":elm[0][0],
        //             "value":
        //             "point":radial_to_cart(radius,elm[1][0]),
        //             "max_value":elm[1][1]}
        // })


        // if (data_row.length > 0) {
        //     points = zip(topic_names, degree_data).map(elm => { return radial_to_cart(data_row[0][elm[0]] * radius, elm[1]) })

        //     point_path = "M" + points[0][0] + " " + points[0][1] + " "
        //     for (let i = 1; i < points.length; i++) {
        //         point_path += "L" + points[i][0] + " " + points[i][1] + " "
        //     }
        //     point_path += "Z"
        //         // console.log(point_path)


        //     let shape_group = shape_groups.append("g").attr("class", event.target.name + " " + event.target.value)
        //     shape_group.append("path").attr("d", point_path)

        //     shape_group.selectAll("circle").data(zip(topic_names, points)).enter().append("circle")
        //         .attr("cx", elm => elm[1][0]).attr("cy", elm => elm[1][1]).attr("class", elm => elm[0].replaceAll(" ", "_"))

        //     document.querySelectorAll("." + event.target.name + " circle").forEach(
        //         elm => {
        //             elm.addEventListener("mouseover", showPopup);
        //             elm.addEventListener("mouseout", hidePopup);
        //         }
        //     )
        // }

    }


    selectors = document.querySelectorAll("#hex_graph_selectors select")
    selectors.forEach(elm => elm.onchange = update_shape_display)
}