import environ


# Created here so we don't call additional Project Baseline code on server boot.
class ProjectBaseLineEnvNoDefaultException(Exception):
    pass


class ProjectBaseLineEnv(environ.Env):
    """
    Enforces the optional default param for Env() without modifying the entire class.
    """

    def get_value(
        self, var, cast=None, default=environ.Env.NOTSET, parse_default=False
    ):
        if default == self.NOTSET:
            raise ProjectBaseLineEnvNoDefaultException(
                f"'{var}' does not have a default set, please set a default value"  # noqa: B907
            )
        return super().get_value(
            var, cast=cast, default=default, parse_default=parse_default
        )
