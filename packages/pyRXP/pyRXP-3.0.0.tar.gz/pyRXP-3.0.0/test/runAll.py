class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def main():
    import sys, os, psutil, platform
    sys.__old_stderr__ = sys.stderr
    sys.__stderr__ = sys.stderr = sys.stdout = Unbuffered(sys.stdout)
    wd = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.path.insert(0,wd)
    os.chdir(wd)
    platform_attrs = [
        "architecture",
        "java_ver",
        "libc_ver",
        "machine",
        "mac_ver",
        "node",
        "platform",
        "processor",
        "python_branch",
        "python_build",
        "python_compiler",
        "python_implementation",
        "python_revision",
        "python_version",
        "python_version_tuple",
        "release",
        "system",
        "system_alias",
        "uname",
        "version",
        "win32_edition",
        "win32_is_iot",
        "win32_ver",
        ]
    print(f'+++++ {sys.platform}')
    print(f'+++++ {sys.byteorder}')
    for a in platform_attrs:
        if hasattr(platform,a):
            try:
                print(f'+++++ platform.{a}()={getattr(platform,a)()}')
            except:
                print(f'!!!!! platform.{a}()=cannot be determined')

    #special case import to allow reportlab to modify the envirnment in development
    try:
      import reportlab
    except ImportError:
      pass

    import leaktest, testRXPbasic, test_xmltestsuite

    leaktest.main(100)
    testRXPbasic.main()
    if 1 or platform.system()!='Darwin':
        verbose=int(os.environ.get('VERBOSE','0'))
        singles=int(os.environ.get('SINGLES','0'))
        test_xmltestsuite.main(verbose, singles)
    else:
        test_xmltestsuite.main(3,1)
    print(f'+++++ open Files={psutil.Process().open_files()!r}')

if __name__=='__main__':
    main()
