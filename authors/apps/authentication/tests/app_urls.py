from django.urls import reverse

reset_password_url = reverse('authentication:reset-password')
new_passord_url = reverse('authentication:new-password')
activate_url = reverse('authentication:activate-account')
register_url = reverse('authentication:register')
login_url = reverse('authentication:login')
user_action_url = reverse('authentication:user-action')
