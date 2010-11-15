// last
//var w = document.body.clientWidth,
//    h = document.body.clientHeight,
function tocolor(d){ 
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
//////////////////////////////////////////////////////////////////////////////

function generate_graph(jsondata){
	//var w = document.body.clientWidth,
	//h = document.body.clientHeight,
//	var w = 700,
//	    h = 700,
//	    colors = pv.Colors.category19();
	alert("en generate_graph");
	var vis = new pv.Panel()
		.width(window.innerWidth)
	    .height(window.innerHeight)	
	    .fillStyle("white")
	    .event("mousedown", pv.Behavior.pan())
	    .event("mousewheel", pv.Behavior.zoom());
	
	var force = vis.add(pv.Layout.Force)
	    .nodes(jsondata.nodes
	        .sort(function(a, b) b - a))
	    .links(jsondata.links)
	//    .label("Hola")
	    .iterations(150)
	//    .springConstant(0.05);
	    .springLength(100)
	;
	
	force.link.add(pv.Line)
	//    .lineWidth(1)
	    .lineWidth(function(d) d.value*1000)
	    .fillStyle(function() "rgba(182, 182, 182, .6)")
		//.title(function(d) d.value)
//		.anchor("center").add(pv.Label)
//		  .font(function(d) 8 + "px sans-serif")
//		  .text(function(d) d.value)
		//.strokeStyle(function() this.fillStyle().darker())
	    .event("mouseover", function() this.strokeStyle(function() this.fillStyle().darker())) // override
	    .event("mouseout", function() this.strokeStyle(function() this.fillStyle())) // restore
	   
	;
	
	force.node.add(pv.Dot)
	//    .size(function(d) (d.linkDegree + 4) * Math.pow(this.scale, -1.5))
	    .size(function(d) (d.linkDegree/50+10* Math.pow(this.scale, -1.5)))
	//    .fillStyle(function(d) d.fix ? "brown" : colors(d.type))
	    //.fillStyle(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
	    .fillStyle(function(d) (tocolor(d))
	                )

//	    .event("mousedown", pv.Behavior.drag())
//	    .event("drag", force)
//	    .event("dblclick", function(d) (d.toggle(pv.event.altKey), layout.reset()))				
				
//	    .event("mouseover", function() this.fillStyle("orange")) // override
//	    .event("mouseout", function(d) this.fillStyle(tocolor(d))) // restore

	    
	  		//.event("mouseover", alert("orange")) // override
		  	
//	    .def("active", false)
////		.event("mouseover", function() this.parent.active(true))
////        .event("mouseout", function() this.parent.active(false))
		
		.cursor("pointer")
		.event("click", function(d) {
            var list = self.location.href.split("/");
    		self.location = list[0]+"//"+list[2]+"/rest/"+list[4]+"/"+list[7]+"/"+list[8] //d.id
				})

	    .strokeStyle(function() this.fillStyle().darker())
	    .lineWidth(1)
	    .title(function(d) d.linkDegree)
	    
	    .anchor("center").add(pv.Label)
	        .font(function(d) 8 + "px sans-serif")
	//        .color(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
	        .text(function(d) d.nodeName)
	
	    .event("mousedown", pv.Behavior.drag())
	    .event("drag", force);
	
	vis.render();
}
//////////////////////////////////////////////////////////////////////////////

function render_graph(){
	//var w = document.body.clientWidth,
	//h = document.body.clientHeight,
//	var w = 700,
//	    h = 700,
//	    colors = pv.Colors.category19();
	
	var vis = new pv.Panel()
		.width(window.innerWidth)
	    .height(window.innerHeight)	
	    .fillStyle("white")
	    .event("mousedown", pv.Behavior.pan())
	    .event("mousewheel", pv.Behavior.zoom());
	
	var force = vis.add(pv.Layout.Force)
	    .nodes(jsondata.nodes
	        .sort(function(a, b) b - a))
	    .links(jsondata.links)
	//    .label("Hola")
	    .iterations(150)
	//    .springConstant(0.05);
	    .springLength(100)
	;
	
	force.link.add(pv.Line)
	//    .lineWidth(1)
	    .lineWidth(function(d) d.value*1000)
	    .fillStyle(function() "rgba(182, 182, 182, .6)")
		//.title(function(d) d.value)
//		.anchor("center").add(pv.Label)
//		  .font(function(d) 8 + "px sans-serif")
//		  .text(function(d) d.value)
		//.strokeStyle(function() this.fillStyle().darker())
	    .event("mouseover", function() this.strokeStyle(function() this.fillStyle().darker())) // override
	    .event("mouseout", function() this.strokeStyle(function() this.fillStyle())) // restore
	   
	;
	
	force.node.add(pv.Dot)
	//    .size(function(d) (d.linkDegree + 4) * Math.pow(this.scale, -1.5))
	    .size(function(d) (d.linkDegree/50+10* Math.pow(this.scale, -1.5)))
	//    .fillStyle(function(d) d.fix ? "brown" : colors(d.type))
	    //.fillStyle(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
	    .fillStyle(function(d) (tocolor(d))
	                )

//	    .event("mousedown", pv.Behavior.drag())
//	    .event("drag", force)
//	    .event("dblclick", function(d) (d.toggle(pv.event.altKey), layout.reset()))				
				
//	    .event("mouseover", function() this.fillStyle("orange")) // override
//	    .event("mouseout", function(d) this.fillStyle(tocolor(d))) // restore

	    
	  		//.event("mouseover", alert("orange")) // override
		  	
//	    .def("active", false)
////		.event("mouseover", function() this.parent.active(true))
////        .event("mouseout", function() this.parent.active(false))
		
		.cursor("pointer")
		.event("click", function(d) {
            var list = self.location.href.split("/");
    		self.location = list[0]+"//"+list[2]+"/rest/"+list[4]+"/"+list[7]+"/"+list[8] //d.id
				})

	    .strokeStyle(function() this.fillStyle().darker())
	    .lineWidth(1)
	    .title(function(d) d.linkDegree)
	    
	    .anchor("center").add(pv.Label)
	        .font(function(d) 8 + "px sans-serif")
	//        .color(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
	        .text(function(d) d.nodeName)
	
	    .event("mousedown", pv.Behavior.drag())
	    .event("drag", force);
	
	vis.render();
}
//////////////////////////////////////////////////////////////////////////////
// with ids: http://groups.google.com/group/protovis/browse_thread/thread/9898441167f3657c/08f1b2798cf7f7ae

function render_graph_customids(){
	var root = pv.dom(jsondata).root("svgroot");
	root.toggle(true);
	root.toggle();
	//var w = document.body.clientWidth,
	//h = document.body.clientHeight,
//	var w = 700,
//	h = 700,
//	colors = pv.Colors.category19();
	
	var vis = new pv.Panel()
//		.width(w)
//		.height(h)
    	.width(window.innerWidth)
        .height(window.innerHeight)	
		.fillStyle("white")
		.event("mousedown", pv.Behavior.pan())
		.event("mousewheel", pv.Behavior.zoom())
	;
	
	
	var idToNode = {}; // map from id -> node 
	window.idToNode = idToNode;
	for (var i = 0; i < jsondata.nodes.length; i++) { 
	    var n = jsondata.nodes[i]; 
	    window.n = n;
	    idToNode[n.id] = n; 
	} 
	for (var i = 0; i < jsondata.links.length; i++) { 
	    var l = jsondata.links[i]; 
	    l.sourceNode = idToNode[l.sourceId]; 
	    l.targetNode = idToNode[l.targetId]; 
	} 
	
	var force = vis.add(pv.Layout.Force)
		.nodes(jsondata.nodes
		  .sort(function(a, b) b - a))
		.links(jsondata.links)
		//.label("Hola")
		.iterations(150)
		//.springConstant(0.05);
		.springLength(100)
	;
	
	force.link.add(pv.Line)
		//.lineWidth(1)
		.lineWidth(function(d) d.value*100)
		.fillStyle(function() "rgba(182, 182, 182, .6)")
		//.title(function(d) d.value)
//		.anchor("center").add(pv.Label)
//		  .font(function(d) 8 + "px sans-serif")
//		  .text(function(d) d.value)
		//.strokeStyle(function() this.fillStyle().darker())
	    .event("mouseover", function() this.strokeStyle(function() this.fillStyle().darker())) // override
	    .event("mouseout", function() this.strokeStyle(function() this.fillStyle())) // restore
	    
	;
	
	force.node.add(pv.Dot)
		//.size(function(d) (d.linkDegree + 4) * Math.pow(this.scale, -1.5))
		.size(function(d) (d.linkDegree/50 +10* Math.pow(this.scale, -1.5)))

		//.fillStyle(function(d) d.fix ? "brown" : colors(d.type))
		//.fillStyle(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
		.fillStyle(function(d) (tocolor(d))
				)
//		  		.event("mousedown", pv.Behavior.drag())
//		  		.event("drag", force)
//  		.event("mousedown", pv.Behavior.select())
//  		.event("select", force) //function() this.parent
	
//	    .event("mousedown", pv.Behavior.drag())
//	    .event("drag", force)
//	    .event("dblclick", function(d) (d.toggle(pv.event.altKey), layout.reset()))				
				
	    .event("mouseover", function() this.fillStyle("orange")) // override
	    .event("mouseout", function(d) this.fillStyle(tocolor(d))) // restore

	    
	  		//.event("mouseover", alert("orange")) // override
		  	
//	    .def("active", false)
////		.event("mouseover", function() this.parent.active(true))
////        .event("mouseout", function() this.parent.active(false))
		
		.cursor("pointer")
		.event("click", function(d) {
            var list = self.location.href.split("/");
    		self.location = list[0]+"//"+list[2]+"/rest/"+list[4]+"/"+list[7]+"/"+list[8] //d.id
				})

		.strokeStyle(function() this.fillStyle().darker())
		.lineWidth(1)
		.title(function(d) d.linkDegree)
		
		.anchor("center").add(pv.Label)
		  .font(function(d) 8 + "px sans-serif")
		//  .color(function(d) d.type ? "rgba(30, 120, 180, .4)" : "rgba(180, 120, 30, .4)")
		  .text(function(d) d.nodeName)

//  force.node.add(pv.Image)
//    .imageHeight(4)
//    .imageWidth(4)
//    .url("http://vis.stanford.edu/protovis/ex/stanford.png")
//    .cursor("pointer")
//    .title("Go to stanford.edu")
//    .event("mouseover", function() self.status = "Go to \"http://stanford.edu\"")
//    .event("mouseout", function() self.status = "")
//    .event("click", function() self.location = "http://stanford.edu")
    
	;
	vis.render();
}