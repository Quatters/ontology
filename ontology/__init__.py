try:
    from vstutils.environment import prepare_environment
except ImportError:  # nocv
    def prepare_environment(*args, **kwargs):
        pass

__version__ = '1.0.0'

settings = {
    "VST_PROJECT": 'ontology',
    "VST_PROJECT_GUI_NAME": 'Trucking',
    "DJANGO_SETTINGS_MODULE": 'ontology.settings',
}

prepare_environment(**settings)
