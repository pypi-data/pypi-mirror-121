Name of the module is self-explanatory.

Works only for Images and Files.

* Class used for Images:
   * [`djangocms_bootstrap4.contrib.bootstrap4_picture.models.Bootstrap4Picture`](https://github.com/django-cms/djangocms-bootstrap4/blob/master/djangocms_bootstrap4/contrib/bootstrap4_picture/models.py#L7)
   * [`djangocms_picture.models.Picture`](https://github.com/django-cms/djangocms-picture/blob/master/djangocms_picture/models.py#L387)
* Class used for Files:
   * [`djangocms_file.models.File`](https://github.com/django-cms/djangocms-file/blob/master/djangocms_file/models.py#L190)

----

## Install

* pip
   ```bash
   python3 -m pip install djangocms-filer-display-pages-where-files-are-used-before-removing-them
   ```

* Add this ***just before `filer`*** in your `INSTALLED_APPS`:
   ```python
       'djangocms_filer_display_pages_where_files_are_used_before_removing_them',
    ```

* ![that's all folks!](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/ce92945bf31ba742cbe1de93ead4b503/image.png)

----

## Screenshots/video

| Remove multiple files | Remove folder | Video |
| ---- | ---- | ---- |
| [![1](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/eb52070954358881bc73b0bc51fa9b11/image.png)](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/cae9ab7299f5eb9d0e93cb446e06bb7f/image.png) | [![2](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/ca576f3d4de9ba63b8f9268c052baefe/image.png)](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/0bd2e1cf2d850336a0e04f9aa3744700/image.png) | ![django-filer-this-module-name-is-too-long-damn](https://gitlab.com/kapt/open-source/djangocms-filer-display-pages-where-files-are-used-before-removing-them/uploads/e5cbf76772455532df6f49a5bc97ee72/django-filer-this-module-name-is-too-long-damn.webm)
