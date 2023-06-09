from IPython.display import display, HTML

def display_dict( info ):

    html = ["<table width=100%>"]
    for key, value in info.items():
        html.append("<tr>")
        html.append("<td>{0}</td>".format(key))
        html.append("<td>{0}</td>".format(value))
        html.append("</tr>")
    html.append("</table>")
    display( HTML( ''.join(html)))
