
import models

models.Passwords.create_table(safe=True)

models.Passwords.create(password=input("Vvedite parol: "), accesstype=input("Vvedite access: "))
models.Passwords.save()