# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tripay', 'tripay.payment']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tripay',
    'version': '0.1.1',
    'description': 'Tripay Client For Python (UNOFFICIAL)',
    'long_description': '# tripay\n\nTripay Client For Python (UNOFFICIAL)\n\nSupport:\n\n* Sandbox & Production Mode\n* Get Payment Instruction\n* Fee Calculator\n* Get Payment Channels\n* Closed Payment\n\n    * Helper to make order items\n    * Automatic signature generation\n    * Request payment\n    * Detail transaction\n    * List transaction\n\n* Open Payment\n\n    * Automatic signature generation\n    * Request payment\n    * Detail transaction\n    * List transaction\n\n* Easy to use\n\n# Usage\n\nInstallation:\n\n```\npip install tripay\n```\n\nSetup client:\n\n```python\nfrom tripay import TriPay\n\ntripay = TriPay(\n    api_key="DEV-xxx",\n    merchant_code="xxx",\n    merchant_private_key="xxx",\n    debug=True # sandbox mode\n)\n```\n\nGet Payment Instruction:\n\n```python\ntripay.get_payment_instruction("BRIVA").json()\n```\n\nFee Calculator:\n\n```python\ntripay.fee_calculator(5000).json()\n```\n\nGet Payment Channels:\n\n```python\ntripay.get_payment_channel().json()\n```\n\nClosed Payment:\n\n```python\n# access to closed payments\ncp = tripay.closed_payment\n\n# creating items\nitems = []\nitems.append(\n    cp.create_item(\n        sku="099999888",\n        name="sabun",\n        price=2500,\n        quantity=10\n    )\n)\n\n# request payment\nresp = cp.request(\n    "BRIVA",\n    2500 * 10,\n    customer_name="Dadang",\n    customer_email="someone@test.com",\n    customer_phone="0899988234",\n    order_items=items\n).json()\nprint(resp)\n```\n\nOpen Payment:\n\n```python\n# notes: for open payments currently does not support sandbox mode\ntripay.debug = False\n\n# access to open payments\nop = tripay.open_payment\n\n# request payment\nresp = op.request("BCAVA").json()\nprint(resp)\n```\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aprilahijriyan/tripay-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
