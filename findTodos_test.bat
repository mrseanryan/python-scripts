@echo OFF
ECHO Should find (10 - 4 = 6) TODOs
ECHO .
findTodos.py test_data\findTodos cs;ts; -iDesigner.cs -sobj;debug -w -y
