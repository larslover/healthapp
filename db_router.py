class DBRouter:
    def db_for_read(self, model, **hints):
        # Only LegacyStudent reads go to legacy DB
        if model._meta.model_name == 'legacystudent':
            return 'legacy'
        return 'default'

    def db_for_write(self, model, **hints):
        # Never write to legacy
        if model._meta.model_name == 'legacystudent':
            return None
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # No migrations on legacy DB
        if db == 'legacy':
            return False
        return True
