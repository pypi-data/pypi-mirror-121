# Django Rest Framework Wraper
A customized wrapper for djangorestframework
### Installation
```bash
pip install djrest-wrapper
```
### Quick Start
simply set these variables in `settings.py`
```python
REST_FRAMEWORK = {                                                              
'EXCEPTION_HANDLER': 'djrest_wrapper.exceptions.handler.exception_handler', 
'DEFAULT_RENDERER_CLASSES': ['djrest_wrapper.renderers.defaultjson.DefaultJsonRenderer'],
'DEFAULT_PAGINATION_CLASS': 'djrest_wrapper.paginations.default.DefaultPagination',
}
```