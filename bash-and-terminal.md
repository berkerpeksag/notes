# Shortcuts

* Pressing `ctrl-p` moves to the previous command in history (replacing the
  up arrow)
* and `ctrl-n` moves to the next command (replacing the down arrow)
* `ctrl-a` - move the cursor to the beginning of the current line
* `ctrl-e` - move the cursor to the end of the current line
* `alt-b` - move the cursor backwards one word
* `alt-f` - move the cursor forward one word
* `ctrl-k` - delete from cursor to the end of the line
* `ctrl-u` - delete from cursor to the beginning of the line
* `alt-d` - delete the word in front of the cursor
* `ctrl-w` - delete the word behind of the cursor
* ```sh
  cd ~/go/
  cd ~/tmp/
  cd - # <- this puts you back to ~/go/
  cd - # <- this puts you back to ~/tmp/
  ```

## Background processes

If you need to run a command indefinitely you can send it to the background by
first running it and then pressing `ctrl-z`. This will suspend or pause the
process. After it has been suspended, type `bg` and press enter. This will move
it to a running state, but it will no longer have control of your terminal
window. However, if you close the terminal that job will terminate. To avoid
this, you disown the process by typing `disown` and pressing enter.

* `ctrl-z` - move the current process to the background in a suspended state.
* `jobs -l` - list the current background processes for the current tty session.
* `bg` - tell the most recent background process to continue running in the background
* `fg` - bring the most recent background process back to the foreground
* `disown -h` - disown the most recent background job.

  **Note:** This will remove it from your current tty session. It will not be
  able to be brought back to the foreground. You will have to control it with
  `kill`.
* `bg`, `fg`, and `disown` can be used with the job number found in `jobs -l`.
  If you run `jobs -l` you will see the job number at the beginning of the
  line. If you want to bring the 2nd job to the foreground you run `fg %2`.
* The plus sign (or minus sign) at the bigging of the line has meaning as well.
  A plus sign indicates that the job is the most recently used, or the one that
  will be targeted if you type any of the commands without a job ID. The minus
  sign is the second most recently used.

**Reference:** https://www.blockloop.io/mastering-bash-and-terminal
