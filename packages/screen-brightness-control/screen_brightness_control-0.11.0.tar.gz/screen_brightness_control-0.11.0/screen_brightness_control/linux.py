import subprocess
import os
from . import _monitor_brand_lookup, filter_monitors, __cache__, EDID
from typing import List, Union, Optional


class SysFiles:
    '''
    A way of getting display information and adjusting the brightness
    that does not rely on any 3rd party software.

    This class works with displays that show up in the `/sys/class/backlight`
    directory (so usually laptop displays).

    To set the brightness, your user will need write permissions for
    `/sys/class/backlight/*/brightness` or you will need to run the program
    as root.
    '''
    @classmethod
    def get_display_info(cls, display: Optional[Union[int, str]] = None) -> List[dict]:
        '''
        Returns information about detected displays by reading files from the
        `/sys/class/backlight` directory

        Args:
            display (str or int): [*Optional*] The monitor to return info about.
                Pass in the serial number, name, model, interface, edid or index.
                This is passed to `filter_monitors`

        Returns:
            list: list of dicts

        Example:
            ```python
            import screen_brightness_control as sbc

            # get info about all monitors
            info = sbc.linux.SysFiles.get_display_info()
            # EG output: [{'name': 'edp-backlight', 'path': '/sys/class/backlight/edp-backlight', edid': '00ffff...'}]

            # get info about the primary monitor
            primary_info = sbc.linux.SysFiles.get_display_info(0)[0]

            # get info about a monitor called 'edp-backlight'
            edp_info = sbc.linux.SysFiles.get_display_info('edp-backlight')[0]
            ```
        '''
        displays = {}
        index = 0
        for folder in os.listdir('/sys/class/backlight'):
            if os.path.isfile(f'/sys/class/backlight/{folder}/device/edid'):
                device = {
                    'name': folder,
                    'path': f'/sys/class/backlight/{folder}',
                    'method': cls,
                    'index': index,
                    'model': None,
                    'serial': None,
                    'manufacturer': None,
                    'manufacturer_id': None,
                    'edid': EDID.hexdump(f'/sys/class/backlight/{folder}/device/edid'),
                    'scale': None
                }

                try:
                    # try to get resolution of brightness settings
                    with open(os.path.join(device['path'], 'max_brightness'), 'r') as f:
                        device['scale'] = int(f.read().rstrip('\n')) / 100
                except (FileNotFoundError, TypeError):
                    # if the scale cannot be figured out then exclude the display
                    continue

                # now check for duplicate displays
                if device['edid'] in displays:
                    if (
                        displays[device['edid']]['scale'] == 1
                        or displays[device['edid']]['scale'] >= device['scale']
                    ):
                        # if there is a duplicate display, pick the display with
                        # a scale equal to 1 or the display with the highest scale.
                        # Reduces rounding errrors when converting percentages
                        # to 'actual' values
                        continue

                name, serial = EDID.parse_edid(device['edid'])
                if name is not None:
                    device['name'], device['serial'] = name, serial

                    try:
                        manufacturer_id, manufacturer = _monitor_brand_lookup(name.split(' ')[0])
                    except TypeError:
                        device['manufacturer'] = name.split(' ')[0]
                        device['manufacturer_id'] = None
                    else:
                        device['manufacturer_id'], device['manufacturer'] = manufacturer_id, manufacturer

                    device['model'] = name.split(' ')[1]

                displays[device['edid']] = device
                index += 1

        displays = list(displays.values())
        if display is not None:
            displays = filter_monitors(display=display, haystack=displays, include=['path'])
        return displays

    @classmethod
    def get_brightness(cls, display: Optional[int] = None) -> List[int]:
        '''
        Gets the brightness for a display by reading the brightness files
        stored in `/sys/class/backlight/*/brightness`

        Args:
            display (int): The specific display you wish to query.

        Returns:
            list: list of ints (0 to 100)

        Example:
            ```python
            import screen_brightness_control as sbc

            # get the current display brightness
            current_brightness = sbc.linux.SysFiles.get_brightness()

            # get the brightness of the primary display
            primary_brightness = sbc.linux.SysFiles.get_brightness(display = 0)[0]

            # get the brightness of the secondary display
            edp_brightness = sbc.linux.SysFiles.get_brightness(display = 1)[0]
            ```
        '''
        info = cls.get_display_info()
        if display is not None:
            info = [info[display]]

        results = []
        for device in info:
            with open(os.path.join(device['path'], 'brightness'), 'r') as f:
                brightness = int(f.read().rstrip('\n'))
            results.append(int(brightness / device['scale']))

        return results

    @classmethod
    def set_brightness(cls, value: int, display: Optional[int] = None):
        '''
        Sets the brightness for a display by writing to the brightness files
        stored in `/sys/class/backlight/*/brightness`.
        This function requires permission to write to these files which is
        usually provided when it's run as root.

        Args:
            value (int): Sets the brightness to this value
            display (int): The specific display you wish to query.

        Example:
            ```python
            import screen_brightness_control as sbc

            # set the brightness to 50%
            sbc.linux.SysFiles.set_brightness(50)

            # set the primary display brightness to 75%
            sbc.linux.SysFiles.set_brightness(75, display = 0)

            # set the secondary display brightness to 25%
            sbc.linux.SysFiles.set_brightness(75, display = 1)
            ```
        '''
        info = cls.get_display_info()
        if display is not None:
            info = [info[display]]

        for device in info:
            with open(os.path.join(device['path'], 'brightness'), 'w') as f:
                f.write(str(int(value * device['scale'])))


class Light:
    '''collection of screen brightness related methods using the light executable'''

    executable: str = 'light'
    '''the light executable to be called'''

    @classmethod
    def get_display_info(cls, display: Optional[Union[int, str]] = None) -> List[dict]:
        '''
        Returns information about detected displays as reported by Light.

        It works by taking the output of `SysFiles.get_display_info` and
        filtering out any displays that aren't supported by Light

        Args:
            display (str or int): [*Optional*] The monitor to return info about.
                Pass in the serial number, name, model, interface, edid or index.
                This is passed to `filter_monitors`

        Returns:
            list: list of dicts

        Example:
            ```python
            import screen_brightness_control as sbc

            # get info about all monitors
            info = sbc.linux.Light.get_display_info()
            # EG output: [{'name': 'edp-backlight', 'path': '/sys/class/backlight/edp-backlight', edid': '00ffff...'}]

            # get info about the primary monitor
            primary_info = sbc.linux.Light.get_display_info(0)[0]

            # get info about a monitor called 'edp-backlight'
            edp_info = sbc.linux.Light.get_display_info('edp-backlight')[0]
            ```
        '''
        light_output = subprocess.check_output([cls.executable, '-L']).decode()
        displays = []
        index = 0
        for device in SysFiles.get_display_info():
            # SysFiles scrapes info from the same place that Light used to
            # so it makes sense to use that output
            if device['path'].replace('/sys/class', 'sysfs') in light_output:
                del device['scale']
                device['light_path'] = device['path'].replace('/sys/class', 'sysfs')
                device['method'] = cls
                device['index'] = index

                displays.append(device)
                index += 1

        if display is not None:
            displays = filter_monitors(display=display, haystack=displays, include=['path', 'light_path'])
        return displays

    @classmethod
    def set_brightness(cls, value: int, display: Optional[int] = None):
        '''
        Sets the brightness for a display using the light executable

        Args:
            value (int): Sets the brightness to this value
            display (int): The specific display you wish to query.

        Example:
            ```python
            import screen_brightness_control as sbc

            # set the brightness to 50%
            sbc.linux.Light.set_brightness(50)

            # set the primary display brightness to 75%
            sbc.linux.Light.set_brightness(75, display = 0)

            # set the secondary display brightness to 25%
            sbc.linux.Light.set_brightness(75, display = 1)
            ```
        '''
        info = cls.get_display_info()
        if display is not None:
            info = [info[display]]

        for i in info:
            subprocess.call(f'{cls.executable} -S {value} -s {i["light_path"]}'.split(" "))

    @classmethod
    def get_brightness(cls, display: Optional[int] = None) -> List[int]:
        '''
        Gets the brightness for a display using the light executable

        Args:
            display (int): The specific display you wish to query.

        Returns:
            list: list of ints (0 to 100)

        Example:
            ```python
            import screen_brightness_control as sbc

            # get the current display brightness
            current_brightness = sbc.linux.Light.get_brightness()

            # get the brightness of the primary display
            primary_brightness = sbc.linux.Light.get_brightness(display = 0)[0]

            # get the brightness of the secondary display
            edp_brightness = sbc.linux.Light.get_brightness(display = 1)[0]
            ```
        '''
        info = cls.get_display_info()
        if display is not None:
            info = [info[display]]

        results = []
        for i in info:
            results.append(
                subprocess.check_output(
                    [
                        cls.executable, '-G', '-s', i['light_path']
                    ]
                )
            )
        results = [int(round(float(i.decode()), 0)) for i in results]
        return results


class XBacklight:
    '''collection of screen brightness related methods using the xbacklight executable'''

    executable: str = 'xbacklight'
    '''the xbacklight executable to be called'''

    @classmethod
    def set_brightness(cls, value: int, **kwargs):
        '''
        Sets the screen brightness to a supplied value

        Args:
            value (int): the value to set the brightnes to
            **kwargs: arbitrary keyword arguments. Ignored

        Example:
            ```python
            import screen_brightness_control as sbc

            # set the brightness to 100%
            sbc.linux.XBacklight.set_brightness(100)
            ```
        '''
        subprocess.call([cls.executable, '-set', str(value)])

    @classmethod
    def get_brightness(cls, **kwargs) -> int:
        '''
        Returns the screen brightness as reported by xbacklight

        Returns:
            int: from 0 to 100
            **kwargs: arbitrary keyword arguments. Ignored

        Example:
            ```python
            import screen_brightness_control as sbc

            current_brightness = sbc.linux.XBacklight.get_brightness()
            ```
        '''
        res = subprocess.run(
            [cls.executable, '-get'],
            stdout=subprocess.PIPE
        ).stdout.decode()
        return int(round(float(str(res)), 0))


class XRandr:
    '''collection of screen brightness related methods using the xrandr executable'''

    executable: str = 'xrandr'
    '''the xrandr executable to be called'''

    @classmethod
    def get_display_info(cls, display: Optional[Union[int, str]] = None, brightness: bool = False) -> List[dict]:
        '''
        Returns info about all detected monitors as reported by xrandr

        Args:
            display (str or int): [*Optional*] The monitor to return info about.
                Pass in the serial number, name, model, interface, edid or index.
                This is passed to `filter_monitors`
            brightness (bool): whether to include the current brightness
                in the returned info

        Returns:
            list: list of dicts

        Example:
            ```python
            import screen_brightness_control as sbc

            info = sbc.linux.XRandr.get_display_info()
            for i in info:
                print('================')
                for key, value in i.items():
                    print(key, ':', value)

            # get information about the first XRandr addressable monitor
            primary_info = sbc.linux.XRandr.get_display_info(0)[0]

            # get information about a monitor with a specific name
            benq_info = sbc.linux.XRandr.get_display_info('BenQ GL2450HM')[0]
            ```
        '''
        def check_tmp(tmp):
            if tmp != {}:
                if tmp['serial'] is None or '\\x' not in tmp['serial']:
                    if 'line' in tmp:
                        del(tmp['line'])
                    return True
            return False

        out = subprocess.check_output([cls.executable, '--verbose']).decode().split('\n')
        names = cls.get_display_interfaces()
        data = []
        tmp = {}
        count = 0
        for i in out:
            if i != '':
                if i.startswith(tuple(names)):
                    if check_tmp(tmp):
                        data.append(tmp)
                    tmp = {
                        'interface': i.split(' ')[0],
                        'name': i.split(' ')[0],
                        'line': i,
                        'method': cls,
                        'index': count,
                        'model': None,
                        'serial': None,
                        'manufacturer': None,
                        'manufacturer_id': None,
                        'edid': None
                    }
                    count += 1
                elif 'EDID:' in i:
                    st = out[out.index(tmp['line']):]
                    edid = []
                    for j in range(st.index(i) + 1, st.index(i) + 9):
                        edid.append(st[j].replace('\t', '').replace(' ', ''))
                    edid = ''.join(edid)
                    tmp['edid'] = edid
                    name, serial = EDID.parse_edid(edid)
                    tmp['name'] = name if name is not None else tmp['interface']
                    if name is not None:
                        tmp['manufacturer'] = name.split(' ')[0]
                        try:
                            tmp['manufacturer_id'], tmp['manufacturer'] = _monitor_brand_lookup(
                                tmp['manufacturer']
                            )
                        except Exception:
                            tmp['manufacturer_id'] = None
                        tmp['model'] = name.split(' ')[1]
                        tmp['serial'] = serial
                elif 'Brightness:' in i and brightness:
                    tmp['brightness'] = int(
                        float(i.replace('Brightness:', '').replace(' ', '').replace('\t', '')) * 100
                    )
        if check_tmp(tmp):
            data.append(tmp)

        if display is not None:
            data = filter_monitors(display=display, haystack=data, include=['interface'])
        return data

    @classmethod
    def get_display_interfaces(cls) -> List[str]:
        '''
        Returns the interfaces of each display, as reported by xrandr

        Returns:
            list: list of strings

        Example:
            ```python
            import screen_brightness_control as sbc

            names = sbc.linux.XRandr.get_display_interfaces()
            # EG output: ['eDP-1', 'HDMI1', 'HDMI2']
            ```
        '''
        out = subprocess.check_output([cls.executable, '-q']).decode().split('\n')
        return [i.split(' ')[0] for i in out if 'connected' in i and 'disconnected' not in i]

    @classmethod
    def get_brightness(cls, display: Optional[int] = None) -> List[int]:
        '''
        Returns the brightness for a display using the xrandr executable

        Args:
            display (int): The specific display you wish to query.

        Returns:
            list: list of integers (from 0 to 100)

        Example:
            ```python
            import screen_brightness_control as sbc

            # get the current brightness
            current_brightness = sbc.linux.XRandr.get_brightness()

            # get the current brightness for the primary display
            primary_brightness = sbc.linux.XRandr.get_brightness(display=0)[0]
            ```
        '''
        monitors = cls.get_display_info(brightness=True)
        if display is not None:
            monitors = [monitors[display]]
        brightness = [i['brightness'] for i in monitors]

        return brightness

    @classmethod
    def set_brightness(cls, value: int, display: Optional[int] = None):
        '''
        Sets the brightness for a display using the xrandr executable

        Args:
            value (int): Sets the brightness to this value
            display (int): The specific display you wish to query.

        Example:
            ```python
            import screen_brightness_control as sbc

            # set the brightness to 50
            sbc.linux.XRandr.set_brightness(50)

            # set the brightness of the primary display to 75
            sbc.linux.XRandr.set_brightness(75, display=0)
            ```
        '''
        value = str(float(value) / 100)
        info = cls.get_display_info()
        if display is not None:
            info = [info[display]]

        for i in info:
            subprocess.run([cls.executable, '--output', i['interface'], '--brightness', value])

        # The get_brightness method takes the brightness value from get_display_info
        # The problem is that that display info is cached, meaning that the brightness
        # value is also cached. We must expire it here.


class DDCUtil:
    '''collection of screen brightness related methods using the ddcutil executable'''

    executable: str = 'ddcutil'
    '''the ddcutil executable to be called'''
    sleep_multiplier: float = 0.5
    '''how long ddcutil should sleep between each DDC request (lower is shorter).
    See [the ddcutil docs](https://www.ddcutil.com/performance_options/) for more info.'''

    @classmethod
    def get_display_info(cls, display: Optional[Union[int, str]] = None) -> List[dict]:
        '''
        Returns information about all DDC compatible monitors shown by DDCUtil
        Works by calling the command 'ddcutil detect' and parsing the output.

        Args:
            display (int or str): [*Optional*] The monitor to return info about.
                Pass in the serial number, name, model, i2c bus, edid or index.
                This is passed to `filter_monitors`

        Returns:
            list: list of dicts

        Example:
            ```python
            import screen_brightness_control as sbc

            info = sbc.linux.DDCUtil.get_display_info()
            for i in info:
                print('================')
                for key, value in i.items():
                    print(key, ':', value)

            # get information about the first DDCUtil addressable monitor
            primary_info = sbc.linux.DDCUtil.get_display_info(0)[0]

            # get information about a monitor with a specific name
            benq_info = sbc.linux.DDCUtil.get_display_info('BenQ GL2450HM')[0]
            ```
        '''
        def check_tmp(tmp):
            if tmp != {} and 'Invalid display' not in tmp['tmp']:
                if 'tmp' in tmp:
                    del(tmp['tmp'])
                return True
            return False

        data = __cache__.get('ddcutil_monitors_info')
        if data is None:
            out = []
            # Use -v to get EDID string but this means output cannot be decoded.
            # Or maybe it can. I don't know the encoding though, so let's assume it cannot be decoded.
            # Use str()[2:-1] workaround
            cmd_out = str(
                subprocess.check_output(
                    [
                        cls.executable,
                        'detect', '-v',
                        f'--sleep-multiplier={cls.sleep_multiplier}'
                    ], stderr=subprocess.DEVNULL
                )
            )[2:-1].split('\\n')

            for line in cmd_out:
                if line != '' and line.startswith(('Invalid display', 'Display', '\t', ' ')):
                    out.append(line)
            data = []
            tmp = {}
            count = 0
            for i in range(len(out)):
                line = out[i]
                if not line.startswith(('\t', ' ')):
                    if check_tmp(tmp):
                        data.append(tmp)
                    tmp = {
                        'tmp': line,
                        'method': cls,
                        'index': count,
                        'model': None,
                        'serial': None,
                        'manufacturer': None,
                        'manufacturer_id': None,
                        'edid': None
                    }
                    count += 1
                else:
                    if 'I2C bus' in line:
                        tmp['i2c_bus'] = line[line.index('/'):]
                        tmp['bus_number'] = int(tmp['i2c_bus'].replace('/dev/i2c-', ''))
                    elif 'Mfg id' in line:
                        tmp['manufacturer_id'] = line.replace('Mfg id:', '').replace('\t', '').replace(' ', '')
                        try:
                            tmp['manufacturer_id'], tmp['manufacturer'] = _monitor_brand_lookup(tmp['manufacturer_id'])
                        except Exception:
                            pass
                    elif 'Model' in line:
                        name = [i for i in line.replace('Model:', '').replace('\t', '').split(' ') if i != '']
                        try:
                            name[0] = name[0].lower().capitalize()
                        except IndexError:
                            pass
                        tmp['name'] = ' '.join(name)
                        try:
                            tmp['model'] = name[1]
                        except IndexError:
                            pass
                    elif 'Serial number' in line:
                        tmp['serial'] = line.replace('Serial number:', '').replace('\t', '').replace(' ', '')
                    elif 'EDID hex dump:' in line:
                        try:
                            tmp['edid'] = ''.join(
                                j[j.index('+0') + 8: j.index('+0') + 55].replace(' ', '') for j in out[i + 2: i + 10]
                            )
                        except Exception:
                            pass
            if check_tmp(tmp):
                data.append(tmp)
            __cache__.store('ddcutil_monitors_info', data)

        if display is not None:
            data = filter_monitors(display=display, haystack=data, include=['i2c_bus'])
        return data

    @classmethod
    def get_brightness(cls, display: Optional[int] = None) -> List[int]:
        '''
        Returns the brightness for a display using the ddcutil executable

        Args:
            display (int): The specific display you wish to query.

        Returns:
            list: list of ints (0 to 100)

        Example:
            ```python
            import screen_brightness_control as sbc

            # get the current brightness
            current_brightness = sbc.linux.DDCUtil.get_brightness()

            # get the current brightness for the primary display
            primary_brightness = sbc.linux.DDCUtil.get_brightness(display=0)[0]
            ```
        '''
        monitors = cls.get_display_info()
        if display is not None:
            monitors = [monitors[display]]

        res = []
        for m in monitors:
            out = __cache__.get(f'ddcutil_brightness_{m["index"]}')
            if out is None:
                out = subprocess.check_output(
                    [
                        cls.executable,
                        'getvcp', '10', '-t',
                        '-b', str(m['bus_number']),
                        f'--sleep-multiplier={cls.sleep_multiplier}'
                    ]
                ).decode().split(' ')[-2]
                __cache__.store(f'ddcutil_brightness_{m["index"]}', out, expires=0.5)
            try:
                res.append(int(out))
            except Exception:
                pass
        return res

    @classmethod
    def set_brightness(cls, value: int, display: Optional[int] = None):
        '''
        Sets the brightness for a display using the ddcutil executable

        Args:
            value (int): Sets the brightness to this value
            display (int): The specific display you wish to query.

        Example:
            ```python
            import screen_brightness_control as sbc

            # set the brightness to 50
            sbc.linux.DDCUtil.set_brightness(50)

            # set the brightness of the primary display to 75
            sbc.linux.DDCUtil.set_brightness(75, display=0)
            ```
        '''
        monitors = cls.get_display_info()
        if display is not None:
            monitors = [monitors[display]]

        __cache__.expire(startswith='ddcutil_', endswith='_brightness')
        for m in monitors:
            subprocess.run(
                [
                    cls.executable, 'setvcp', '10', str(value),
                    '-b', str(m['bus_number']),
                    f'--sleep-multiplier={cls.sleep_multiplier}'
                ]
            )


def list_monitors_info(method: Optional[str] = None, allow_duplicates: bool = False) -> List[dict]:
    '''
    Lists detailed information about all detected monitors

    Args:
        method (str): the method the monitor can be addressed by. Can be 'xrandr' or 'ddcutil' or 'light'
        allow_duplicates (bool): whether to filter out duplicate displays (displays with the same EDID) or not

    Returns:
        list: list of dicts

    Raises:
        ValueError: if the method kwarg is invalid

    Example:
        ```python
        import screen_brightness_control as sbc

        monitors = sbc.linux.list_monitors_info()
        for monitor in monitors:
            print('=======================')
            # the manufacturer name plus the model OR a generic name for the monitor, depending on the method
            print('Name:', monitor['name'])
            # the general model of the display
            print('Model:', monitor['model'])
            # the serial of the display
            print('Serial:', monitor['serial'])
            # the name of the brand of the monitor
            print('Manufacturer:', monitor['manufacturer'])
            # the 3 letter code corresponding to the brand name, EG: BNQ -> BenQ
            print('Manufacturer ID:', monitor['manufacturer_id'])
            # the index of that display FOR THE SPECIFIC METHOD THE DISPLAY USES
            print('Index:', monitor['index'])
            # the method this monitor can be addressed by
            print('Method:', monitor['method'])
        ```
    '''
    info = __cache__.get('linux_monitors_info', method=method, allow_duplicates=allow_duplicates)
    if info is None:
        methods = [XRandr, DDCUtil, Light, SysFiles]
        if method is not None:
            method = method.lower()
            if method not in ('xrandr', 'ddcutil', 'light', 'sysfiles'):
                raise ValueError((
                    'method must be "xrandr" or "ddcutil" or "light"'
                    ' or "sysfiles" to get monitor information'
                ))

        info = []
        edids = []
        for m in methods:
            if method is None or method == m.__name__.lower():
                # to make sure each display (with unique edid) is only reported once
                try:
                    tmp = m.get_display_info()
                except Exception:
                    pass
                else:
                    for i in tmp:
                        if allow_duplicates or i['edid'] not in edids:
                            edids.append(i['edid'])
                            info.append(i)
        __cache__.store('linux_monitors_info', info, method=method, allow_duplicates=allow_duplicates)
    return info
