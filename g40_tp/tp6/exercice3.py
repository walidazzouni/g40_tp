html = """<html>
<body>
<h1>Bonjour</h1>
</body>
</html>"""

headers = {
    "Server": "PythonTPServer",
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": str(len(html.encode("utf-8"))),
    "Connection": "close"
}

rep = format_http_response(1, 200, "OK", headers, html)
print(rep)
