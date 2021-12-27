from datetime import datetime

import click

from pinata.api_key import get_key_manager
from pinata.exceptions import PinataException
from pinata.sdk import Pinata

profile_option = click.option(
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
        click.echo("There are no stored API keys.")

    for name in profile_names:
        click.echo(name)


@keys.command("import")
@click.argument("profile_name")
@click.option("--api-key", help="The API key.", prompt=True)
@click.option("--api-secret", help="The API secret.", prompt=True)
def _import(profile_name, api_key, api_secret):
    """Import an existing API key pair."""
    key_manager = get_key_manager()
    key_manager.set_key_pair(profile_name, api_key, api_secret)
    click.echo(f"Successfully added API key profile {profile_name}")


@keys.command()
@click.argument("profile_name")
def remove(profile_name):
    """Remove an API key pair profile."""
    key_manager = get_key_manager()
    key_manager.delete_key_pair(profile_name)


@cli.command()
@click.option(
    "--status", default="all", type=click.Choice(["all", "pinned", "unpinned"])
)
@profile_option
def list_pins(status, profile):
    """List pins."""
    key_manager = get_key_manager()
    api_key, api_secret = key_manager.get_key_pair(profile)
    pinata = Pinata.from_api_key(api_key, api_secret)
    response = pinata.data.search_pins(status="pinned")
    pins = response["rows"]
    for pin in pins:
        date = datetime.strptime(pin["date_pinned"], "%Y-%m-%dT%H:%M:%S.%fZ")
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        row = f"CID (IPFS Pin Hash): {pin['ipfs_pin_hash']}, Pinned: {date_str}"
        click.echo(row)
