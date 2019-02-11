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
      };var element = document.getElementById("83b105ba-8d79-47c9-92be-ea54ed327ef8");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid '83b105ba-8d79-47c9-92be-ea54ed327ef8' but no matching script tag was found. ")
        return false;
      }
    
      var js_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.0.3.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.3.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.3.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-gl-1.0.3.min.js"];
    
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
                    
                  var docs_json = '{"7e735dfe-9700-4a1a-8792-c10c3ea05a52":{"roots":{"references":[{"attributes":{},"id":"1736","type":"PanTool"},{"attributes":{"below":[{"id":"1725","type":"LinearAxis"}],"left":[{"id":"1730","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":700,"renderers":[{"id":"1725","type":"LinearAxis"},{"id":"1729","type":"Grid"},{"id":"1730","type":"LinearAxis"},{"id":"1734","type":"Grid"},{"id":"1744","type":"BoxAnnotation"},{"id":"1755","type":"GlyphRenderer"}],"title":{"id":"1716","type":"Title"},"toolbar":{"id":"1740","type":"Toolbar"},"x_range":{"id":"1713","type":"Range1d"},"x_scale":{"id":"1721","type":"LinearScale"},"y_range":{"id":"1714","type":"Range1d"},"y_scale":{"id":"1723","type":"LinearScale"}},"id":"1717","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"1737","type":"WheelZoomTool"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","line_alpha":1,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"1753","type":"Patch"},{"attributes":{"overlay":{"id":"1744","type":"BoxAnnotation"}},"id":"1738","type":"BoxZoomTool"},{"attributes":{"fill_alpha":0.5,"fill_color":"#1f77b4","x":{"field":"x"},"y":{"field":"y"}},"id":"1752","type":"Patch"},{"attributes":{"callback":null,"end":0.07884748542109647,"reset_end":0.07884748542109647,"reset_start":0.0,"tags":[[["line_counts_density","Density",null]]]},"id":"1714","type":"Range1d"},{"attributes":{"fill_alpha":0.2,"fill_color":"#1f77b4","line_alpha":0.2,"line_color":"black","x":{"field":"x"},"y":{"field":"y"}},"id":"1754","type":"Patch"},{"attributes":{"callback":null,"renderers":[{"id":"1755","type":"GlyphRenderer"}],"tooltips":[["line_counts","@{line_counts}"],["Density","@{line_counts_density}"]]},"id":"1715","type":"HoverTool"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1715","type":"HoverTool"},{"id":"1735","type":"SaveTool"},{"id":"1736","type":"PanTool"},{"id":"1737","type":"WheelZoomTool"},{"id":"1738","type":"BoxZoomTool"},{"id":"1739","type":"ResetTool"}]},"id":"1740","type":"Toolbar"},{"attributes":{},"id":"1750","type":"Selection"},{"attributes":{"axis_label":"line_counts","bounds":"auto","formatter":{"id":"1757","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1717","subtype":"Figure","type":"Plot"},"ticker":{"id":"1726","type":"BasicTicker"}},"id":"1725","type":"LinearAxis"},{"attributes":{},"id":"1735","type":"SaveTool"},{"attributes":{},"id":"1759","type":"BasicTickFormatter"},{"attributes":{},"id":"1726","type":"BasicTicker"},{"attributes":{"callback":null,"end":367.0147832050558,"reset_end":367.0147832050558,"reset_start":-3.014783205055803,"start":-3.014783205055803,"tags":[[["line_counts","line_counts",null]]]},"id":"1713","type":"Range1d"},{"attributes":{"source":{"id":"1749","type":"ColumnDataSource"}},"id":"1756","type":"CDSView"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"1717","subtype":"Figure","type":"Plot"},"ticker":{"id":"1731","type":"BasicTicker"}},"id":"1734","type":"Grid"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"1744","type":"BoxAnnotation"},{"attributes":{},"id":"1721","type":"LinearScale"},{"attributes":{},"id":"1723","type":"LinearScale"},{"attributes":{"plot":null,"text":"Word Counts Per Line Distribution"},"id":"1716","type":"Title"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"1717","subtype":"Figure","type":"Plot"},"ticker":{"id":"1726","type":"BasicTicker"}},"id":"1729","type":"Grid"},{"attributes":{"data_source":{"id":"1749","type":"ColumnDataSource"},"glyph":{"id":"1752","type":"Patch"},"hover_glyph":null,"muted_glyph":{"id":"1754","type":"Patch"},"nonselection_glyph":{"id":"1753","type":"Patch"},"selection_glyph":null,"view":{"id":"1756","type":"CDSView"}},"id":"1755","type":"GlyphRenderer"},{"attributes":{"callback":null,"data":{"x":{"__ndarray__":"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","dtype":"float64","shape":[200]},"y":{"__ndarray__":"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","dtype":"float64","shape":[200]}},"selected":{"id":"1750","type":"Selection"},"selection_policy":{"id":"1767","type":"UnionRenderers"}},"id":"1749","type":"ColumnDataSource"},{"attributes":{"axis_label":"Density","bounds":"auto","formatter":{"id":"1759","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"1717","subtype":"Figure","type":"Plot"},"ticker":{"id":"1731","type":"BasicTicker"}},"id":"1730","type":"LinearAxis"},{"attributes":{},"id":"1739","type":"ResetTool"},{"attributes":{},"id":"1757","type":"BasicTickFormatter"},{"attributes":{},"id":"1731","type":"BasicTicker"},{"attributes":{},"id":"1767","type":"UnionRenderers"}],"root_ids":["1717"]},"title":"Bokeh Application","version":"1.0.3"}}';
                  var render_items = [{"docid":"7e735dfe-9700-4a1a-8792-c10c3ea05a52","roots":{"1717":"83b105ba-8d79-47c9-92be-ea54ed327ef8"}}];
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
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-1.0.3.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-1.0.3.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.3.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.3.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.3.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.3.min.css");
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