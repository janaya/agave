function render_graph() {
//var url = window.document.URL.replace('graph','json');
//$.getJSON(url)
var w = document.body.clientWidth,
    h = document.body.clientHeight,
    colors = pv.Colors.category19();

var vis = new pv.Panel()
    .width(w)
    .height(h)
    .fillStyle("white")
    .event("mousedown", pv.Behavior.pan())
    .event("mousewheel", pv.Behavior.zoom());

var force = vis.add(pv.Layout.Force)
    .nodes(miserables.nodes
        .sort(function(a, b){return b - a);})
    .links(miserables.links)
//    .label("Hola")
    .iterations(150)
//    .springConstant(0.05);
    .springLength(100)
;

force.link.add(pv.Line)
//    .lineWidth(1)
    .lineWidth(function(d){return d.value*100;})
//    .fillStyle(function(d) d.value*100)
//    .strokeStyle(function() this.fillStyle().darker());
//    .title(function(d) d.value);
;

force.node.add(pv.Dot)
//    .size(function(d) (d.linkDegree + 4) * Math.pow(this.scale, -1.5))
    .size(function(d){return (d.linkDegree/50+10* Math.pow(this.scale, -1.5));})
//    .fillStyle(function(d) d.fix ? "brown" : colors(d.type))
    //.fillStyle(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
    .fillStyle(function(d){ 
                    switch(d.type) {
                        case 2: 
                            //return "rgba(120, 120, 120, .4)";
                            return "rgba(0, 255, 0, .6)";
                            break;
                        case 1:
                            //return "rgba(180, 120, 30, .4)";
                            return "rgba(255, 0, 0, .6)";
                            break;
                        case 0:
                            //return "rgba(30, 120, 180, .4)";
                            return "rgba(0, 0, 255, .6)";
                            break;
                    }
                    }
                )
    .strokeStyle(function(){return this.fillStyle().darker();})
    .lineWidth(1)
    .title(function(d){return d.linkDegree;})
    
    .anchor("center").add(pv.Label)
        .font(function(d){return 8 + "px sans-serif";})
//        .color(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
        .text(function(d){return d.nodeName;})

    .event("mousedown", pv.Behavior.drag())
    .event("drag", force);

vis.render();
};
