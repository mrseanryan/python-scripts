<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <head>
	   <style type="text/css">
		p.fail {
			background-color: orangered;
			}
		p.pass {
			background-color: lime;
			}
		tr.TestHeading {
			background-color: cyan;
		}
	  </style>
  </head>
  <body>
  <h2>Test Results</h2>
  <table border="1">
    <tr class="TestHeading">
      <th>Test ID</th>
      <th>Result</th>
    </tr>
	
    <xsl:for-each select="Tests/Test">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td>	  
		<xsl:choose>
			<xsl:when test="@result = 'fail' ">
				<p class="fail">Fail</p>
			</xsl:when>
			<xsl:otherwise>
				<p class="pass">Pass</p>
			</xsl:otherwise>
		</xsl:choose>
	  </td>
    </tr>
    </xsl:for-each>
	
	<table>

	<xsl:value-of select="count(//Test[@result='fail'])"/> out of  
	<xsl:value-of select="count(//Test)"/> tests failed.

	</table>
	
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>