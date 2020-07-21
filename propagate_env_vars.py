import os
import platform
import re


IS_ARM64 = platform.processor() == "aarch64"
IS_OSX = platform.system() == "Darwin"

ENV_VARS = [
    "STATIC_DEPS",
    "CFLAGS",
    "LDFLAGS",
    "AR",
    "NM",
    "RANLIB",
    "LIBXML2_VERSION",
    "LIBXSLT_VERSION",
]


def append_env(env, name, value):
    env[name] = env.get(name, '') + ' ' + value


def copy_makefile_env(env):
    for name in ENV_VARS:
        if name in env:
            continue
        value = read_makefile_var(name)
        if value:
            env[name] = value


def read_makefile_var(name, _makefile={}):
    if not _makefile:
        with open("lxml/Makefile") as f:
            lines = iter(f)
            for line in lines:
                if '=' not in line:
                    continue
                match = re.match(r"([A-Z0-9_]+)\s*?=\s*(.+)", line)
                if match and match.group(1) not in _makefile:
                    value = match.group(2).strip()
                    while value.endswith("\\"):
                        value = value[:-1].rstrip() + " " + next(lines).strip()
                    _makefile[match.group(1)] = value.strip('\'"')

    return _makefile.get(name) or _makefile.get("MANYLINUX_" + name) or ""


def main():
    env = os.environ.copy()
    copy_makefile_env(env)
    append_env(env, "CFLAGS", "-march=armv8-a -mtune=cortex-a72" if IS_ARM64 else "-march=core2")

    if IS_ARM64:
        env.update([
            [s.strip('\'" ') for s in env_var.split("=")]
            for env_var in (" " + read_makefile_var("AARCH64_ENV") + " ").split(" -e ")
            if "=" in env_var
        ])
    elif IS_OSX:
        append_env(env, "LDFLAGS", "-arch x86_64")

    env_vars = [
        (name, env[name])
        for name in ENV_VARS
        if env.get(name)
    ]

    with open("env_vars.sh", "w") as f:
        for name, value in env_vars:
            env_var = '{}="{}"'.format(name, value)
            print(env_var)
            f.write("export {}\n".format(env_var))


if __name__ == "__main__":
    main()
