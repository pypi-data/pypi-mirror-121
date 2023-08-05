# cursedspace

A python library/framework for TUI application on the basis of the curses
package.


## Example use

Here’s a very simple example of how to use the cursedspace package:

    #!/usr/bin/env python3

    from cursedspace import Application, Key, Panel


    class DemoApplication(Application):
        def __init__(self):
            super().__init__()
            self.panel = None

        def main(self):
            self.panel = Panel(self)
            self.resize()

            while True:
                curses.doupdate()

                key = self.read_key()

                if key == Key.RESIZE:
                    self.resize()
                elif key in [Key.ESCAPE, "q", "^C"]:
                    break

        def resize(self):
            height, width = self.size()
            self.panel.resize(height, width)
            self.panel.paint()


    # run the application
    DemoApplication().run()


## Components

 * `Application` is the main application class and provides boilerplate
   initialisations
 * `Panel` is a basic panel with support for borders and key handling in the
   context of an `Application`
 * `InputLine` is a panel with very basic editing support.
 * `Key` provides a convenient wrapper around curses’ key system. It can be
   used standalone even when you don’t want to use `Application` or `Panel`.
 * `ShellContext` is a convenient wrapper to execute external processes (e.g.
   through subprocess) and returning to the curses context afterwards again.

