function funding_graph(zoom_update_call_back, funding_data, emmissions_data, init_selected = ["all"], init_zoom = 1, init_pan = 0, domains = [
    [0, 10 ** 7.3],
    [new Date("1/1/2008"), new Date("1/1/2028")]
], svg_height_function = svg => { end = [svg.getBoundingClientRect.height, svg.getBoundingClientRect().width]; if (isNaN(end[0])) { end[0] = 600 }; return end }, dims_function = svg_size => [svg_size[0] - 200, svg_size[1] - 100], y_lin = true, showPopup = elm => {}, hidePopup = elm => {}) {

    var all_topic_names = { "all": "all" };
    let topic_checkbox_group = document.getElementById("check_boxes")
    var selected = init_selected

    //set all checkboxes to match the list of selected above
    function update_check_status() {
        let check_boxes = document.querySelectorAll("#check_boxes.control_panel input[type='checkbox']")
        var new_selected = []
        check_boxes.forEach((e, i, a) => { if (e.checked) { new_selected.push(e.name) } })
        selected = new_selected
        update_graph_display()
    }
    //generate all the check boxes for controlling the graph
    function display_topic_checkboxes() {
        recursive_group_collect(group_data).forEach((v, i, a) => {
            all_topic_names["topic" + i] = v
        })
        items(all_topic_names).forEach((v, i, a) => {

            valid_topics = ["geothermal energy", "fossil energy", "biofuels", "wind power", "solar energy", "hydroelectricity", "nuclear energy"]


            var checkbox_container = document.createElement("div")
            checkbox_container.setAttribute("class", "checkbox_container")
                //checkbox_container.setAttribute("style", "display:inline")

            var checkbox_input = document.createElement("input")
            checkbox_input.setAttribute("name", v[1])
            checkbox_input.setAttribute("type", "checkbox")
            if (selected.indexOf(v[1]) != -1) {
                checkbox_input.setAttribute("checked", true)
            }
            checkbox_input.onchange = update_check_status
            var checkbox_label = document.createElement("label")
            checkbox_label.setAttribute("for", v[1])
            if (valid_topics.includes(checkbox_label.getAttribute("for"))) {

                label = titleCase(checkbox_label.getAttribute("for"))

                checkbox_label.innerHTML = label
                id = checkbox_label.getAttribute("for")
                checkbox_input.setAttribute("id", id)

                checkbox_label.setAttribute("id", id + "_label")

                checkbox_input.setAttribute("style", "margin-top: 30px;")
                checkbox_container.appendChild(checkbox_input)
                checkbox_container.appendChild(checkbox_label)
                topic_checkbox_group.appendChild(checkbox_container)

            }

        })
    }
    graph_down = 10
        //vars related to the svg
    var main_window = d3.select("#funding_graph");
    var graph_window = main_window.append("g").attr("class", "graph_window scrollable").attr("transform", "translate(10," + graph_down + ")")
    var graph_area = graph_window.append("g").attr("class", "graph_area").attr("transform", "translate(-10,-" + graph_down + ")")
    var bar = graph_area.append("g").attr("class", "bar")
    var series_group = graph_area.append("g").attr("class", "series_group")
    var svg = document.querySelector("#funding_graph");

    let svg_size = svg_height_function(svg)
        // console.log(svg_size)

    let dims = dims_function(svg_size); // y-x
    var zoom = init_zoom;
    var pan = [0, 0];


    var dim_scales = [null, null];
    var em_scales = [null, null];
    var dim_axis;
    var em_axis;
    var connect_back = false


    var start_pos = null
    var dragging_element = null
    document.querySelector("#funding_graph").onmousedown = (e) => {
        e = e || window.event;
        e.preventDefault();
        console.log(e)
        dragging_element = e.target
        start_pos = [e.clientX, e.clientY]
        window.onmousemove = (e) => {
            difference = [start_pos[0] - e.clientX, start_pos[1] - e.clientY]
            console.log(difference)

            graph_area.attr("transform", "translate(" + (Math.max(Math.min(pan[1] - difference[0], dims[1] / 2), -dims[1]-50)) + ")")
            d3.select("#funding_graph .event_lines").attr("transform", "translate(" + (Math.max(Math.min(-difference[0], dims[1] / 2), -dims[1]-50)) + ")")
        }

        drag_end = (e) => {
            console.log(e)
            difference = [start_pos[0] - e.clientX, start_pos[1] - e.clientY]
            window.onmouseup = null
            window.onmousemove = null
            dragging_element.mouseleave = null
            pan[1] = Math.max(Math.min(pan[1] - difference[0], dims[1] / 2), -dims[1]-50)
            calc_axes()
            d3.select("#funding_graph .event_lines").attr("transform", null)
        }
        dragging_element.mouseleave = drag_end
        window.onmouseup = drag_end
    }

    // graph_area.attr("transform", "translate(" + (pan[1]) + ")")
    //event for detecting scroll
    // document.querySelector("#funding_graph").onwheel = (e) => {
    //     // console.log("zoom "+ e.deltaY + ":" +e.offsetX+ ","+e.offsetY)

    //     // if(e.deltaY<0){
    //     //     if(zoom < 10){
    //     //         zoom = Math.min(zoom + 0.1,10)
    //     //     }

    //     // }
    //     // if(e.deltaY>0){
    //     //     if(zoom > 1){
    //     //         zoom = Math.max(zoom - 0.1,1)

    //     //     }

    //     // }

    //     // if(e.deltaX<0){pan[1] = Math.min(pan[1] + 0.05,1)}
    //     // if(e.deltaX>0){pan[1] = Math.max(pan[1] - 0.05,-1)}
    //     if (e.deltaY < 0) { pan[1] = Math.min(pan[1] + 0.05, 1) }
    //     if (e.deltaY > 0) { pan[1] = Math.max(pan[1] - 0.05, -1) }
    //     calc_axes()
    //         // update_graph_display()
    // }
    graph_window.append("g").attr("class", "y_axis")
    graph_window.append("g").attr("class", "x_axis")
    graph_window.append("g").attr("class", "y_axis_bar")
    graph_area.append("g").attr("class", "y_axis_overall")
    graph_area.append("g").attr("class", "x_axis_overall")
        //on size change
    function graph_setup() {
        console.log("funding graph redraw axis")
        svg_size = svg_height_function(svg)

        dims = dims_function(svg_size)
        console.log("dims:" + dims)
            // console.log(svg_size)
            // console.log(funding_data);
            // main_window.attr("height",svg_size[0]).attr("width",svg_size[1])

        // date_times = funding_data.map(e=>e.start_date)
        // min_date = new Date(Math.min(...date_times))
        // max_date = new Date(Math.max(...date_times))
        // console.log(min_date.toLocaleDateString()+","+max_date.toLocaleDateString())

        // all_funding = funding_data.map(e=>e.all)
        // max_funding = Math.max(...all_funding)
        // Math.round(Math.log10(max_funding)+.5)

        graph_window.select("g.y_axis")
        graph_window.select("g.x_axis").attr("transform", "translate(0," + dims[0] + ")")
        graph_window.select("g.y_axis_bar").attr("transform", "translate(" + (dims[1]) + ",0)")
        graph_area.select("g.y_axis_overall").attr("transform", "translate(100,0)")
        graph_area.select("g.x_axis_overall").attr("transform", "translate(0,100)")
            // console.log(dims[1])

        bar.attr("transform", "translate(0," + (dims[0]) + ")")

        // graph_window.append("g").attr("class", "x_axis_bar").attr("transform", "translate(0," + dims[0] + ")")



        if (y_lin) { //y-axis
            dim_scales[0] = d3.scaleLinear().domain([domains[0][0], domains[0][1]/1e6]).range([dims[0], 0])
        } else {
            money_domain = range(domains[0][0], Math.round(Math.log10(domains[0][1]) + .5)).map(x => Math.pow(10, x))
            money_range = range(0, Math.round(Math.log10(domains[0][1]) + .5)).map(x => (1 - x / Math.round(Math.log10(domains[0][1]) + .5)) * dims[0])
            dim_scales[0] = d3.scaleLog().domain(money_domain).range(money_range)


        }

        dim_scales[1] = d3.scaleTime().domain([domains[1][0], domains[1][1]]).range([0, dims[1] * zoom])
        bar_scale_y = d3.scaleLinear().domain([0, 100]).range([dims[0], 0])
        bar_axis_y = d3.axisLeft().scale(bar_scale_y)
        dim_axis = [d3.axisRight().scale(dim_scales[0]),
                d3.axisBottom().scale(dim_scales[1])
            ]
            // em_axis = [d3.axisRight().scale(em_scales[0]),
            //     d3.axisBottom().scale(em_scales[1])
            // ]
        graph_area.select("g.x_axis_overall").call(dim_axis[1])
        graph_window.select(".y_axis").call(dim_axis[0])
        graph_window.select(".y_axis_bar").call(bar_axis_y)
        graph_area.select(".y_axis_overall").call(dim_axis[0])


        calc_axes()
        update_graph_display()

        //draw target line

        graph_area.select("line.target_line").remove()
        graph_area.append("line").attr("class","target_line").attr("y1",bar_scale_y(55)).attr("y2",bar_scale_y(55))
            .attr("x1",dim_scales[1](new Date("12/01/15"))).attr("x2",dim_scales[1](new Date("1/1/2030")))

        //draw bars
        bar_plot_points = em_data.map((point) => {

                rect_points = [
                    [new Date("1-1-" + (point["TIME_PERIOD"] - 1)), point["OBS_VALUE"]],
                    [new Date("1-1-" + point["TIME_PERIOD"]), 0]
                ]


                rect_points[0][0] = dim_scales[1](rect_points[0][0])
                rect_points[1][0] = dim_scales[1](rect_points[1][0]) - rect_points[0][0]

                rect_points[0][1] = bar_scale_y(rect_points[0][1])
                rect_points[1][1] = bar_scale_y(rect_points[1][1]) - rect_points[0][1]

                return rect_points
            })
            // console.log(bar_plot_points)
        bar.selectAll("g").remove()
        bar.selectAll("g").data(bar_plot_points).enter().append("g")
            .attr("transform", elm => "translate(" + elm[0][0] + "," + 0 + ")").append("rect")
            .attr("x", 0).attr("y", elm => -elm[1][1])
            .attr("width", elm => elm[1][0] - elm[1][0] * 0.2)
            .attr("height", elm => elm[1][1])





    }
    //on pan/zoom
    function calc_axes() {


        graph_area.attr("transform", "translate(" + (pan[1]) + ")")



        // dim_scales[1] = d3.scaleTime().domain([domains[1][0], domains[1][1]]).range([0, dims[1] * zoom])

        // local_time_range =  time_range / zoom
        // start = domains[1][0]
        // end = new Date(domains[1][0].getTime()+local_time_range)
        time_range = (domains[1][1] - domains[1][0]) / zoom
        start = new Date(domains[1][0].getTime() - pan[1] * time_range / dims[1])
        end = new Date(start.getTime() + time_range)
        let local_scale = d3.scaleTime().domain([start, end]).range([0, dims[1]])
        let local_time_dim = d3.axisBottom().scale(local_scale)

        // graph_window.select(".y_axis").call(dim_axis[0])
        graph_window.select(".x_axis").call(local_time_dim)
            //graph_window.select(".x_axis_bar").call(local_time_dim)
            // graph_area.select(".x_axis_overall").call(dim_axis[1])

        //TODO add bar graph and axis

        //var yScale_bar = d3.scaleLinear().range([dims[1], 0])
        //var xScale_bar = d3.scaleBand().range([0, dims[0]])
        //graph_area.append("g").attr("class", "y_axis_bar").attr("translate(90,0)")
        //graph_window.select(".y_axis_bar").call(dim_axis[0])

        // drawn_bars = svg.querySelectorAll("#funding_graph .bar")
        //xScale_bar.domain(emmissions_data.map(function(d) { return d.year; }));
        //yScale_bar.domain([0, d3.max(emmissions_data, function(d) { return d.value; })]);

        //y axis
        //dim_scales[0] = d3.scaleLinear().domain([domains[0][0], domains[0][1]]).range([dims[0], 0])
        //x-axis

        // graph_area.selectAll(".bar")
        //     .data(emmissions_data)
        //     .enter().append("rect")
        //     .attr("class", "bar")
        //     .attr("x", function(d) { return em_scales[0](d.year); })
        //     .attr("y", function(d) { return em_scales[1](d.value); })
        //     .attr("width", 100)
        //     .attr("height", function(d) { return 400 - em_scales[1](d.value); });


        zoom_update_call_back(local_scale, start, end)
        update_graph_display()
    }

    //on content/checkbox change
    //update the series group for the graph
    function update_graph_display() {


        drawn = []
        drawn_groups = svg.querySelectorAll("#funding_graph .series_group g")
        for (let i = 0; i < drawn_groups.length; i++) {
            drawn.push(drawn_groups[i].classList[0].replaceAll("_", " "))
        }
        //collect data
        // console.log("select,draw,remove,to_draw")
        // console.log(selected)
        // console.log(drawn)
        remove = drawn.filter(x => selected.indexOf(x) == -1)
        to_draw = selected.filter(x => drawn.indexOf(x) == -1)
            // console.log(remove)
            // console.log(to_draw)

        data_points = {}
        to_draw.forEach((topic_name, i, a) => {
                // console.log(topic_name)
                // console.log(funding_data.map(e => e[topic_name]))
                data_points[topic_name] = zip(funding_data.map(e => e[topic_name]/1e6), funding_data.map(e => new Date(e.start_date))).filter((elm) => elm[0] > 0)
            })
            //make group for each serries
            // graph_area.select(".series_group").remove()




        remove.forEach(group => {
            graph_area.select(".series_group g." + group.replaceAll(" ", "_")).remove()
        })




        // graph_area.select(".series_group").selectAll("g").data(Object.keys(data_points)).enter().append("g").attr("class", (d) => d.replaceAll(" ", "_"))


        //update the dots
        items(data_points).forEach(series => {
            if (series[1].length > 0) {
                var path = "M" + dim_scales[1](series[1][0][1]) + " " + dim_scales[0](series[1][0][0]) + " "
                for (let i = 1; i < series[1].length; i++) {
                    path += "L" + dim_scales[1](series[1][i][1]) + " " + dim_scales[0](series[1][i][0]) + " "
                }

                if (connect_back) { path += "Z" }
            }



            // console.log(pairs)

            series_group.append("g").attr("class", series[0].replaceAll(" ", "_")).selectAll("circle").data(series[1])
                .enter().append("circle")
                .attr("cy", function(e, i) { return dim_scales[0](e[0]) })
                .attr("cx", function(e, i) { return dim_scales[1](e[1]) })
                .attr("data", elm => elm[0] + "," + elm[1].toDateString())
                .exit().remove()

            series_group.select("g." + series[0].replaceAll(" ", "_")).append("path").attr("d", path)



        })

        document.querySelectorAll(".series_group circle").forEach(
            elm => {
                elm.addEventListener("mouseover", showPopup);
                elm.addEventListener("mouseout", hidePopup);
            }
        )


    }
    window.addEventListener("resize", evt => { graph_setup() }, true)

    graph_setup();
    display_topic_checkboxes()
}