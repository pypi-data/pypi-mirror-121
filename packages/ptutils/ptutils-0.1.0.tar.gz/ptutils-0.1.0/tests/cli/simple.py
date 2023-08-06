#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module defines unit tests for `pt.ptutils.cli.simple`.
"""

from pt.ptutils.cli.simple import (
    arg,
    shared_arg,
    use_shared_arg,
    shared_arg_exists,
    remove_shared_arg,
    arg_group,
    use_arg_group,
    arg_group_exists,
    remove_arg_group,
    command,
    command_exists,
    remove_command,
    get_argument,
    has_argument
)


# ------------------------------------------------------------------------------------------------------------------------
def test_cli_simple_create_command():
    """ Test ability to create a command using the `pt.ptutils.cli.simple.command` decorator. """
    try:
        @command
        def my_command():
            pass
        assert command_exists('my_command')
    finally:
        remove_command('my_command')
        assert not command_exists('my_command')


# ------------------------------------------------------------------------------------------------------------------------
def test_cli_simple_create_arg_group():
    """ Test ability to create an argument group using the `pt.ptutils.cli.simple.arg_group` decorator. """
    try:
        @arg_group
        def fruits():
            pass
        assert arg_group_exists('fruits')
    finally:
        remove_arg_group('fruits')
        assert not arg_group_exists('fruits')


# ------------------------------------------------------------------------------------------------------------------------
def test_cli_simple_create_shared_arg():
    """ Test ability to create a shared argument using the `pt.ptutils.cli.simple.shared_arg` function. """
    try:
        shared_arg(
            '-w', '--whatchamacallits',
            dest = "whatchamacallits"
        )
        assert shared_arg_exists('whatchamacallits')
    finally:
        remove_shared_arg('whatchamacallits')
        assert not shared_arg_exists('whatchamacallits')


# ------------------------------------------------------------------------------------------------------------------------
def test_cli_simple_use_shared_arg():
    """ Test ability to use a shared argument using the `pt.ptutils.cli.simple.use_shared_arg` function. """
    try:
        # define shared arg
        batch = shared_arg(
            '-b', '--batch',
            metavar = "BATCH_SIZE",
            help = "Batch size"
        )

        # define command using shared arg
        @use_shared_arg('batch')
        @command
        def my_command(batch: int = 5):
            assert batch == 25

        # check
        assert shared_arg_exists('batch')
        assert shared_arg_exists(batch)
        assert command_exists('my_command')
        assert command_exists(my_command)
        assert get_argument('my_command', 'batch') == {
            "kind":   "arg",
            "args":   tuple(['-b', '--batch']),
            "kwargs": {
                "metavar": "BATCH_SIZE",
                "help": "Batch size"
            },
            "name": "batch"
        }
        assert get_argument('my_command', batch) == {
            "kind":   "arg",
            "args":   tuple(['-b', '--batch']),
            "kwargs": {
                "metavar": "BATCH_SIZE",
                "help": "Batch size"
            },
            "name": "batch"
        }
        assert has_argument(my_command, batch)
        assert has_argument('my_command', 'batch')

    finally:
        # cleanup
        remove_command('my_command')
        remove_shared_arg(batch)

        assert not command_exists('my_command')
        assert not shared_arg_exists('batch')


# ------------------------------------------------------------------------------------------------------------------------
def test_cli_simple():
    """ Tests many functions of the simple cli system together. """
    try:
        # define a fruits arguments group
        @arg(
            '-b', '--banana',
            help    = 'Yummy yellow fruit',
            dest    = 'banana',
            metavar = 'BANANA',
            default = 'banana'
        )
        @arg(
            '-c', '--cherry',
            help    = 'Yummy red fruit',
            dest    = 'cherry',
            metavar = 'CHERRY',
            default = 'cherry'
        )
        @arg_group
        def fruits():
            pass

        # define a vegetables arguments group
        @arg(
            '-s', '--squash',
            help    = 'Yucky green vegetable',
            dest    = 'squash',
            metavar = 'SQUASH',
            default = 'squash'
        )
        @arg(
            '-t', '--tomato',
            help    = 'Yummy red vegetable',
            dest    = 'tomato',
            metavar = 'TOMATO',
            default = 'tomato'
        )
        @arg_group
        def vegetables():
            pass

        # define a produce arguments group
        @use_arg_group('fruits')
        @use_arg_group('vegetables')
        @arg_group
        def produce():
            pass

        # define a shared argument
        shared_arg(
            '-w', '--whatchamacallits',
            dest = "whatchamacallits"
        )

        # define a command using shared argument, argument group, and some directly defined arguments
        @use_shared_arg('whatchamacallits')
        @use_arg_group('produce')
        @arg(
            '-p', '--prefix',
            help    = 'Folder prefix',
            dest    = 'prefix',
            metavar = 'FOLDER',
            default = '/tmp'
        )
        @arg(
            '-f', '--force',
            help    = 'When present, ignore cached results and perform all actions again.',
            dest    = 'force',
            action  = 'store_true',
            default = False
        )
        @command
        def my_command(prefix: str, force: bool, **kwargs) -> None:
            print("I'm now running stuff!")

        assert arg_group_exists('fruits')
        assert has_argument('fruits', 'cherry')
        assert has_argument('fruits', 'banana')

        assert arg_group_exists('vegetables')
        assert has_argument('vegetables', 'squash')
        assert has_argument('vegetables', 'tomato')

        assert arg_group_exists('produce')
        assert has_argument(produce, 'cherry')
        assert has_argument('produce', 'banana')
        assert get_argument(produce, 'squash') is not None
        assert get_argument('produce', 'tomato') is not None

        assert shared_arg_exists('whatchamacallits')
        assert command_exists('my_command')

        assert has_argument('my_command', 'whatchamacallits')
        assert has_argument('my_command', 'cherry')
        assert has_argument('my_command', 'banana')
        assert has_argument('my_command', 'squash')
        assert has_argument('my_command', 'tomato')
        assert has_argument('my_command', 'force')
        assert has_argument('my_command', 'prefix')

        assert get_argument('my_command', 'whatchamacallits') == {
            "kind":   "arg",
            "args":   tuple(['-w', '--whatchamacallits']),
            "kwargs": {
                "dest": "whatchamacallits"
            },
            "name": "whatchamacallits"
        }

    finally:
        remove_shared_arg('whatchamacallits')
        remove_arg_group('produce')
        remove_arg_group('vegetables')
        remove_arg_group('fruits')
        remove_command('my_command')

        assert not command_exists('my_command')
        assert not arg_group_exists('produce')
        assert not arg_group_exists('vegetables')
        assert not arg_group_exists('fruits')
        assert not shared_arg_exists('whatchamacallits')
