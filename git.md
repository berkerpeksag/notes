## Tips on search in commit logs

```sh
git grep get_ $(git rev-list --all -- astor) -- astor
```

See https://stackoverflow.com/a/2929502 for more information.

## Difference between HEAD and master

`master` is a reference to the end of a branch. `HEAD` is actually a special type
of reference that points to another reference. It may point to `master` or it may
not (it will point to whichever branch is currently checked out). If you know
you want to be committing to the `master` branch then push to this.

![](http://i.stack.imgur.com/hRanK.png)

On your own repository you can check where the `HEAD` is pointing to by running
this:

```sh
$ git symbolic-ref HEAD
refs/heads/master
```

**Note:** Finding out where the `remotes/origin/HEAD` is pointing to is more
tricky because it is on the remote machine.

## Git Objects

### Blob

The simplest object, just a bunch of bytes. This is often a file, but can be
a symlink or pretty much anything else. The object that points to the blob
determines the semantics.

### Tree

Directories are represented by tree object. They refer to blobs that have the
contents of files (filename, access mode, etc is all stored in the tree), and
to other trees for subdirectories.

Nodes that nothing points to can be garbage collected with `git gc`, or rescued
much like filesystem inodes with no filenames pointing to them with `git
lost-found`.

### Commit

A commit refers to a tree that represents the state of the files at the time of
the commit. It also refers to 0..n other commits that are its parents. More
than one parent means the commit is a merge, no parents means it is an initial
commit, and interestingly there can be more than one initial commit; this
usually means two separate projects merged. The body of the commit object is
the commit message.

### Refs

References, or heads or branches, are like post-it notes slapped on a node in
the DAG. Where as the DAG only gets added to and existing nodes cannot be
mutated, the post-its can be moved around freely. They don't get stored in the
history, and they aren't directly transferred between repositories. They act as
sort of bookmarks, "I'm working here".

### Remote refs

Remote references are post-it notes of a different color. The difference to
normal refs is the different namespace, and the fact that remote refs are
essentially controlled by the remote server. `git fetch` updates them.

### Tag

A tag is both a node in the DAG and a post-it note (of yet another color).
A tag points to a commit, and includes an optional message and a GPG signature.
The post-it is just a fast way to access the tag, and if lost can be recovered
from just the DAG with `git lost-found`.


# Notes

## Change author date of a commit

```sh
$ git commit --amend --date="Wed Feb 16 14:00 2011 +0100"
```

To change the commit date instead of the author date:

```sh
$ GIT_COMMITTER_DATE="Wed Feb 16 14:00 2011 +0100" git commit --amend
```
