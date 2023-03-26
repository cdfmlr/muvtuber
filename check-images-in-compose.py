import subprocess

result = subprocess.run('docker images | grep cdfmlr/muv', stdout=subprocess.PIPE, shell=True)

with open('docker-compose.yml') as f:
    yml = f.read()


for line in result.stdout.decode()[:-1].split('\n'):
    print('image:', line)
    # fields = filter(lambda x: x, line.split(' '))
    # image  = ':'.join(map(lambda x: x(), [lambda: next(fields)]*2))
    # 太阴间了
    fields = list(filter(lambda x: x, line.split(' ')))
    image  = ':'.join(fields[:2])
    assert image in yml, f'missmatch: image {image} not in docker-compose.yml.'

print('✅')

