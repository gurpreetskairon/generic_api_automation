from xml_parser import query_xml

xml = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:ns="http://example.com/msd">
  <soap:Body>
    <ns:CourseResponse>
      <ns:courseDetails id="C123">
        <ns:participation>
          <ns:weekCode>
            <ns:tableName>MSDWeek</ns:tableName>
            <ns:value>WK1</ns:value>
            <ns:description>Week 1</ns:description>
          </ns:weekCode>
        </ns:participation>
        <ns:participation>
          <ns:weekCode>
            <ns:tableName>MSDWeek</ns:tableName>
            <ns:value>WK3</ns:value>
            <ns:description>Week 3</ns:description>
          </ns:weekCode>
        </ns:participation>
      </ns:courseDetails>
    </ns:CourseResponse>
  </soap:Body>
</soap:Envelope>"""

patterns = [
    "//weekCode/value",                   # -> WK1
    "//weekCode/description",             # -> Week 1
    "value=WK3",                          # -> {'value': 'WK3'}
    "value=WK3:-1",                       # -> dict of parent <weekCode>
    "value=WK3:-1/description",           # -> Week 3
    "//courseDetails//value=WK1:-1/description",  # -> Week 1
    "//courseDetails@id=C123",                           # -> {'@id': 'C123'} or node containing it
    "@id=C123",                         # -> dict of <courseDetails>
]

for i, pattern in enumerate(patterns, start=1):
    result = query_xml(xml, pattern)
    print(f"{i}: Pattern = {pattern}\nResult = {result}\n")
