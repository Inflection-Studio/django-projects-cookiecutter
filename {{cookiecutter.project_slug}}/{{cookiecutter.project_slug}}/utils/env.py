import environ


# Created here so we don't call additional Project Baseline code on server boot.
class {{ cookiecutter.class_name_prefix }}EnvNoDefaultException(Exception):
    pass


class {{ cookiecutter.class_name_prefix }}Env(environ.Env):
    """
    Enforces the optional default param for Env() without modifying the entire class.
    """

    def get_value(
        self, var, cast=None, default=environ.Env.NOTSET, parse_default=False
    ):
        if default == self.NOTSET:
            raise  {{ cookiecutter.class_name_prefix }}EnvNoDefaultException(
                f"'{var}' does not have a default set, please set a default value"  # noqa: B907
            )
        return super().get_value(
            var, cast=cast, default=default, parse_default=parse_default
        )
