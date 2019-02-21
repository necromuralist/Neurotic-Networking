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
      };var element = document.getElementById("773c7916-deec-4585-ab46-ea42b196f1dd");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid '773c7916-deec-4585-ab46-ea42b196f1dd' but no matching script tag was found. ")
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
                    
                  var docs_json = '{"3cf73876-3f75-4923-a418-f5c609e0ddd4":{"roots":{"references":[{"attributes":{},"id":"1102","type":"UnionRenderers"},{"attributes":{},"id":"1086","type":"Selection"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1080","type":"BoxAnnotation"},{"attributes":{},"id":"1095","type":"BasicTickFormatter"},{"attributes":{},"id":"1059","type":"LinearScale"},{"attributes":{"axis_label":"line_counts","bounds":"auto","formatter":{"id":"1093","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1053","subtype":"Figure","type":"Plot"},"ticker":{"id":"1062","type":"BasicTicker"}},"id":"1061","type":"LinearAxis"},{"attributes":{"callback":null,"end":0.0788474854210965,"reset_end":0.0788474854210965,"reset_start":0.0,"tags":[[["line_counts_density","Density",null]]]},"id":"1050","type":"Range1d"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1051","type":"HoverTool"},{"id":"1071","type":"SaveTool"},{"id":"1072","type":"PanTool"},{"id":"1073","type":"WheelZoomTool"},{"id":"1074","type":"BoxZoomTool"},{"id":"1075","type":"ResetTool"}]},"id":"1076","type":"Toolbar"},{"attributes":{},"id":"1071","type":"SaveTool"},{"attributes":{},"id":"1062","type":"BasicTicker"},{"attributes":{"callback":null,"end":367.0147832050558,"reset_end":367.0147832050558,"reset_start":-3.014783205055803,"start":-3.014783205055803,"tags":[[["line_counts","line_counts",null]]]},"id":"1049","type":"Range1d"},{"attributes":{"data_source":{"id":"1085","type":"ColumnDataSource"},"glyph":{"id":"1088","type":"Patch"},"hover_glyph":null,"muted_glyph":{"id":"1090","type":"Patch"},"nonselection_glyph":{"id":"1089","type":"Patch"},"selection_glyph":null,"view":{"id":"1092","type":"CDSView"}},"id":"1091","type":"GlyphRenderer"},{"attributes":{},"id":"1072","type":"PanTool"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"1053","subtype":"Figure","type":"Plot"},"ticker":{"id":"1062","type":"BasicTicker"}},"id":"1065","type":"Grid"},{"attributes":{"source":{"id":"1085","type":"ColumnDataSource"}},"id":"1092","type":"CDSView"},{"attributes":{"callback":null,"renderers":[{"id":"1091","type":"GlyphRenderer"}],"tooltips":[["line_counts","@{line_counts}"],["Density","@{line_counts_density}"]]},"id":"1051","type":"HoverTool"},{"attributes":{"axis_label":"Density","bounds":"auto","formatter":{"id":"1095","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1053","subtype":"Figure","type":"Plot"},"ticker":{"id":"1067","type":"BasicTicker"}},"id":"1066","type":"LinearAxis"},{"attributes":{},"id":"1073","type":"WheelZoomTool"},{"attributes":{"callback":null,"data":{"x":{"__ndarray__":"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","dtype":"float64","shape":[200]},"y":{"__ndarray__":"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","dtype":"float64","shape":[200]}},"selected":{"id":"1086","type":"Selection"},"selection_policy":{"id":"1102","type":"UnionRenderers"}},"id":"1085","type":"ColumnDataSource"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","line_alpha":1,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"1089","type":"Patch"},{"attributes":{"below":[{"id":"1061","type":"LinearAxis"}],"left":[{"id":"1066","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":700,"renderers":[{"id":"1061","type":"LinearAxis"},{"id":"1065","type":"Grid"},{"id":"1066","type":"LinearAxis"},{"id":"1070","type":"Grid"},{"id":"1080","type":"BoxAnnotation"},{"id":"1091","type":"GlyphRenderer"}],"title":{"id":"1052","type":"Title"},"toolbar":{"id":"1076","type":"Toolbar"},"x_range":{"id":"1049","type":"Range1d"},"x_scale":{"id":"1057","type":"LinearScale"},"y_range":{"id":"1050","type":"Range1d"},"y_scale":{"id":"1059","type":"LinearScale"}},"id":"1053","subtype":"Figure","type":"Plot"},{"attributes":{"overlay":{"id":"1080","type":"BoxAnnotation"}},"id":"1074","type":"BoxZoomTool"},{"attributes":{},"id":"1067","type":"BasicTicker"},{"attributes":{"fill_alpha":0.2,"fill_color":"#1f77b4","line_alpha":0.2,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"1090","type":"Patch"},{"attributes":{"plot":null,"text":"Word Counts Per Line Distribution"},"id":"1052","type":"Title"},{"attributes":{},"id":"1075","type":"ResetTool"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"1053","subtype":"Figure","type":"Plot"},"ticker":{"id":"1067","type":"BasicTicker"}},"id":"1070","type":"Grid"},{"attributes":{},"id":"1093","type":"BasicTickFormatter"},{"attributes":{},"id":"1057","type":"LinearScale"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","x":{"field":"x"},"y":{"field":"y"}},"id":"1088","type":"Patch"}],"root_ids":["1053"]},"title":"Bokeh Application","version":"1.0.4"}}';
                  var render_items = [{"docid":"3cf73876-3f75-4923-a418-f5c609e0ddd4","roots":{"1053":"773c7916-deec-4585-ab46-ea42b196f1dd"}}];
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