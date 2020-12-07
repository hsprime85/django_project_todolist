import re
from django.db import models
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}

        if len(post_data["register_first_name"]) < 2:
            errors["register_first_name"] = "Your first name should be 2 characters"
        if len(post_data["register_last_name"]) < 2:
            errors["register_last_name"] = "Your last name should be 2 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data["register_email"]):
            errors["register_email"] = "Invalid email address!"

        if post_data["register_password"] != post_data["register_confirm_pw"]:
            errors["register_password"] = "Password does not match"

        if len(post_data["register_password"]) < 8:
            errors["register_confirm_pw"] = "Password should be 8 characters"
        return errors

    def login_validator(self, post_data):
        errors = {}

        user_list_to_login = User.objects.filter(
            email=post_data["login_email"])

        if len(user_list_to_login) == 0:
            errors["login_email"] = "Email not found!"
        else:
            if not bcrypt.checkpw(post_data["login_pw"].encode(), user_list_to_login[0].password.encode()):
                errors["login_pw"] = "there was a problem pw"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
