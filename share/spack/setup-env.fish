# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


########################################################################
#
# This file is part of Spack and sets up the spack environment for
# fish.  This includes dotkit support, module support, and
# it also puts spack in your path.  The script also checks that
# at least module support exists, and provides suggestions if it
# doesn't. Source it like this:
#
#    source /path/to/spack/share/spack/setup-env.fish
#
########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack use' and 'spack unuse' to shell functions.  This in turn
# allows them to be used to invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its
# arguments into a unique spack spec that is then passed to dotkit
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack dotfiles.
########################################################################

echo "WARNING: Fish is not officially support by the Spack community."
echo "Some of the latest features may not yet be implemented."

function spack -d "spack"

    set -l _argv_original $argv

    # In order to properly capture spack flags,
    # they must *all* be enumerated here.
    # !! Developers must keep this up-to-date with any changes.

    # Each fish opt is required to have a 1 character short id.
    # The order here is based on
    # https://spack.readthedocs.io/en/latest/command_index.html

    # TODO: validate required opt values, plus better error messages

    set -l options 'h/help' 'H/all-help' 'c-color=' 'C/config-scope='
    set options $options 'd/debug' 'z-pdb' 'e/env=' 'D/env-dir=' 'E/no-env'
    set options $options 'u-use-env-repo' 'k/insecure' 'l/enable-locks'
    set options $options 'L/disable-locks' 'm/mock' 'p/profile'
    set options $options 'x-storted-profile=' 'y-lines' 'v/verbose'
    set options $options 't-stacktrace' 'V/version' 'w-print-shell-vars='
    argparse -n spack --stop-nonopt $options -- $argv
    or return

    set -l _sp_flags ""
    if set -q _flag_help
        set _sp_flags $_sp_flags "--help"
    end
    if set -q _flag_all_help
        set _sp_flags $_sp_flags "--all-help"
    end
    if set -q _flag_color
        set _sp_flags $_sp_flags "--color $_flag_color"
    end
    if set -q _flag_config_scope
        set _sp_flags $_sp_flags "--config-scope $_flag_config_scope"
    end
    if set -q _flag_debug
        set _sp_flags $_sp_flags "--debug"
    end
    if set -q _flag_pdb
        set _sp_flags $_sp_flags "--pdb"
    end
    if set -q _flag_env
        set _sp_flags $_sp_flags "--env $_flag_e"
    end
    if set -q _flag_env_dir
        set _sp_flags $_sp_flags "--env-dir $_flag_D"
    end
    if set -q _flag_no_env
        set _sp_flags $_sp_flags "--no-env"
    end
    if set -q _flag_use_env_repo
        set _sp_flags $_sp_flags "--use-env-repo"
    end
    if set -q _flag_insecure
        set _sp_flags $_sp_flags "--insecure"
    end
    if set -q _flag_enable_locks
        set _sp_flags $_sp_flags "--enable-locks"
    end
    if set -q _flag_disable_locks
        set _sp_flags $_sp_flags "--diable-locks"
    end
    if set -q _flag_mock
        set _sp_flags $_sp_flags "--mock"
    end
    if set -q _flag_profile
        set _sp_flags $_sp_flags "--profile"
    end
    if set -q _flag_sorted_profile
        set _sp_flags $_sp_flags "--sorted-profile $_flag_x"
    end
    if set -q _flag_lines
        set _sp_flags $_sp_flags "--lines"
    end
    if set -q _flag_verbose
        set _sp_flags $_sp_flags "--verbose"
    end
    if set -q _flag_stacktrace
        set _sp_flags $_sp_flags "--stacktrace"
    end
    if set -q _flag_version
        set _sp_flags $_sp_flags "--version"
    end
    if set -q _flag_print_shell_vars
        set _sp_flags $_sp_flags "--print-shell-vars $_flag_w"
    end

    # an extra ' ' is added to _sp_flags
    if test (count $_sp_flags) -gt 1
        set _sp_flags $_sp_flags[2..-1]
    end

    # if help, version, or no sub-commands
    #    short circut to spack
    if set -q _flag_help
        or test (count $argv) -eq 0
        command spack -h
        return 0
    else if set -q _flag_all_help
        command spack -H
        return 0
    else if set -q _flag_version
        command spack -V
        return 0
    end

    # CONSUME subcommand from argv
    set -l _sp_subcommand $argv[1]
    set argv $argv[2..-1]


    # match with shell handled commands
    switch $_sp_subcommand
        case cd
            set -l _subcmd_argv_original $argv
            set -l options 'h/help' 'm/module-dir' 'r/spack-root'
            set options $options 'i/install-dir' 'p/package-dir'
            set options $options 'P/packages' 's/stage-dir' 'S/stages'
            set options $options 'b/build-dir' 'e/env='
            argparse -n __spack_helper_cd --stop-nonopt $options -- $argv
            or return

            if set -q _flag_help
                command spack help cd
                return 0
            end

            set -l LOC (command spack $_sp_flags location $_subcmd_argv_original)
            if test $status -ne 0
                echo "ERROR with spack location command"
                return 1
            else if test -d $LOC
                cd $LOC
            else
                return 1
            end

        case env
            set -l options 'h/help'
            argparse -n __spack_helper_env --stop-nonopt $options -- $argv
            or return

            if set -q _flag_help
                or test (count $argv) -eq 0
                command spack help env
                return 0
            end

            #consume to next subcommand
            set -l _sp_env_subcmd $argv[1]
            set argv $argv[2..-1]

            switch $_sp_env_subcmd
                case activate
                    echo "spack activate"
                    if test (count $argv) -eq 0
                        command spack $_argv_original
                    else
                        eval (command spack $_sp_flags env activate --sh $argv)
                    end

                case deactivate
                    echo "spack deactivate"
                    if test (count $argv) -eq 0
                        eval (command spack $_sp_flags env deactivate --sh)
                    else
                        command spack $_argv_original
                    end
            end

        case use unuse load unload
            # parse the flags from this sub-command
            set -l options 'h/help' 'r/dependencies'
            argparse -n __spack_helper_use --stop-nonopt $options -- $argv
            or return

            if set -q _flag_help
                command spack help $_sp_subcommand
                return 0
            end

            switch $_sp_subcommand
                case use unuse
                    set -l _sp_full_spec "spack thing"
                    command spack $_sp_flags module dotkit find $_flag_dependencies $argv
                    if test $status -ne 0
                        return 1
                    end
                    switch $_sp_subcommand
                        case use
                            use $_sp_module_args $_sp_full_spec
                        case unuse
                            unuse $_sp_module_args $_sp_full_spec
                    end
                case load unload
                    set -l _sp_full_spec "spack thing"
                    command spack $_sp_flags module tcl find $_flag_dependencies $argv
                    if test $status -ne 0
                        return 1
                    end
                    switch $_sp_command
                        case load
                            module load $_sp_module_args $_sp_full_spec
                        case unload
                            module unload $_sp_module_args $_sp_full_spec
                    end
            end
        case '*'
            command spack $_argv_original
    end
end

########################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
########################################################################
function _spack_pathadd -d "spack helper: adds path to env vars"
    # add to PATH if only one arg
    if test (count $argv) -eq 1
        set -x PATH $argv[1] $PATH
        return 0
    end

    # if path not in the list, prepend to list
    if not contains $argv[2] $$argv[1]
        set -x $argv[1] $argv[2] $$argv[1]
    end
end

#
# Find root directory and add bin to path.
#
set -l _sp_share_dir (cd (dirname (status -f)); pwd)
set -l _sp_prefix (cd (dirname (dirname $_sp_share_dir)); pwd)
_spack_pathadd PATH $_sp_prefix/bin
set -x SPACK_ROOT $_sp_prefix


#
# Determine which shell is being used
#
set -x SPACK_SHELL "fish"

#
# Check whether a function of the given name is defined
#
function _spack_fn_exists -d "check if arg exists as a function"
    if not type -q $argv
        return 1
    else
        return test (type -t $argv) = "function"
    end
end


set -l need_module "no"
if not _spack_fn_exists use
    and not _spack_fn_exists module
    set need_module "yes"
end

#
# make available environment-modules
#
# Note: multi-line evals become a pipe to source
if test $need_module = "yes"
    command spack --print-shell-vars fish,modules | source
    if test $_sp_module_prefix != "not_installed"
        set -x MODULE_PREFIX $_sp_module_prefix
        _spack_pathadd PATH "$MODULE_PREFIX/Modules/bin"
        function module -d "module"
            eval ($MODULE_PREFIX/Modules/bin/modulecmd $SPACK_SHELL $argv)
        end
    end
else
    command spack --print-shell-vars fish | source
end


#
# set module system roots
#
_spack_pathadd DK_NODE    $_sp_dotkit_root/$_sp_sys_type
_spack_pathadd MODULEPATH $_sp_tcl_root/$_sp_sys_type


# TODO fish completions coming soon
