(function() {
  var fn = function() {
    
    (function(root) {
      function now() {
        return new Date();
      }
    
      var force = false;
    
      if (typeof (root._bokeh_onload_callbacks) === "undefined" || force === true) {
        root._bokeh_onload_callbacks = [];
        root._bokeh_is_loading = undefined;
      }
    
      
      
    
      
      
    
      function run_callbacks() {
        try {
          root._bokeh_onload_callbacks.forEach(function(callback) { callback() });
        }
        finally {
          delete root._bokeh_onload_callbacks
        }
        console.info("Bokeh: all callbacks have finished");
      }
    
      function load_libs(js_urls, callback) {
        root._bokeh_onload_callbacks.push(callback);
        if (root._bokeh_is_loading > 0) {
          console.log("Bokeh: BokehJS is being loaded, scheduling callback at", now());
          return null;
        }
        if (js_urls == null || js_urls.length === 0) {
          run_callbacks();
          return null;
        }
        console.log("Bokeh: BokehJS not loaded, scheduling load and callback at", now());
        root._bokeh_is_loading = js_urls.length;
        for (var i = 0; i < js_urls.length; i++) {
          var url = js_urls[i];
          var s = document.createElement('script');
          s.src = url;
          s.async = false;
          s.onreadystatechange = s.onload = function() {
            root._bokeh_is_loading--;
            if (root._bokeh_is_loading === 0) {
              console.log("Bokeh: all BokehJS libraries loaded");
              run_callbacks()
            }
          };
          s.onerror = function() {
            console.warn("failed to load library " + url);
          };
          console.log("Bokeh: injecting script tag for BokehJS library: ", url);
          document.getElementsByTagName("head")[0].appendChild(s);
        }
      };var element = document.getElementById("230997c5-e96a-4f55-b027-a3b3904c18a3");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid '230997c5-e96a-4f55-b027-a3b3904c18a3' but no matching script tag was found. ")
        return false;
      }
    
      var js_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.0.4.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.4.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.4.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-gl-1.0.4.min.js"];
    
      var inline_js = [
        function(Bokeh) {
          Bokeh.set_log_level("info");
        },
        
        function(Bokeh) {
          
        },
        
        function(Bokeh) {
          (function() {
            var fn = function() {
              Bokeh.safely(function() {
                (function(root) {
                  function embed_document(root) {
                    
                  var docs_json = '{"f5ea069f-b5cc-4666-8fa0-acfbf8f4bc5f":{"roots":{"references":[{"attributes":{"callback":null,"data":{"Count":[16373,13911,12831,12096,11594,5490,5210,4741,4283,4047,3798,3250,3102,3101,3087,3030,2953,2932,2920,2714],"Word":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"]},"selected":{"id":"1478","type":"Selection"},"selection_policy":{"id":"1494","type":"UnionRenderers"}},"id":"1477","type":"ColumnDataSource"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"1446","subtype":"Figure","type":"Plot"},"ticker":{"id":"1459","type":"BasicTicker"}},"id":"1462","type":"Grid"},{"attributes":{},"id":"1452","type":"LinearScale"},{"attributes":{},"id":"1486","type":"CategoricalTickFormatter"},{"attributes":{"axis_label":"Word","bounds":"auto","formatter":{"id":"1486","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1446","subtype":"Figure","type":"Plot"},"ticker":{"id":"1455","type":"CategoricalTicker"}},"id":"1454","type":"CategoricalAxis"},{"attributes":{"plot":null,"text":"Twenty Most Used Words"},"id":"1445","type":"Title"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1444","type":"HoverTool"},{"id":"1463","type":"SaveTool"},{"id":"1464","type":"PanTool"},{"id":"1465","type":"WheelZoomTool"},{"id":"1466","type":"BoxZoomTool"},{"id":"1467","type":"ResetTool"}]},"id":"1468","type":"Toolbar"},{"attributes":{},"id":"1463","type":"SaveTool"},{"attributes":{"axis_label":"Count","bounds":"auto","formatter":{"id":"1487","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1446","subtype":"Figure","type":"Plot"},"ticker":{"id":"1459","type":"BasicTicker"}},"id":"1458","type":"LinearAxis"},{"attributes":{"data_source":{"id":"1477","type":"ColumnDataSource"},"glyph":{"id":"1480","type":"VBar"},"hover_glyph":null,"muted_glyph":{"id":"1482","type":"VBar"},"nonselection_glyph":{"id":"1481","type":"VBar"},"selection_glyph":null,"view":{"id":"1484","type":"CDSView"}},"id":"1483","type":"GlyphRenderer"},{"attributes":{},"id":"1464","type":"PanTool"},{"attributes":{"source":{"id":"1477","type":"ColumnDataSource"}},"id":"1484","type":"CDSView"},{"attributes":{},"id":"1450","type":"CategoricalScale"},{"attributes":{},"id":"1467","type":"ResetTool"},{"attributes":{},"id":"1494","type":"UnionRenderers"},{"attributes":{},"id":"1455","type":"CategoricalTicker"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1472","type":"BoxAnnotation"},{"attributes":{},"id":"1465","type":"WheelZoomTool"},{"attributes":{},"id":"1459","type":"BasicTicker"},{"attributes":{"callback":null,"end":16373.0,"reset_end":16373.0,"reset_start":0,"tags":[[["Count","Count",null]]]},"id":"1443","type":"Range1d"},{"attributes":{},"id":"1487","type":"BasicTickFormatter"},{"attributes":{"overlay":{"id":"1472","type":"BoxAnnotation"}},"id":"1466","type":"BoxZoomTool"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"1446","subtype":"Figure","type":"Plot"},"ticker":{"id":"1455","type":"CategoricalTicker"}},"id":"1457","type":"Grid"},{"attributes":{"fill_color":{"value":"#1f77b4"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"1480","type":"VBar"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.1},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"1481","type":"VBar"},{"attributes":{"callback":null,"renderers":[{"id":"1483","type":"GlyphRenderer"}],"tooltips":[["Word","@{Word}"],["Count","@{Count}"]]},"id":"1444","type":"HoverTool"},{"attributes":{"callback":null,"factors":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"],"tags":[[["Word","Word",null]]]},"id":"1442","type":"FactorRange"},{"attributes":{"below":[{"id":"1454","type":"CategoricalAxis"}],"left":[{"id":"1458","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":700,"renderers":[{"id":"1454","type":"CategoricalAxis"},{"id":"1457","type":"Grid"},{"id":"1458","type":"LinearAxis"},{"id":"1462","type":"Grid"},{"id":"1472","type":"BoxAnnotation"},{"id":"1483","type":"GlyphRenderer"}],"title":{"id":"1445","type":"Title"},"toolbar":{"id":"1468","type":"Toolbar"},"x_range":{"id":"1442","type":"FactorRange"},"x_scale":{"id":"1450","type":"CategoricalScale"},"y_range":{"id":"1443","type":"Range1d"},"y_scale":{"id":"1452","type":"LinearScale"}},"id":"1446","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"1478","type":"Selection"},{"attributes":{"fill_alpha":{"value":0.2},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.2},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"1482","type":"VBar"}],"root_ids":["1446"]},"title":"Bokeh Application","version":"1.0.4"}}';
                  var render_items = [{"docid":"f5ea069f-b5cc-4666-8fa0-acfbf8f4bc5f","roots":{"1446":"230997c5-e96a-4f55-b027-a3b3904c18a3"}}];
                  root.Bokeh.embed.embed_items(docs_json, render_items);
                
                  }
                  if (root.Bokeh !== undefined) {
                    embed_document(root);
                  } else {
                    var attempts = 0;
                    var timer = setInterval(function(root) {
                      if (root.Bokeh !== undefined) {
                        embed_document(root);
                        clearInterval(timer);
                      }
                      attempts++;
                      if (attempts > 100) {
                        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                        clearInterval(timer);
                      }
                    }, 10, root)
                  }
                })(window);
              });
            };
            if (document.readyState != "loading") fn();
            else document.addEventListener("DOMContentLoaded", fn);
          })();
        },
        function(Bokeh) {
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-1.0.4.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-1.0.4.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.4.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.4.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.4.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.4.min.css");
        }
      ];
    
      function run_inline_js() {
        
        for (var i = 0; i < inline_js.length; i++) {
          inline_js[i].call(root, root.Bokeh);
        }
        
      }
    
      if (root._bokeh_is_loading === 0) {
        console.log("Bokeh: BokehJS loaded, going straight to plotting");
        run_inline_js();
      } else {
        load_libs(js_urls, function() {
          console.log("Bokeh: BokehJS plotting callback run at", now());
          run_inline_js();
        });
      }
    }(window));
  };
  if (document.readyState != "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
})();