from features.nlp_parser import parse_command, register_contact

# Register a test contact
register_contact('rahim', '0xEEe7600847dbE0b271e9eBDd792C157D2EEF0343')

# Test commands
tests = [
    'send 0.01 ETH to rahim',
    'rahim ke 0.01 ETH pathao',
    'balance',
    'daily report',
    'should i buy 0.05 ETH',
    'swap 0.01 ETH to USDC',
    'help',
    'ki korte paro',
]

for cmd in tests:
    result = parse_command(cmd)
    print(f"{cmd!r:50} -> {result['action']:20} {result.get('params', {})}")
