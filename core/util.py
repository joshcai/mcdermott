# Utility functions used by multiple modules

from slackclient import SlackClient

from mcdermott import config

slack = SlackClient(config.SLACK_TOKEN)

def log_slack(message):
  slack.api_call(
    method="chat.postMessage",
    channel="#logging",
    text=message,
    username='logger',
    icon_emoji=':ant:'
  )

def normalize_name(name):
  return ''.join([c.lower() for c in name if c.isalpha()])