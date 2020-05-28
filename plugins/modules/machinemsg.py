#!/usr/bin/python3

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: machinemsg

author:
    - Kasra Amirsarvari (@KasraMforce)

short_description: Set the machine motd and banner message

version_added: "2.9"

description:
    - Module that helps to set the machine motd and banner message

options:
    text:
        description:
            - The free text message to display
        type: str
        required: true
    when:
        description:
            - Whether to display before or after the login
        required: true
    state:
        description:
            - Whether to be present or absent
    fqdn:
        description:
            - If True, a new line with the full FQDN of the machine will be displayd

'''

EXAMPLES = '''
# make a before login message
- name: Message before login
  machinemsg:
    text: "Ola, user. You are bout to ENTER"
    when: before
    fqdn: true

# remove an after login message
- name: Message after login
  machinemsg:
    text: "Ola, user. You have ENTERED"
    when: after
    state: absent
    fqdn: False

'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

import socket
import os


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        text=dict(type='str', required=True),
        when=dict(type='str', required=True),
        state=dict(type='str', required=False, default="present"),
        fqdn=dict(type=bool, required=False, default=False)
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.params['when'] == "before":
        file = "/etc/issue"
    elif module.params['when'] == "after":
        file = "/etc/motd"
    else:
        module.fail_json(msg='syntax error in "when" parameter', **result)

    if module.params['fqdn']:
        finalmsg = module.params['text'] + "\nMachine: " + socket.getfqdn() + "\n"
    else:
        finalmsg = module.params['text'] + "\n"

    if module.params['state'] == "present":
        if not module.check_mode:
            f = open(file, "w")
            f.write(finalmsg)
            f.close()
        result['changed'] = True
    elif module.params['state'] == "absent":
        if not module.check_mode:
            os.remove(file)
        result['changed'] = True
    else:
        module.fail_json(msg='syntax error in state parameter', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
