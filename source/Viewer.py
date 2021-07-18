import re

text = """testo di prova
senza tag,
<layout(size=10,
color="red")>      Testo di
prova con tag;
</layout> altro testo senza tag"""

# --- separazione elementi -------------------------------------------------------------------------------
lista = []
flag = 0
for match in re.finditer(r'</?[a-zA-Z]*\s*(\((\s*[a-zA-Z]*[0-9]*\=*\,*\'*\"*)*\))?>', text):
    start, end = match.span()
    print(match)
    lista.append(text[flag:start])
    lista.append(text[start:end])
    flag = end
lista.append(text[flag:])

# --- elaborazione elementi -------------------------------------------------------------------------------
for i in range(len(lista)):
    if re.search(r'</?[a-zA-Z]*\s*(\((\s*[a-zA-Z]*[0-9]*\=*\,*\'*\"*)*\))?>', lista[i]):
        pass
    else:
        for j in range(len(lista[i])):
            if lista[i][j].isalpha():
                lista[i] = lista[i][j:]
                break

print(lista)
