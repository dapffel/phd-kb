import sys

from agents.supervisor.graph import Supervisor


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage: kb <command> [args]")
        print("Commands: init, status, catalog, catalog-update, find, ingest,")
        print("          ingest-all, compile-concepts, synthesize, slides, eval,")
        print("          eval-all, lint, query, update-chapter, watch")
        sys.exit(1)

    command = args[0]

    if command == "watch":
        from agents.file_watcher import watch
        watch()
        return

    rest = " ".join(args[1:])
    supervisor = Supervisor()
    output = supervisor.run(command, rest)
    print(output)


if __name__ == "__main__":
    main()
