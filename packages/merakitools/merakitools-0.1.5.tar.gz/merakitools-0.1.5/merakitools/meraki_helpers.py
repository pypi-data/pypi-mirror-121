"""
merakitools - meraki_helpers.py
Billy Zoellers

CLI tools for managing Meraki networks based on Typer
"""
import os
from meraki.exceptions import APIError
import requests
import typer
from merakitools.console import console
from merakitools.dashboardapi import dashboard
from typer import Abort
from rich.prompt import Confirm

def find_orgs_by_name(org_name: str):
  """
  Given a name, find any matching organizations
  """
  with console.status("Accessing API..."):
    orgs = dashboard.organizations.getOrganizations()
  if org_name:
    orgs = [org for org in orgs if org_name in org['name']]
  return orgs

def find_org_by_name(org_name: str):
  """
  Given a name, find a single matching organization by prompting the user
  """
  orgs = find_orgs_by_name(org_name)

  if len(orgs) == 1:
    return orgs[0]

  if len(orgs) > 1:
    console.print(f"Found {len(orgs)} orgs matching [bold]{org_name}[/bold]...")
    for org in orgs:
      found = Confirm.ask(f" Did you mean [bold]{org['name']}[/bold], with ID {org['id']}?", console=console)
      if found:
        return org

  print("No orgs found.")
  raise Abort()

def find_org_id_by_device_serial(serial: str):
  """
  Given a serial, find the organization it belongs to
  """
  try:
    device = dashboard.devices.getDevice(serial=serial)
  except APIError as err:
    console.print(f"[red]Unable to find device with serial \'{serial}\'")
    raise typer.Abort()

  network = dashboard.networks.getNetwork(networkId=device["networkId"])
  
  return network["organizationId"]

def find_network_by_name(org_name: str, net_name: str):
  """
  Find a network given an orgaization name and network name
  """
  org = find_org_by_name(org_name)
  with console.status("Accessing API..."):
    nets = dashboard.organizations.getOrganizationNetworks(org["id"])

  try:
    return next(net for net in nets if net["name"] == net_name)
  except StopIteration:
    print("Network not found.")
    raise Abort() 

def api_req(resource: str, method: str = "GET", **kwargs):
  """
  API request outside of the Meraki Python SDK
  """
  base_url = "https://api.meraki.com/api/v1"
  headers = {
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": os.getenv('MERAKI_DASHBOARD_API_KEY')
  }

  resp = requests.request(
    url=f"{base_url}/{resource}",
    method=method,
    headers=headers,
    **kwargs
  )

  resp.raise_for_status()
  if resp.text:
    return resp.json()

  return {}