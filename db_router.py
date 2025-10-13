class DBRouter:
    def db_for_read(self, model, **hints):
        if getattr(model._meta, 'app_label', '') == 'legacy':
            return 'legacy'
        return 'default'

    def db_for_write(self, model, **hints):
        if getattr(model._meta, 'app_label', '') == 'legacy':
            return 'legacy'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'legacy':
            return False  # don't run migrations on legacy DB
        return True
