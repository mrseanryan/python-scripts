SETLOCAL

SET XML_OUT_DIR=%TEMP%

SET XML_OUT=%XML_OUT_DIR%\testResults.xml

TestResults_to_XML.py > "%XML_OUT%"

copy /y  testResult.xslt    "%XML_OUT_DIR%"

explorer "%XML_OUT%"
