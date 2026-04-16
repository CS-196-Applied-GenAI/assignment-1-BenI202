import re
from datetime import datetime


def clean_email_data(raw_data):
    cleaned = []
    for line in raw_data:
        parts = [p.strip() for p in line.split(",")]
        email, birth_date, start_date, title = parts[0], parts[1], parts[2], parts[3]

        email = email.lower().replace("#", "@")
        email = re.sub(r"@+", "@", email)
        if "@" in email:
            local, domain = email.split("@", 1)
            domain = re.sub(r"\.+", ".", domain)
            email = f"{local}@{domain}"

        title = re.sub(r"[^\w\s]+$", "", title).strip()

        cleaned.append({
            "email": email,
            "birth_date": birth_date,
            "start_date": start_date,
            "title": title,
        })
    return cleaned


def _name_from_email(email):
    local = email.split("@")[0]
    parts = re.split(r"[._]", local)
    return " ".join(p.capitalize() for p in parts if p)


def generate_messages(data, today):
    messages = []
    for person in data:
        name = _name_from_email(person["email"])
        birth = datetime.strptime(person["birth_date"], "%Y-%m-%d")
        start = datetime.strptime(person["start_date"], "%Y-%m-%d")

        if today.month == birth.month and today.day == birth.day:
            messages.append(f"Happy Birthday, {name}! Have a fantastic day!")
            years = today.year - start.year
            if years > 0 and years % 5 == 0:
                messages.append(
                    f"Happy Work Anniversary, {name}! {years} years at the company!"
                )
    return messages

