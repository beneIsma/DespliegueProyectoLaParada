from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from Users.models import Users


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False, max_length=50)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=100)


    class Meta:
        model = Users
        fields = ('email', 'password')

    def validate_email(self, email):
        if Users.objects.filter(email=email).first():
            return email
        else:
            raise serializers.ValidationError("Email no válido")

    def validate_password(self, password):
        if not any(d.isdigit() for d in password):
            raise serializers.ValidationError("Contraseña no válida")
        else:
            return password

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        if email:
            if "@" not in email:
                raise serializers.ValidationError("El email debe de contener el '@'")
            #if any(ext for ext in settings.EXTENSIONES_BLACKLIST):
            #    raise serializers.ValidationError(f"La extensión no es válida")

        if not email or not password:
            raise serializers.ValidationError("Faltan rellenar los campos")

        user = Users.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("El usuario no existe")
        else:
            if not user.check_password(password):
                raise serializers.ValidationError("La contraseña no coincide")

        # Defensivo: rol y personalInfo pueden ser None (FK con null=True),
        # sobre todo en superusers creados con createsuperuser.
        rol_nombre = user.rol.nombre if user.rol else "sin rol"
        telefono = user.personalInfo.telefono if user.personalInfo else ""

        refresh = RefreshToken.for_user(user)
        refresh["nombre"] = user.nombre
        refresh["rol"] = rol_nombre
        return {
            "success": True,
            "data": {
                "nombre": user.nombre,
                "email": user.email,
                "teléfono": telefono,
                "rol": rol_nombre,
                "refreshToken": str(refresh),
                "token": str(refresh.access_token)
            }
        }