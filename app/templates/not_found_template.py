ticket_not_found_file = open("./app/templates/html/404.html", "r")
ticket_not_found_html = ticket_not_found_file.read()


def get_ticket_not_found_html(redirect_url: str, ticket_id: str) -> str:
    return ticket_not_found_html.replace("#[redirect_url]", redirect_url).replace(
        "#[ticket_id]", ticket_id
    ).replace("#[type]", "ticket")


def get_project_not_found_html(redirect_url: str, prefix_id: str) -> str:
    return ticket_not_found_html.replace("#[redirect_url]", redirect_url).replace(
        "#[ticket_id]", prefix_id
    ).replace("#[type]", "project")
