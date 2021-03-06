"Functions for checking/adjusting the configuration of the SR python user site package"
import site, os, sys

def check_installed():
    "Check that we're installed, if not, install"
    s = site.getusersitepackages()

    # There should be a symlink
    sym = os.path.join( s, "sr" )
    # to here:
    target = os.path.abspath( os.path.join( os.path.dirname(__file__),
                                            "..", "python" ) )

    if not os.path.exists( s ):
        os.makedirs( s )

    if os.path.exists(sym):
        try:
            cur_target = os.readlink( sym )
            c = os.path.abspath( cur_target )

            if c == target:
                "Installed, and pointing at the right place"
                return

            # Wrong target directory -- rewrite it
            os.unlink( sym )

        except OSError:
            print >>sys.stderr, "Error: %s is not a symlink.  Refusing to continue." % sym
            exit(1)

    print >>sys.stderr, "Installing SR python usersitepackage"
    os.symlink( target, sym )
