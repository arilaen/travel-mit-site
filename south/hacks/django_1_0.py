"""
Hacks for the Django 1.0/1.0.2 releases.
"""

from django.conf import settings
from django.db import models
from django.db.backends.creation import BaseDatabaseCreation
from django.db.models.loading import AppCache, cache
from django.core import management
from django.core.management.commands.flush import Command as FlushCommand
from django.utils.datastructures import SortedDict

class SkipFlushCommand(FlushCommand):
    def handle_noargs(self, **options):
        # no-op to avoid calling flush
        return

class Hacks:
    
    def set_installed_apps(self, apps):
        """
        Sets Django's INSTALLED_APPS setting to be effectively the list passed in.
        """
        
        # Make sure it's a list.
        apps = list(apps)
        
        # Make sure it contains strings
        if apps:
            assert isinstance(apps[0], basestring), "The argument to set_installed_apps must be a list of strings."
        
        # Monkeypatch in!
        settings.INSTALLED_APPS, settings.OLD_INSTALLED_APPS = (
            apps,
            settings.INSTALLED_APPS,
        )
        self._redo_app_cache()
    
    
    def reset_installed_apps(self):
        """
        Undoes the effect of set_installed_apps.
        """
        settings.INSTALLED_APPS = settings.OLD_INSTALLED_APPS
        self._redo_app_cache()
    
    
    def _redo_app_cache(self):
        """
        Used to repopulate AppCache after fiddling with INSTALLED_APPS.
        """
        a = AppCache()
        a.loaded = False
        a.handled = {}
        a.postponed = []
        a.app_store = SortedDict()
        a.app_models = SortedDict()
        a.app_errors = {}
        a._populate()
    
    
    def clear_app_cache(self):
        """
        Clears the contents of AppCache to a blank state, so new models
        from the ORM can be added.
        """
        self.old_app_models, cache.app_models = cache.app_models, {}
    
    
    def unclear_app_cache(self):
        """
        Reversed the effects of clear_app_cache.
        """
        cache.app_models = self.old_app_models
        cache._get_models_cache = {}
    
    
    def repopulate_app_cache(self):
        """
        Rebuilds AppCache with the real model definitions.
        """
        cache._populate()

    def patch_flush_during_test_db_creation(self):
        """
        Patches BaseDatabaseCreation.create_test_db to not flush database
        """

        def patch(f):
            def wrapper(*args, **kwargs):
                # hold onto the original and replace flush command with a no-op
                original_flush_command = management._commands['flush']
                try:
                    management._commands['flush'] = SkipFlushCommand()
                    # run create_test_db
                    f(*args, **kwargs)
                finally:
                    # unpatch flush back to the original
                    management._commands['flush'] = original_flush_command
            return wrapper
            
        BaseDatabaseCreation.create_test_db = patch(BaseDatabaseCreation.create_test_db)

