import logging
import sys
from pathlib import Path

import click
import prompt_toolkit as pt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.status import Status

from qwikcrud import __version__
from qwikcrud.generator import FastAPIAppGenerator
from qwikcrud.logger import setup_logging
from qwikcrud.provider.base import AIProvider
from qwikcrud.provider.google import GoogleProvider
from qwikcrud.provider.openai import OpenAIProvider


@click.command()
@click.option(
    "-o", "--output-dir", default=".", help="Output directory for the generated app."
)
@click.option(
    "--ai",
    "ai_provider",
    type=click.Choice(["google", "openai"]),
    default="google",
    help="Choose the AI provider to use for generation. Default is Google.",
)
def main(output_dir: str, ai_provider: AIProvider) -> None:
    setup_logging()

    history = Path().home() / ".qwikcrud-prompt-history.txt"
    session = pt.PromptSession(history=FileHistory(str(history)))

    ai_provider_map: dict[str, type[AIProvider]] = {
        "google": GoogleProvider,
        "openai": OpenAIProvider,
    }
    ai = ai_provider_map[ai_provider]()
    code_generator = FastAPIAppGenerator(Path(output_dir).resolve())

    console = Console()
    console.print(
        f"[bold green]Qwikcrud v{__version__}[/bold green] - {ai.get_name()}\n\n"
        "Type [blink]/exit[/blink] at any time to exit the generator.\n"
    )

    is_first_prompt = True
    while True:
        prompt = session.prompt(
            "qwikcrud"
            f" ({'Describe your app' if is_first_prompt else 'Specify any modifications or enhancements'}) ➤ ",
            auto_suggest=AutoSuggestFromHistory(),
        )
        if prompt == "/exit":
            return
        try:
            with Status(
                f"[dim]Asking {ai.get_name()} …[/dim]", console=console
            ) as status:
                app = ai.query(prompt)
                status.update("[dim]Generating the app[/dim]")
                code_generator.clean()
                code_generator.generate(app)
            console.print(f"App successfully generated in {Path(output_dir).resolve()}")
            console.print("\nHere is the summary of the generated app:\n")
            app.summary()
            console.print(
                "Follow the instructions in the README.md file to run your application."
            )
            console.print(
                "\nYou can request changes if the generated app doesn't meet your"
                " expectations."
            )
            is_first_prompt = False
        except Exception as e:
            logging.exception(e)
            console.print("[red]Something went wrong, Try again![/red]")


if __name__ == "__main__":
    sys.exit(main())
