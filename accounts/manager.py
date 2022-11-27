from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self,email,phone_no,first_name,last_name,password=None):
        if not email:
            raise ValueError('user Must have an email address')
        
        if not phone_no:
            raise ValueError('user Must have an phone number')
        
        if not password:
            raise ValueError('user Must have an password')
        
        user_obj=self.model(
            email=self.normalize_email(email),
            phone_no=phone_no,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,email,phone_no,first_name,last_name,password=None):
        user_obj=self.create_user(
            email=self.normalize_email(email),
            phone_no=phone_no,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user_obj.is_admin=False
        user_obj.is_staff=True
        user_obj.is_active=True
        user_obj.is_superadmin=False
        user_obj.save(using=self._db)
        return user_obj
    
    

    def create_superuser(self,email,phone_no,first_name,last_name,password=None):
        user_obj=self.create_user(
            email=self.normalize_email(email),
            phone_no=phone_no,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user_obj.is_admin=True
        user_obj.is_staff=True
        user_obj.is_active=True
        user_obj.is_superadmin=True
        user_obj.save(using=self._db)
        return user_obj