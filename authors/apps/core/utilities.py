from django.template.defaultfilters import slugify


def get_unique_slug(model_instance, data_to_slugify, slugable_field_name, slug_field_name):
    slug = slugify(data_to_slugify)
    unique_slug = slug
    # Use a hash string to create a unigue extension to
    # append to the slug inorder to create a unique slag
    extention = 1
    ModelClass = model_instance.__class__
    # Search through the existing slags to check whether
    # the slag we created above already exists. If it does,
    # make it unique by appending a hyphen and the extension
    # to it.
    while ModelClass.objects.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = f"{slug}-{extention}"
        extention += 1

    return unique_slug
