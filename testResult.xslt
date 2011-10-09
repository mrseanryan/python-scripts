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
		
		tr.IRDsummaryHeading {
			background-color: cyan;
		}
		
		tr.IRDsFailedHeading {
			background-color: orangered;
		}
	  </style>
	  
	  <title>IRD Test Results</title>
  </head>
  <body>
  <h2>IRD Test Results</h2>

	<!-- IRD Summary ================================================ -->
	<table border="1">
    <tr class="IRDsummaryHeading">
      <th>
	  	<xsl:value-of select="count(IRDTests/IRDs/IRD)"/>
		IRDs Tested
	  </th>
    </tr>
    <tr>
      <td>
		<xsl:for-each select="IRDTests/IRDs/IRD">
			<xsl:value-of select="@name"/>
				,
			</xsl:for-each>
	  </td>
    </tr>
  </table>

	<!-- IRDs Failed ================================================ -->
	<table border="1">
    <tr class="IRDsFailedHeading">
      <th>
	  		<xsl:value-of select="count(IRDTests/IRDs/IRD[@pass='False'])"/>
			IRDs Failed
	  </th>
    </tr>
    <tr>
      <td>
		<xsl:for-each select="IRDTests/IRDs/IRD[@pass='False']">
			<xsl:value-of select="@name"/>
				,
			</xsl:for-each>
	  </td>
    </tr>
  </table>

	<!-- IRD Tests ================================================== -->
  <table border="1">
    <tr class="TestHeading">
      <th>Test ID</th>
      <th>IRD</th>
      <th>Result</th>
    </tr>
    <xsl:for-each select="IRDTests/Tests/Test">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="@IRD"/></td>
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
  </table>
	
	<table>
		<xsl:value-of select="count(//Test[@result='fail'])"/> out of  
		<xsl:value-of select="count(//Test)"/> tests failed.
	</table>

  </body>
  </html>
</xsl:template>

</xsl:stylesheet>