# popin-aladdin-light

CLI to control popIn Aladdin 2 ceiling light

## Examples

Turn on and off:

```
./popin_aladdin_light.py --host 192.168.22.111 --light on
./popin_aladdin_light.py --host 192.168.22.111 --light off
```

Change color and brightness:

```
./popin_aladdin_light.py --host 192.168.22.111 --light cooler --repeat 10
./popin_aladdin_light.py --host 192.168.22.111 --light warmer --repeat 10

./popin_aladdin_light.py --host 192.168.22.111 --light darker --repeat 10
./popin_aladdin_light.py --host 192.168.22.111 --light brighter --repeat 10
```
