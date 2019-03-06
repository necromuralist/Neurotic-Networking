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
      };var element = document.getElementById("ac2d294c-56ee-4a11-ad9d-5f3898591e84");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid 'ac2d294c-56ee-4a11-ad9d-5f3898591e84' but no matching script tag was found. ")
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
                    
                  var docs_json = '{"da7c8890-ad47-45d1-8a31-ef24fdbe6804":{"roots":{"references":[{"attributes":{"callback":null,"end":0.07884748542109649,"reset_end":0.07884748542109649,"reset_start":0.0,"tags":[[["line_counts_density","Density",null]]]},"id":"2106","type":"Range1d"},{"attributes":{"data_source":{"id":"2141","type":"ColumnDataSource"},"glyph":{"id":"2144","type":"Patch"},"hover_glyph":null,"muted_glyph":{"id":"2146","type":"Patch"},"nonselection_glyph":{"id":"2145","type":"Patch"},"selection_glyph":null,"view":{"id":"2148","type":"CDSView"}},"id":"2147","type":"GlyphRenderer"},{"attributes":{},"id":"2129","type":"WheelZoomTool"},{"attributes":{},"id":"2113","type":"LinearScale"},{"attributes":{},"id":"2151","type":"BasicTickFormatter"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"2109","subtype":"Figure","type":"Plot"},"ticker":{"id":"2118","type":"BasicTicker"}},"id":"2121","type":"Grid"},{"attributes":{"overlay":{"id":"2136","type":"BoxAnnotation"}},"id":"2130","type":"BoxZoomTool"},{"attributes":{},"id":"2123","type":"BasicTicker"},{"attributes":{"source":{"id":"2141","type":"ColumnDataSource"}},"id":"2148","type":"CDSView"},{"attributes":{},"id":"2131","type":"ResetTool"},{"attributes":{},"id":"2118","type":"BasicTicker"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"2109","subtype":"Figure","type":"Plot"},"ticker":{"id":"2123","type":"BasicTicker"}},"id":"2126","type":"Grid"},{"attributes":{"axis_label":"Density","bounds":"auto","formatter":{"id":"2151","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"2109","subtype":"Figure","type":"Plot"},"ticker":{"id":"2123","type":"BasicTicker"}},"id":"2122","type":"LinearAxis"},{"attributes":{"callback":null,"data":{"x":{"__ndarray__":"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","dtype":"float64","shape":[200]},"y":{"__ndarray__":"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","dtype":"float64","shape":[200]}},"selected":{"id":"2142","type":"Selection"},"selection_policy":{"id":"2158","type":"UnionRenderers"}},"id":"2141","type":"ColumnDataSource"},{"attributes":{},"id":"2149","type":"BasicTickFormatter"},{"attributes":{},"id":"2115","type":"LinearScale"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"2107","type":"HoverTool"},{"id":"2127","type":"SaveTool"},{"id":"2128","type":"PanTool"},{"id":"2129","type":"WheelZoomTool"},{"id":"2130","type":"BoxZoomTool"},{"id":"2131","type":"ResetTool"}]},"id":"2132","type":"Toolbar"},{"attributes":{"below":[{"id":"2117","type":"LinearAxis"}],"left":[{"id":"2122","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"renderers":[{"id":"2117","type":"LinearAxis"},{"id":"2121","type":"Grid"},{"id":"2122","type":"LinearAxis"},{"id":"2126","type":"Grid"},{"id":"2136","type":"BoxAnnotation"},{"id":"2147","type":"GlyphRenderer"}],"title":{"id":"2108","type":"Title"},"toolbar":{"id":"2132","type":"Toolbar"},"x_range":{"id":"2105","type":"Range1d"},"x_scale":{"id":"2113","type":"LinearScale"},"y_range":{"id":"2106","type":"Range1d"},"y_scale":{"id":"2115","type":"LinearScale"}},"id":"2109","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"2142","type":"Selection"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"2136","type":"BoxAnnotation"},{"attributes":{"axis_label":"line_counts","bounds":"auto","formatter":{"id":"2149","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"2109","subtype":"Figure","type":"Plot"},"ticker":{"id":"2118","type":"BasicTicker"}},"id":"2117","type":"LinearAxis"},{"attributes":{"callback":null,"end":367.0147832050558,"reset_end":367.0147832050558,"reset_start":-3.014783205055803,"start":-3.014783205055803,"tags":[[["line_counts","line_counts",null]]]},"id":"2105","type":"Range1d"},{"attributes":{"callback":null,"renderers":[{"id":"2147","type":"GlyphRenderer"}],"tooltips":[["line_counts","@{line_counts}"],["Density","@{line_counts_density}"]]},"id":"2107","type":"HoverTool"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","x":{"field":"x"},"y":{"field":"y"}},"id":"2144","type":"Patch"},{"attributes":{},"id":"2127","type":"SaveTool"},{"attributes":{"plot":null,"text":"Word Counts Per Line Distribution"},"id":"2108","type":"Title"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","line_alpha":1,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"2145","type":"Patch"},{"attributes":{},"id":"2128","type":"PanTool"},{"attributes":{},"id":"2158","type":"UnionRenderers"},{"attributes":{"fill_alpha":0.2,"fill_color":"#1f77b4","line_alpha":0.2,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"2146","type":"Patch"}],"root_ids":["2109"]},"title":"Bokeh Application","version":"1.0.4"}}';
                  var render_items = [{"docid":"da7c8890-ad47-45d1-8a31-ef24fdbe6804","roots":{"2109":"ac2d294c-56ee-4a11-ad9d-5f3898591e84"}}];
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