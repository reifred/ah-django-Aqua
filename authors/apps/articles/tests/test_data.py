valid_article = {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian"
}

article_without_title = {
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian"
}

article_without_description = {
    "title": "How to train your dragon",
    "body": "It takes a Jacobian"
}

article_without_body = {
    "title": "How to train your dragon",
    "description": "Ever wonder how?"
}

update_article_title = {
    "title": "How to train my dragon"
}

valid_article_2= {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "Ask Question I added validate_mail and also installed py3dns\
            to check if the email the user signs up with is valid(like their\
            emails are not fake). The tests seem Ask Question I added validail\
            and also installed py3dns to check if the email the user sis up fh \
            is valid(like their emails are not fake). The tests seem Ask Qion\
            I added validate_mail and also installed py3dns to check if the il\
            the user signs up with is valid(like their emails are not fake). Te \
            tests seem Ask Question I added validate_mail and also installed \
            py3dns to check if the email the user signs up with is valid(like\
            their emails are not fake). The tests seem Ask Question I added \
            validate_mail and also installed py3dns to check if the email the \
            user signs up with is valid(like their emails are not fake). \
            The tests seem v Ask Question I added validate_mail and also \
            installed py3dns to check if the email the user signs up with is \
            valid(like their emails are not fake). The tests seem \
            Question I added validate_mail and also installed py3dns \
            to check if the email the user signs up with is valid(like their \
            emails are not fake). The tests seem vvvv Ask Question I added ]\
            validate_mail and also installed py3dns to check if the email the\
            user signs up with is valid(like their emails are not fake). \
            The tests seem Ask Question I added validate_mail and also ins\
            talled  to check if the email the user signs up with is valid(like\
            their emails are not fake). The tests seem                                                                                                                                                                                                             Ask Question I added validate_mail and also installed py3dns to check if the email the user signs up with is valid(like their emails are not fake). The tests seem Ask Question I added validate_mail and also installed py3dns to check if the email the user signs up with is valid(like their emails are not fake). The tests seem  Ask Question I added validate_mail and also installed py3dns to check if the email the user signs up with is valid(like their emails are not fake). The tests seem Ask Question I added validate_mail and also installed py3dns to check if the email the user signs up with is valid(like their emails are not fake). The tests seem Ask Question I added validate_mail and also installed py3dns to check if the email the user signs up with is valid(like their emails are not fake). The tests seem v "
}

slug = "how-to-train-your-dragon"

non_existent_slug = "Three-blind-mice"

auth_error = "Authentication credentials were not provided."

not_found = "Not found"

valid_rating = {
    "article":{
               "ratings":5
}
}

invalid_rating = {  
    "article":{
               "ratings":7
}}

invalid_rating2 = {
    "article":{
               "ratings":-1
}}

valid_rating_2 = {
    "article":{
               "ratings":3
}}

invalid_integer = {
    "article":{
               "ratings":1.5
}}

def signup_and_login_user(User,valid_user2,client):
    user = User.objects.create_user(**valid_user2)
    client.force_authenticate(user=user)
    loged_in_user = client.login(**valid_user2)
    return loged_in_user
