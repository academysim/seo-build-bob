# -*- coding: utf-8 -*-
"""RETIRED. Do not use. Superseded by shared/tools/deploy.py.

This script is kept only for its history. It must never run again, because it
would silently ship a WRONG deploy:

  * Its source directory (driver/tools/driver_new) no longer exists. os.walk over a
    missing directory yields nothing, and unlike shared/tools/deploy.py this
    script has no "if not local" guard, so it would build a deploy from its
    stale manifest, upload nothing, and exit 0 reporting success.
  * Its manifest is stale relative to the live site.

A digest deploy declares the COMPLETE file list, so anything missing from the
stale manifest is DELETED from the live site. That is how a deploy that looks
like it worked takes the money path backwards.

Use instead:
    python shared/tools/deploy.py driver --prod --replace /path,/path
"""
import sys

sys.exit("""driver_deploy.py is retired and will not run.
It would deploy from a stale manifest and silently revert live pages.
Use: python shared/tools/deploy.py driver --prod --replace <paths>""")
