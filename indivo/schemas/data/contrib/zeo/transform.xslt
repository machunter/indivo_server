<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:SleepStats">
    <Models>
      <Model name="SleepStats">
        <Field name="awakenings"><xsl:value-of select='indivodoc:awakenings/text()' /></Field>
        <Field name="awakeningsZqPoints"><xsl:value-of select='indivodoc:awakeningsZqPoints/text()' /></Field>
        <Field name="bedTime"><xsl:value-of select='indivodoc:bedTime/text()' /></Field>
        <Field name="grouping"><xsl:value-of select='indivodoc:grouping/text()' /></Field>
        <Field name="morningFeel"><xsl:value-of select='indivodoc:morningFeel/text()' /></Field>
        <Field name="riseTime"><xsl:value-of select='indivodoc:riseTime/text()' /></Field>
        <Field name="startDate"><xsl:value-of select='indivodoc:startDate/text()' /></Field>
        <Field name="timeInDeep"><xsl:value-of select='indivodoc:timeInDeep/text()' /></Field>
        <Field name="timeInDeepPercentage"><xsl:value-of select='indivodoc:timeInDeepPercentage/text()' /></Field>
        <Field name="timeInDeepZqPoints"><xsl:value-of select='indivodoc:timeInDeepZqPoints/text()' /></Field>
        <Field name="timeInLight"><xsl:value-of select='indivodoc:timeInLight/text()' /></Field>
        <Field name="timeInLightPercentage"><xsl:value-of select='indivodoc:timeInLightPercentage/text()' /></Field>
        <Field name="timeInLightZqPoints"><xsl:value-of select='indivodoc:timeInLightZqPoints/text()' /></Field>
        <Field name="timeInRem"><xsl:value-of select='indivodoc:timeInRem/text()' /></Field>
        <Field name="timeInRemPercentage"><xsl:value-of select='indivodoc:timeInRemPercentage/text()' /></Field>
        <Field name="timeInRemZqPoints"><xsl:value-of select='indivodoc:timeInRemZqPoints/text()' /></Field>
        <Field name="timeInWake"><xsl:value-of select='indivodoc:timeInWake/text()' /></Field>
        <Field name="timeInWakePercentage"><xsl:value-of select='indivodoc:timeInWakePercentage/text()' /></Field>
        <Field name="timeInWakeZqPoints"><xsl:value-of select='indivodoc:timeInWakeZqPoints/text()' /></Field>
        <Field name="timeToZ"><xsl:value-of select='indivodoc:timeToZ/text()' /></Field>
        <Field name="totalZ"><xsl:value-of select='indivodoc:totalZ/text()' /></Field>
        <Field name="totalZZqPoints"><xsl:value-of select='indivodoc:totalZZqPoints/text()' /></Field>
        <Field name="zq"><xsl:value-of select='indivodoc:zq/text()' /></Field>
      </Model>
    </Models>
  </xsl:template>
</xsl:stylesheet>