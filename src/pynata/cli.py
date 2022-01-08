import sys
from pathlib import Path

import click

from pynata.api_key import get_key_manager
from pynata.exceptions import PinataException
from pynata.sdk import Pinata
from pynata.utils import prettify_date


def profile_option():
    return click.option(
        "--profile",
        "-p",
        help="The profile to use",
        default=get_key_manager().default_profile_name,
    )


class ExceptionHandlingGroup(click.Group):
    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except PinataException as err:
            click.echo(str(err), err=True)


@click.group(cls=ExceptionHandlingGroup)
def cli():
    pass


@cli.group("api-key")
def keys():
    """Manage your API key."""


@keys.command("list")
def list_keys():
    """List your API key profile names."""

    key_manager = get_key_manager()
    profile_names = key_manager.profile_names

    if not profile_names:
        _echo_no_profile()

    for name in profile_names:
        click.echo(name)


def _get_pinata(profile: str) -> Pinata:
    key_manager = get_key_manager()
    api_key, api_secret = key_manager.get_key_pair(profile)
    return Pinata.from_api_key(api_key, api_secret)


@keys.command("import")
@click.argument("profile_name")
@click.option("--api-key", help="The API key.", prompt=True)
@click.option("--api-secret", help="The API secret.", prompt=True)
def import_key(profile_name, api_key, api_secret):
    """Import an existing API key pair."""
    key_manager = get_key_manager()
    key_manager.set_key_pair(profile_name, api_key, api_secret)
    click.echo(f"Successfully added API key profile {profile_name}")


@keys.command("remove")
@click.argument("profile_name")
def remove_key(profile_name):
    """Remove an API key pair profile."""
    key_manager = get_key_manager()
    key_manager.delete_key_pair(profile_name)


@keys.command("rename")
@click.option("--old-name", help="The name of the profile to change.", required=True)
@click.option("--new-name", help="The new name of the profile.", required=True)
def rename_key(old_name, new_name):
    """Remove an API key pair profile."""
    key_manager = get_key_manager()
    key_manager.rename_key_pair(old_name, new_name)
    click.echo(f"Successfully renamed API key profile '{old_name}' to '{new_name}'.")


@cli.command()
@click.option(
    "--status", default="pinned", type=click.Choice(["all", "pinned", "unpinned"])
)
@profile_option()
def list_pins(status, profile):
    """List pins."""
    if not profile:
        _echo_no_profile()
        sys.exit(1)

    pinata = _get_pinata(profile)
    response = pinata.data.search_pins(status=status)
    pins = response["rows"]
    for pin in pins:
        name = pin["metadata"].get("name", "<Unnamed>")
        date_str = prettify_date(pin["date_pinned"])
        row = f"Name: {name}, CID (IPFS Pin Hash): {pin['ipfs_pin_hash']}, Pinned: {date_str}"
        click.echo(row)


@cli.command()
@click.argument("file_path", type=Path)
@profile_option()
def pin(file_path, profile):
    """Pin a new file."""
    pinata = _get_pinata(profile)
    cid = pinata.pin_file(file_path)
    click.echo(f"Successfully unpinned content. CID={cid}")


@cli.command()
@click.argument("content_hash")
@profile_option()
def unpin(content_hash, profile):
    """Remove a pin."""
    pinata = _get_pinata(profile)
    pinata.unpin(content_hash)
    click.echo("Successfully unpinned content.")


def _echo_no_profile():
    click.echo("There are no stored API keys.")
