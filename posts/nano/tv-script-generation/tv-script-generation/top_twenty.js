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
      };var element = document.getElementById("5894f7b4-b928-4605-9835-f7bcbfc0b940");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid '5894f7b4-b928-4605-9835-f7bcbfc0b940' but no matching script tag was found. ")
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
                    
                  var docs_json = '{"e7f672ae-7f6d-4e64-9ff8-bc761bcfded7":{"roots":{"references":[{"attributes":{"callback":null,"factors":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"],"tags":[[["Word","Word",null]]]},"id":"3042","type":"FactorRange"},{"attributes":{},"id":"3055","type":"CategoricalTicker"},{"attributes":{},"id":"3065","type":"WheelZoomTool"},{"attributes":{},"id":"3096","type":"UnionRenderers"},{"attributes":{"fill_color":{"value":"#1f77b4"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"3080","type":"VBar"},{"attributes":{"callback":null,"renderers":[{"id":"3083","type":"GlyphRenderer"}],"tooltips":[["Word","@{Word}"],["Count","@{Count}"]]},"id":"3044","type":"HoverTool"},{"attributes":{"overlay":{"id":"3072","type":"BoxAnnotation"}},"id":"3066","type":"BoxZoomTool"},{"attributes":{},"id":"3059","type":"BasicTicker"},{"attributes":{},"id":"3085","type":"CategoricalTickFormatter"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"3046","subtype":"Figure","type":"Plot"},"ticker":{"id":"3055","type":"CategoricalTicker"}},"id":"3057","type":"Grid"},{"attributes":{"below":[{"id":"3054","type":"CategoricalAxis"}],"left":[{"id":"3058","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":500,"renderers":[{"id":"3054","type":"CategoricalAxis"},{"id":"3057","type":"Grid"},{"id":"3058","type":"LinearAxis"},{"id":"3062","type":"Grid"},{"id":"3072","type":"BoxAnnotation"},{"id":"3083","type":"GlyphRenderer"}],"title":{"id":"3045","type":"Title"},"toolbar":{"id":"3068","type":"Toolbar"},"x_range":{"id":"3042","type":"FactorRange"},"x_scale":{"id":"3050","type":"CategoricalScale"},"y_range":{"id":"3043","type":"Range1d"},"y_scale":{"id":"3052","type":"LinearScale"}},"id":"3046","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"3067","type":"ResetTool"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"3046","subtype":"Figure","type":"Plot"},"ticker":{"id":"3059","type":"BasicTicker"}},"id":"3062","type":"Grid"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.1},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"3081","type":"VBar"},{"attributes":{},"id":"3087","type":"BasicTickFormatter"},{"attributes":{},"id":"3064","type":"PanTool"},{"attributes":{"callback":null,"data":{"Count":[16373,13911,12831,12096,11594,5490,5210,4741,4283,4047,3798,3250,3102,3101,3087,3030,2953,2932,2920,2714],"Word":["the","I","you","a","to","of","and","in","is","that","it","my","with","have","on","for","was","this","I&#x27;m","don&#x27;t"]},"selected":{"id":"3078","type":"Selection"},"selection_policy":{"id":"3096","type":"UnionRenderers"}},"id":"3077","type":"ColumnDataSource"},{"attributes":{"callback":null,"end":16373.0,"reset_end":16373.0,"reset_start":0,"tags":[[["Count","Count",null]]]},"id":"3043","type":"Range1d"},{"attributes":{"source":{"id":"3077","type":"ColumnDataSource"}},"id":"3084","type":"CDSView"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"3072","type":"BoxAnnotation"},{"attributes":{},"id":"3078","type":"Selection"},{"attributes":{"fill_alpha":{"value":0.2},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.2},"line_color":{"value":"black"},"top":{"field":"Count"},"width":{"value":0.8},"x":{"field":"Word"}},"id":"3082","type":"VBar"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"3044","type":"HoverTool"},{"id":"3063","type":"SaveTool"},{"id":"3064","type":"PanTool"},{"id":"3065","type":"WheelZoomTool"},{"id":"3066","type":"BoxZoomTool"},{"id":"3067","type":"ResetTool"}]},"id":"3068","type":"Toolbar"},{"attributes":{"data_source":{"id":"3077","type":"ColumnDataSource"},"glyph":{"id":"3080","type":"VBar"},"hover_glyph":null,"muted_glyph":{"id":"3082","type":"VBar"},"nonselection_glyph":{"id":"3081","type":"VBar"},"selection_glyph":null,"view":{"id":"3084","type":"CDSView"}},"id":"3083","type":"GlyphRenderer"},{"attributes":{},"id":"3063","type":"SaveTool"},{"attributes":{},"id":"3050","type":"CategoricalScale"},{"attributes":{"axis_label":"Word","bounds":"auto","formatter":{"id":"3085","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"3046","subtype":"Figure","type":"Plot"},"ticker":{"id":"3055","type":"CategoricalTicker"}},"id":"3054","type":"CategoricalAxis"},{"attributes":{"plot":null,"text":"Twenty Most Used Words"},"id":"3045","type":"Title"},{"attributes":{"axis_label":"Count","bounds":"auto","formatter":{"id":"3087","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"3046","subtype":"Figure","type":"Plot"},"ticker":{"id":"3059","type":"BasicTicker"}},"id":"3058","type":"LinearAxis"},{"attributes":{},"id":"3052","type":"LinearScale"}],"root_ids":["3046"]},"title":"Bokeh Application","version":"1.0.4"}}';
                  var render_items = [{"docid":"e7f672ae-7f6d-4e64-9ff8-bc761bcfded7","roots":{"3046":"5894f7b4-b928-4605-9835-f7bcbfc0b940"}}];
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