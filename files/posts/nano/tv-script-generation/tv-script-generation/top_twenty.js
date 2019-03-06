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
      };var element = document.getElementById("bdb2cdbb-c979-49d2-975e-6c03d12c95b7");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid 'bdb2cdbb-c979-49d2-975e-6c03d12c95b7' but no matching script tag was found. ")
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
                    
                  var docs_json = '{"aa4f29c4-58a0-4079-9c9c-e879079d344f":{"roots":{"references":[{"attributes":{},"id":"2506","type":"CategoricalScale"},{"attributes":{"overlay":{"id":"2528","type":"BoxAnnotation"}},"id":"2522","type":"BoxZoomTool"},{"attributes":{},"id":"2515","type":"BasicTicker"},{"attributes":{"data_source":{"id":"2533","type":"ColumnDataSource"},"glyph":{"id":"2536","type":"VBar"},"hover_glyph":null,"muted_glyph":{"id":"2538","type":"VBar"},"nonselection_glyph":{"id":"2537","type":"VBar"},"selection_glyph":null,"view":{"id":"2540","type":"CDSView"}},"id":"2539","type":"GlyphRenderer"},{"attributes":{"callback":null,"end":16373.0,"reset_end":16373.0,"reset_start":0,"tags":[[["Count","Count",null]]]},"id":"2499","type":"Range1d"},{"attributes":{"fill_alpha":{"value":0.2},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.2},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"2538","type":"VBar"},{"attributes":{"fill_color":{"value":"#1f77b4"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"2536","type":"VBar"},{"attributes":{"axis_label":"Word","bounds":"auto","formatter":{"id":"2541","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"2502","subtype":"Figure","type":"Plot"},"ticker":{"id":"2511","type":"CategoricalTicker"}},"id":"2510","type":"CategoricalAxis"},{"attributes":{},"id":"2541","type":"CategoricalTickFormatter"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"2502","subtype":"Figure","type":"Plot"},"ticker":{"id":"2515","type":"BasicTicker"}},"id":"2518","type":"Grid"},{"attributes":{},"id":"2523","type":"ResetTool"},{"attributes":{},"id":"2520","type":"PanTool"},{"attributes":{"callback":null,"renderers":[{"id":"2539","type":"GlyphRenderer"}],"tooltips":[["Word","@{Word}"],["Count","@{Count}"]]},"id":"2500","type":"HoverTool"},{"attributes":{},"id":"2543","type":"BasicTickFormatter"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"2502","subtype":"Figure","type":"Plot"},"ticker":{"id":"2511","type":"CategoricalTicker"}},"id":"2513","type":"Grid"},{"attributes":{},"id":"2534","type":"Selection"},{"attributes":{},"id":"2511","type":"CategoricalTicker"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"2528","type":"BoxAnnotation"},{"attributes":{"below":[{"id":"2510","type":"CategoricalAxis"}],"left":[{"id":"2514","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":500,"renderers":[{"id":"2510","type":"CategoricalAxis"},{"id":"2513","type":"Grid"},{"id":"2514","type":"LinearAxis"},{"id":"2518","type":"Grid"},{"id":"2528","type":"BoxAnnotation"},{"id":"2539","type":"GlyphRenderer"}],"title":{"id":"2501","type":"Title"},"toolbar":{"id":"2524","type":"Toolbar"},"x_range":{"id":"2498","type":"FactorRange"},"x_scale":{"id":"2506","type":"CategoricalScale"},"y_range":{"id":"2499","type":"Range1d"},"y_scale":{"id":"2508","type":"LinearScale"}},"id":"2502","subtype":"Figure","type":"Plot"},{"attributes":{"callback":null,"factors":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"],"tags":[[["Word","Word",null]]]},"id":"2498","type":"FactorRange"},{"attributes":{},"id":"2519","type":"SaveTool"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.1},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"2537","type":"VBar"},{"attributes":{"source":{"id":"2533","type":"ColumnDataSource"}},"id":"2540","type":"CDSView"},{"attributes":{"plot":null,"text":"Twenty Most Used Words"},"id":"2501","type":"Title"},{"attributes":{"callback":null,"data":{"Count":[16373,13911,12831,12096,11594,5490,5210,4741,4283,4047,3798,3250,3102,3101,3087,3030,2953,2932,2920,2714],"Word":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"]},"selected":{"id":"2534","type":"Selection"},"selection_policy":{"id":"2550","type":"UnionRenderers"}},"id":"2533","type":"ColumnDataSource"},{"attributes":{},"id":"2550","type":"UnionRenderers"},{"attributes":{},"id":"2521","type":"WheelZoomTool"},{"attributes":{},"id":"2508","type":"LinearScale"},{"attributes":{"axis_label":"Count","bounds":"auto","formatter":{"id":"2543","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"2502","subtype":"Figure","type":"Plot"},"ticker":{"id":"2515","type":"BasicTicker"}},"id":"2514","type":"LinearAxis"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"2500","type":"HoverTool"},{"id":"2519","type":"SaveTool"},{"id":"2520","type":"PanTool"},{"id":"2521","type":"WheelZoomTool"},{"id":"2522","type":"BoxZoomTool"},{"id":"2523","type":"ResetTool"}]},"id":"2524","type":"Toolbar"}],"root_ids":["2502"]},"title":"Bokeh Application","version":"1.0.4"}}';
                  var render_items = [{"docid":"aa4f29c4-58a0-4079-9c9c-e879079d344f","roots":{"2502":"bdb2cdbb-c979-49d2-975e-6c03d12c95b7"}}];
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