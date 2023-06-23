function graph( column, { is_measure, is_categorical, n_categories, legend, data_changed_callback } = { }) {

// Set the dimensions of the canvas / graph
const margin = {top: 10, right: 20, bottom: 30, left: 50},
    width = 700 - margin.left - margin.right,
    height = 100 - margin.top - margin.bottom;

// Parse the date / time
const parseDate = d3.timeParse("%Y-%m-%d");
//reverse
const formatDate = d3.timeFormat("%Y-%m-%d");

// Set the ranges
const x = d3.scaleTime().range([0, width]);
const y = d3.scaleLinear().range([height, 0]);

// Define the axes
const xAxis = d3.axisBottom( ).scale(x)
    .ticks(20);

const yAxis = d3.axisLeft( ).scale(y)
    .ticks( is_categorical ? n_categories : 4);

// Define the line
const valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

const row = ( is_measure ? d3.select( ".measures" ) : d3.select( ".outcomes" )).append( "tr" );
const div = row.append( "td" ).append( "div" );
const right_div = row.append( "td" ).append( "div" );

const title = div.append( "p" );
title.style( "margin", 0 );
    

// Adds the svg canvas
const svg = div
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

//Create a group element for the horizontal lines.
var linesGroup = svg.append("g")
  .attr("class", "lines-group");

const orgline = svg.append( "g" ).append("path");

//outcomes have an extra line for the measure that is focused right now
const measureline = ! is_measure ? svg.append( "g" ).append("path").attr("class","measureline") : null;

let line = svg.append( "g" );
    // Select the SVG and append a 'g' element for each line segment

svg.append( "rect" )
    .attr("fill", "none")
    .attr("stroke", "none")
    .attr("pointer-events", "all")
    .on("click", function(event) { // d3 v6 uses event as first argument
        const coordinates = d3.pointer(event, svg.node());

        const d = { x: coordinates[ 0 ], y: coordinates[ 1 ], index: handles.length };

        snap_to_line( d );
        handles.push( d );
        update_handles( );
        select_newest_handle( );
    })
    .on( "mouseenter", on_mouse )
    .on( "mouseover", on_mouse )
    .on( "mousemove", on_mouse )

function on_mouse(event) {
    
    update_measurelines( );
    update_cursor( true );
}

function update_measurelines( ) {

    if( is_measure ) {

        d3.selectAll( ".measureline" ).attr("d", valueline(data)).attr( "stroke", d3.schemeCategory10[ 4 ] + "88" );
    }
    else {

        d3.selectAll( ".measureline" ).attr("d", "");
    }
}

// Add the X Axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

// Add the Y Axis
svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

const handle_circles = svg.append( "g" );

const dotline = svg.append("g").append( "line" );
const predline = svg.append("g").append( "line" );
const dot = svg.append("g").append( "circle" );

let predline_x = null;

// Create a color scale
const colorScale = d3.scaleLinear()
    .domain([0, 1])  // replace with appropriate domain
    .range([ is_measure ? d3.schemeCategory10[ 4 ] : d3.schemeCategory10[ 0 ], d3.schemeCategory10[ 1 ]]);  // replace with your own colors

let handles = [ ];
let data = [ ];
let orgdata = [ ];
let last_data = null;

let selected_handle = null;

function set_selected( handle ) {

    if( selected_handle ) selected_handle.d.selected = false;
    selected_handle = handle;
    if( selected_handle ) selected_handle.d.selected = true;
    update_handles( );
    update_data_hard( );
}

window.addEventListener('keydown', function(event) {
  if (event.key == "x" || event.key == "Backspace") {
    if( selected_handle ) {

        handles = handles.filter( h => h != selected_handle.d );
        set_selected( null );
        update_handles( );
    }
  }

  if (event.key === 'Escape' ) {
    set_selected( null );
    update_handles( );
  }
});

const day_radius = ( 1000 * 60 * 60 * 24 );
//amounts to 50 days of effective radius
const weight_radius = 50 * day_radius;

function weight_fn( d, date ) {

    return Math.exp( - Math.pow(( d.date - date ) / weight_radius, 2 ));
}

function data_is_equal( d1, d2 ) {

    return Math.max( ...d1.map(( _, i ) => Math.abs( d1[ i ].close - d2[ i ].close ))) < 1e-9;
}

function check_data_changed( ) {

    const unchanged = last_data === null || data_is_equal( data, last_data );
    if( ! unchanged ) data_changed_callback( column );

    last_data = data.map( d => ({ ...d })); //deep copy
    if( ! data_is_equal( data, last_data )) console.error( "data should be equal" );
}

function categorical_recompute_data( ) {

    const orderer_to_sorter = f => ( a, b ) => f( a ) - f( b );
    const sorted = handles.sort( orderer_to_sorter( h => h.x ));
    
    sorted.forEach( h => {

        const date = x.invert( h.x );
        const close = y.invert( h.y );
        data.forEach(( d, i ) => d.close = d.date >= date - day_radius ? close : d.close );   
        data.forEach( d => d.close = Math.max( d.close, 0 ));
        data.forEach( d => d.close = Math.round( Math.min( n_categories, d.close ))); 
    });

    check_data_changed( );
}

let is_dragging = false;

const drag = ( _ => {

    let start = null;

    function dragstarted( event, d ) {
        
        start = { date: x.invert( d.x ), close: y.invert( d.y ), data: data.map( d => ({ ...d })) /*deep copy*/ };
        set_selected({ el: this, d });
        is_dragging = true;
    }

    function dragged(event, d) {
        is_dragging = true;
        d3.select(this).raise().attr( "cx", d.x = is_categorical ? event.x : d.x ).attr("cy", d.y = event.y); //do not set x        
        
        if( is_categorical ) {

            categorical_recompute_data( );
        }
        else {

            const date = x.invert( d.x );
            const close = y.invert( d.y );
            const delta = { date: date - start.date, close: close - start.close };
            const weights = start.data.map(( d, i ) => weight_fn( d, date ));
            data = start.data.map(( d, i ) => ({ date: d.date, close: d.close + weights[ i ] * delta.close }));    
            data.forEach( d => d.close = Math.max( d.close, 0 ));
            check_data_changed( );
        }

        update_data_hard( );

        handles.forEach( snap_to_line );
        update_handles( );
        update_cursor( true );
    }

    function dragended( event, d ) {
        
        set_selected({ el: this, d });
        is_dragging = false;
    }

    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);

})( );

function update_handles( ) {

    handle_circles.selectAll("circle")
    .data(handles)
    .join("circle")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("r", 5)
      .attr("fill", is_measure ? d3.schemeCategory10[ 4 ] : d3.schemeCategory10[ 0 ] )
      .attr("stroke", d => d.selected ? d3.schemeCategory10[ 1 ] : "none" )
      .attr( "cursor", is_categorical ? "move": "ns-resize" )
      .call(drag)
}

function select_newest_handle( ) {

    handle_circles.selectAll( "circle" ).each( function( d, i ) {

        if( d.index == handles.length - 1 ) set_selected({ el: this, d });
    });
}

function get_snapped_to_line( cursor_x ) {

    if( data.length == 0 ) return 0;

    const date = x.invert( cursor_x );

    // Find the data point that has the closest date to the target date
    const closestDataPoint = data.reduce((a, b) => Math.abs(b.date - date) < Math.abs(a.date - date) ? b : a );

    // Get the y-value
    return y( closestDataPoint.close );
}

function snap_to_line( d ) {

    d.y = get_snapped_to_line( d.x );
}

function update_predline( ) {

    if( predline_x == null ) return;

    //looks ugly
    /*
    predline
            .attr( "x1", predline_x )
            .attr( "x2", predline_x )
            .attr( "y1", height )
            .attr( "y2", 0 )
            .attr( "pointer-events", "none" )
            .attr( "stroke", d3.schemeCategory10[ 1 ] )
    */
}

function update_cursor( is_active_column = false ) {

    const coordinates = d3.pointer(event, svg.node());
    const d = { x: coordinates[ 0 ], y: coordinates[ 1 ], index: handles.length };
    d3.select( "body" ).selectAll( `.cursor` )
        .data([ 0 ])
        .join( "span" )
        .attr( "class", "cursor" )
        .style( "display", "none" )
        .attr( "data-x", d.x )
        .attr( "data-y", d.y )

    if( is_active_column === true ) d3.select( "body" ).selectAll( `.cursor` ).attr( "data-active-column", column );

    const [ cursor ] = d3.select( "body" ).selectAll( ".cursor" );

    if( cursor ) {

        const cursor_x = cursor.getAttribute( "data-x" );        
        const close = y.invert( get_snapped_to_line( cursor_x ));
        const is_categorical_and_active = is_categorical && cursor.getAttribute( "data-active-column" ) == column;

        right_div.selectAll( "p" )
            .data([ 0 ])
            .join( "p" )
            .html( `<b>${ is_categorical ? close.toFixed( 0 ) : close.toFixed( 2 )}</b> `+ ( is_categorical_and_active ? "= " + legend[ "" + close.toFixed( 0 )] : "" ));    

        dotline
            .attr( "x1", cursor_x )
            .attr( "x2", cursor_x )
            .attr( "y1", get_snapped_to_line( cursor_x ))
            .attr( "y2", 0 )
            .attr( "pointer-events", "none" )
            .attr( "stroke", "#88888888" )
            .attr( "stroke-dasharray", "5 5" )

        dot
            .attr( "cx", cursor_x )
            .attr( "cy", get_snapped_to_line( cursor_x ))
            .attr( "pointer-events", "none" )
            .attr( "r", 3 )
            .attr( "fill", "#88888888" )

        d3.select( ".date" )
            .style( "margin", "10px" )
            .style( "margin-left", "350px" )
            .html( `<b> ${ x.invert( cursor_x ).toISOString().slice(0,10) }</b> `);
    }
}

document.body.addEventListener( "mousemove", update_cursor );

function update_data_hard( ) {

    title.text( column.replaceAll( "_", " " ));

    const [ cursor ] = d3.select( "body" ).selectAll( ".cursor" );

    if( cursor ) {
        
        const cursor_x = cursor.getAttribute( "data-x" );        
        title.text( column.replaceAll( "_", " " ) + ( predline_x && cursor_x >= predline_x ? "(predicted)" : "" ));
    }

    if( is_categorical ) categorical_recompute_data( );

    // Scale the range of the data again 
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, is_categorical ? n_categories : Math.max( 1, d3.max(data, function(d) { return d.close; }))]);

    if( is_categorical ) {

        linesGroup.selectAll("line")
            .data( d3.range( 1, n_categories + 1 )) // Assuming yourData is an array of values associated with the categorical variable
            .join("line")
            .attr("class", "line")
            .attr("x1", 0)
            .attr("x2", width) // Adjust the width as needed
            .attr("y1", function(d) { return y(d); }) // Adjust the yScale function according to your data
            .attr("y2", function(d) { return y(d); }) // Adjust the yScale function according to your data
            .style("stroke", "lightgrey");
    }

    orgline.attr("d", valueline(orgdata)).attr( "stroke", is_measure ? d3.schemeCategory10[ 4 ] + "88" : d3.schemeCategory10[ 0 ] + "88" );

    // Make the changes
    line.selectAll("path")   // change the line
        .data(data.slice(0, -1))  // exclude the last point, because it has no next point
        .join( "path" )
        .attr( "class", "line" )
        .attr("d", function(d, i) {
            // Create an array of the current point and the next point
            const points = [d, data[i+1]];
            return valueline(points);
        })
        .attr("stroke", function(d, i) {
            
            // Use the color scale to get a color for this distance
            const weight = selected_handle ? weight_fn( d, x.invert( selected_handle.d.x )) : 0;
            return predline_x && x( d.date ) >= predline_x ? d3.schemeCategory10[ 1 ] : colorScale( weight );
        });

    //update bounding box
    const bbox = line.node().getBBox();

    svg.selectAll( "rect" )
        .attr( "x", bbox.x )
        .attr( "y", 0 )
        .attr("width", width )
        .attr("height", height )
        .attr( "cursor", "pointer" )

    svg.select(".x.axis") // change the x axis
        .call(xAxis);
    svg.select(".y.axis") // change the y axis
        .call(yAxis);

    update_measurelines( );
}

function set_country( country ) {

    socket.emit( "get_data", country, callback = df => {

        set_data_from_csv( df, false );

        orgdata = data.map( d => ({ date: d.date, close: d.close }));
        last_data = null;

        handles = [ ];
        set_selected( null );
        update_handles( );
        
        last_data = null;
        update_data_hard( );

        if( is_categorical ) {

            let last = -1;
            data.forEach( d => {

                if( last != d.close ) {

                    const hd = { x: x( d.date ), y: y( d.close ), index: handles.length };
                    snap_to_line( hd );
                    handles.push( hd );
                }

                last = d.close;
            });
        }

        update_handles( );
        last_data = null;
    });
}

set_country( "Germany" );

function data_to_csv( data ) {

    const mapped = data.map(d => ({
        date: formatDate(d.date),
        close: d.close.toString() // Convert the numbers back to strings
    }));

    const csv = d3.csvFormat(mapped);

    return csv;
}

function set_data_from_csv( df, trigger_update = true ) {

    data = d3.csvParse( df[ column ]);

    data.forEach(function(d) {

        d.date = parseDate(d.date);
        d.close = +d.close;
    });

    if( trigger_update ) update_data_hard( );
}

return { 

    set_country, 
    data_csv: _ => data_to_csv( data ), 
    orgdata_csv: _ => data_to_csv( orgdata ), 
    get_column: _ => column, 
    set_data_from_csv, 
    is_measure: _ => is_measure,
    set_pred_start_index: index => { predline_x = index === null ? null : x( data[ index ].date ); update_predline( ); update_data_hard( )}
};

}

/*
TODO: inter-plot cursor √
- legend for categorical data √
- date cursor √
- cache trained models on disk using the node system √
- transmit logs before end of event handler (python) √
- length check of time series (cropping to valid range may have changed length) √
- determine effective predicted range √
- introduce alternative model (window regression)
*/