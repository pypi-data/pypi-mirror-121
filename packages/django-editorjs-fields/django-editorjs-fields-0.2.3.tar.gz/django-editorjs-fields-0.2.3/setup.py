# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_editorjs_fields', 'django_editorjs_fields.templatetags']

package_data = \
{'': ['*'],
 'django_editorjs_fields': ['static/django-editorjs-fields/css/*',
                            'static/django-editorjs-fields/js/*',
                            'templates/django-editorjs-fields/*']}

setup_kwargs = {
    'name': 'django-editorjs-fields',
    'version': '0.2.3',
    'description': 'Django plugin for using Editor.js',
    'long_description': '# Editor.js for Django\n\nDjango plugin for using [Editor.js](https://editorjs.io/)\n\n> This plugin works fine with JSONField in Django >= 3.1\n\n[![Django Editor.js](https://i.ibb.co/r6xt4HJ/image.png)](https://github.com/2ik/django-editorjs-fields)\n\n[![Python versions](https://img.shields.io/pypi/pyversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)\n[![Python versions](https://img.shields.io/pypi/djversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)\n[![Downloads](https://static.pepy.tech/personalized-badge/django-editorjs-fields?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/django-editorjs-fields)\n\n## Installation\n\n```bash\npip install django-editorjs-fields\n```\n\nAdd `django_editorjs_fields` to `INSTALLED_APPS` in `settings.py` for your project:\n\n```python\n# settings.py\nINSTALLED_APPS = [\n    ...\n    \'django_editorjs_fields\',\n]\n```\n\n## Upgrade\n\n```bash\npip install django-editorjs-fields --upgrade\npython manage.py collectstatic  # upgrade js and css files\n```\n\n\n## Usage\n\nAdd code in your model\n\n```python\n# models.py\nfrom django.db import models\nfrom django_editorjs_fields import EditorJsJSONField, EditorJsTextField\n\n\nclass Post(models.Model):\n    body_default = models.TextField()\n    body_editorjs = EditorJsJSONField()  # Django >= 3.1\n    body_editorjs_text = EditorJsTextField()  # Django <= 3.0\n\n```\n\n#### New in version 0.2.1. Django Templates support\n\n```html\n<!-- template.html -->\n\n<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta http-equiv="X-UA-Compatible" content="IE=edge" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <title>Document</title>\n  </head>\n  <body>\n    {% load editorjs %} \n    {{ post.body_default }}\n    {{ post.body_editorjs | editorjs}}\n    {{ post.body_editorjs_text | editorjs}}\n  </body>\n</html>\n```\n\n## Additionally\n\nYou can add custom Editor.js plugins and configs ([List plugins](https://github.com/editor-js/awesome-editorjs))\n\nExample custom field in models.py\n\n```python\n# models.py\nfrom django.db import models\nfrom django_editorjs_fields import EditorJsJSONField\n\n\nclass Post(models.Model):\n    body_editorjs_custom = EditorJsJSONField(\n        plugins=[\n            "@editorjs/image",\n            "@editorjs/header",\n            "editorjs-github-gist-plugin",\n            "@editorjs/code@2.6.0",  # version allowed :)\n            "@editorjs/list@latest",\n            "@editorjs/inline-code",\n            "@editorjs/table",\n        ],\n        tools={\n            "Gist": {\n                "class": "Gist"  # Include the plugin class. See docs Editor.js plugins\n            },\n            "Image": {\n                "config": {\n                    "endpoints": {\n                        "byFile": "/editorjs/image_upload/"  # Your custom backend file uploader endpoint\n                    }\n                }\n            }\n        },\n        i18n={\n            \'messages\': {\n                \'blockTunes\': {\n                    "delete": {\n                        "Delete": "Удалить"\n                    },\n                    "moveUp": {\n                        "Move up": "Переместить вверх"\n                    },\n                    "moveDown": {\n                        "Move down": "Переместить вниз"\n                    }\n                }\n            },\n        }\n        null=True,\n        blank=True\n    )\n\n```\n\n**django-editorjs-fields** support this list of Editor.js plugins by default:\n<a name="plugins"></a>\n\n<details>\n    <summary>EDITORJS_DEFAULT_PLUGINS</summary>\n\n```python\nEDITORJS_DEFAULT_PLUGINS = (\n    \'@editorjs/paragraph\',\n    \'@editorjs/image\',\n    \'@editorjs/header\',\n    \'@editorjs/list\',\n    \'@editorjs/checklist\',\n    \'@editorjs/quote\',\n    \'@editorjs/raw\',\n    \'@editorjs/code\',\n    \'@editorjs/inline-code\',\n    \'@editorjs/embed\',\n    \'@editorjs/delimiter\',\n    \'@editorjs/warning\',\n    \'@editorjs/link\',\n    \'@editorjs/marker\',\n    \'@editorjs/table\',\n)\n```\n\n</details>\n\n<details>\n    <summary>EDITORJS_DEFAULT_CONFIG_TOOLS</summary>\n\n```python\nEDITORJS_DEFAULT_CONFIG_TOOLS = {\n    \'Image\': {\n        \'class\': \'ImageTool\',\n        \'inlineToolbar\': True,\n        "config": {"endpoints": {"byFile": "/editorjs/image_upload/"}},\n    },\n    \'Header\': {\n        \'class\': \'Header\',\n        \'inlineToolbar\': True,\n        \'config\': {\n            \'placeholder\': \'Enter a header\',\n            \'levels\': [2, 3, 4],\n            \'defaultLevel\': 2,\n        }\n    },\n    \'Checklist\': {\'class\': \'Checklist\', \'inlineToolbar\': True},\n    \'List\': {\'class\': \'List\', \'inlineToolbar\': True},\n    \'Quote\': {\'class\': \'Quote\', \'inlineToolbar\': True},\n    \'Raw\': {\'class\': \'RawTool\'},\n    \'Code\': {\'class\': \'CodeTool\'},\n    \'InlineCode\': {\'class\': \'InlineCode\'},\n    \'Embed\': {\'class\': \'Embed\'},\n    \'Delimiter\': {\'class\': \'Delimiter\'},\n    \'Warning\': {\'class\': \'Warning\', \'inlineToolbar\': True},\n    \'LinkTool\': {\'class\': \'LinkTool\'},\n    \'Marker\': {\'class\': \'Marker\', \'inlineToolbar\': True},\n    \'Table\': {\'class\': \'Table\', \'inlineToolbar\': True},\n}\n```\n\n</details>\n\n`EditorJsJSONField` accepts all the arguments of `JSONField` class.\n\n`EditorJsTextField` accepts all the arguments of `TextField` class.\n\nAdditionally, it includes arguments such as:\n\n| Args            | Description                                                                                                                                  | Default                         |\n| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |\n| `plugins`       | List plugins Editor.js                                                                                                                       | `EDITORJS_DEFAULT_PLUGINS`      |\n| `tools`         | Map of Tools to use. Set config `tools` for Editor.js [See docs](https://editorjs.io/configuration#passing-saved-data)                       | `EDITORJS_DEFAULT_CONFIG_TOOLS` |\n| `use_editor_js` | Enables or disables the Editor.js plugin for the field                                                                                       | `True`                          |\n| `autofocus`     | If true, set caret at the first Block after Editor is ready                                                                                  | `False`                         |\n| `hideToolbar`   | If true, toolbar won\'t be shown                                                                                                              | `False`                         |\n| `inlineToolbar` | Defines default toolbar for all tools.                                                                                                       | `True`                          |\n| `readOnly`      | Enable read-only mode                                                                                                                        | `False`                         |\n| `minHeight`     | Height of Editor\'s bottom area that allows to set focus on the last Block                                                                    | `300`                           |\n| `logLevel`      | Editors log level (how many logs you want to see)                                                                                            | `ERROR`                         |\n| `placeholder`   | First Block placeholder                                                                                                                      | `Type text...`                  |\n| `defaultBlock`  | This Tool will be used as default. Name should be equal to one of Tool`s keys of passed tools. If not specified, Paragraph Tool will be used | `paragraph`                     |\n| `i18n`          | Internalization config                                                                                                                       | `{}`                            |\n| `sanitizer`     | Define default sanitizer configuration                                                                                                       | `{ p: true, b: true, a: true }` |\n\n## Image uploads\n\nIf you want to upload images to the editor then add `django_editorjs_fields.urls` to `urls.py` for your project with `DEBUG=True`:\n\n```python\n# urls.py\nfrom django.contrib import admin\nfrom django.urls import path, include\nfrom django.conf import settings\nfrom django.conf.urls.static import static\n\nurlpatterns = [\n    ...\n    path(\'editorjs/\', include(\'django_editorjs_fields.urls\')),\n    ...\n] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n```\n\nIn production `DEBUG=False` (use nginx to display images):\n\n```python\n# urls.py\nfrom django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    ...\n    path(\'editorjs/\', include(\'django_editorjs_fields.urls\')),\n    ...\n]\n```\n\nSee an example of how you can work with the plugin [here](https://github.com/2ik/django-editorjs-fields/blob/main/example)\n\n## Forms\n\n```python\nfrom django import forms\nfrom django_editorjs_fields import EditorJsWidget\n\n\nclass TestForm(forms.ModelForm):\n    class Meta:\n        model = Post\n        exclude = []\n        widgets = {\n            \'body_editorjs\': EditorJsWidget(config={\'minHeight\': 100}),\n            \'body_editorjs_text\': EditorJsWidget(plugins=["@editorjs/image", "@editorjs/header"])\n        }\n```\n\n## Theme\n\n### Default Theme\n\n![image](https://user-images.githubusercontent.com/6692517/124242133-7a7dad00-db2d-11eb-812f-84a5c44e88c9.png)\n\n### Dark Theme\n\nplugin use css property [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) to define a dark theme in browser\n\n![image](https://user-images.githubusercontent.com/6692517/124240864-3dfd8180-db2c-11eb-85c1-21f0faf41775.png)\n\n## Configure\n\nThe application can be configured by editing the project\'s `settings.py`\nfile.\n\n| Key                               | Description                                                            | Default               | Type                                                                                                                                                    |\n| --------------------------------- | ---------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| `EDITORJS_DEFAULT_PLUGINS`        | List of plugins names Editor.js from npm                               | [See above](#plugins) | `list[str]`, `tuple[str]`                                                                                                                               |\n| `EDITORJS_DEFAULT_CONFIG_TOOLS`   | Map of Tools to use                                                    | [See above](#plugins) | `dict[str, dict]`                                                                                                                                       |\n| `EDITORJS_IMAGE_UPLOAD_PATH`      | Path uploads images                                                    | `uploads/images/`     | `str`                                                                                                                                                   |\n| `EDITORJS_IMAGE_UPLOAD_PATH_DATE` | Subdirectories                                                         | `%Y/%m/`              | `str`                                                                                                                                                   |\n| `EDITORJS_IMAGE_NAME_ORIGINAL`    | To use the original name of the image file?                            | `False`               | `bool`                                                                                                                                                  |\n| `EDITORJS_IMAGE_NAME`             | Image file name. Ignored when `EDITORJS_IMAGE_NAME_ORIGINAL` is `True` | `token_urlsafe(8)`    | `callable(filename: str, file: InMemoryUploadedFile)` ([docs](https://docs.djangoproject.com/en/3.0/ref/files/uploads/)) |\n| `EDITORJS_VERSION`                | Version Editor.js                                                      | `2.22.3`              | `str`                                                                                                                                                   |\n\nFor `EDITORJS_IMAGE_NAME` was used `from secrets import token_urlsafe`\n\n## Support and updates\n\nUse github issues https://github.com/2ik/django-editorjs-fields/issues\n',
    'author': 'Ilya Kotlyakov',
    'author_email': 'm@2ik.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2ik/django-editorjs-fields',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
