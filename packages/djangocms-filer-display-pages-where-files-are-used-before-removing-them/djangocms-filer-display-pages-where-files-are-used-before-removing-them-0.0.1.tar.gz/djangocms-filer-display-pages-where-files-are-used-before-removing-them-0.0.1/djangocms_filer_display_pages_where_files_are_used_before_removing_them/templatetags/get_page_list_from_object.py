from django import template


use_images = True
use_media = True

try:
    from djangocms_bootstrap4.contrib.bootstrap4_picture.models import Bootstrap4Picture
except ModuleNotFoundError:
    use_images = False
try:
    from djangocms_file.models import File
except ModuleNotFoundError:
    use_media = False

register = template.Library()


def get_page_list_from_image(obj):
    images_list = []
    if use_images:
        for image in Bootstrap4Picture.objects.filter(picture_id=obj.id):
            try:
                if not image.placeholder.page.publisher_is_draft:
                    images_list.append(
                        {
                            "name": image.picture.original_filename,
                            "url": image.placeholder.page.get_absolute_url(
                                image.language
                            ),
                            "title": image.placeholder.page.get_page_title(
                                image.language
                            ),
                            "lang": image.language,
                        }
                    )
            except AttributeError:
                pass
    return images_list


def get_page_list_from_media(obj):
    media_list = []
    if use_media:
        for media in File.objects.filter(file_src__sha1=obj.sha1):
            try:
                if not media.placeholder.page.publisher_is_draft:
                    media_list.append(
                        {
                            "name": media.file_src.original_filename,
                            "url": media.placeholder.page.get_absolute_url(
                                media.language
                            ),
                            "title": media.placeholder.page.get_page_title(
                                media.language
                            ),
                            "lang": media.language,
                        }
                    )
            except AttributeError:
                pass
    return media_list


def get_page_list_from_object(object):
    media_list = []
    images_list = []
    _media_list = get_page_list_from_media(object)
    if len(_media_list):
        media_list += _media_list

    _images_list = get_page_list_from_image(object)
    if len(_images_list):
        images_list += _images_list
    return {"media": media_list, "images": images_list}


def get_files_from_folder(folder):
    childrens = folder.children.all()
    if childrens.exists():
        for child_folder in folder.children.all():
            return list(folder.files) + list(get_files_from_folder(child_folder))
    else:
        return list(folder.files)


def get_page_list_from_folder_and_files(folders, files):
    # lots of empty lists
    media_list = []
    images_list = []
    files_list = []

    # get files in every deleted folder
    for folder in folders:
        files_list += get_files_from_folder(folder)

    # add deleted files to the list
    for file in files:
        files_list.append(file)

    # assign every file in images or media list
    for file in files_list:
        _media_list = get_page_list_from_media(file)
        if len(_media_list):
            media_list += _media_list

        _images_list = get_page_list_from_image(file)
        if len(_images_list):
            images_list += _images_list
    return {"media": media_list, "images": images_list}


register.filter(
    "get_page_list_from_folder_and_files", get_page_list_from_folder_and_files
)
register.filter("get_page_list_from_object", get_page_list_from_object)
