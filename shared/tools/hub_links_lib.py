# -*- coding: utf-8 -*-
"""Shared helpers for the four add_hub_links.py scripts.

Extracted from lounge/events/builds/health add_hub_links.py to eliminate the
duplicated rd/wr/adapt helpers and the near-identical --tree parsing, footer-
patch and template-patch loops.  Each property's add_hub_links.py is now a
thin wrapper: it imports from here, defines its HTML content constants, and
calls the helpers.

The adapt() function is kept byte-for-byte identical to the copies in the
original scripts, because builds/source/index.html existed before the
.gitattributes eol=lf pin and may carry CRLF line endings.  Do not simplify it.
"""
import io
import os
import sys


# ---------------------------------------------------------------------------
# Low-level I/O
# ---------------------------------------------------------------------------

def rd(p):
    """Read a file as a UTF-8 string, preserving its native line endings."""
    with io.open(p, encoding='utf-8', newline='') as f:
        return f.read()


def wr(p, s):
    """Write a UTF-8 string to a file, preserving whatever endings are in s."""
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def adapt(pattern, s):
    """Convert a LF-written pattern to match the line endings of s.

    The patterns in every add_hub_links.py are authored with LF.  A file that
    is CRLF throughout (builds/source/index.html) needs the same pattern with
    CRLF, and the replacement written back with the file's own endings, so the
    source tree never gains mixed line endings from this tool.
    """
    return pattern.replace('\n', '\r\n') if '\r\n' in s else pattern


# ---------------------------------------------------------------------------
# --tree argument parsing
# ---------------------------------------------------------------------------

def parse_tree_arg(valid=('site', 'source', 'upload')):
    """Return the tree directory name from --tree <name> in sys.argv.

    Exits with an error message if the value is not in *valid*.
    Returns 'upload' when --tree is absent.
    """
    tree = 'upload'
    if '--tree' in sys.argv:
        tree = sys.argv[sys.argv.index('--tree') + 1]
    if tree not in valid:
        raise SystemExit('--tree must be one of: %s' % ', '.join(valid))
    return tree


# ---------------------------------------------------------------------------
# Patch helpers
# ---------------------------------------------------------------------------

def patch_homepage(up, anchor, section_html, sentinel):
    """Prepend *section_html* before *anchor* in up/index.html if not present.

    Parameters
    ----------
    up          : str   — absolute path to the tree root (e.g. lounge/upload/)
    anchor      : str   — literal string that must appear exactly once
    section_html: str   — the <section> block to insert (authored with LF)
    sentinel    : str   — a string whose presence means the patch is already done

    All string comparisons adapt to the file's actual line endings via adapt().
    Prints a one-line status message.
    """
    p = os.path.join(up, 'index.html')
    s = rd(p)
    real_anchor = adapt(anchor, s)
    n = s.count(real_anchor)
    assert n == 1, 'homepage anchor %r x%d' % (anchor, n)
    if sentinel not in s:
        s = s.replace(real_anchor, adapt(section_html, s) + real_anchor, 1)
        wr(p, s)
        print('homepage: section added')
    else:
        print('homepage: section already present, skipped')


def patch_footer(up, old_block, new_block):
    """Replace *old_block* with *new_block* in every up/**/index.html.

    Skips the homepage (it is handled by patch_homepage).
    Adapts both blocks to each file's actual line endings.
    Prints counts of patched / already-updated / unmatched pages.

    Returns a tuple (touched, present, unmatched) of path lists.
    """
    touched, present, unmatched = [], [], []
    for root, _, fs in os.walk(up):
        for f in fs:
            if f != 'index.html':
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, up).replace(os.sep, '/')
            if rel == 'index.html':
                continue  # homepage handled separately
            s = rd(p)
            old = adapt(old_block, s)
            new = adapt(new_block, s)
            if old in s:
                s = s.replace(old, new, 1)
                wr(p, s)
                touched.append(rel)
            elif new in s:
                present.append(rel)
            else:
                unmatched.append(rel)

    print('pages patched: %d' % len(touched))
    for rel in touched:
        print('  ' + rel)
    if present:
        print('pages already updated, skipped: %d' % len(present))
    if unmatched:
        print('pages unmatched (left alone): %d' % len(unmatched))
        for rel in unmatched:
            print('  ' + rel)
    return touched, present, unmatched


def patch_template(tpath, old_block, new_block):
    """Replace *old_block* with *new_block* in the template file at *tpath*.

    Adapts both blocks to the file's actual line endings.
    Prints a one-line status message.
    """
    ts = rd(tpath)
    old = adapt(old_block, ts)
    new = adapt(new_block, ts)
    if old in ts:
        wr(tpath, ts.replace(old, new, 1))
        print('template/_footer.html: updated')
    elif new in ts:
        print('template/_footer.html: already updated, skipped')
    else:
        print('template/_footer.html: !! block not found verbatim, left untouched -- check by hand')
