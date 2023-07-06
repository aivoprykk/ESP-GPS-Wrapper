Import("env")

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
project_config = configparser.ConfigParser()
project_config.read("platformio.ini")
version = project_config.get("common", "release_version")


def publish_firmware(source, target, env):
    firmware_path = str(source[0])
    firmware_name = basename(firmware_path)

    print("Uploading {0} to Repository. Version: {1}".format(
        firmware_name, version))

    url = "/".join([
        "https://esplogger.majasa.ee", "api", "firmware", version, firmware_name
    ])

    headers = {
        "Content-type": "application/octet-stream",
        "X-F-Publish": "1",
        "X-F-Override": "1"
    }

    r = None
    try:
        r = requests.put(url,
                         data=open(firmware_path, "rb"),
                         headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        sys.stderr.write("Failed to submit package: %s\n" %
                         ("%s\n%s" % (r.status_code, r.text) if r else str(e)))
        env.Exit(1)

    print("The firmware has been successfuly published at Bintray.com!")


env.Replace(PROGNAME="firmware_v_%s" % version)