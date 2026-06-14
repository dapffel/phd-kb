import sys

from agents.config import configure_tracing
from agents.supervisor.graph import Supervisor


AGENT_REGISTRY = {
    "supervisor": "agents.supervisor.graph:Supervisor",
    "ingest": "agents.sub_agents.ingest.graph:IngestAgent",
    "catalog": "agents.sub_agents.catalog.graph:CatalogAgent",
    "compile-concepts": "agents.sub_agents.compile_concepts.graph:CompileConceptsAgent",
    "synthesize": "agents.sub_agents.synthesize.graph:SynthesizeAgent",
    "eval": "agents.sub_agents.eval_agent.graph:EvalAgent",
    "lint": "agents.sub_agents.lint.graph:LintAgent",
    "query": "agents.sub_agents.query.graph:QueryAgent",
    "status": "agents.sub_agents.status.graph:StatusAgent",
}


def _print_graph(agent_name: str) -> None:
    if agent_name not in AGENT_REGISTRY:
        print(f"Unknown agent: {agent_name}")
        print(f"Available: {', '.join(sorted(AGENT_REGISTRY))}")
        sys.exit(1)

    module_path, class_name = AGENT_REGISTRY[agent_name].rsplit(":", 1)
    import importlib
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)

    if class_name == "Supervisor":
        instance = cls()
        graph = instance.build_graph().compile()
    else:
        from agents.vault import Vault
        instance = cls(Vault())
        graph = instance.build_graph().compile()

    print(graph.get_graph().draw_mermaid())


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("Usage: kb <command> [args]")
        print("Commands: init, status, catalog, catalog-update, find, ingest,")
        print("          ingest-all, compile-concepts, synthesize, slides, eval,")
        print("          eval-all, lint, query, update-chapter, watch, graph")
        sys.exit(1)

    tracing = configure_tracing()
    command = args[0]

    if command == "watch":
        from agents.file_watcher import watch
        watch()
        return

    if command == "graph":
        name = args[1] if len(args) > 1 else "supervisor"
        _print_graph(name)
        return

    dry_run = "--dry-run" in args
    rest_parts = [a for a in args[1:] if a != "--dry-run"]
    rest = " ".join(rest_parts)
    supervisor = Supervisor()
    output = supervisor.run(command, rest, dry_run=dry_run)
    print(output)
    if tracing:
        print("\n[LangSmith] Trace available at https://smith.langchain.com")


if __name__ == "__main__":
    main()
