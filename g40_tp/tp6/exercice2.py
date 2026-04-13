def format_http_response(version, status_code, status_message, headers, body):
    # Version HTTP
    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    # Première ligne
    response = f"{http_version} {status_code} {status_message}\r\n"

    # Headers
    for key, value in headers.items():
        response += f"{key}: {value}\r\n"

    # Ligne vide + body
    response += "\r\n"
    response += body

    return response
#exemple
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