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
      };var element = document.getElementById("f6d6808a-e555-43f2-ad3a-a1ace816aa10");
      if (element == null) {
        console.log("Bokeh: ERROR: autoload.js configured with elementid 'f6d6808a-e555-43f2-ad3a-a1ace816aa10' but no matching script tag was found. ")
        return false;
      }
    
      var js_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.0.1.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.1.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.1.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-gl-1.0.1.min.js"];
    
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
                    
                  var docs_json = '{"701dc05e-8f90-4ef3-9746-af034416e6ed":{"roots":{"references":[{"attributes":{},"id":"1415","type":"LinearScale"},{"attributes":{},"id":"1420","type":"BasicTicker"},{"attributes":{},"id":"1429","type":"PanTool"},{"attributes":{},"id":"1451","type":"UnionRenderers"},{"attributes":{},"id":"1417","type":"LinearScale"},{"attributes":{},"id":"1430","type":"WheelZoomTool"},{"attributes":{"formatter":{"id":"1450","type":"BasicTickFormatter"},"plot":{"id":"1409","subtype":"Figure","type":"Plot"},"ticker":{"id":"1420","type":"BasicTicker"}},"id":"1419","type":"LinearAxis"},{"attributes":{},"id":"1432","type":"SaveTool"},{"attributes":{"plot":{"id":"1409","subtype":"Figure","type":"Plot"},"ticker":{"id":"1420","type":"BasicTicker"}},"id":"1423","type":"Grid"},{"attributes":{"callback":null,"data":{"color":["#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00","#00ff00"],"names":["edie","antwone","din","gunga","goldsworthy","gypo","paulie","visconti","flavia","blandings","kells","brashear","gino","deathtrap","harilal","panahi","ossessione","tsui","caruso","sabu","ahmad","khouri","dominick","aweigh","mj","mcintire","kriemhild","blackie","daisies","newcombe","kei","trelkovsky","jaffar","hilliard","gundam","bathsheba","pazu","sheeta","krell","offside","venoms","fineman","paine","pimlico","ranma","ronny","abhay","iturbi","kipling","pym","gabe","audiard","kelso","milverton","scalise","giovanna","grisby","mukhsin","feinstone","xica","moonwalker","felix","chikatilo","togar","heaton","jannings","luzhin","miklos","pidgeon","soha","matuschek","leonora","desdemona","fanfan","matador","philo","firemen","lindy","joss","microfilm","maradona","reda","gauri","bjm","capote","fido","quibble","emory","carrre","prote","coe","mcintyre","siegfried","coonskin","excellently","clutter","vance","versatility","knockout","anchors","digicorp","malfique","schlesinger","magnus","burakov","ackland","rvd","baloo","hillyer","ferdie","pakeezah","petiot","pinjar","flippen","railly","kolchak","deanna","hayworth","falco","lando","iphigenia","pappas","guerrero","burgade","iek","hobson","geer","pollak","volckman","hoechlin","korda","sammo","hewlett","naudet","nighy","sox","toughness","laputa","orked","callahan","kralik","biko","nagra","jeon","jacknife","peralta","beckett","polanski","alvin","matthau","aiello","coulouris","delpy","mathieu","firefighter","macready","janos","santos","duffell","natalia","bombshells","hulce","gaiman","yvaine","bedknobs","endor","rotj","antz","myrtle","adele","gackt","bake","gilliam","lian","bernsen","uld","egon","oro","johnnie","baton","cheh","valette","gunbuster","mcanally","calamai","hickock","ashraf","aviv","doktor","gannon","eustache","schildkraut","rotoscoped","hilda","cognac","lanisha","soutendijk","kiley","shintaro","silberling","ballantine","karas","parador","goines","grasshoppers","burman","victoria","beery","dench","partition","conroy","chavez","ratso","intricately","ingram","duprez","harriet","treaty","melancholic","embezzler","fetisov","cb","pilgrimage","tulip","pang","rien","gardenia","gialli","ishwar","cartwrights","emy","danelia","scrat","beek","kabei","laine","atoz","megs","kulkarni","bathhouse","hickam","ultimatum","mildred","fricker","emil","katsu","dev","cynics","holloway","tissues","odysseus","bouvier","luchino","girotti","mclaglen","choi","brownstone","riget","unsung","autograph","saura","sugiyama","chavo","mcdoakes","dola","broadbent","goring","adjani","boop","freebird","eglantine","oakie","gabriella","guadalcanal","yelnats","nibelungen","sputnik","bahrain","corbett","zu","abu","gandhi","sammi","warhols","delightfully","sirk","rosenstrasse","creasy","braveheart","unpretentious","kazan","strindberg","holodeck","hanlon","natures","lassalle","cacoyannis","euripides","hecht","luger","bouzaglo","mcadam","lupino","bischoff","herge","anselmo","bressart","talos","blackadder","clutters","perdition","parminder","santiago","yeon","binder","vierde","hayao","barrister","lafitte","yuzna","killian","trenholm","gallico","attila","mcphillip","balduin","poonam","vonnegut","mccoy","taker","flawless","othello","abbey","judi","natali","mahatma","jonestown","godmother","mcnally","novak","durbin","christy","cheadle","cannavale","fuller","radiant","nandini","wilhelm","rf","noriko","viennese","prologues","woronov","spacecamp","eisenhower","faultless","lok","unsurpassed","thursby","filone","ramones","eminent","soapdish","seine","taoist","huns","cookbook","waterman","sweetin","nord","showings","bazza","yasmin","stitzer","dorsey","fanshawe","pike","tykwer","hoss","dorfman","sjoman","antonietta","faust","arrondissement","hanka","muska","tetsur","stockwell","gorris","fellowes","regent","bartel","pei","zp","nyqvist","leaud","dragoon","gracia","bruhl","bolan","starewicz","atul","capano","vadar","gundams","hallen","shep","pita","cal","reservations","elsa","johnston","brisson","schmid","marylee","oberon","winchester","jabba","chamberlain","shetty","ori","calvet","chamberlains","rozsa","unparalleled","separating","bowser","hardworking","quebec","rea","yam","beale","tigerland","pquerette","virile","jud","rollicking","wuhl","coop","apatow","margo","montrose","ungar","haines","arzenta","manny","ref","rhapsody","levitt","strombel","kidd","strickland","waterloo","bannister","colman","broinowski","floraine","waxworks","ernesto","athens","ankush","flamenco","hundstage","katey","sikes","restoring","parkins","mariner","hickcock","fps","topher","tollinger","overpopulation","ghibli","girlfight","rudyard","gwizdo","milyang","hisaishi","maetel","pasdar","tam","philipps","pneumonic","poldi","hemo","swashbucklers","manfred","gervais","portobello","spanky","gilberte","randell","homeward"],"x1":{"__ndarray__":"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","dtype":"float32","shape":[494]},"x2":{"__ndarray__":"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","dtype":"float32","shape":[494]}},"selected":{"id":"1452","type":"Selection"},"selection_policy":{"id":"1451","type":"UnionRenderers"}},"id":"1438","type":"ColumnDataSource"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"1429","type":"PanTool"},{"id":"1430","type":"WheelZoomTool"},{"id":"1431","type":"ResetTool"},{"id":"1432","type":"SaveTool"}]},"id":"1433","type":"Toolbar"},{"attributes":{},"id":"1431","type":"ResetTool"},{"attributes":{"formatter":{"id":"1448","type":"BasicTickFormatter"},"plot":{"id":"1409","subtype":"Figure","type":"Plot"},"ticker":{"id":"1425","type":"BasicTicker"}},"id":"1424","type":"LinearAxis"},{"attributes":{"below":[{"id":"1419","type":"LinearAxis"}],"left":[{"id":"1424","type":"LinearAxis"}],"plot_height":1000,"plot_width":1000,"renderers":[{"id":"1419","type":"LinearAxis"},{"id":"1423","type":"Grid"},{"id":"1424","type":"LinearAxis"},{"id":"1428","type":"Grid"},{"id":"1442","type":"GlyphRenderer"},{"id":"1444","type":"LabelSet"}],"title":{"id":"1408","type":"Title"},"toolbar":{"id":"1433","type":"Toolbar"},"toolbar_location":"above","x_range":{"id":"1411","type":"DataRange1d"},"x_scale":{"id":"1415","type":"LinearScale"},"y_range":{"id":"1413","type":"DataRange1d"},"y_scale":{"id":"1417","type":"LinearScale"}},"id":"1409","subtype":"Figure","type":"Plot"},{"attributes":{"fill_color":{"field":"color"},"line_color":{"value":"#1f77b4"},"size":{"units":"screen","value":8},"x":{"field":"x1"},"y":{"field":"x2"}},"id":"1440","type":"Scatter"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#1f77b4"},"line_alpha":{"value":0.1},"line_color":{"value":"#1f77b4"},"size":{"units":"screen","value":8},"x":{"field":"x1"},"y":{"field":"x2"}},"id":"1441","type":"Scatter"},{"attributes":{},"id":"1425","type":"BasicTicker"},{"attributes":{},"id":"1452","type":"Selection"},{"attributes":{"plot":null,"text":"vector T-SNE for most polarized words"},"id":"1408","type":"Title"},{"attributes":{},"id":"1448","type":"BasicTickFormatter"},{"attributes":{"data_source":{"id":"1438","type":"ColumnDataSource"},"glyph":{"id":"1440","type":"Scatter"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"1441","type":"Scatter"},"selection_glyph":null,"view":{"id":"1443","type":"CDSView"}},"id":"1442","type":"GlyphRenderer"},{"attributes":{"dimension":1,"plot":{"id":"1409","subtype":"Figure","type":"Plot"},"ticker":{"id":"1425","type":"BasicTicker"}},"id":"1428","type":"Grid"},{"attributes":{"callback":null},"id":"1411","type":"DataRange1d"},{"attributes":{"source":{"id":"1438","type":"ColumnDataSource"}},"id":"1443","type":"CDSView"},{"attributes":{"plot":{"id":"1409","subtype":"Figure","type":"Plot"},"source":{"id":"1438","type":"ColumnDataSource"},"text":{"field":"names"},"text_align":"center","text_color":{"value":"#555555"},"text_font_size":{"value":"8pt"},"x":{"field":"x1"},"y":{"field":"x2"},"y_offset":{"value":6}},"id":"1444","type":"LabelSet"},{"attributes":{"callback":null},"id":"1413","type":"DataRange1d"},{"attributes":{},"id":"1450","type":"BasicTickFormatter"}],"root_ids":["1409"]},"title":"Bokeh Application","version":"1.0.1"}}';
                  var render_items = [{"docid":"701dc05e-8f90-4ef3-9746-af034416e6ed","roots":{"1409":"f6d6808a-e555-43f2-ad3a-a1ace816aa10"}}];
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
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-1.0.1.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-1.0.1.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.1.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.0.1.min.css");
          console.log("Bokeh: injecting CSS: https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.1.min.css");
          Bokeh.embed.inject_css("https://cdn.pydata.org/bokeh/release/bokeh-tables-1.0.1.min.css");
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