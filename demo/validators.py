
import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\["\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

def valid_email(email):
  """ Check email address validity. Same code used by Django.

  Related Articles:
    http://aralbalkan.com/1353
    http://haacked.com/archive/2007/
      08/21/i-knew-how-to-validate-an-email-address-until-i.aspx
  """
  return True if email and email_re.match(email) else False
