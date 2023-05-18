import re


class Verification:
    @staticmethod
    def is_password_valid(password):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        return bool(re.match(pattern, password))

    @staticmethod
    def is_phone_valid(phone):
        pattern = r"^(0098|\+98|0)9[0-9]{9}$"
        return bool(re.match(pattern, phone))

    @classmethod
    def reformat_phone(cls, phone: str):
        phone = phone.replace("+98", "0")
        if phone.startswith("0098"):
            phone.replace("0098", "0")
        return phone

    @staticmethod
    def is_email_valid(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def is_username_valid(username):
        pattern = r"^[A-Za-z0-9_]{6,16}$"
        return bool(re.match(pattern, username))

    @staticmethod
    def reformat_tags(tags: str) -> str:
        tags = tags.replace(" ", "")
        tags = tags.replace(",", ", ")
        tags = tags.lower()
        return tags

    @classmethod
    def validate_tags_arr(cls, tags: str) -> list:
        tags = cls.reformat_tags(tags).split(", ")
        valid_tags = []
        for tag in tags:
            if re.match(r"^[0-9a-z]+-?[0-9a-z]*$", tag) and len(tag) > 3:
                valid_tags.append(tag)
        return valid_tags

    @classmethod
    def validate_tags_str(cls, tags) -> str:
        tags = cls.validate_tags_arr(tags)
        return ', '.join(tags)

    @classmethod
    def is_prompt_valid(cls, prompt: str):
        pattern = r"^[cue][ad][gn]$"
        return bool(re.match(pattern, prompt))
