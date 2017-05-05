@echo OFF
ECHO Should find (12 - 4 = 8) TODOs
ECHO .
findTodos.py test_data\findTodos cs;ts;js;html;cshtml;scss;sass;css -iDesigner.cs -sobj;debug;bower_components;node_modules;tmp;temp;assets;lib;dist;published;vendor;apps_out;bin -w -y
