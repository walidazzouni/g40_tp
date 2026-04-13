from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == "POST":
        login = request.POST.get("login", "")
        password = request.POST.get("password", "")

        return HttpResponse(f"""<!DOCTYPE html>
<html>
<body>
    <h2>Connexion reçue</h2>
    <p><b>Login :</b> {login}</p>
    <p><b>Mot de passe :</b> {password}</p>
</body>
</html>""")

    return HttpResponse("""<!DOCTYPE html>
<html>
<body>

<h2>Connexion au chat</h2>

<form method="post" action="/chat/">
    <label>Login :</label><br>
    <input type="text" name="login"><br><br>

    <label>Mot de passe :</label><br>
    <input type="password" name="password"><br><br>

    <button type="submit">Se connecter</button>
    <button type="reset">Annuler</button>
</form>

</body>
</html>""")


def page_404(request, exception):
    return HttpResponseNotFound("""<!DOCTYPE html>
<html>
<body>
    <h1>404 Not Found</h1>
</body>
</html>""")